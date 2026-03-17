"""Pytest configuration and fixtures for project-completeness-scorer tests."""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
scripts_dir = Path(__file__).resolve().parents[1]
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))


@pytest.fixture
def sample_skill_project(tmp_path):
    """Create a minimal skill project structure for testing."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()

    # Create SKILL.md with valid frontmatter
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        """---
name: test-skill
description: A test skill for unit testing.
---

# Test Skill

## Overview

A test skill for unit testing the project completeness scorer.

## When to Use

- When running unit tests
- When validating scoring logic

## Prerequisites

- Python 3.9+
- No API keys required

## Workflow

### Step 1: Test

Run the tests.

## Output Format

JSON report.

## Resources

- `scripts/main.py` -- Main script
"""
    )

    # Create scripts directory with a Python file
    scripts = skill_dir / "scripts"
    scripts.mkdir()
    main_py = scripts / "main.py"
    main_py.write_text(
        """#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    print("Hello")

if __name__ == "__main__":
    main()
"""
    )

    # Create tests directory
    tests = scripts / "tests"
    tests.mkdir()
    conftest = tests / "conftest.py"
    conftest.write_text('"""Test config."""\n')

    test_main = tests / "test_main.py"
    test_main.write_text(
        """def test_example():
    assert True

def test_another():
    assert 1 + 1 == 2

def test_third():
    assert "hello".upper() == "HELLO"
"""
    )

    # Create references directory
    refs = skill_dir / "references"
    refs.mkdir()
    ref_md = refs / "guide.md"
    ref_md.write_text("# Guide\n\nThis is a reference guide.\n")

    # Create assets directory
    assets = skill_dir / "assets"
    assets.mkdir()

    return skill_dir


@pytest.fixture
def incomplete_skill_project(tmp_path):
    """Create an incomplete skill project for testing gap detection."""
    skill_dir = tmp_path / "incomplete-skill"
    skill_dir.mkdir()

    # Create SKILL.md without proper frontmatter
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        """# Incomplete Skill

This skill has no frontmatter.

## Overview

Missing the yaml frontmatter section.
"""
    )

    # No scripts directory
    # No tests
    # No references

    return skill_dir


@pytest.fixture
def webapp_project(tmp_path):
    """Create a sample webapp project structure."""
    webapp_dir = tmp_path / "test-webapp"
    webapp_dir.mkdir()

    # package.json
    (webapp_dir / "package.json").write_text('{"name": "test-webapp", "version": "1.0.0"}')

    # src directory
    src = webapp_dir / "src"
    src.mkdir()
    (src / "index.js").write_text("console.log('hello');")

    # README
    readme = webapp_dir / "README.md"
    readme.write_text("# Test Webapp\n\n## Installation\n\nnpm install\n")

    # tests
    tests = webapp_dir / "tests"
    tests.mkdir()
    (tests / "test_app.js").write_text("test('example', () => {});")

    # .gitignore
    (webapp_dir / ".gitignore").write_text("node_modules/\n")

    # LICENSE
    (webapp_dir / "LICENSE").write_text("MIT License")

    return webapp_dir
