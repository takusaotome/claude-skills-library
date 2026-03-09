---
name: codebase-onboarding-generator
description: Automatically analyze a codebase and generate comprehensive CLAUDE.md documentation for future Claude Code sessions. Use when onboarding to a new project, creating project documentation, or generating AI coding assistant context files.
---

# Codebase Onboarding Generator

## Overview

This skill analyzes a codebase to automatically generate comprehensive CLAUDE.md documentation. It identifies common commands, build processes, test patterns, directory structure conventions, and key architectural decisions. The generated documentation follows best practices for Claude Code onboarding and enables efficient AI-assisted development.

## When to Use

- Setting up Claude Code for a new project that lacks CLAUDE.md
- Generating initial project documentation for AI assistants
- Refreshing outdated CLAUDE.md files after significant project changes
- Creating standardized onboarding documentation for team codebases
- Analyzing unfamiliar codebases to understand structure and conventions

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (pathlib, json, os, re)

## Workflow

### Step 1: Analyze Codebase Structure

Run the codebase analyzer to detect project type, directory structure, and key files.

```bash
python3 scripts/analyze_codebase.py \
  --path /path/to/project \
  --output analysis.json
```

The analyzer detects:
- Project type (Python, Node.js, Java, Go, Rust, etc.)
- Package manager and dependency files
- Build and test configuration
- Directory conventions (src/, lib/, tests/, etc.)
- Key configuration files (.gitignore, CI configs, etc.)

### Step 2: Extract Common Commands

Parse package.json, Makefile, pyproject.toml, or other build files to extract:
- Build commands
- Test commands
- Lint/format commands
- Development server commands
- Deployment commands

### Step 3: Identify Architectural Patterns

Analyze code structure to identify:
- Framework usage (React, Django, Spring, etc.)
- Design patterns (MVC, microservices, monolith)
- API conventions (REST, GraphQL, gRPC)
- Database technologies (SQL, NoSQL, ORM)
- Testing frameworks and patterns

### Step 4: Generate CLAUDE.md

Synthesize analysis results into a comprehensive CLAUDE.md file.

```bash
python3 scripts/analyze_codebase.py \
  --path /path/to/project \
  --generate-claude-md \
  --output CLAUDE.md
```

### Step 5: Review and Customize

Review the generated CLAUDE.md for:
- Accuracy of detected commands and patterns
- Missing project-specific conventions
- Security considerations (ensure no secrets are referenced)
- Team-specific guidelines to add manually

## Output Format

### JSON Analysis Report

```json
{
  "schema_version": "1.1",
  "project_name": "example-project",
  "project_type": "python",
  "detected_at": "2024-01-15T10:30:00Z",
  "structure": {
    "root_files": ["README.md", "pyproject.toml", ".gitignore"],
    "directories": {
      "src": "Source code",
      "tests": "Test files",
      "docs": "Documentation"
    }
  },
  "commands": {
    "build": ["pip install -e ."],
    "test": ["pytest tests/ -v"],
    "lint": ["ruff check ."],
    "format": ["black ."]
  },
  "architecture": {
    "framework": "FastAPI",
    "patterns": ["REST API", "Repository Pattern"],
    "database": "PostgreSQL with SQLAlchemy"
  },
  "conventions": {
    "naming": "snake_case for files and functions",
    "testing": "pytest with fixtures in conftest.py",
    "documentation": "Google-style docstrings"
  }
}
```

### Generated CLAUDE.md Structure

The generated CLAUDE.md follows this structure:

1. **Project Overview** - Brief description and purpose
2. **Monorepo Structure** - Workspace tools and packages (if detected)
3. **Common Commands** - Build, test, lint, run commands with examples
4. **Directory Structure** - Annotated directory tree
5. **Architecture** - Framework, patterns, and design decisions
6. **Coding Conventions** - Naming, style, and documentation standards
7. **Testing** - Test framework, patterns, and how to run tests
8. **Key Files** - Important configuration and entry points

## Resources

- `scripts/analyze_codebase.py` -- Main analysis script that detects project structure and generates documentation
- `references/claude-md-best-practices.md` -- Guidelines for effective CLAUDE.md documentation

## Key Principles

1. **Non-invasive analysis** -- Only read files, never modify the target codebase
2. **Framework-agnostic** -- Support multiple languages and build systems
3. **Security-conscious** -- Never include secrets, credentials, or sensitive paths
4. **Incremental updates** -- Support refreshing existing CLAUDE.md with new findings
5. **Human-in-the-loop** -- Generate draft documentation for human review and customization
