#!/usr/bin/env python3
"""
Codebase Analyzer for CLAUDE.md Generation

Analyzes a codebase to detect project type, directory structure, common commands,
and architectural patterns. Generates comprehensive CLAUDE.md documentation.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class ProjectAnalysis:
    """Container for codebase analysis results."""

    project_name: str
    project_type: str
    root_path: Path
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    root_files: list[str] = field(default_factory=list)
    directories: dict[str, str] = field(default_factory=dict)
    commands: dict[str, list[str]] = field(default_factory=dict)
    architecture: dict[str, Any] = field(default_factory=dict)
    conventions: dict[str, str] = field(default_factory=dict)
    frameworks: list[str] = field(default_factory=list)
    env_vars: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "schema_version": "1.0",
            "project_name": self.project_name,
            "project_type": self.project_type,
            "detected_at": self.detected_at,
            "structure": {
                "root_files": self.root_files,
                "directories": self.directories,
            },
            "commands": self.commands,
            "architecture": self.architecture,
            "conventions": self.conventions,
            "frameworks": self.frameworks,
            "env_vars": self.env_vars,
        }


class CodebaseAnalyzer:
    """Analyzes a codebase to extract structure and patterns."""

    # Project type detection patterns
    PROJECT_PATTERNS = {
        "python": ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile"],
        "node": ["package.json"],
        "rust": ["Cargo.toml"],
        "go": ["go.mod"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "ruby": ["Gemfile"],
        "php": ["composer.json"],
        "dotnet": ["*.csproj", "*.fsproj", "*.sln"],
    }

    # Directory descriptions
    DIRECTORY_DESCRIPTIONS = {
        "src": "Source code",
        "lib": "Library code",
        "app": "Application code",
        "tests": "Test files",
        "test": "Test files",
        "spec": "Test specifications",
        "docs": "Documentation",
        "doc": "Documentation",
        "scripts": "Utility scripts",
        "bin": "Executable scripts",
        "config": "Configuration files",
        "migrations": "Database migrations",
        "static": "Static assets",
        "public": "Public assets",
        "templates": "Template files",
        "views": "View templates",
        "models": "Data models",
        "controllers": "Controllers",
        "services": "Service layer",
        "utils": "Utility functions",
        "helpers": "Helper functions",
        "api": "API endpoints",
        "core": "Core functionality",
        "common": "Shared code",
        "shared": "Shared code",
        "components": "UI components",
        "pages": "Page components",
        "hooks": "React hooks",
        "assets": "Asset files",
        "resources": "Resource files",
        "fixtures": "Test fixtures",
        "mocks": "Mock implementations",
        "stubs": "Stub implementations",
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        "FastAPI": ["fastapi", "from fastapi import"],
        "Django": ["django", "DJANGO_SETTINGS_MODULE"],
        "Flask": ["flask", "from flask import"],
        "React": ["react", '"react":', "'react':"],
        "Vue": ["vue", '"vue":', "'vue':"],
        "Angular": ["@angular/core"],
        "Express": ["express", '"express":'],
        "Spring": ["org.springframework"],
        "Rails": ["rails", "gem 'rails'"],
        "Laravel": ["laravel/framework"],
        "Next.js": ["next", '"next":'],
        "Nuxt": ["nuxt", '"nuxt":'],
        "Svelte": ["svelte", '"svelte":'],
        "Gin": ["github.com/gin-gonic/gin"],
        "Echo": ["github.com/labstack/echo"],
        "Actix": ["actix-web"],
        "Rocket": ["rocket"],
    }

    def __init__(self, root_path: Path):
        self.root_path = root_path.resolve()
        self.analysis = ProjectAnalysis(
            project_name=self.root_path.name,
            project_type="unknown",
            root_path=self.root_path,
        )

    def analyze(self) -> ProjectAnalysis:
        """Run full codebase analysis."""
        self._detect_project_type()
        self._analyze_structure()
        self._extract_commands()
        self._detect_frameworks()
        self._analyze_conventions()
        self._detect_env_vars()
        return self.analysis

    def _detect_project_type(self) -> None:
        """Detect the primary project type."""
        for project_type, patterns in self.PROJECT_PATTERNS.items():
            for pattern in patterns:
                if "*" in pattern:
                    # Glob pattern
                    if list(self.root_path.glob(pattern)):
                        self.analysis.project_type = project_type
                        return
                else:
                    # Exact file
                    if (self.root_path / pattern).exists():
                        self.analysis.project_type = project_type
                        return

    def _analyze_structure(self) -> None:
        """Analyze directory structure."""
        # Get root files
        self.analysis.root_files = sorted(
            [f.name for f in self.root_path.iterdir() if f.is_file() and not f.name.startswith(".")]
        )

        # Get directories with descriptions
        for item in sorted(self.root_path.iterdir()):
            if item.is_dir() and not item.name.startswith(".") and item.name != "__pycache__":
                name = item.name.lower()
                description = self.DIRECTORY_DESCRIPTIONS.get(name, self._infer_directory_description(item))
                self.analysis.directories[item.name] = description

    def _infer_directory_description(self, directory: Path) -> str:
        """Infer directory description from contents."""
        files = list(directory.glob("*"))
        if not files:
            return "Empty directory"

        extensions = set()
        for f in files[:20]:  # Sample first 20 files
            if f.is_file() and f.suffix:
                extensions.add(f.suffix)

        if ".py" in extensions:
            return "Python modules"
        if ".js" in extensions or ".ts" in extensions:
            return "JavaScript/TypeScript code"
        if ".go" in extensions:
            return "Go packages"
        if ".rs" in extensions:
            return "Rust modules"
        if ".java" in extensions:
            return "Java classes"
        if ".md" in extensions:
            return "Markdown documentation"

        return "Project files"

    def _extract_commands(self) -> None:
        """Extract common commands from build files."""
        commands: dict[str, list[str]] = {
            "install": [],
            "build": [],
            "test": [],
            "lint": [],
            "format": [],
            "run": [],
        }

        # Python projects
        if self.analysis.project_type == "python":
            commands.update(self._extract_python_commands())

        # Node.js projects
        elif self.analysis.project_type == "node":
            commands.update(self._extract_node_commands())

        # Rust projects
        elif self.analysis.project_type == "rust":
            commands.update(self._extract_rust_commands())

        # Go projects
        elif self.analysis.project_type == "go":
            commands.update(self._extract_go_commands())

        # Java projects
        elif self.analysis.project_type == "java":
            commands.update(self._extract_java_commands())

        # Check for Makefile
        makefile_commands = self._extract_makefile_commands()
        for key, vals in makefile_commands.items():
            if vals:
                commands[key] = vals

        # Filter empty command lists
        self.analysis.commands = {k: v for k, v in commands.items() if v}

    def _extract_python_commands(self) -> dict[str, list[str]]:
        """Extract commands for Python projects."""
        commands: dict[str, list[str]] = {}

        # Check for pyproject.toml
        pyproject = self.root_path / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()

            # Detect package manager
            if "[tool.poetry]" in content:
                commands["install"] = ["poetry install"]
            elif "[project]" in content:
                commands["install"] = ["pip install -e '.[dev]'"]

            # Check for test configuration
            if "[tool.pytest" in content:
                commands["test"] = ["pytest tests/ -v"]

            # Check for ruff
            if "[tool.ruff]" in content:
                commands["lint"] = ["ruff check ."]
                commands["format"] = ["ruff format ."]

            # Check for black
            if "[tool.black]" in content:
                if "format" not in commands:
                    commands["format"] = []
                commands["format"].append("black .")

            # Check for mypy
            if "[tool.mypy]" in content:
                if "lint" not in commands:
                    commands["lint"] = []
                commands["lint"].append("mypy .")

        # Check for requirements.txt
        elif (self.root_path / "requirements.txt").exists():
            commands["install"] = ["pip install -r requirements.txt"]
            commands["test"] = ["pytest tests/ -v"]

        return commands

    def _extract_node_commands(self) -> dict[str, list[str]]:
        """Extract commands for Node.js projects."""
        commands: dict[str, list[str]] = {}

        package_json = self.root_path / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                scripts = data.get("scripts", {})

                # Map npm scripts to command categories
                script_mapping = {
                    "install": ["install", "setup"],
                    "build": ["build", "compile"],
                    "test": ["test", "test:unit", "test:e2e"],
                    "lint": ["lint", "eslint"],
                    "format": ["format", "prettier"],
                    "run": ["dev", "start", "serve"],
                }

                # Detect package manager
                pkg_manager = "npm"
                if (self.root_path / "yarn.lock").exists():
                    pkg_manager = "yarn"
                elif (self.root_path / "pnpm-lock.yaml").exists():
                    pkg_manager = "pnpm"
                elif (self.root_path / "bun.lockb").exists():
                    pkg_manager = "bun"

                for category, script_names in script_mapping.items():
                    for script_name in script_names:
                        if script_name in scripts:
                            run_cmd = "run " if pkg_manager == "npm" else ""
                            commands[category] = [f"{pkg_manager} {run_cmd}{script_name}"]
                            break

                # Install command
                commands["install"] = [f"{pkg_manager} install"]

            except json.JSONDecodeError:
                pass

        return commands

    def _extract_rust_commands(self) -> dict[str, list[str]]:
        """Extract commands for Rust projects."""
        return {
            "install": ["cargo build"],
            "build": ["cargo build --release"],
            "test": ["cargo test"],
            "lint": ["cargo clippy"],
            "format": ["cargo fmt"],
            "run": ["cargo run"],
        }

    def _extract_go_commands(self) -> dict[str, list[str]]:
        """Extract commands for Go projects."""
        return {
            "install": ["go mod download"],
            "build": ["go build ./..."],
            "test": ["go test ./..."],
            "lint": ["golangci-lint run"],
            "format": ["go fmt ./..."],
            "run": ["go run ."],
        }

    def _extract_java_commands(self) -> dict[str, list[str]]:
        """Extract commands for Java projects."""
        commands: dict[str, list[str]] = {}

        if (self.root_path / "pom.xml").exists():
            commands = {
                "install": ["mvn install"],
                "build": ["mvn package"],
                "test": ["mvn test"],
                "run": ["mvn spring-boot:run"],
            }
        elif (self.root_path / "build.gradle").exists() or (self.root_path / "build.gradle.kts").exists():
            commands = {
                "install": ["./gradlew build"],
                "build": ["./gradlew build"],
                "test": ["./gradlew test"],
                "run": ["./gradlew bootRun"],
            }

        return commands

    def _extract_makefile_commands(self) -> dict[str, list[str]]:
        """Extract commands from Makefile."""
        commands: dict[str, list[str]] = {}

        makefile = self.root_path / "Makefile"
        if not makefile.exists():
            return commands

        content = makefile.read_text()

        # Look for common targets
        target_mapping = {
            "install": ["install", "setup", "deps"],
            "build": ["build", "compile"],
            "test": ["test", "tests", "check"],
            "lint": ["lint", "check-style"],
            "format": ["format", "fmt"],
            "run": ["run", "start", "serve"],
        }

        for category, targets in target_mapping.items():
            for target in targets:
                if re.search(rf"^{target}:", content, re.MULTILINE):
                    commands[category] = [f"make {target}"]
                    break

        return commands

    def _detect_frameworks(self) -> None:
        """Detect frameworks used in the project."""
        frameworks = []

        # Check various files for framework indicators
        files_to_check = [
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "go.mod",
            "Cargo.toml",
            "pom.xml",
            "build.gradle",
            "Gemfile",
            "composer.json",
        ]

        combined_content = ""
        for filename in files_to_check:
            filepath = self.root_path / filename
            if filepath.exists():
                combined_content += filepath.read_text()

        # Also check source files
        for ext in [".py", ".js", ".ts", ".go", ".rs", ".java"]:
            for filepath in list(self.root_path.rglob(f"*{ext}"))[:10]:
                try:
                    combined_content += filepath.read_text()
                except (UnicodeDecodeError, PermissionError):
                    continue

        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in combined_content.lower():
                    frameworks.append(framework)
                    break

        self.analysis.frameworks = sorted(set(frameworks))

        # Set architecture info
        if frameworks:
            self.analysis.architecture["frameworks"] = frameworks

    def _analyze_conventions(self) -> None:
        """Analyze coding conventions."""
        conventions = {}

        # Detect naming convention from files
        py_files = list(self.root_path.rglob("*.py"))[:10]
        js_files = list(self.root_path.rglob("*.js"))[:10] + list(self.root_path.rglob("*.ts"))[:10]

        if py_files:
            # Check for snake_case
            snake_case_count = sum(1 for f in py_files if "_" in f.stem and f.stem.islower())
            if snake_case_count > len(py_files) / 2:
                conventions["file_naming"] = "snake_case"

        if js_files:
            # Check for camelCase/PascalCase
            pascal_count = sum(1 for f in js_files if f.stem[0].isupper())
            camel_count = sum(1 for f in js_files if f.stem[0].islower() and "_" not in f.stem)
            if pascal_count > len(js_files) / 2:
                conventions["file_naming"] = "PascalCase"
            elif camel_count > len(js_files) / 2:
                conventions["file_naming"] = "camelCase"

        # Check for test framework
        if (self.root_path / "pytest.ini").exists() or (self.root_path / "conftest.py").exists():
            conventions["testing"] = "pytest"
        elif (self.root_path / "tests").is_dir():
            conventions["testing"] = "Test directory present"

        # Check for linter configs
        if (self.root_path / ".eslintrc.js").exists() or (self.root_path / ".eslintrc.json").exists():
            conventions["linting"] = "ESLint"
        if (self.root_path / "ruff.toml").exists() or (self.root_path / ".ruff.toml").exists():
            conventions["linting"] = "Ruff"

        self.analysis.conventions = conventions

    def _detect_env_vars(self) -> None:
        """Detect required environment variables."""
        env_vars = set()

        # Check .env.example or .env.sample
        for env_file in [".env.example", ".env.sample", ".env.template"]:
            filepath = self.root_path / env_file
            if filepath.exists():
                content = filepath.read_text()
                # Extract variable names
                for match in re.finditer(r"^([A-Z][A-Z0-9_]*)\s*=", content, re.MULTILINE):
                    env_vars.add(match.group(1))

        # Check source files for os.environ or process.env
        patterns = [
            r"os\.environ\[?['\"]([A-Z][A-Z0-9_]*)['\"]",
            r"os\.getenv\(['\"]([A-Z][A-Z0-9_]*)['\"]",
            r"process\.env\.([A-Z][A-Z0-9_]*)",
            r"env::var\(['\"]([A-Z][A-Z0-9_]*)['\"]",
            r"os\.Getenv\(['\"]([A-Z][A-Z0-9_]*)['\"]",
        ]

        source_extensions = [".py", ".js", ".ts", ".go", ".rs"]
        for ext in source_extensions:
            for filepath in list(self.root_path.rglob(f"*{ext}"))[:20]:
                try:
                    content = filepath.read_text()
                    for pattern in patterns:
                        for match in re.finditer(pattern, content):
                            env_vars.add(match.group(1))
                except (UnicodeDecodeError, PermissionError):
                    continue

        self.analysis.env_vars = sorted(env_vars)


class ClaudeMdGenerator:
    """Generates CLAUDE.md from analysis results."""

    def __init__(self, analysis: ProjectAnalysis):
        self.analysis = analysis

    def generate(self) -> str:
        """Generate CLAUDE.md content."""
        sections = [
            self._generate_header(),
            self._generate_overview(),
            self._generate_commands(),
            self._generate_structure(),
            self._generate_architecture(),
            self._generate_conventions(),
            self._generate_testing(),
            self._generate_env_vars(),
        ]

        return "\n\n".join(filter(None, sections))

    def _generate_header(self) -> str:
        """Generate CLAUDE.md header."""
        return "# CLAUDE.md\n\nThis file provides guidance to Claude Code when working with this codebase."

    def _generate_overview(self) -> str:
        """Generate project overview section."""
        project_type = self.analysis.project_type.title()
        frameworks = ", ".join(self.analysis.frameworks) if self.analysis.frameworks else "standard libraries"

        return f"""## Project Overview

{self.analysis.project_name} is a {project_type} project using {frameworks}.

<!-- TODO: Add 2-3 sentences describing what the project does and its primary purpose -->"""

    def _generate_commands(self) -> str:
        """Generate common commands section."""
        if not self.analysis.commands:
            return ""

        sections = ["## Common Commands"]

        command_order = ["install", "build", "run", "test", "lint", "format"]

        for category in command_order:
            if category in self.analysis.commands:
                commands = self.analysis.commands[category]
                sections.append(f"\n### {category.title()}\n\n```bash")
                for cmd in commands:
                    sections.append(cmd)
                sections.append("```")

        return "\n".join(sections)

    def _generate_structure(self) -> str:
        """Generate directory structure section."""
        if not self.analysis.directories:
            return ""

        lines = ["## Directory Structure\n\n```"]
        lines.append(f"{self.analysis.project_name}/")

        # Add root files (limited to key files)
        key_files = ["README.md", "CLAUDE.md", "pyproject.toml", "package.json", "Cargo.toml", "go.mod", "Makefile"]
        for f in self.analysis.root_files:
            if f in key_files:
                lines.append(f"├── {f}")

        # Add directories
        dirs = list(self.analysis.directories.items())
        for i, (name, desc) in enumerate(dirs):
            prefix = "└──" if i == len(dirs) - 1 else "├──"
            lines.append(f"{prefix} {name}/".ljust(25) + f"# {desc}")

        lines.append("```")
        return "\n".join(lines)

    def _generate_architecture(self) -> str:
        """Generate architecture section."""
        if not self.analysis.frameworks and not self.analysis.architecture:
            return ""

        lines = ["## Architecture"]

        if self.analysis.frameworks:
            lines.append("\n### Frameworks\n\n- " + "\n- ".join(self.analysis.frameworks))

        lines.append("\n### Patterns\n\n<!-- TODO: Document key architectural patterns and design decisions -->")

        return "\n".join(lines)

    def _generate_conventions(self) -> str:
        """Generate coding conventions section."""
        if not self.analysis.conventions:
            return """## Coding Conventions

<!-- TODO: Document naming conventions, style guidelines, and coding standards -->"""

        lines = ["## Coding Conventions"]

        if "file_naming" in self.analysis.conventions:
            lines.append(f"\n- **File naming**: {self.analysis.conventions['file_naming']}")

        if "linting" in self.analysis.conventions:
            lines.append(f"- **Linting**: {self.analysis.conventions['linting']}")

        return "\n".join(lines)

    def _generate_testing(self) -> str:
        """Generate testing section."""
        test_commands = self.analysis.commands.get("test", [])

        lines = ["## Testing"]

        if self.analysis.conventions.get("testing"):
            lines.append(f"\n### Framework\n\n- {self.analysis.conventions['testing']}")

        if test_commands:
            lines.append("\n### Running Tests\n\n```bash")
            for cmd in test_commands:
                lines.append(cmd)
            lines.append("```")
        else:
            lines.append("\n<!-- TODO: Document how to run tests -->")

        return "\n".join(lines)

    def _generate_env_vars(self) -> str:
        """Generate environment variables section."""
        if not self.analysis.env_vars:
            return ""

        lines = ["## Environment Variables\n"]
        lines.append("Required environment variables:\n")
        lines.append("| Variable | Description |")
        lines.append("|----------|-------------|")

        for var in self.analysis.env_vars:
            lines.append(f"| `{var}` | <!-- TODO: Add description --> |")

        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze a codebase and generate CLAUDE.md documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze and output JSON
  python3 analyze_codebase.py --path /path/to/project --output analysis.json

  # Generate CLAUDE.md directly
  python3 analyze_codebase.py --path /path/to/project --generate-claude-md --output CLAUDE.md

  # Analyze current directory
  python3 analyze_codebase.py
        """,
    )
    parser.add_argument(
        "--path",
        "-p",
        type=Path,
        default=Path.cwd(),
        help="Path to the codebase to analyze (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--generate-claude-md",
        "-g",
        action="store_true",
        help="Generate CLAUDE.md instead of JSON analysis",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "claude-md"],
        default="json",
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    # Validate path
    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not args.path.is_dir():
        print(f"Error: Path is not a directory: {args.path}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    analyzer = CodebaseAnalyzer(args.path)
    analysis = analyzer.analyze()

    # Generate output
    if args.generate_claude_md or args.format == "claude-md":
        generator = ClaudeMdGenerator(analysis)
        output = generator.generate()
    else:
        output = json.dumps(analysis.to_dict(), indent=2)

    # Write output
    if args.output:
        args.output.write_text(output)
        print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
