#!/usr/bin/env python3
"""
Build cross-reference links between extracted project artifacts.

Usage:
    python3 link_artifacts.py --artifacts artifacts.json --output links.json
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Link:
    """Represents a link between two artifacts."""

    source_type: str
    source_id: str
    target_type: str
    target_id: str
    link_type: str
    confidence: float
    match_reason: str


class ArtifactLinker:
    """Build cross-reference links between project artifacts."""

    # Domain keywords for matching
    DOMAIN_KEYWORDS = {
        "security": [
            "authentication",
            "authorization",
            "encryption",
            "oauth",
            "saml",
            "jwt",
            "access",
            "password",
            "mfa",
            "sso",
            "security",
            "login",
        ],
        "performance": [
            "latency",
            "throughput",
            "response",
            "scalability",
            "cache",
            "load",
            "optimization",
            "benchmark",
            "performance",
            "speed",
        ],
        "data": [
            "database",
            "schema",
            "migration",
            "etl",
            "backup",
            "restore",
            "replication",
            "index",
            "data",
            "storage",
            "sql",
            "query",
        ],
        "integration": [
            "api",
            "interface",
            "connector",
            "import",
            "export",
            "integration",
            "webhook",
            "rest",
            "graphql",
            "endpoint",
        ],
        "usability": [
            "ui",
            "ux",
            "accessibility",
            "user",
            "interface",
            "design",
            "navigation",
            "usability",
            "experience",
        ],
    }

    def __init__(self, artifacts: dict):
        self.artifacts = artifacts
        self.links: list[Link] = []

    # Common English stopwords that don't carry semantic weight when matching.
    _STOPWORDS = frozenset(
        {
            "the",
            "and",
            "for",
            "with",
            "this",
            "that",
            "from",
            "will",
            "have",
            "has",
            "been",
            "are",
            "was",
            "were",
            "can",
            "may",
            "should",
            "would",
            "could",
            "must",
            "shall",
            "need",
            "use",
        }
    )

    # Long derivational suffixes — only strip when the remaining stem is
    # still substantial (>=5 chars), so e.g. "implement" (already base form)
    # is NOT stripped down to "impl".
    _LONG_SUFFIXES = ("ations", "ation", "ements", "ement", "ings", "ing")
    # Short inflections — fine to strip with a smaller minimum stem length.
    _SHORT_SUFFIXES = ("ies", "ied", "ed", "es", "s")

    @classmethod
    def _stem(cls, word: str) -> str:
        """Very small English stemmer to align noun/verb pairs.

        Examples:
            "implementation" -> "implement"   (long suffix, stem stays >=5)
            "implementing"   -> "implement"
            "implements"     -> "implement"
            "implement"      -> "implement"   (no change; would yield <5)
            "tests"          -> "test"        (short suffix path)

        Intentionally minimal — heavier stemmers (Porter / Snowball) would
        add a runtime dependency we don't need.
        """
        for suffix in cls._LONG_SUFFIXES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 5:
                return word[: -len(suffix)]
        for suffix in cls._SHORT_SUFFIXES:
            if word.endswith(suffix) and len(word) - len(suffix) >= 3:
                return word[: -len(suffix)]
        return word

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract significant keywords from text (stop-worded, original forms).

        Returns the original tokens (no stemming) so callers and tests can
        introspect the surface words. For matching that should treat
        noun/verb variants as equivalent (e.g. "implement" vs
        "implementation"), use ``_extract_stems`` below.
        """
        if not text:
            return set()
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        return {w for w in words if w not in self._STOPWORDS}

    def _extract_stems(self, text: str) -> set[str]:
        """Extract stemmed keywords for matching (noun/verb variants collapse)."""
        return {self._stem(w) for w in self._extract_keywords(text)}

    def _jaccard_similarity(self, set_a: set, set_b: set) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def _normalize_name(self, name: str) -> str:
        """Normalize a person's name for comparison."""
        if not name:
            return ""
        # Remove titles
        name = re.sub(r"\b(?:Mr|Ms|Mrs|Dr|Prof)\.?\s*", "", name, flags=re.IGNORECASE)
        # Normalize whitespace and case
        return " ".join(name.lower().split())

    def _owner_match_score(self, owner_a: Optional[str], owner_b: Optional[str]) -> float:
        """Calculate owner match score."""
        if not owner_a or not owner_b:
            return 0.0

        norm_a = self._normalize_name(owner_a)
        norm_b = self._normalize_name(owner_b)

        if norm_a == norm_b:
            return 1.0

        # Partial match (first name only)
        if norm_a.split()[0] == norm_b.split()[0]:
            return 0.7

        return 0.0

    def _get_domain(self, text: str) -> Optional[str]:
        """Identify the domain category of text."""
        if not text:
            return None
        text_lower = text.lower()
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return domain
        return None

    def _date_proximity_score(self, date_a: Optional[str], date_b: Optional[str], max_days: int = 30) -> float:
        """Calculate temporal proximity score between two dates."""
        if not date_a or not date_b:
            return 0.0
        try:
            dt_a = datetime.fromisoformat(date_a)
            dt_b = datetime.fromisoformat(date_b)
            delta = abs((dt_a - dt_b).days)
            if delta == 0:
                return 1.0
            if delta > max_days:
                return 0.0
            return 1.0 - (delta / max_days)
        except ValueError:
            return 0.0

    def link_action_items_to_wbs(self) -> list[Link]:
        """Link action items from meetings to WBS tasks."""
        links = []

        for meeting in self.artifacts.get("meetings", []):
            for action_item in meeting.get("action_items", []):
                ai_keywords = self._extract_stems(action_item.get("description", ""))
                ai_owner = action_item.get("owner")
                ai_due = action_item.get("due_date")

                best_match = None
                best_score = 0.0
                best_reasons = []

                for task in self.artifacts.get("wbs_tasks", []):
                    task_keywords = self._extract_stems(task.get("name", ""))
                    task_owner = task.get("owner")
                    task_start = task.get("start_date")
                    task_end = task.get("end_date")

                    reasons = []
                    score = 0.0

                    # Owner match (weight: 0.35)
                    owner_score = self._owner_match_score(ai_owner, task_owner)
                    if owner_score > 0:
                        score += owner_score * 0.35
                        reasons.append(f"owner_match({owner_score:.2f})")

                    # Keyword overlap (weight: 0.30)
                    keyword_sim = self._jaccard_similarity(ai_keywords, task_keywords)
                    if keyword_sim > 0.1:
                        score += keyword_sim * 0.30
                        reasons.append(f"keyword_overlap({keyword_sim:.2f})")

                    # Date proximity (weight: 0.20)
                    date_score = 0.0
                    if ai_due and task_end:
                        date_score = self._date_proximity_score(ai_due, task_end)
                    elif ai_due and task_start:
                        date_score = self._date_proximity_score(ai_due, task_start) * 0.5
                    if date_score > 0:
                        score += date_score * 0.20
                        reasons.append(f"date_proximity({date_score:.2f})")

                    # Explicit reference (weight: 0.15)
                    task_id = task.get("id", "")
                    if task_id and task_id in action_item.get("description", ""):
                        score += 0.15
                        reasons.append("explicit_reference")

                    if score > best_score and score >= 0.15:
                        best_score = score
                        best_match = task
                        best_reasons = reasons

                if best_match:
                    link = Link(
                        source_type="action_item",
                        source_id=action_item.get("id"),
                        target_type="wbs_task",
                        target_id=best_match.get("id"),
                        link_type="implements",
                        confidence=round(best_score, 2),
                        match_reason=" + ".join(best_reasons),
                    )
                    links.append(link)

        self.links.extend(links)
        return links

    def link_decisions_to_requirements(self) -> list[Link]:
        """Link decisions to requirements they address."""
        links = []

        # Collect decisions from meetings and standalone
        decisions = list(self.artifacts.get("decisions", []))
        for meeting in self.artifacts.get("meetings", []):
            decisions.extend(meeting.get("decisions", []))

        for decision in decisions:
            dec_keywords = self._extract_stems(decision.get("description", ""))
            dec_domain = self._get_domain(decision.get("description", ""))

            best_match = None
            best_score = 0.0
            best_reasons = []

            for req in self.artifacts.get("requirements", []):
                req_keywords = self._extract_stems(req.get("description", ""))
                req_domain = self._get_domain(req.get("description", ""))

                reasons = []
                score = 0.0

                # Keyword exact match (weight: 0.40)
                common_keywords = dec_keywords & req_keywords
                keyword_sim = self._jaccard_similarity(dec_keywords, req_keywords)
                if keyword_sim > 0.1:
                    score += keyword_sim * 0.40
                    if common_keywords:
                        reasons.append(f"keyword_match({','.join(list(common_keywords)[:3])})")

                # Domain alignment (weight: 0.25)
                if dec_domain and dec_domain == req_domain:
                    score += 0.25
                    reasons.append(f"domain_match({dec_domain})")

                # Explicit reference (weight: 0.15)
                req_id = req.get("id", "")
                if req_id and req_id in decision.get("description", ""):
                    score += 0.15
                    reasons.append("explicit_reference")

                if score > best_score and score >= 0.15:
                    best_score = score
                    best_match = req
                    best_reasons = reasons

            if best_match:
                link = Link(
                    source_type="decision",
                    source_id=decision.get("id"),
                    target_type="requirement",
                    target_id=best_match.get("id"),
                    link_type="addresses",
                    confidence=round(best_score, 2),
                    match_reason=" + ".join(best_reasons),
                )
                links.append(link)

        self.links.extend(links)
        return links

    def link_meetings_to_wbs(self) -> list[Link]:
        """Link meetings to WBS tasks discussed."""
        links = []

        for meeting in self.artifacts.get("meetings", []):
            meeting_attendees = {self._normalize_name(a) for a in meeting.get("attendees", [])}
            meeting_date = meeting.get("date")

            # Collect all text from meeting for keyword extraction
            meeting_text = " ".join(
                [
                    meeting.get("title", ""),
                    " ".join(ai.get("description", "") for ai in meeting.get("action_items", [])),
                    " ".join(d.get("description", "") for d in meeting.get("decisions", [])),
                ]
            )
            meeting_keywords = self._extract_stems(meeting_text)

            for task in self.artifacts.get("wbs_tasks", []):
                task_owner = task.get("owner")
                task_keywords = self._extract_stems(task.get("name", ""))
                task_start = task.get("start_date")
                task_end = task.get("end_date")

                reasons = []
                score = 0.0

                # Task owner present (weight: 0.30)
                if task_owner and self._normalize_name(task_owner) in meeting_attendees:
                    score += 0.30
                    reasons.append("owner_present")

                # Task mentioned (weight: 0.35)
                task_id = task.get("id", "")
                keyword_sim = self._jaccard_similarity(meeting_keywords, task_keywords)
                if task_id and task_id in meeting_text:
                    score += 0.35
                    reasons.append("task_mentioned")
                elif keyword_sim > 0.2:
                    score += keyword_sim * 0.35
                    reasons.append(f"topic_alignment({keyword_sim:.2f})")

                # Date relevance (weight: 0.15)
                if meeting_date and task_start and task_end:
                    try:
                        mtg_dt = datetime.fromisoformat(meeting_date)
                        start_dt = datetime.fromisoformat(task_start)
                        end_dt = datetime.fromisoformat(task_end)
                        if start_dt <= mtg_dt <= end_dt:
                            score += 0.15
                            reasons.append("date_in_range")
                    except ValueError:
                        pass

                if score >= 0.15:
                    link = Link(
                        source_type="meeting",
                        source_id=meeting.get("id"),
                        target_type="wbs_task",
                        target_id=task.get("id"),
                        link_type="discusses",
                        confidence=round(score, 2),
                        match_reason=" + ".join(reasons),
                    )
                    links.append(link)

        self.links.extend(links)
        return links

    def link_requirements_to_wbs(self) -> list[Link]:
        """Link requirements to implementing WBS tasks."""
        links = []

        for req in self.artifacts.get("requirements", []):
            req_keywords = self._extract_stems(req.get("description", ""))
            req_domain = self._get_domain(req.get("description", ""))

            best_match = None
            best_score = 0.0
            best_reasons = []

            for task in self.artifacts.get("wbs_tasks", []):
                task_keywords = self._extract_stems(task.get("name", ""))
                task_domain = self._get_domain(task.get("name", ""))

                reasons = []
                score = 0.0

                # Explicit traceability (weight: 0.45)
                req_id = req.get("id", "")
                task_id = task.get("id", "")
                if req_id and req_id in task.get("name", ""):
                    score += 0.45
                    reasons.append("explicit_trace")

                # Functional alignment (weight: 0.30)
                keyword_sim = self._jaccard_similarity(req_keywords, task_keywords)
                if keyword_sim > 0.15:
                    score += keyword_sim * 0.30
                    reasons.append(f"functional_alignment({keyword_sim:.2f})")
                elif req_domain and req_domain == task_domain:
                    score += 0.15
                    reasons.append(f"domain_match({req_domain})")

                if score > best_score and score >= 0.15:
                    best_score = score
                    best_match = task
                    best_reasons = reasons

            if best_match:
                link = Link(
                    source_type="requirement",
                    source_id=req.get("id"),
                    target_type="wbs_task",
                    target_id=best_match.get("id"),
                    link_type="implemented_by",
                    confidence=round(best_score, 2),
                    match_reason=" + ".join(best_reasons),
                )
                links.append(link)

        self.links.extend(links)
        return links

    def build_all_links(self) -> list[Link]:
        """Build all cross-reference links."""
        self.link_action_items_to_wbs()
        self.link_decisions_to_requirements()
        self.link_meetings_to_wbs()
        self.link_requirements_to_wbs()
        return self.links

    def to_dict(self) -> dict:
        """Convert links to dictionary format."""
        return {
            "schema_version": "1.0",
            "link_date": datetime.now().isoformat(),
            "links": [asdict(link) for link in self.links],
        }


def main():
    parser = argparse.ArgumentParser(description="Build cross-reference links between project artifacts")
    parser.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="Path to artifacts JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("links.json"),
        help="Output JSON file path",
    )

    args = parser.parse_args()

    if not args.artifacts.exists():
        print(f"Error: Artifacts file not found: {args.artifacts}", file=sys.stderr)
        sys.exit(1)

    # Load artifacts
    artifacts = json.loads(args.artifacts.read_text(encoding="utf-8"))

    # Build links
    linker = ArtifactLinker(artifacts.get("artifacts", artifacts))
    linker.build_all_links()

    # Write output
    result = linker.to_dict()
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"Links written to {args.output}")

    # Print summary
    link_types = {}
    for link in result["links"]:
        lt = link["link_type"]
        link_types[lt] = link_types.get(lt, 0) + 1

    print(f"\nSummary: {len(result['links'])} links created")
    for lt, count in sorted(link_types.items()):
        print(f"  {lt}: {count}")


if __name__ == "__main__":
    main()
