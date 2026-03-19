#!/usr/bin/env python3
"""
Requirements Parser
Extract requirements from various document formats (Markdown, PDF, DOCX, plain text)
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class RequirementsParser:
    """Parse requirements documents and extract structured requirement data"""

    # Common requirement ID patterns
    REQ_PATTERNS = [
        r"\b(REQ-\d+)\b",  # REQ-001
        r"\b(UC-\d+)\b",  # UC-01 (Use Case)
        r"\b(FR-\d+)\b",  # FR-001 (Functional Requirement)
        r"\b(NFR-\d+)\b",  # NFR-001 (Non-Functional)
        r"\b(要件-\d+)\b",  # Japanese format
        r"\b(機能-\d+)\b",  # Japanese functional
    ]

    def __init__(self, file_path: str):
        """Initialize parser with file path"""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Requirements file not found: {file_path}")

        self.requirements: List[Dict] = []
        self.scope_in: List[str] = []
        self.scope_out: List[str] = []
        self.tech_stack: Dict[str, str] = {}

    def parse(self) -> Dict:
        """
        Parse requirements document and extract structured data

        Returns:
            Dict with keys: requirements, scope_in, scope_out, tech_stack
        """
        content = self._read_file()

        # Extract requirements with IDs
        self.requirements = self._extract_requirements(content)

        # Extract scope boundaries
        self.scope_in, self.scope_out = self._extract_scope(content)

        # Extract technology choices
        self.tech_stack = self._extract_tech_stack(content)

        return {
            "requirements": self.requirements,
            "scope_in": self.scope_in,
            "scope_out": self.scope_out,
            "tech_stack": self.tech_stack,
        }

    def _read_file(self) -> str:
        """Read file content based on extension"""
        ext = self.file_path.suffix.lower()

        if ext in [".md", ".txt"]:
            return self.file_path.read_text(encoding="utf-8")
        elif ext == ".pdf":
            return self._read_pdf()
        elif ext in [".docx", ".doc"]:
            return self._read_docx()
        else:
            # Try reading as plain text
            try:
                return self.file_path.read_text(encoding="utf-8")
            except Exception as e:
                raise ValueError(f"Unsupported file format: {ext}") from e

    def _read_pdf(self) -> str:
        """Read PDF file (placeholder - requires PyPDF2 or similar)"""
        try:
            import PyPDF2

            with open(self.file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                return "\n".join(text)
        except ImportError:
            # Fallback: suggest using docling or other tools
            print("Warning: PyPDF2 not available. PDF content not parsed.", file=sys.stderr)
            return f"[PDF file: {self.file_path.name} - requires manual extraction]"

    def _read_docx(self) -> str:
        """Read DOCX file (placeholder - requires python-docx)"""
        try:
            from docx import Document

            doc = Document(self.file_path)
            text = []
            for para in doc.paragraphs:
                text.append(para.text)
            return "\n".join(text)
        except ImportError:
            print("Warning: python-docx not available. DOCX content not parsed.", file=sys.stderr)
            return f"[DOCX file: {self.file_path.name} - requires manual extraction]"

    def _extract_requirements(self, content: str) -> List[Dict]:
        """
        Extract requirements with IDs and descriptions

        Returns:
            List of dicts with keys: req_id, description, category
        """
        requirements = []

        # Combine all requirement patterns
        all_patterns = "|".join(self.REQ_PATTERNS)

        # Find all requirement IDs
        matches = re.finditer(all_patterns, content)

        for match in matches:
            req_id = match.group(0)
            start_pos = match.start()

            # Extract context around requirement (up to 200 chars after ID)
            context_end = min(start_pos + 300, len(content))
            context = content[start_pos:context_end]

            # Extract description (text after ID until newline or period)
            desc_match = re.search(r":?\s*(.+?)(?:\n|$)", context[len(req_id) :])
            description = desc_match.group(1).strip() if desc_match else ""

            # Determine category based on prefix
            category = self._categorize_requirement(req_id)

            requirements.append(
                {"req_id": req_id, "description": description, "category": category, "context": context[:200]}
            )

        # Remove duplicates (same req_id)
        seen = set()
        unique_reqs = []
        for req in requirements:
            if req["req_id"] not in seen:
                seen.add(req["req_id"])
                unique_reqs.append(req)

        return unique_reqs

    def _categorize_requirement(self, req_id: str) -> str:
        """Categorize requirement based on ID prefix"""
        if req_id.startswith("FR-"):
            return "functional"
        elif req_id.startswith("NFR-"):
            return "non_functional"
        elif req_id.startswith("UC-"):
            return "use_case"
        elif req_id.startswith("REQ-"):
            return "general"
        elif "機能" in req_id:
            return "functional"
        elif "要件" in req_id:
            return "general"
        else:
            return "unknown"

    def _extract_scope(self, content: str) -> Tuple[List[str], List[str]]:
        """
        Extract in-scope and out-of-scope items

        Returns:
            Tuple of (in_scope_list, out_of_scope_list)
        """
        in_scope = []
        out_of_scope = []

        # Look for scope sections
        in_scope_pattern = r"(?:In[- ]Scope|スコープ内|対象範囲)[\s:：]*(.*?)(?=Out[- ]Scope|スコープ外|対象外|$)"
        out_scope_pattern = r"(?:Out[- ]of[- ]Scope|スコープ外|対象外)[\s:：]*(.*?)(?=\n#{1,3}|$)"

        # Extract in-scope items
        in_matches = re.finditer(in_scope_pattern, content, re.IGNORECASE | re.DOTALL)
        for match in in_matches:
            items = self._extract_list_items(match.group(1))
            in_scope.extend(items)

        # Extract out-of-scope items
        out_matches = re.finditer(out_scope_pattern, content, re.IGNORECASE | re.DOTALL)
        for match in out_matches:
            items = self._extract_list_items(match.group(1))
            out_of_scope.extend(items)

        return in_scope, out_of_scope

    def _extract_list_items(self, text: str) -> List[str]:
        """Extract bullet point or numbered list items from text"""
        items = []

        # Match bullet points (-, *, •) or numbered lists (1., 2.)
        lines = text.strip().split("\n")
        for line in lines:
            line = line.strip()
            # Match list item patterns
            match = re.match(r"^(?:[-*•]|\d+\.)\s*(.+)$", line)
            if match:
                items.append(match.group(1).strip())
            elif line and not line.startswith("#"):
                # Non-empty line that's not a header
                items.append(line)

        return [item for item in items if len(item) > 3]  # Filter very short items

    def _extract_tech_stack(self, content: str) -> Dict[str, str]:
        """
        Extract technology stack choices

        Returns:
            Dict with keys: frontend, backend, database, etc.
        """
        tech_stack = {}

        # Common technology keywords
        tech_patterns = {
            "frontend": r"(?:Frontend|Front-end|フロントエンド)[\s:：]*([^\n]+)",
            "backend": r"(?:Backend|Back-end|バックエンド)[\s:：]*([^\n]+)",
            "database": r"(?:Database|DB|データベース)[\s:：]*([^\n]+)",
            "framework": r"(?:Framework|フレームワーク)[\s:：]*([^\n]+)",
            "language": r"(?:Language|Programming Language|言語)[\s:：]*([^\n]+)",
            "cloud": r"(?:Cloud|Platform|クラウド)[\s:：]*([^\n]+)",
        }

        for category, pattern in tech_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                tech_stack[category] = match.group(1).strip()

        # Also extract specific technology mentions
        specific_techs = [
            "React",
            "Angular",
            "Vue",
            "Django",
            "Flask",
            "FastAPI",
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "AWS",
            "Azure",
            "GCP",
        ]

        for tech in specific_techs:
            if re.search(rf"\b{tech}\b", content, re.IGNORECASE):
                if "mentioned" not in tech_stack:
                    tech_stack["mentioned"] = []
                tech_stack["mentioned"].append(tech)

        return tech_stack


def main():
    """CLI interface for testing requirements parser"""
    import argparse

    parser = argparse.ArgumentParser(description="Parse requirements document")
    parser.add_argument("file_path", help="Path to requirements document")
    parser.add_argument("--output", "-o", help="Output JSON file path")

    args = parser.parse_args()

    # Parse requirements
    req_parser = RequirementsParser(args.file_path)
    result = req_parser.parse()

    # Print summary
    print(f"Requirements parsed: {len(result['requirements'])}")
    print(f"In-scope items: {len(result['scope_in'])}")
    print(f"Out-of-scope items: {len(result['scope_out'])}")
    print(f"Tech stack items: {len(result['tech_stack'])}")

    # Print requirements
    print("\n=== Requirements ===")
    for req in result["requirements"]:
        print(f"{req['req_id']}: {req['description'][:80]}...")

    # Save to JSON if requested
    if args.output:
        import json

        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
