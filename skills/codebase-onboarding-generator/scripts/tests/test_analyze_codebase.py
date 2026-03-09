"""
Tests for analyze_codebase.py

Tests codebase analysis functionality including project type detection,
command extraction, framework detection, and CLAUDE.md generation.
"""

import json
from pathlib import Path

import pytest
from analyze_codebase import ClaudeMdGenerator, CodebaseAnalyzer, ProjectAnalysis


class TestCodebaseAnalyzer:
    """Tests for CodebaseAnalyzer class."""

    def test_detect_python_project(self, tmp_path: Path):
        """Test detection of Python project from pyproject.toml."""
        # Create a minimal Python project
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 88
""")
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.project_type == "python"
        assert "src" in analysis.directories
        assert "tests" in analysis.directories

    def test_detect_node_project(self, tmp_path: Path):
        """Test detection of Node.js project from package.json."""
        # Create a minimal Node.js project
        package_json = {
            "name": "test-project",
            "version": "1.0.0",
            "scripts": {"dev": "vite", "build": "vite build", "test": "vitest", "lint": "eslint ."},
            "dependencies": {"react": "^18.0.0"},
        }
        (tmp_path / "package.json").write_text(json.dumps(package_json, indent=2))
        (tmp_path / "src").mkdir()

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.project_type == "node"
        assert "test" in analysis.commands
        assert "build" in analysis.commands

    def test_detect_rust_project(self, tmp_path: Path):
        """Test detection of Rust project from Cargo.toml."""
        (tmp_path / "Cargo.toml").write_text("""
[package]
name = "test-project"
version = "0.1.0"
edition = "2021"
""")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.rs").write_text('fn main() { println!("Hello"); }')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.project_type == "rust"
        assert "build" in analysis.commands
        assert "test" in analysis.commands
        assert "cargo build --release" in analysis.commands["build"]

    def test_detect_go_project(self, tmp_path: Path):
        """Test detection of Go project from go.mod."""
        (tmp_path / "go.mod").write_text("""
module github.com/test/project

go 1.21
""")
        (tmp_path / "main.go").write_text("package main\nfunc main() {}")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.project_type == "go"
        assert "go test ./..." in analysis.commands.get("test", [])

    def test_extract_makefile_commands(self, tmp_path: Path):
        """Test extraction of commands from Makefile."""
        (tmp_path / "Makefile").write_text("""
.PHONY: build test lint

build:
\tgo build ./...

test:
\tgo test ./...

lint:
\tgolangci-lint run
""")
        (tmp_path / "go.mod").write_text("module test\ngo 1.21")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        # Makefile commands should be detected
        assert "build" in analysis.commands
        assert "test" in analysis.commands
        assert "lint" in analysis.commands

    def test_detect_frameworks(self, tmp_path: Path):
        """Test detection of frameworks in project."""
        # Create a FastAPI project
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-api"
dependencies = ["fastapi", "uvicorn"]
""")
        (tmp_path / "app").mkdir()
        (tmp_path / "app" / "main.py").write_text("""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}
""")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert "FastAPI" in analysis.frameworks

    def test_detect_env_vars(self, tmp_path: Path):
        """Test detection of environment variables."""
        (tmp_path / ".env.example").write_text("""
DATABASE_URL=postgresql://localhost/db
SECRET_KEY=your-secret-key
DEBUG=false
API_KEY=
""")
        (tmp_path / "config.py").write_text("""
import os

database_url = os.environ["DATABASE_URL"]
secret = os.getenv("SECRET_KEY")
""")
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert "DATABASE_URL" in analysis.env_vars
        assert "SECRET_KEY" in analysis.env_vars
        assert "DEBUG" in analysis.env_vars
        assert "API_KEY" in analysis.env_vars

    def test_directory_descriptions(self, tmp_path: Path):
        """Test that common directories get proper descriptions."""
        # Create common directories
        for dir_name in ["src", "tests", "docs", "scripts", "config"]:
            (tmp_path / dir_name).mkdir()

        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.directories["src"] == "Source code"
        assert analysis.directories["tests"] == "Test files"
        assert analysis.directories["docs"] == "Documentation"
        assert analysis.directories["scripts"] == "Utility scripts"
        assert analysis.directories["config"] == "Configuration files"

    def test_analysis_to_dict(self, tmp_path: Path):
        """Test that analysis converts to valid JSON-serializable dict."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        result = analysis.to_dict()

        # Should be JSON serializable
        json_str = json.dumps(result)
        assert json_str is not None

        # Check structure
        assert result["schema_version"] == "1.1"
        assert "project_name" in result
        assert "project_type" in result
        assert "detected_at" in result
        assert "structure" in result
        assert "commands" in result


class TestClaudeMdGenerator:
    """Tests for ClaudeMdGenerator class."""

    def test_generate_basic_claude_md(self, tmp_path: Path):
        """Test generation of basic CLAUDE.md."""
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-project"

[tool.pytest.ini_options]
testpaths = ["tests"]
""")
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        # Check for required sections
        assert "# CLAUDE.md" in output
        assert "## Project Overview" in output
        assert "## Common Commands" in output
        assert "## Directory Structure" in output

    def test_generate_with_frameworks(self, tmp_path: Path):
        """Test CLAUDE.md generation includes detected frameworks."""
        (tmp_path / "pyproject.toml").write_text("""
[project]
dependencies = ["django"]
""")
        (tmp_path / "manage.py").write_text("""
import django
from django.core.management import execute_from_command_line
""")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Architecture" in output
        assert "Django" in output

    def test_generate_with_env_vars(self, tmp_path: Path):
        """Test CLAUDE.md generation includes environment variables."""
        (tmp_path / ".env.example").write_text("""
DATABASE_URL=postgres://localhost/db
API_KEY=secret
""")
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Environment Variables" in output
        assert "DATABASE_URL" in output
        assert "API_KEY" in output

    def test_generate_commands_section(self, tmp_path: Path):
        """Test that commands section is properly formatted."""
        package_json = {"name": "test", "scripts": {"dev": "vite", "build": "vite build", "test": "vitest"}}
        (tmp_path / "package.json").write_text(json.dumps(package_json))

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Common Commands" in output
        assert "### Test" in output or "### Build" in output
        assert "```bash" in output

    def test_directory_structure_format(self, tmp_path: Path):
        """Test that directory structure is properly formatted."""
        (tmp_path / "src").mkdir()
        (tmp_path / "tests").mkdir()
        (tmp_path / "README.md").write_text("# Test")
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Directory Structure" in output
        assert "```" in output
        assert "src/" in output or "tests/" in output


class TestProjectAnalysis:
    """Tests for ProjectAnalysis dataclass."""

    def test_project_analysis_defaults(self):
        """Test ProjectAnalysis default values."""
        analysis = ProjectAnalysis(project_name="test", project_type="python", root_path=Path("/tmp/test"))

        assert analysis.project_name == "test"
        assert analysis.project_type == "python"
        assert analysis.root_files == []
        assert analysis.directories == {}
        assert analysis.commands == {}
        assert analysis.frameworks == []
        assert analysis.env_vars == []
        assert analysis.detected_at is not None

    def test_project_analysis_to_dict_schema(self):
        """Test that to_dict produces correct schema."""
        analysis = ProjectAnalysis(project_name="test-project", project_type="python", root_path=Path("/tmp/test"))
        analysis.root_files = ["README.md", "pyproject.toml"]
        analysis.directories = {"src": "Source code"}
        analysis.commands = {"test": ["pytest"]}
        analysis.frameworks = ["FastAPI"]
        analysis.env_vars = ["DATABASE_URL"]

        result = analysis.to_dict()

        assert result["schema_version"] == "1.1"
        assert result["project_name"] == "test-project"
        assert result["project_type"] == "python"
        assert result["structure"]["root_files"] == ["README.md", "pyproject.toml"]
        assert result["structure"]["directories"] == {"src": "Source code"}
        assert result["commands"] == {"test": ["pytest"]}
        assert result["frameworks"] == ["FastAPI"]
        assert result["env_vars"] == ["DATABASE_URL"]


class TestIterSourceFiles:
    """Tests for _iter_source_files helper method."""

    def test_excludes_node_modules(self, tmp_path: Path):
        """Test that node_modules/ files are excluded."""
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "react").mkdir(parents=True)
        (tmp_path / "node_modules" / "react" / "index.js").write_text("export default React;")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "app.js").write_text("import React from 'react';")

        analyzer = CodebaseAnalyzer(tmp_path)
        files = analyzer._iter_source_files([".js"], limit=100)

        filenames = [f.name for f in files]
        assert "app.js" in filenames
        assert "index.js" not in filenames

    def test_excludes_venv(self, tmp_path: Path):
        """Test that .venv/ files are excluded."""
        (tmp_path / ".venv" / "lib").mkdir(parents=True)
        (tmp_path / ".venv" / "lib" / "site.py").write_text("# venv site")
        (tmp_path / "main.py").write_text("print('hello')")

        analyzer = CodebaseAnalyzer(tmp_path)
        files = analyzer._iter_source_files([".py"], limit=100)

        file_strs = [str(f) for f in files]
        assert any("main.py" in s for s in file_strs)
        assert not any(".venv" in s for s in file_strs)

    def test_respects_limit(self, tmp_path: Path):
        """Test that limit parameter caps the number of files returned."""
        (tmp_path / "src").mkdir()
        for i in range(10):
            (tmp_path / "src" / f"file_{i}.py").write_text(f"# file {i}")

        analyzer = CodebaseAnalyzer(tmp_path)
        files = analyzer._iter_source_files([".py"], limit=3)

        assert len(files) <= 3

    def test_returns_matching_extensions(self, tmp_path: Path):
        """Test that only files with specified extensions are returned."""
        (tmp_path / "app.py").write_text("# python")
        (tmp_path / "app.js").write_text("// javascript")
        (tmp_path / "data.csv").write_text("a,b,c")

        analyzer = CodebaseAnalyzer(tmp_path)
        files = analyzer._iter_source_files([".py"], limit=100)

        assert len(files) == 1
        assert files[0].suffix == ".py"


class TestExcludedDirectories:
    """Tests for directory exclusion in various analysis methods."""

    def test_framework_detection_ignores_node_modules(self, tmp_path: Path):
        """Test that framework detection ignores files in node_modules."""
        (tmp_path / "node_modules" / "react").mkdir(parents=True)
        (tmp_path / "node_modules" / "react" / "index.js").write_text("from fastapi import FastAPI")
        (tmp_path / "package.json").write_text('{"name": "test"}')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert "FastAPI" not in analysis.frameworks

    def test_structure_excludes_node_modules(self, tmp_path: Path):
        """Test that node_modules/ is excluded from directory structure."""
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "src").mkdir()
        (tmp_path / "package.json").write_text('{"name": "test"}')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert "node_modules" not in analysis.directories
        assert "src" in analysis.directories


class TestMonorepoDetection:
    """Tests for monorepo detection."""

    def test_detect_yarn_workspaces(self, tmp_path: Path):
        """Test detection of Yarn/npm workspaces in package.json."""
        (tmp_path / "package.json").write_text(
            json.dumps(
                {
                    "name": "my-monorepo",
                    "private": True,
                    "workspaces": ["packages/*"],
                }
            )
        )
        (tmp_path / "packages" / "app").mkdir(parents=True)

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.monorepo["detected"] is True
        assert "npm/yarn workspaces" in analysis.monorepo["tools"]

    def test_detect_pnpm_workspace(self, tmp_path: Path):
        """Test detection of pnpm workspace."""
        (tmp_path / "pnpm-workspace.yaml").write_text("packages:\n  - 'packages/*'")
        (tmp_path / "package.json").write_text('{"name": "test"}')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.monorepo["detected"] is True
        assert "pnpm" in analysis.monorepo["tools"]

    def test_detect_turborepo(self, tmp_path: Path):
        """Test detection of Turborepo."""
        (tmp_path / "turbo.json").write_text('{"pipeline": {}}')
        (tmp_path / "package.json").write_text('{"name": "test"}')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.monorepo["detected"] is True
        assert "Turborepo" in analysis.monorepo["tools"]

    def test_detect_cargo_workspaces(self, tmp_path: Path):
        """Test detection of Cargo workspaces."""
        (tmp_path / "Cargo.toml").write_text("""
[workspace]
members = ["crates/*"]

[package]
name = "my-workspace"
""")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()

        assert analysis.monorepo["detected"] is True
        assert "Cargo workspaces" in analysis.monorepo["tools"]

    def test_monorepo_claude_md_section(self, tmp_path: Path):
        """Test that CLAUDE.md includes monorepo section when detected."""
        (tmp_path / "package.json").write_text(
            json.dumps(
                {
                    "name": "my-monorepo",
                    "workspaces": ["packages/*"],
                }
            )
        )
        (tmp_path / "turbo.json").write_text('{"pipeline": {}}')

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Monorepo" in output
        assert "Turborepo" in output

    def test_no_monorepo_no_section(self, tmp_path: Path):
        """Test that non-monorepo projects don't get monorepo section."""
        (tmp_path / "pyproject.toml").write_text("[project]\nname='test'")

        analyzer = CodebaseAnalyzer(tmp_path)
        analysis = analyzer.analyze()
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()

        assert "## Monorepo" not in output
