#!/usr/bin/env python3
"""
Project Completeness Scorer

Evaluates project deliverables across multiple dimensions and calculates
a weighted 0-100 completeness score with prioritized action items.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Severity weights for priority calculation
SEVERITY_WEIGHTS = {"critical": 3, "major": 2, "minor": 1}

# Effort multipliers for priority calculation
EFFORT_MULTIPLIERS = {"low": 1, "medium": 2, "high": 4}


@dataclass
class Criterion:
    """A single evaluation criterion."""

    name: str
    criterion_type: str  # binary, count, content, percentage
    severity: str  # critical, major, minor
    check_type: str  # file_exists, dir_exists, file_count, contains, etc.
    params: dict = field(default_factory=dict)
    action: str = ""
    met: bool = False
    score: float = 0.0
    details: str = ""


@dataclass
class Dimension:
    """An evaluation dimension with weight and criteria."""

    name: str
    weight: float
    criteria: list = field(default_factory=list)
    raw_score: float = 0.0
    weighted_score: float = 0.0


@dataclass
class Gap:
    """An identified gap in the project."""

    criterion: str
    dimension: str
    severity: str
    effort: str
    priority: float
    action: str


@dataclass
class ScoringResult:
    """Complete scoring result."""

    project_path: str
    project_type: str
    timestamp: str
    overall_score: float
    dimensions: list
    gaps: list
    summary: dict


def get_skill_template() -> dict:
    """Return the skill project template."""
    return {
        "template_id": "skill",
        "display_name": "Claude Skill",
        "description": "Evaluation template for Claude Code skill projects",
        "dimensions": [
            {
                "name": "Functional Requirements",
                "weight": 0.30,
                "criteria": [
                    {
                        "name": "SKILL.md exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": "SKILL.md",
                        "severity": "critical",
                        "action": "Create SKILL.md with proper YAML frontmatter",
                    },
                    {
                        "name": "YAML frontmatter present",
                        "type": "content",
                        "check": "yaml_frontmatter",
                        "path": "SKILL.md",
                        "severity": "critical",
                        "action": "Add YAML frontmatter with name and description fields",
                    },
                    {
                        "name": "scripts/ directory exists",
                        "type": "binary",
                        "check": "dir_exists",
                        "path": "scripts",
                        "severity": "major",
                        "action": "Create scripts/ directory with at least one Python script",
                    },
                    {
                        "name": "At least one Python script",
                        "type": "count",
                        "check": "file_count",
                        "pattern": "scripts/*.py",
                        "minimum": 1,
                        "severity": "major",
                        "action": "Add executable Python scripts to scripts/ directory",
                    },
                    {
                        "name": "references/ directory exists",
                        "type": "binary",
                        "check": "dir_exists",
                        "path": "references",
                        "severity": "minor",
                        "action": "Create references/ directory for methodology docs",
                    },
                    {
                        "name": "At least one reference document",
                        "type": "count",
                        "check": "file_count",
                        "pattern": "references/*.md",
                        "minimum": 1,
                        "severity": "major",
                        "action": "Add reference documentation to references/",
                    },
                ],
            },
            {
                "name": "Quality Standards",
                "weight": 0.15,
                "criteria": [
                    {
                        "name": "Python scripts have shebang",
                        "type": "content",
                        "check": "shebang",
                        "pattern": "scripts/*.py",
                        "severity": "minor",
                        "action": "Add #!/usr/bin/env python3 to Python scripts",
                    },
                    {
                        "name": "No hardcoded absolute paths",
                        "type": "content",
                        "check": "no_pattern",
                        "pattern": "scripts/*.py",
                        "forbidden": ["/Users/", "/home/"],
                        "severity": "major",
                        "action": "Replace hardcoded paths with relative paths",
                    },
                    {
                        "name": "CLI interface with argparse",
                        "type": "content",
                        "check": "contains",
                        "pattern": "scripts/*.py",
                        "search": "argparse",
                        "severity": "minor",
                        "action": "Add argparse CLI interface to main script",
                    },
                ],
            },
            {
                "name": "Test Coverage",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "tests/ directory exists",
                        "type": "binary",
                        "check": "dir_exists",
                        "path": "scripts/tests",
                        "severity": "major",
                        "action": "Create scripts/tests/ directory",
                    },
                    {
                        "name": "conftest.py exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": "scripts/tests/conftest.py",
                        "severity": "major",
                        "action": "Create conftest.py with sys.path setup",
                    },
                    {
                        "name": "At least 3 tests",
                        "type": "count",
                        "check": "test_count",
                        "pattern": "scripts/tests/test_*.py",
                        "minimum": 3,
                        "severity": "major",
                        "action": "Add at least 3 meaningful tests",
                    },
                ],
            },
            {
                "name": "Documentation",
                "weight": 0.20,
                "criteria": [
                    {
                        "name": "Overview section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## Overview",
                        "severity": "major",
                        "action": "Add ## Overview section to SKILL.md",
                    },
                    {
                        "name": "When to Use section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## When to Use",
                        "severity": "major",
                        "action": "Add ## When to Use section to SKILL.md",
                    },
                    {
                        "name": "Prerequisites section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## Prerequisites",
                        "severity": "major",
                        "action": "Add ## Prerequisites section to SKILL.md",
                    },
                    {
                        "name": "Workflow section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## Workflow",
                        "severity": "major",
                        "action": "Add ## Workflow section to SKILL.md",
                    },
                    {
                        "name": "Output Format section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## Output Format",
                        "severity": "minor",
                        "action": "Add ## Output Format section to SKILL.md",
                    },
                    {
                        "name": "Resources section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "SKILL.md",
                        "heading": "## Resources",
                        "severity": "minor",
                        "action": "Add ## Resources section to SKILL.md",
                    },
                ],
            },
            {
                "name": "Deployment Readiness",
                "weight": 0.10,
                "criteria": [
                    {
                        "name": "assets/ directory exists",
                        "type": "binary",
                        "check": "dir_exists",
                        "path": "assets",
                        "severity": "minor",
                        "action": "Create assets/ directory for templates",
                    },
                ],
            },
        ],
    }


def get_webapp_template() -> dict:
    """Return the web application template."""
    return {
        "template_id": "webapp",
        "display_name": "Web Application",
        "description": "Evaluation template for web application projects",
        "dimensions": [
            {
                "name": "Functional Requirements",
                "weight": 0.35,
                "criteria": [
                    {
                        "name": "Package manifest exists",
                        "type": "binary",
                        "check": "file_exists_any",
                        "paths": ["package.json", "pyproject.toml"],
                        "severity": "critical",
                        "action": "Create package.json or pyproject.toml",
                    },
                    {
                        "name": "Source directory exists",
                        "type": "binary",
                        "check": "dir_exists_any",
                        "paths": ["src", "app", "lib"],
                        "severity": "critical",
                        "action": "Create source directory (src/ or app/)",
                    },
                    {
                        "name": "README.md exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": "README.md",
                        "severity": "critical",
                        "action": "Create README.md with project documentation",
                    },
                ],
            },
            {
                "name": "Quality Standards",
                "weight": 0.20,
                "criteria": [
                    {
                        "name": ".gitignore exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": ".gitignore",
                        "severity": "minor",
                        "action": "Create .gitignore file",
                    },
                ],
            },
            {
                "name": "Test Coverage",
                "weight": 0.20,
                "criteria": [
                    {
                        "name": "Test directory exists",
                        "type": "binary",
                        "check": "dir_exists_any",
                        "paths": ["tests", "__tests__", "test"],
                        "severity": "major",
                        "action": "Create tests/ directory",
                    },
                ],
            },
            {
                "name": "Documentation",
                "weight": 0.10,
                "criteria": [
                    {
                        "name": "README has installation section",
                        "type": "content",
                        "check": "has_heading",
                        "path": "README.md",
                        "heading": "## Install",
                        "severity": "major",
                        "action": "Add installation instructions to README.md",
                    },
                ],
            },
            {
                "name": "Deployment Readiness",
                "weight": 0.15,
                "criteria": [
                    {
                        "name": "License file exists",
                        "type": "binary",
                        "check": "file_exists_any",
                        "paths": ["LICENSE", "LICENSE.md", "LICENSE.txt"],
                        "severity": "minor",
                        "action": "Add LICENSE file",
                    },
                ],
            },
        ],
    }


def get_library_template() -> dict:
    """Return the library template."""
    return {
        "template_id": "library",
        "display_name": "Library/Package",
        "description": "Evaluation template for reusable library projects",
        "dimensions": [
            {
                "name": "Functional Requirements",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "Package manifest exists",
                        "type": "binary",
                        "check": "file_exists_any",
                        "paths": ["pyproject.toml", "package.json", "setup.py"],
                        "severity": "critical",
                        "action": "Create pyproject.toml or package.json",
                    },
                    {
                        "name": "Source directory exists",
                        "type": "binary",
                        "check": "dir_exists_any",
                        "paths": ["src", "lib"],
                        "severity": "critical",
                        "action": "Create src/ or lib/ directory",
                    },
                ],
            },
            {
                "name": "Quality Standards",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "Type hints present",
                        "type": "content",
                        "check": "contains_any",
                        "pattern": "**/*.py",
                        "search": ["->", ": str", ": int", ": bool", ": list", ": dict"],
                        "severity": "major",
                        "action": "Add type hints to function signatures",
                    },
                ],
            },
            {
                "name": "Test Coverage",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "Test directory exists",
                        "type": "binary",
                        "check": "dir_exists",
                        "path": "tests",
                        "severity": "critical",
                        "action": "Create tests/ directory with test files",
                    },
                ],
            },
            {
                "name": "Documentation",
                "weight": 0.15,
                "criteria": [
                    {
                        "name": "README.md exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": "README.md",
                        "severity": "critical",
                        "action": "Create README.md",
                    },
                    {
                        "name": "CHANGELOG.md exists",
                        "type": "binary",
                        "check": "file_exists",
                        "path": "CHANGELOG.md",
                        "severity": "minor",
                        "action": "Create CHANGELOG.md",
                    },
                ],
            },
            {
                "name": "Deployment Readiness",
                "weight": 0.10,
                "criteria": [
                    {
                        "name": "License file exists",
                        "type": "binary",
                        "check": "file_exists_any",
                        "paths": ["LICENSE", "LICENSE.md", "LICENSE.txt"],
                        "severity": "major",
                        "action": "Add LICENSE file",
                    },
                ],
            },
        ],
    }


def get_document_template() -> dict:
    """Return the document project template."""
    return {
        "template_id": "document",
        "display_name": "Documentation Project",
        "description": "Evaluation template for documentation-only projects",
        "dimensions": [
            {
                "name": "Content Completeness",
                "weight": 0.40,
                "criteria": [
                    {
                        "name": "Main document exists",
                        "type": "binary",
                        "check": "file_exists_any",
                        "paths": ["README.md", "index.md", "main.md"],
                        "severity": "critical",
                        "action": "Create main document file",
                    },
                    {
                        "name": "No TODO placeholders",
                        "type": "content",
                        "check": "no_pattern",
                        "pattern": "**/*.md",
                        "forbidden": ["TODO", "TBD", "FIXME"],
                        "severity": "major",
                        "action": "Replace TODO/TBD/FIXME with actual content",
                    },
                ],
            },
            {
                "name": "Structure & Organization",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "Table of contents present",
                        "type": "content",
                        "check": "has_heading_any",
                        "pattern": "**/*.md",
                        "headings": ["## Table of Contents", "## Contents", "## TOC"],
                        "severity": "minor",
                        "action": "Add table of contents section",
                    },
                ],
            },
            {
                "name": "Quality & Clarity",
                "weight": 0.25,
                "criteria": [
                    {
                        "name": "Headings use consistent style",
                        "type": "content",
                        "check": "heading_hierarchy",
                        "pattern": "**/*.md",
                        "severity": "minor",
                        "action": "Fix heading hierarchy (H1 -> H2 -> H3)",
                    },
                ],
            },
            {
                "name": "Accessibility",
                "weight": 0.10,
                "criteria": [
                    {
                        "name": "Images have alt text",
                        "type": "content",
                        "check": "images_have_alt",
                        "pattern": "**/*.md",
                        "severity": "major",
                        "action": "Add alt text to all images: ![alt text](image.png)",
                    },
                ],
            },
        ],
    }


def get_templates() -> dict:
    """Return all available templates."""
    return {
        "skill": get_skill_template(),
        "webapp": get_webapp_template(),
        "library": get_library_template(),
        "document": get_document_template(),
    }


class ProjectScorer:
    """Evaluates project completeness against a template."""

    def __init__(self, project_path: Path, template: dict):
        self.project_path = project_path
        self.template = template
        self.dimensions: list[Dimension] = []
        self.gaps: list[Gap] = []

    def check_file_exists(self, path: str) -> tuple[bool, str]:
        """Check if a file exists."""
        full_path = self.project_path / path
        exists = full_path.is_file()
        return exists, f"File {'exists' if exists else 'missing'}: {path}"

    def check_dir_exists(self, path: str) -> tuple[bool, str]:
        """Check if a directory exists."""
        full_path = self.project_path / path
        exists = full_path.is_dir()
        return exists, f"Directory {'exists' if exists else 'missing'}: {path}"

    def check_file_exists_any(self, paths: list[str]) -> tuple[bool, str]:
        """Check if any of the files exist."""
        for path in paths:
            if (self.project_path / path).is_file():
                return True, f"Found: {path}"
        return False, f"None found: {', '.join(paths)}"

    def check_dir_exists_any(self, paths: list[str]) -> tuple[bool, str]:
        """Check if any of the directories exist."""
        for path in paths:
            if (self.project_path / path).is_dir():
                return True, f"Found: {path}"
        return False, f"None found: {', '.join(paths)}"

    def check_file_count(self, pattern: str, minimum: int) -> tuple[bool, str]:
        """Check if minimum number of files matching pattern exist."""
        matches = list(self.project_path.glob(pattern))
        count = len(matches)
        met = count >= minimum
        return met, f"Found {count} files (minimum: {minimum})"

    def check_test_count(self, pattern: str, minimum: int) -> tuple[bool, str]:
        """Count test functions in test files."""
        matches = list(self.project_path.glob(pattern))
        test_count = 0
        for match in matches:
            try:
                content = match.read_text()
                # Count def test_ and async def test_ functions
                test_count += len(re.findall(r"(async\s+)?def\s+test_", content))
            except (OSError, UnicodeDecodeError):
                continue
        met = test_count >= minimum
        return met, f"Found {test_count} test functions (minimum: {minimum})"

    def check_yaml_frontmatter(self, path: str) -> tuple[bool, str]:
        """Check if file has valid YAML frontmatter."""
        full_path = self.project_path / path
        if not full_path.is_file():
            return False, "File does not exist"
        try:
            content = full_path.read_text()
            if content.startswith("---"):
                # Find closing ---
                end_idx = content.find("---", 3)
                if end_idx > 3:
                    frontmatter = content[3:end_idx].strip()
                    if "name:" in frontmatter and "description:" in frontmatter:
                        return True, "Valid YAML frontmatter found"
                    return False, "Missing name or description in frontmatter"
            return False, "No YAML frontmatter (must start with ---)"
        except (OSError, UnicodeDecodeError) as e:
            return False, f"Error reading file: {e}"

    def check_has_heading(self, path: str, heading: str) -> tuple[bool, str]:
        """Check if file contains a specific heading."""
        full_path = self.project_path / path
        if not full_path.is_file():
            return False, "File does not exist"
        try:
            content = full_path.read_text()
            # Case-insensitive heading check
            pattern = re.escape(heading)
            if re.search(pattern, content, re.IGNORECASE):
                return True, f"Found heading: {heading}"
            return False, f"Missing heading: {heading}"
        except (OSError, UnicodeDecodeError) as e:
            return False, f"Error reading file: {e}"

    def check_shebang(self, pattern: str) -> tuple[bool, str]:
        """Check if Python files have shebang."""
        matches = list(self.project_path.glob(pattern))
        if not matches:
            return True, "No Python files to check"
        missing = []
        for match in matches:
            try:
                content = match.read_text()
                if not content.startswith("#!"):
                    missing.append(match.name)
            except (OSError, UnicodeDecodeError):
                continue
        if missing:
            return False, f"Missing shebang in: {', '.join(missing)}"
        return True, "All Python files have shebang"

    def check_no_pattern(self, pattern: str, forbidden: list[str]) -> tuple[bool, str]:
        """Check that files don't contain forbidden patterns."""
        matches = list(self.project_path.glob(pattern))
        found = []
        for match in matches:
            try:
                content = match.read_text()
                for f in forbidden:
                    if f in content:
                        found.append(f"{match.name}: {f}")
            except (OSError, UnicodeDecodeError):
                continue
        if found:
            return False, f"Found forbidden patterns: {', '.join(found[:3])}"
        return True, "No forbidden patterns found"

    def check_contains(self, pattern: str, search: str) -> tuple[bool, str]:
        """Check if any file matching pattern contains search string."""
        matches = list(self.project_path.glob(pattern))
        for match in matches:
            try:
                content = match.read_text()
                if search in content:
                    return True, f"Found '{search}' in {match.name}"
            except (OSError, UnicodeDecodeError):
                continue
        return False, f"'{search}' not found in any matching files"

    def check_contains_any(self, pattern: str, search: list[str]) -> tuple[bool, str]:
        """Check if any file contains any of the search strings."""
        matches = list(self.project_path.glob(pattern))
        for match in matches:
            try:
                content = match.read_text()
                for s in search:
                    if s in content:
                        return True, f"Found '{s}' in {match.name}"
            except (OSError, UnicodeDecodeError):
                continue
        return False, "None of the patterns found"

    def check_has_heading_any(self, pattern: str, headings: list[str]) -> tuple[bool, str]:
        """Check if any file contains any of the headings."""
        matches = list(self.project_path.glob(pattern))
        for match in matches:
            try:
                content = match.read_text()
                for h in headings:
                    if re.search(re.escape(h), content, re.IGNORECASE):
                        return True, f"Found heading: {h}"
            except (OSError, UnicodeDecodeError):
                continue
        return False, "No matching headings found"

    def check_heading_hierarchy(self, pattern: str) -> tuple[bool, str]:
        """Check that markdown files have proper heading hierarchy."""
        matches = list(self.project_path.glob(pattern))
        for match in matches:
            try:
                content = match.read_text()
                lines = content.split("\n")
                prev_level = 0
                for line in lines:
                    if line.startswith("#"):
                        level = len(line) - len(line.lstrip("#"))
                        if prev_level > 0 and level > prev_level + 1:
                            return False, f"Hierarchy skip in {match.name}"
                        prev_level = level
            except (OSError, UnicodeDecodeError):
                continue
        return True, "Heading hierarchy is valid"

    def check_images_have_alt(self, pattern: str) -> tuple[bool, str]:
        """Check that images in markdown have alt text."""
        matches = list(self.project_path.glob(pattern))
        missing_alt = []
        for match in matches:
            try:
                content = match.read_text()
                # Find images without alt text: ![](...)
                if re.search(r"!\[\]\(", content):
                    missing_alt.append(match.name)
            except (OSError, UnicodeDecodeError):
                continue
        if missing_alt:
            return False, f"Missing alt text in: {', '.join(missing_alt)}"
        return True, "All images have alt text"

    def evaluate_criterion(self, criterion_def: dict) -> Criterion:
        """Evaluate a single criterion."""
        c = Criterion(
            name=criterion_def["name"],
            criterion_type=criterion_def["type"],
            severity=criterion_def["severity"],
            check_type=criterion_def["check"],
            action=criterion_def.get("action", ""),
        )

        check = criterion_def["check"]
        if check == "file_exists":
            c.met, c.details = self.check_file_exists(criterion_def["path"])
        elif check == "dir_exists":
            c.met, c.details = self.check_dir_exists(criterion_def["path"])
        elif check == "file_exists_any":
            c.met, c.details = self.check_file_exists_any(criterion_def["paths"])
        elif check == "dir_exists_any":
            c.met, c.details = self.check_dir_exists_any(criterion_def["paths"])
        elif check == "file_count":
            c.met, c.details = self.check_file_count(criterion_def["pattern"], criterion_def["minimum"])
        elif check == "test_count":
            c.met, c.details = self.check_test_count(criterion_def["pattern"], criterion_def["minimum"])
        elif check == "yaml_frontmatter":
            c.met, c.details = self.check_yaml_frontmatter(criterion_def["path"])
        elif check == "has_heading":
            c.met, c.details = self.check_has_heading(criterion_def["path"], criterion_def["heading"])
        elif check == "shebang":
            c.met, c.details = self.check_shebang(criterion_def["pattern"])
        elif check == "no_pattern":
            c.met, c.details = self.check_no_pattern(criterion_def["pattern"], criterion_def["forbidden"])
        elif check == "contains":
            c.met, c.details = self.check_contains(criterion_def["pattern"], criterion_def["search"])
        elif check == "contains_any":
            c.met, c.details = self.check_contains_any(criterion_def["pattern"], criterion_def["search"])
        elif check == "has_heading_any":
            c.met, c.details = self.check_has_heading_any(criterion_def["pattern"], criterion_def["headings"])
        elif check == "heading_hierarchy":
            c.met, c.details = self.check_heading_hierarchy(criterion_def["pattern"])
        elif check == "images_have_alt":
            c.met, c.details = self.check_images_have_alt(criterion_def["pattern"])
        else:
            c.met = False
            c.details = f"Unknown check type: {check}"

        c.score = 100.0 if c.met else 0.0
        return c

    def evaluate_dimension(self, dim_def: dict) -> Dimension:
        """Evaluate a dimension and all its criteria."""
        dim = Dimension(name=dim_def["name"], weight=dim_def["weight"])

        critical_missing = False
        total_score = 0.0
        for crit_def in dim_def["criteria"]:
            criterion = self.evaluate_criterion(crit_def)
            dim.criteria.append(criterion)
            total_score += criterion.score
            if not criterion.met and criterion.severity == "critical":
                critical_missing = True

        if dim.criteria:
            dim.raw_score = total_score / len(dim.criteria)
        else:
            dim.raw_score = 100.0

        # Critical missing caps dimension at 60%
        if critical_missing:
            dim.raw_score = min(dim.raw_score, 60.0)

        dim.weighted_score = dim.raw_score * dim.weight
        return dim

    def calculate_priority(self, severity: str, dim_weight: float, effort: str) -> float:
        """Calculate gap priority score."""
        impact = SEVERITY_WEIGHTS.get(severity, 1) * dim_weight * 100
        effort_mult = EFFORT_MULTIPLIERS.get(effort, 2)
        return impact / effort_mult

    def estimate_effort(self, criterion: Criterion) -> str:
        """Estimate effort to fix a gap based on criterion type."""
        # Simple heuristic based on check type
        low_effort = {"file_exists", "dir_exists", "shebang"}
        high_effort = {"test_count", "contains", "heading_hierarchy"}

        if criterion.check_type in low_effort:
            return "low"
        elif criterion.check_type in high_effort:
            return "high"
        return "medium"

    def score(self) -> ScoringResult:
        """Run the full scoring process."""
        # Evaluate all dimensions
        for dim_def in self.template["dimensions"]:
            dim = self.evaluate_dimension(dim_def)
            self.dimensions.append(dim)

            # Collect gaps
            for criterion in dim.criteria:
                if not criterion.met:
                    effort = self.estimate_effort(criterion)
                    priority = self.calculate_priority(criterion.severity, dim.weight, effort)
                    self.gaps.append(
                        Gap(
                            criterion=criterion.name,
                            dimension=dim.name,
                            severity=criterion.severity,
                            effort=effort,
                            priority=priority,
                            action=criterion.action,
                        )
                    )

        # Sort gaps by priority (descending)
        self.gaps.sort(key=lambda g: g.priority, reverse=True)

        # Calculate overall score
        overall = sum(d.weighted_score for d in self.dimensions)

        # Prepare summary
        critical_gaps = len([g for g in self.gaps if g.severity == "critical"])
        major_gaps = len([g for g in self.gaps if g.severity == "major"])
        minor_gaps = len([g for g in self.gaps if g.severity == "minor"])
        ready = critical_gaps == 0 and major_gaps == 0

        return ScoringResult(
            project_path=str(self.project_path),
            project_type=self.template["template_id"],
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=round(overall),
            dimensions=[
                {
                    "name": d.name,
                    "weight": d.weight,
                    "raw_score": round(d.raw_score, 1),
                    "weighted_score": round(d.weighted_score, 2),
                    "criteria": [
                        {
                            "name": c.name,
                            "met": c.met,
                            "severity": c.severity,
                            "details": c.details,
                        }
                        for c in d.criteria
                    ],
                }
                for d in self.dimensions
            ],
            gaps=[
                {
                    "criterion": g.criterion,
                    "dimension": g.dimension,
                    "severity": g.severity,
                    "effort": g.effort,
                    "priority": round(g.priority, 2),
                    "action": g.action,
                }
                for g in self.gaps
            ],
            summary={
                "critical_gaps": critical_gaps,
                "major_gaps": major_gaps,
                "minor_gaps": minor_gaps,
                "ready_for_release": ready,
            },
        )


def generate_markdown_report(result: ScoringResult) -> str:
    """Generate a markdown report from scoring result."""
    lines = [
        "# Project Completeness Report",
        "",
        f"**Project**: {result.project_path}",
        f"**Type**: {result.project_type}",
        f"**Date**: {result.timestamp[:10]}",
        f"**Overall Score**: {result.overall_score}/100",
        "",
        "## Score Breakdown",
        "",
        "| Dimension | Weight | Score | Weighted |",
        "|-----------|--------|-------|----------|",
    ]

    for dim in result.dimensions:
        lines.append(
            f"| {dim['name']} | {int(dim['weight'] * 100)}% | {dim['raw_score']:.0f} | {dim['weighted_score']:.1f} |"
        )

    lines.extend(["", "## Dimension Details", ""])

    for dim in result.dimensions:
        lines.append(f"### {dim['name']}")
        lines.append("")
        for crit in dim["criteria"]:
            status = "+" if crit["met"] else "x"
            severity_badge = f"[{crit['severity'].upper()}]"
            lines.append(f"- [{status}] {severity_badge} {crit['name']}")
            lines.append(f"  - {crit['details']}")
        lines.append("")

    if result.gaps:
        lines.extend(["## Priority Actions", ""])
        for i, gap in enumerate(result.gaps, 1):
            severity_badge = f"**[{gap['severity'].capitalize()}]**"
            lines.append(f"{i}. {severity_badge} {gap['action']}")
            lines.append(f"   - Dimension: {gap['dimension']}, Effort: {gap['effort']}")
        lines.append("")

    lines.extend(
        [
            "## Readiness Assessment",
            "",
            f"- Critical Gaps: {result.summary['critical_gaps']}",
            f"- Major Gaps: {result.summary['major_gaps']}",
            f"- Minor Gaps: {result.summary['minor_gaps']}",
            f"- **Ready for Release**: {'Yes' if result.summary['ready_for_release'] else 'No (resolve gaps first)'}",
        ]
    )

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Evaluate project completeness and generate a score.")
    parser.add_argument(
        "--project-path",
        "-p",
        type=Path,
        help="Path to the project directory",
    )
    parser.add_argument(
        "--template",
        "-t",
        choices=["skill", "webapp", "library", "document", "custom"],
        default="skill",
        help="Evaluation template to use (default: skill)",
    )
    parser.add_argument(
        "--template-file",
        type=Path,
        help="Path to custom template JSON file (requires --template custom)",
    )
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available templates and exit",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        help="Output directory for reports",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "markdown", "both"],
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed evaluation progress",
    )

    args = parser.parse_args()

    if args.list_templates:
        templates = get_templates()
        print("Available templates:\n")
        for tid, t in templates.items():
            print(f"  {tid}: {t['display_name']}")
            print(f"    {t['description']}")
            print()
        return 0

    if not args.project_path:
        print("Error: --project-path is required", file=sys.stderr)
        return 1

    if not args.project_path.is_dir():
        print(f"Error: {args.project_path} is not a directory", file=sys.stderr)
        return 1

    # Load template
    if args.template == "custom":
        if not args.template_file:
            print("Error: --template-file required with custom template", file=sys.stderr)
            return 1
        try:
            template = json.loads(args.template_file.read_text())
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error loading custom template: {e}", file=sys.stderr)
            return 1
    else:
        templates = get_templates()
        template = templates[args.template]

    if args.verbose:
        print(f"Evaluating: {args.project_path}")
        print(f"Template: {template['display_name']}")
        print()

    # Run scoring
    scorer = ProjectScorer(args.project_path, template)
    result = scorer.score()

    # Generate output
    json_report = json.dumps(
        {
            "schema_version": "1.0",
            "project_path": result.project_path,
            "project_type": result.project_type,
            "timestamp": result.timestamp,
            "overall_score": result.overall_score,
            "dimensions": result.dimensions,
            "gaps": result.gaps,
            "summary": result.summary,
        },
        indent=2,
    )
    md_report = generate_markdown_report(result)

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"completeness_{args.project_path.name}_{timestamp}"

        if args.format in ("json", "both"):
            json_path = args.output_dir / f"{base_name}.json"
            json_path.write_text(json_report)
            print(f"JSON report: {json_path}")

        if args.format in ("markdown", "both"):
            md_path = args.output_dir / f"{base_name}.md"
            md_path.write_text(md_report)
            print(f"Markdown report: {md_path}")
    else:
        # Output to stdout
        if args.format == "json":
            print(json_report)
        elif args.format == "markdown":
            print(md_report)
        else:
            print("=== JSON Report ===")
            print(json_report)
            print("\n=== Markdown Report ===")
            print(md_report)

    # Summary to stderr for visibility
    print(f"\nOverall Score: {result.overall_score}/100", file=sys.stderr)
    if result.summary["ready_for_release"]:
        print("Status: Ready for release", file=sys.stderr)
    else:
        print(
            f"Status: {result.summary['critical_gaps']} critical, {result.summary['major_gaps']} major gaps remain",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
