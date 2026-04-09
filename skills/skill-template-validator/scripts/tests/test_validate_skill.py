"""Tests for validate_skill.py - skill template validation."""

import json
from pathlib import Path

import pytest
from validate_skill import (
    Severity,
    SkillValidator,
    ValidationIssue,
    ValidationResult,
)


class TestValidationIssue:
    """Tests for ValidationIssue dataclass."""

    def test_issue_creation(self):
        """Test creating a validation issue with all fields."""
        issue = ValidationIssue(
            severity=Severity.ERROR,
            code="STRUCT001",
            message="SKILL.md not found",
            suggestion="Create SKILL.md file",
            file="SKILL.md",
            line=None,
        )
        assert issue.severity == Severity.ERROR
        assert issue.code == "STRUCT001"
        assert issue.message == "SKILL.md not found"
        assert issue.suggestion == "Create SKILL.md file"

    def test_issue_to_dict(self):
        """Test converting issue to dictionary."""
        issue = ValidationIssue(
            severity=Severity.WARNING,
            code="PATH001",
            message="Hardcoded path found",
            suggestion="Use relative paths",
            file="SKILL.md",
            line=45,
        )
        d = issue.to_dict()
        assert d["severity"] == "warning"
        assert d["code"] == "PATH001"
        assert d["line"] == 45


class TestStructureValidation:
    """Tests for structure validation checks."""

    def test_valid_structure(self, tmp_path):
        """Test validation passes for valid skill structure."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: Test skill description\n---\n# My Skill\n"
        )
        (skill_dir / "scripts").mkdir()
        (skill_dir / "references").mkdir()

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_missing_skill_md(self, tmp_path):
        """Test error when SKILL.md is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "STRUCT001" in error_codes

    def test_invalid_directory_name_uppercase(self, tmp_path):
        """Test error for directory names with uppercase letters."""
        skill_dir = tmp_path / "MySkill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: MySkill\ndescription: Test skill\n---\n")

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "STRUCT002" in error_codes

    def test_invalid_directory_name_underscore(self, tmp_path):
        """Test error for directory names with underscores."""
        skill_dir = tmp_path / "my_skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my_skill\ndescription: Test skill\n---\n")

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "STRUCT002" in error_codes

    def test_missing_scripts_directory(self, tmp_path):
        """Test warning when scripts/ directory is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: Test skill description\n---\n")

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "STRUCT003" in warning_codes

    def test_missing_tests_directory(self, tmp_path):
        """Test warning when scripts/tests/ directory is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: Test skill description\n---\n")
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "main.py").write_text("# script")

        validator = SkillValidator(skill_dir)
        result = validator.validate_structure()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "STRUCT007" in warning_codes


class TestFrontmatterValidation:
    """Tests for YAML frontmatter validation."""

    def test_valid_frontmatter(self, tmp_path):
        """Test validation passes for valid frontmatter."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "---\nname: my-skill\ndescription: A test skill for validation testing purposes\n---\n# My Skill\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_missing_frontmatter(self, tmp_path):
        """Test error when frontmatter is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# My Skill\n\nNo frontmatter here.\n")

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "FRONT001" in error_codes

    def test_content_before_frontmatter(self, tmp_path):
        """Test error when content appears before frontmatter."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "# Title First\n\n---\nname: my-skill\ndescription: Test\n---\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "FRONT002" in error_codes

    def test_missing_name_field(self, tmp_path):
        """Test error when name field is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "---\ndescription: Test skill\n---\n# My Skill\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "FRONT005" in error_codes

    def test_name_mismatch(self, tmp_path):
        """Test error when name doesn't match directory."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "---\nname: different-name\ndescription: Test skill description here\n---\n# My Skill\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "FRONT006" in error_codes

    def test_description_too_short(self, tmp_path):
        """Test warning when description is too short."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "---\nname: my-skill\ndescription: Short\n---\n# My Skill\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_frontmatter()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "FRONT008" in warning_codes


class TestPathValidation:
    """Tests for path validation checks."""

    def test_no_path_issues(self, tmp_path):
        """Test validation passes with clean paths."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

## Workflow

```bash
python3 scripts/main.py
```
"""
        (skill_dir / "SKILL.md").write_text(content)
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "main.py").write_text("# script")

        validator = SkillValidator(skill_dir)
        result = validator.validate_paths()

        errors = [i for i in result.issues if i.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_hardcoded_absolute_path(self, tmp_path):
        """Test error for hardcoded absolute paths."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

## Workflow

```bash
python3 /usr/local/bin/python scripts/main.py
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_paths()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "PATH001" in error_codes

    def test_username_in_path(self, tmp_path):
        """Test error for paths containing username."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

## Workflow

```bash
python3 /Users/john/scripts/main.py
```
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_paths()

        error_codes = [i.code for i in result.issues if i.severity == Severity.ERROR]
        assert "PATH002" in error_codes

    def test_repo_relative_path(self, tmp_path):
        """Test warning for repo-relative paths."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

See `skills/my-skill/references/guide.md` for details.
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_paths()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "PATH004" in warning_codes


class TestContentValidation:
    """Tests for content quality validation."""

    def test_complete_content(self, tmp_path):
        """Test validation passes for complete content."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation testing
---

# My Skill

## Overview

This is a test skill.

## When to Use

- When testing
- When validating

## Prerequisites

- Python 3.9+

## Workflow

### Step 1: Run the script

Execute the main script.

## Output Format

JSON output.

## Resources

- `scripts/main.py`
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_content()

        warnings = [i for i in result.issues if i.severity == Severity.WARNING]
        # Should have few or no warnings for complete content
        assert len(warnings) <= 1

    def test_missing_overview(self, tmp_path):
        """Test warning when Overview section is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

## When to Use

- Testing
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_content()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "CONTENT001" in warning_codes

    def test_missing_workflow(self, tmp_path):
        """Test warning when Workflow section is missing."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = """---
name: my-skill
description: A test skill for validation
---

# My Skill

## Overview

Test skill.

## When to Use

- Testing
"""
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_content()

        warning_codes = [i.code for i in result.issues if i.severity == Severity.WARNING]
        assert "CONTENT003" in warning_codes


class TestFullValidation:
    """Tests for complete validation workflow."""

    def test_valid_skill_passes(self, tmp_path):
        """Test that a valid skill passes all validation."""
        skill_dir = tmp_path / "valid-skill"
        skill_dir.mkdir()
        (skill_dir / "scripts").mkdir()
        (skill_dir / "scripts" / "tests").mkdir()
        (skill_dir / "references").mkdir()

        skill_md = """---
name: valid-skill
description: A valid test skill for comprehensive validation testing
---

# Valid Skill

## Overview

This is a valid skill for testing purposes.

## When to Use

- When testing validation
- When checking skill structure

## Prerequisites

- Python 3.9+
- No API keys required

## Workflow

### Step 1: Run validation

Execute the validation script.

```bash
python3 scripts/validate.py
```

## Output Format

JSON output with results.

## Resources

- `scripts/validate.py` -- Main script
- `references/guide.md` -- Guide
"""
        (skill_dir / "SKILL.md").write_text(skill_md)
        (skill_dir / "scripts" / "validate.py").write_text("#!/usr/bin/env python3\n# validation script")
        (skill_dir / "scripts" / "tests" / "conftest.py").write_text("# conftest")
        (skill_dir / "scripts" / "tests" / "test_validate.py").write_text("def test_pass(): pass")
        (skill_dir / "references" / "guide.md").write_text("# Guide")

        validator = SkillValidator(skill_dir)
        result = validator.validate_all()

        assert result.passed

    def test_json_output(self, tmp_path):
        """Test JSON output format."""
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        content = "---\nname: my-skill\ndescription: Test skill for JSON output testing\n---\n# My Skill\n"
        (skill_dir / "SKILL.md").write_text(content)

        validator = SkillValidator(skill_dir)
        result = validator.validate_all()
        json_output = result.to_json()

        data = json.loads(json_output)
        assert "schema_version" in data
        assert "skill_name" in data
        assert "checks" in data
        assert "summary" in data
