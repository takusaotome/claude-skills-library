#!/usr/bin/env python3
"""
Patent Search Helper

Generates structured prior art search reports from search parameters.
Supports keyword expansion, classification code lookup, and report generation.

Usage:
    python patent_search_helper.py --keywords "neural network,image segmentation" \
                                   --cpc "G06N3/08,G06V10/82" \
                                   --output prior_art_report.md

    python patent_search_helper.py --invention-file invention.txt --output report.md
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class SearchConfig:
    """Configuration for patent search."""

    keywords: list[str] = field(default_factory=list)
    cpc_codes: list[str] = field(default_factory=list)
    ipc_codes: list[str] = field(default_factory=list)
    jurisdictions: list[str] = field(default_factory=lambda: ["US", "EP", "WO", "JP", "CN"])
    date_range: Optional[str] = None
    assignees: list[str] = field(default_factory=list)
    inventors: list[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """Represents a patent search result."""

    patent_number: str
    title: str
    assignee: str
    priority_date: str
    relevance: str  # HIGH, MEDIUM, LOW
    key_features: str
    differences: str


def parse_keywords(keyword_string: str) -> list[str]:
    """Parse comma-separated keywords into list."""
    if not keyword_string:
        return []
    return [kw.strip() for kw in keyword_string.split(",") if kw.strip()]


def parse_cpc_codes(cpc_string: str) -> list[str]:
    """Parse and validate CPC classification codes."""
    if not cpc_string:
        return []

    codes = [code.strip().upper() for code in cpc_string.split(",") if code.strip()]
    validated = []

    # CPC format: A-H + 2 digits + letter + optional digits/slash
    cpc_pattern = re.compile(r"^[A-H]\d{2}[A-Z]\d*(?:/\d+)?$")

    for code in codes:
        if cpc_pattern.match(code):
            validated.append(code)
        else:
            print(f"Warning: Invalid CPC code format: {code}", file=sys.stderr)

    return validated


def expand_keywords(keywords: list[str]) -> dict[str, list[str]]:
    """Generate keyword variations (synonyms, related terms).

    Returns dict mapping original keyword to expansion list.
    """
    # Common technical term expansions
    expansions_db: dict[str, list[str]] = {
        "neural network": [
            "neural network",
            "deep learning",
            "artificial neural network",
            "ANN",
            "DNN",
            "deep neural network",
        ],
        "cnn": [
            "CNN",
            "convolutional neural network",
            "convnet",
            "convolutional network",
        ],
        "image segmentation": [
            "image segmentation",
            "semantic segmentation",
            "instance segmentation",
            "pixel classification",
            "image partition",
        ],
        "machine learning": [
            "machine learning",
            "ML",
            "artificial intelligence",
            "AI",
            "pattern recognition",
        ],
        "real-time": ["real-time", "realtime", "real time", "low latency", "online"],
        "medical imaging": [
            "medical imaging",
            "diagnostic imaging",
            "medical image",
            "clinical imaging",
            "radiology",
        ],
        "edge device": [
            "edge device",
            "edge computing",
            "embedded device",
            "IoT device",
            "mobile device",
        ],
    }

    result = {}
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in expansions_db:
            result[kw] = expansions_db[kw_lower]
        else:
            # No expansion found, use original
            result[kw] = [kw]

    return result


def build_boolean_query(config: SearchConfig) -> str:
    """Build Boolean search query from configuration."""
    parts = []

    # Keyword groups with OR
    if config.keywords:
        expansions = expand_keywords(config.keywords)
        keyword_groups = []
        for original, expanded in expansions.items():
            quoted = [f'"{term}"' if " " in term else term for term in expanded]
            keyword_groups.append(f"({' OR '.join(quoted)})")
        parts.append(" AND ".join(keyword_groups))

    # CPC codes
    if config.cpc_codes:
        cpc_query = " OR ".join([f"CPC/{code}" for code in config.cpc_codes])
        parts.append(f"({cpc_query})")

    # Assignees
    if config.assignees:
        assignee_query = " OR ".join([f'AN/"{a}"' for a in config.assignees])
        parts.append(f"({assignee_query})")

    return " AND ".join(parts) if parts else "(no query specified)"


def generate_google_patents_url(config: SearchConfig) -> str:
    """Generate Google Patents search URL."""
    base_url = "https://patents.google.com/"

    query_parts = []

    # Keywords
    for kw in config.keywords:
        query_parts.append(kw.replace(" ", "+"))

    # Add type filter
    params = ["type=PATENT"]

    if query_parts:
        params.insert(0, f"q={'+'.join(query_parts)}")

    return f"{base_url}?{'&'.join(params)}"


def generate_report(config: SearchConfig, output_path: Optional[Path] = None) -> str:
    """Generate markdown prior art search report."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    expanded = expand_keywords(config.keywords)
    boolean_query = build_boolean_query(config)
    google_url = generate_google_patents_url(config)

    report = f"""# Prior Art Search Report

## Report Information

| Field | Value |
|-------|-------|
| **Search Date** | {date_str} |
| **Analyst** | [Patent Analyst] |
| **Status** | Draft - Pending Search Execution |

---

## Search Configuration

### Keywords and Expansions

| Original Keyword | Expanded Terms |
|------------------|----------------|
"""

    for original, terms in expanded.items():
        terms_str = ", ".join(terms[:5])  # Limit display
        if len(terms) > 5:
            terms_str += f" (+{len(terms) - 5} more)"
        report += f"| {original} | {terms_str} |\n"

    report += f"""
### Classification Codes

**CPC Codes**: {", ".join(config.cpc_codes) if config.cpc_codes else "None specified"}

**IPC Codes**: {", ".join(config.ipc_codes) if config.ipc_codes else "None specified"}

### Geographic Scope

**Jurisdictions**: {", ".join(config.jurisdictions)}

---

## Search Queries

### Boolean Query (USPTO PatFT / Espacenet)

```
{boolean_query}
```

### Google Patents URL

[Open in Google Patents]({google_url})

---

## Search Execution Checklist

- [ ] Google Patents search completed
- [ ] USPTO PatFT search completed
- [ ] Espacenet search completed
- [ ] J-PlatPat search completed (if JP jurisdiction)
- [ ] Citation analysis (forward/backward) completed
- [ ] Non-patent literature (Google Scholar) search completed

---

## Key References

> **Instructions**: Add key prior art references below after completing search.

### Reference 1

| Field | Value |
|-------|-------|
| **Patent Number** | US_,___,___ |
| **Title** | |
| **Assignee** | |
| **Priority Date** | |
| **Relevance** | HIGH / MEDIUM / LOW |

**Key Features Disclosed**:
- [Feature 1]
- [Feature 2]

**Differences from Invention**:
- [Difference 1]
- [Difference 2]

---

### Reference 2

| Field | Value |
|-------|-------|
| **Patent Number** | |
| **Title** | |
| **Assignee** | |
| **Priority Date** | |
| **Relevance** | HIGH / MEDIUM / LOW |

**Key Features Disclosed**:
- [Feature 1]

**Differences from Invention**:
- [Difference 1]

---

## Feature Comparison Matrix

> **Instructions**: Complete this matrix after identifying key prior art.

| Feature | Invention | Ref 1 | Ref 2 | Ref 3 |
|---------|-----------|-------|-------|-------|
| [Feature A] | Yes | ? | ? | ? |
| [Feature B] | Yes | ? | ? | ? |
| [Feature C] | Yes | ? | ? | ? |

---

## Preliminary Assessment

### Novelty (35 USC 102)

**Assessment**: [NOVEL / NOT NOVEL / UNCERTAIN]

**Rationale**:
> [To be completed after search]

### Non-Obviousness (35 USC 103)

**Assessment**: [NON-OBVIOUS / OBVIOUS / UNCERTAIN]

**Rationale**:
> [To be completed after search]

---

## Recommendations

> [To be completed after analysis]

---

## Appendix: Search Log

| Date/Time | Database | Query | Results | Notes |
|-----------|----------|-------|---------|-------|
| {date_str} | Google Patents | [See above] | TBD | Initial search |

---

*Report generated by patent_search_helper.py*
"""

    if output_path:
        output_path.write_text(report, encoding="utf-8")
        print(f"Report saved to: {output_path}")

    return report


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate structured prior art search reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --keywords "neural network,image segmentation" --output report.md
  %(prog)s --keywords "battery electrode" --cpc "H01M4/00" --output report.md
  %(prog)s --invention-file invention.txt --output report.md
        """,
    )

    parser.add_argument(
        "--keywords",
        "-k",
        type=str,
        help="Comma-separated list of search keywords",
    )

    parser.add_argument(
        "--cpc",
        type=str,
        help="Comma-separated CPC classification codes (e.g., G06N3/08,G06V10/82)",
    )

    parser.add_argument(
        "--ipc",
        type=str,
        help="Comma-separated IPC classification codes",
    )

    parser.add_argument(
        "--jurisdictions",
        "-j",
        type=str,
        default="US,EP,WO,JP,CN",
        help="Comma-separated jurisdiction codes (default: US,EP,WO,JP,CN)",
    )

    parser.add_argument(
        "--assignees",
        "-a",
        type=str,
        help="Comma-separated assignee names to filter",
    )

    parser.add_argument(
        "--invention-file",
        "-i",
        type=Path,
        help="Path to invention disclosure file (extracts keywords)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path for report (default: stdout)",
    )

    parser.add_argument(
        "--query-only",
        "-q",
        action="store_true",
        help="Output only the Boolean query (no full report)",
    )

    args = parser.parse_args()

    # Build configuration
    config = SearchConfig()

    if args.keywords:
        config.keywords = parse_keywords(args.keywords)

    if args.cpc:
        config.cpc_codes = parse_cpc_codes(args.cpc)

    if args.ipc:
        config.ipc_codes = parse_keywords(args.ipc)

    if args.jurisdictions:
        config.jurisdictions = parse_keywords(args.jurisdictions)

    if args.assignees:
        config.assignees = parse_keywords(args.assignees)

    # Validate we have something to search
    if not config.keywords and not config.cpc_codes:
        print("Error: At least --keywords or --cpc must be specified", file=sys.stderr)
        return 1

    # Query-only mode
    if args.query_only:
        print(build_boolean_query(config))
        return 0

    # Generate full report
    report = generate_report(config, args.output)

    if not args.output:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
