#!/usr/bin/env python3
"""
Skill Template Validator

Validates Claude skill directories against standard structure and best practices.
Detects structural issues, metadata problems, and quality concerns.

Usage:
    python3 validate_skill.py /path/to/skill-name [--check CATEGORY] [--format FORMAT]

Examples:
    python3 validate_skill.py ./my-skill
    python3 validate_skill.py ./my-skill --check frontmatter
    python3 validate_skill.py ./my-skill --format json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


class Severity(Enum):
    """Issue severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A single validation issue."""

    severity: Severity
    code: str
    message: str
    suggestion: str
    file: Optional[str] = None
    line: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON output."""
        result = {
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
            "suggestion": self.suggestion,
        }
        if self.file:
            result["file"] = self.file
        if self.line:
            result["line"] = self.line
        return result


@dataclass
class ValidationResult:
    """Result of a validation check category."""

    category: str
    passed: bool = True
    issues: list = field(default_factory=list)

    def add_issue(self, issue: ValidationIssue):
        """Add an issue to the result."""
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.passed = False


@dataclass
class FullValidationResult:
    """Complete validation result across all categories."""

    skill_name: str
    skill_path: str
    timestamp: str
    checks: dict = field(default_factory=dict)
    passed: bool = True

    def add_check(self, result: ValidationResult):
        """Add a category check result."""
        self.checks[result.category] = result
        if not result.passed:
            self.passed = False

    @property
    def total_errors(self) -> int:
        """Count total errors across all checks."""
        return sum(1 for check in self.checks.values() for issue in check.issues if issue.severity == Severity.ERROR)

    @property
    def total_warnings(self) -> int:
        """Count total warnings across all checks."""
        return sum(1 for check in self.checks.values() for issue in check.issues if issue.severity == Severity.WARNING)

    @property
    def total_info(self) -> int:
        """Count total info messages across all checks."""
        return sum(1 for check in self.checks.values() for issue in check.issues if issue.severity == Severity.INFO)

    def to_json(self) -> str:
        """Convert to JSON string."""
        data = {
            "schema_version": "1.0",
            "skill_name": self.skill_name,
            "skill_path": self.skill_path,
            "timestamp": self.timestamp,
            "checks": {
                name: {"passed": check.passed, "issues": [i.to_dict() for i in check.issues]}
                for name, check in self.checks.items()
            },
            "summary": {
                "total_errors": self.total_errors,
                "total_warnings": self.total_warnings,
                "total_info": self.total_info,
                "status": "PASS" if self.passed else "FAIL",
            },
        }
        return json.dumps(data, indent=2)

    def to_console(self) -> str:
        """Format for console output."""
        lines = [
            "=== Skill Template Validation Report ===",
            f"Skill: {self.skill_name}",
            f"Path: {self.skill_path}",
            f"Timestamp: {self.timestamp}",
            "",
        ]

        for name, check in self.checks.items():
            lines.append(f"{name.upper()} CHECK")
            if not check.issues:
                lines.append("  [PASS] All checks passed")
            else:
                for issue in check.issues:
                    status = {
                        Severity.ERROR: "ERROR",
                        Severity.WARNING: "WARN",
                        Severity.INFO: "INFO",
                    }[issue.severity]
                    loc = ""
                    if issue.file and issue.line:
                        loc = f" ({issue.file}:{issue.line})"
                    elif issue.file:
                        loc = f" ({issue.file})"
                    lines.append(f"  [{status}] {issue.message}{loc}")
                    lines.append(f"         -> {issue.suggestion}")
            lines.append("")

        lines.extend(
            [
                "SUMMARY",
                f"  Errors: {self.total_errors}",
                f"  Warnings: {self.total_warnings}",
                f"  Info: {self.total_info}",
                f"  Status: {'PASS' if self.passed else 'FAIL'}",
            ]
        )

        return "\n".join(lines)


class SkillValidator:
    """Validates a skill directory against standards."""

    # Pattern for valid skill directory names
    VALID_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")

    # Patterns for detecting problematic paths
    # Match absolute paths but exclude common placeholders like /Users/name/...
    ABSOLUTE_PATH_PATTERN = re.compile(
        r'(?<![`\w])(/(?:usr|bin|opt|etc|var|tmp|home|Users)/(?!name/|username/|<)[^\s`\'")\]]+)'
    )
    # Match actual usernames (not placeholder words like 'name', 'username', 'user')
    USERNAME_PATH_PATTERN = re.compile(r"/(?:Users|home)/(?!name\b|username\b|user\b)[a-zA-Z][a-zA-Z0-9_-]{2,}/")
    REPO_RELATIVE_PATTERN = re.compile(r"skills/[a-z][a-z0-9-]+/")

    # Required sections in SKILL.md
    REQUIRED_SECTIONS = ["Overview", "When to Use", "Workflow"]
    RECOMMENDED_SECTIONS = ["Prerequisites", "Output Format", "Resources"]

    def __init__(self, skill_path: Path):
        """Initialize validator with skill directory path."""
        self.skill_path = Path(skill_path).resolve()
        self.skill_name = self.skill_path.name
        self.skill_md_path = self.skill_path / "SKILL.md"
        self._skill_md_content: Optional[str] = None
        self._frontmatter: Optional[dict] = None

    @property
    def skill_md_content(self) -> Optional[str]:
        """Lazy load SKILL.md content."""
        if self._skill_md_content is None and self.skill_md_path.exists():
            self._skill_md_content = self.skill_md_path.read_text()
        return self._skill_md_content

    def _parse_frontmatter(self) -> tuple[Optional[dict], list[ValidationIssue]]:
        """Parse YAML frontmatter from SKILL.md."""
        issues = []
        content = self.skill_md_content

        if not content:
            return None, issues

        # Check if content starts with frontmatter
        if not content.startswith("---"):
            # Check if there's content before frontmatter
            if "---" in content:
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="FRONT002",
                        message="Content found before frontmatter",
                        suggestion="Move all content after the closing `---` of frontmatter",
                        file="SKILL.md",
                        line=1,
                    )
                )
            else:
                issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="FRONT001",
                        message="YAML frontmatter not found",
                        suggestion="Add YAML frontmatter at the very beginning of SKILL.md",
                        file="SKILL.md",
                        line=1,
                    )
                )
            return None, issues

        # Find closing ---
        lines = content.split("\n")
        end_index = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end_index = i
                break

        if end_index is None:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="FRONT003",
                    message="Frontmatter not properly closed",
                    suggestion="Add closing `---` after frontmatter fields",
                    file="SKILL.md",
                )
            )
            return None, issues

        # Parse YAML
        yaml_content = "\n".join(lines[1:end_index])
        try:
            # Simple YAML parsing (key: value)
            frontmatter = {}
            for line in yaml_content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
            return frontmatter, issues
        except Exception as e:
            issues.append(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="FRONT004",
                    message=f"Invalid YAML syntax in frontmatter: {e}",
                    suggestion="Check YAML syntax: proper indentation, colon-space separators",
                    file="SKILL.md",
                )
            )
            return None, issues

    def validate_structure(self) -> ValidationResult:
        """Validate skill directory structure."""
        result = ValidationResult(category="structure")

        # STRUCT001: Check SKILL.md exists
        if not self.skill_md_path.exists():
            result.add_issue(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="STRUCT001",
                    message="SKILL.md not found in skill directory",
                    suggestion="Create SKILL.md with YAML frontmatter as the first content",
                    file="SKILL.md",
                )
            )

        # STRUCT002: Validate directory name
        if not self.VALID_NAME_PATTERN.match(self.skill_name):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="STRUCT002",
                    message=f"Directory name '{self.skill_name}' is invalid",
                    suggestion="Use lowercase letters and hyphens only (e.g., 'my-skill-name')",
                )
            )

        # STRUCT003: Check scripts/ directory
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="STRUCT003",
                    message="scripts/ directory not found",
                    suggestion="Create scripts/ directory or mark as knowledge-only skill",
                )
            )
        else:
            # STRUCT005: Check if scripts/ is empty
            py_files = list(scripts_dir.glob("*.py"))
            sh_files = list(scripts_dir.glob("*.sh"))
            if not py_files and not sh_files:
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        code="STRUCT005",
                        message="scripts/ directory is empty",
                        suggestion="Add executable scripts or remove empty directory",
                    )
                )
            else:
                # STRUCT007: Check scripts/tests/ directory
                tests_dir = scripts_dir / "tests"
                if not tests_dir.exists():
                    result.add_issue(
                        ValidationIssue(
                            severity=Severity.WARNING,
                            code="STRUCT007",
                            message="scripts/tests/ directory not found",
                            suggestion="Create scripts/tests/ with conftest.py and test files",
                        )
                    )
                else:
                    # STRUCT008: Check for test files
                    test_files = list(tests_dir.glob("test_*.py"))
                    if not test_files:
                        result.add_issue(
                            ValidationIssue(
                                severity=Severity.WARNING,
                                code="STRUCT008",
                                message="No test files found in scripts/tests/",
                                suggestion="Add at least 3 test files with meaningful test coverage",
                            )
                        )

                    # STRUCT009: Check for conftest.py
                    if not (tests_dir / "conftest.py").exists():
                        result.add_issue(
                            ValidationIssue(
                                severity=Severity.WARNING,
                                code="STRUCT009",
                                message="conftest.py not found in scripts/tests/",
                                suggestion="Create conftest.py with sys.path setup for imports",
                            )
                        )

        # STRUCT004: Check references/ directory
        refs_dir = self.skill_path / "references"
        if not refs_dir.exists():
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="STRUCT004",
                    message="references/ directory not found",
                    suggestion="Create references/ directory with at least one documentation file",
                )
            )
        else:
            # STRUCT006: Check if references/ is empty
            ref_files = list(refs_dir.glob("*"))
            if not ref_files:
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        code="STRUCT006",
                        message="references/ directory is empty",
                        suggestion="Add reference documentation or remove empty directory",
                    )
                )

        return result

    def validate_frontmatter(self) -> ValidationResult:
        """Validate YAML frontmatter in SKILL.md."""
        result = ValidationResult(category="frontmatter")

        if not self.skill_md_path.exists():
            return result

        frontmatter, parse_issues = self._parse_frontmatter()
        for issue in parse_issues:
            result.add_issue(issue)

        if frontmatter is None:
            return result

        # FRONT005: Check name field
        if "name" not in frontmatter:
            result.add_issue(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="FRONT005",
                    message="Required field 'name' not found in frontmatter",
                    suggestion=f"Add 'name: {self.skill_name}' matching the directory name",
                    file="SKILL.md",
                )
            )
        else:
            # FRONT006: Check name matches directory
            if frontmatter["name"] != self.skill_name:
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="FRONT006",
                        message=f"Frontmatter name '{frontmatter['name']}' does not match directory name '{self.skill_name}'",
                        suggestion=f"Change name to exactly match directory: 'name: {self.skill_name}'",
                        file="SKILL.md",
                    )
                )

            # FRONT010: Check for empty name
            if not frontmatter["name"].strip():
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="FRONT010",
                        message="Field 'name' has empty value",
                        suggestion="Provide a meaningful value for 'name'",
                        file="SKILL.md",
                    )
                )

        # FRONT007: Check description field
        if "description" not in frontmatter:
            result.add_issue(
                ValidationIssue(
                    severity=Severity.ERROR,
                    code="FRONT007",
                    message="Required field 'description' not found in frontmatter",
                    suggestion="Add 'description: ...' explaining when to trigger the skill",
                    file="SKILL.md",
                )
            )
        else:
            desc = frontmatter["description"]
            # FRONT010: Check for empty description
            if not desc.strip():
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="FRONT010",
                        message="Field 'description' has empty value",
                        suggestion="Provide a meaningful value for 'description'",
                        file="SKILL.md",
                    )
                )
            else:
                # FRONT008: Check description length
                if len(desc) < 20:
                    result.add_issue(
                        ValidationIssue(
                            severity=Severity.WARNING,
                            code="FRONT008",
                            message=f"Description is too short ({len(desc)} chars, minimum 20)",
                            suggestion="Expand description to clearly explain trigger conditions",
                            file="SKILL.md",
                        )
                    )

                # FRONT009: Check description not too long
                if len(desc) > 500:
                    result.add_issue(
                        ValidationIssue(
                            severity=Severity.WARNING,
                            code="FRONT009",
                            message=f"Description is too long ({len(desc)} chars, maximum 500)",
                            suggestion="Condense description; move details to Overview section",
                            file="SKILL.md",
                        )
                    )

        return result

    def validate_paths(self) -> ValidationResult:
        """Validate path references in SKILL.md and scripts."""
        result = ValidationResult(category="paths")

        if not self.skill_md_path.exists():
            return result

        content = self.skill_md_content
        lines = content.split("\n")

        for i, line in enumerate(lines, start=1):
            # PATH001: Check for hardcoded absolute paths
            matches = self.ABSOLUTE_PATH_PATTERN.findall(line)
            for match in matches:
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="PATH001",
                        message=f"Hardcoded absolute path found: '{match}'",
                        suggestion="Use relative paths (e.g., 'scripts/...' or 'references/...')",
                        file="SKILL.md",
                        line=i,
                    )
                )

            # PATH002: Check for username in paths
            if self.USERNAME_PATH_PATTERN.search(line):
                match = self.USERNAME_PATH_PATTERN.search(line)
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        code="PATH002",
                        message=f"Personal username in path: '{match.group()}'",
                        suggestion="Remove personal paths; use relative paths or $HOME",
                        file="SKILL.md",
                        line=i,
                    )
                )

            # PATH004: Check for repo-relative paths
            if self.REPO_RELATIVE_PATTERN.search(line):
                match = self.REPO_RELATIVE_PATTERN.search(line)
                result.add_issue(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        code="PATH004",
                        message=f"Repo-relative path found: '{match.group()}'",
                        suggestion="Use skill-relative paths (e.g., 'scripts/...' not 'skills/name/scripts/...')",
                        file="SKILL.md",
                        line=i,
                    )
                )

        return result

    def validate_content(self) -> ValidationResult:
        """Validate SKILL.md content quality."""
        result = ValidationResult(category="content")

        if not self.skill_md_path.exists():
            return result

        content = self.skill_md_content

        # CONTENT001: Check for Overview section
        if not re.search(r"^## Overview", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT001",
                    message="Overview section not found",
                    suggestion="Add '## Overview' with 2-3 sentences describing the skill",
                    file="SKILL.md",
                )
            )

        # CONTENT002: Check for When to Use section
        if not re.search(r"^## When to Use", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT002",
                    message="When to Use section not found",
                    suggestion="Add '## When to Use' with bullet list of trigger conditions",
                    file="SKILL.md",
                )
            )

        # CONTENT003: Check for Workflow section
        if not re.search(r"^## Workflow", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT003",
                    message="Workflow section not found",
                    suggestion="Add '## Workflow' with numbered steps using imperative verbs",
                    file="SKILL.md",
                )
            )

        # CONTENT004: Check for Prerequisites section
        if not re.search(r"^## Prerequisites", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT004",
                    message="Prerequisites section not found",
                    suggestion="Add '## Prerequisites' listing Python version, API keys, dependencies",
                    file="SKILL.md",
                )
            )

        # CONTENT005: Check for Output Format section
        if not re.search(r"^## Output Format", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT005",
                    message="Output Format section not found",
                    suggestion="Add '## Output Format' showing expected output structure",
                    file="SKILL.md",
                )
            )

        # CONTENT007: Check for Resources section
        if not re.search(r"^## Resources", content, re.MULTILINE):
            result.add_issue(
                ValidationIssue(
                    severity=Severity.WARNING,
                    code="CONTENT007",
                    message="Resources section not found",
                    suggestion="Add '## Resources' listing all scripts and reference files",
                    file="SKILL.md",
                )
            )

        return result

    def validate_all(self) -> FullValidationResult:
        """Run all validation checks."""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        full_result = FullValidationResult(
            skill_name=self.skill_name,
            skill_path=str(self.skill_path),
            timestamp=timestamp,
        )

        # Run all validations
        full_result.add_check(self.validate_structure())
        full_result.add_check(self.validate_frontmatter())
        full_result.add_check(self.validate_paths())
        full_result.add_check(self.validate_content())

        return full_result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Claude skill templates against standard structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s ./my-skill
    %(prog)s ./my-skill --check frontmatter
    %(prog)s ./my-skill --format json
        """,
    )
    parser.add_argument("skill_path", help="Path to skill directory to validate")
    parser.add_argument(
        "--check",
        "-c",
        choices=["structure", "frontmatter", "paths", "content"],
        help="Run only specified validation category",
    )
    parser.add_argument(
        "--format", "-f", choices=["console", "json"], default="console", help="Output format (default: console)"
    )

    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Skill path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(2)
    if not skill_path.is_dir():
        print(f"Error: Skill path is not a directory: {skill_path}", file=sys.stderr)
        sys.exit(2)

    validator = SkillValidator(skill_path)

    if args.check:
        # Run single check
        check_methods = {
            "structure": validator.validate_structure,
            "frontmatter": validator.validate_frontmatter,
            "paths": validator.validate_paths,
            "content": validator.validate_content,
        }
        result = check_methods[args.check]()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        full_result = FullValidationResult(
            skill_name=validator.skill_name,
            skill_path=str(validator.skill_path),
            timestamp=timestamp,
        )
        full_result.add_check(result)
    else:
        full_result = validator.validate_all()

    # Output results
    if args.format == "json":
        print(full_result.to_json())
    else:
        print(full_result.to_console())

    # Exit code
    sys.exit(0 if full_result.passed else 1)


if __name__ == "__main__":
    main()
