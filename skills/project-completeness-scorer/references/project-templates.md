# Project Evaluation Templates

This document defines evaluation templates for different project types. Each template specifies dimensions, weights, and criteria appropriate for that project category.

## Template Structure

```json
{
  "template_id": "<template-name>",
  "display_name": "<Human Readable Name>",
  "description": "<What this template evaluates>",
  "dimensions": [
    {
      "name": "<Dimension Name>",
      "weight": 0.XX,
      "criteria": [...]
    }
  ]
}
```

---

## Skill Template (`skill`)

For Claude Code skill development projects in this repository.

### Dimension Weights

| Dimension | Weight |
|-----------|--------|
| Functional Requirements | 30% |
| Quality Standards | 15% |
| Test Coverage | 25% |
| Documentation | 20% |
| Deployment Readiness | 10% |

### Criteria

#### Functional Requirements (30%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| SKILL.md exists | binary | critical | `file_exists: SKILL.md` |
| YAML frontmatter valid | content | critical | `yaml_frontmatter: SKILL.md` |
| name field matches directory | content | critical | `name_matches_dir: SKILL.md` |
| description field present | content | critical | `has_field: SKILL.md, description` |
| scripts/ directory exists | binary | major | `dir_exists: scripts/` |
| At least one Python script | count | major | `file_count: scripts/*.py >= 1` |
| references/ directory exists | binary | minor | `dir_exists: references/` |
| At least one reference doc | count | major | `file_count: references/*.md >= 1` |

#### Quality Standards (15%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Python shebang in scripts | content | minor | `shebang: scripts/*.py` |
| No hardcoded paths | content | major | `no_pattern: /Users/, /home/` |
| argparse CLI interface | content | minor | `contains: argparse` |
| Error handling present | content | minor | `contains: try:, except:` |

#### Test Coverage (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| tests/ directory exists | binary | major | `dir_exists: scripts/tests/` |
| conftest.py exists | binary | major | `file_exists: scripts/tests/conftest.py` |
| At least 3 test files/functions | count | major | `test_count >= 3` |
| Tests pass | binary | critical | `pytest_passes: scripts/tests/` |

#### Documentation (20%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Overview section in SKILL.md | content | major | `has_heading: ## Overview` |
| When to Use section | content | major | `has_heading: ## When to Use` |
| Prerequisites section | content | major | `has_heading: ## Prerequisites` |
| Workflow section | content | major | `has_heading: ## Workflow` |
| Output Format section | content | minor | `has_heading: ## Output Format` |
| Resources section | content | minor | `has_heading: ## Resources` |

#### Deployment Readiness (10%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Added to README.md skill catalog | binary | major | `readme_entry` |
| assets/ directory exists (if needed) | binary | minor | `dir_exists: assets/` |

---

## Web Application Template (`webapp`)

For web application projects with frontend and backend components.

### Dimension Weights

| Dimension | Weight |
|-----------|--------|
| Functional Requirements | 35% |
| Quality Standards | 20% |
| Test Coverage | 20% |
| Documentation | 10% |
| Deployment Readiness | 15% |

### Criteria

#### Functional Requirements (35%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Package manifest exists | binary | critical | `file_exists: package.json OR pyproject.toml` |
| Source directory exists | binary | critical | `dir_exists: src/ OR app/` |
| Entry point exists | binary | critical | `file_exists: main.*, index.*, app.*` |
| API routes defined | binary | major | `dir_exists: routes/ OR api/` |
| Database models defined | binary | major | `dir_exists: models/` |
| Configuration management | binary | major | `file_exists: config.*, .env.example` |

#### Quality Standards (20%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Linter config exists | binary | minor | `file_exists: .eslintrc*, pylintrc, ruff.toml` |
| No console.log/print debugging | content | minor | `no_pattern: console.log, print(` |
| Environment variables used | content | major | `contains: process.env, os.environ` |
| No hardcoded secrets | content | critical | `no_secrets` |

#### Test Coverage (20%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Test directory exists | binary | major | `dir_exists: tests/, __tests__/` |
| Test config exists | binary | minor | `file_exists: pytest.ini, jest.config.*` |
| At least 5 test files | count | major | `test_file_count >= 5` |
| Tests pass | binary | critical | `tests_pass` |

#### Documentation (10%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| README.md exists | binary | critical | `file_exists: README.md` |
| Installation instructions | content | major | `has_heading: ## Installation` |
| API documentation | binary | major | `file_exists: docs/api.*, API.md` |
| Environment setup docs | content | major | `has_heading: ## Environment` |

#### Deployment Readiness (15%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Dockerfile exists | binary | major | `file_exists: Dockerfile` |
| CI/CD config exists | binary | major | `file_exists: .github/workflows/*, .gitlab-ci.yml` |
| Build script defined | content | major | `has_script: build` |
| .gitignore exists | binary | minor | `file_exists: .gitignore` |
| License file exists | binary | minor | `file_exists: LICENSE*` |

---

## Library Template (`library`)

For reusable library or package development.

### Dimension Weights

| Dimension | Weight |
|-----------|--------|
| Functional Requirements | 25% |
| Quality Standards | 25% |
| Test Coverage | 25% |
| Documentation | 15% |
| Deployment Readiness | 10% |

### Criteria

#### Functional Requirements (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Package manifest exists | binary | critical | `file_exists: pyproject.toml, package.json` |
| Source module exists | binary | critical | `dir_exists: src/, lib/` |
| __init__.py or index exists | binary | critical | `file_exists: __init__.py, index.*` |
| Public API defined | binary | major | `exports_defined` |

#### Quality Standards (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Type hints/TypeScript | binary | major | `type_annotations` |
| No deprecated APIs used | content | minor | `no_deprecations` |
| Consistent code style | binary | minor | `formatter_config` |
| Semantic versioning | content | major | `semver_version` |

#### Test Coverage (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Test suite exists | binary | critical | `dir_exists: tests/` |
| Coverage > 80% | percentage | major | `coverage >= 80` |
| Edge cases tested | count | minor | `edge_case_tests >= 3` |
| Tests pass | binary | critical | `tests_pass` |

#### Documentation (15%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| README.md exists | binary | critical | `file_exists: README.md` |
| API reference docs | binary | major | `api_docs_exist` |
| Usage examples | content | major | `has_examples` |
| CHANGELOG.md exists | binary | minor | `file_exists: CHANGELOG.md` |

#### Deployment Readiness (10%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Build/publish config | binary | major | `publish_config` |
| CI/CD pipeline | binary | minor | `ci_config` |
| License file | binary | major | `file_exists: LICENSE*` |

---

## Document Template (`document`)

For documentation-only projects.

### Dimension Weights

| Dimension | Weight |
|-----------|--------|
| Content Completeness | 40% |
| Structure & Organization | 25% |
| Quality & Clarity | 25% |
| Accessibility | 10% |

### Criteria

#### Content Completeness (40%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| All required sections present | count | critical | `required_sections` |
| No placeholder text | content | major | `no_pattern: TODO, TBD, FIXME` |
| References complete | content | minor | `links_valid` |
| Examples provided | content | major | `has_examples` |

#### Structure & Organization (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Table of contents | binary | minor | `has_toc` |
| Consistent heading hierarchy | content | major | `heading_hierarchy` |
| Logical section ordering | content | major | `section_order` |
| Cross-references working | content | minor | `internal_links_valid` |

#### Quality & Clarity (25%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| No spelling errors | content | minor | `spellcheck` |
| Consistent terminology | content | minor | `terminology_consistent` |
| Clear language | content | minor | `readability_score` |
| Diagrams where needed | binary | minor | `has_diagrams` |

#### Accessibility (10%)

| Criterion | Type | Severity | Check |
|-----------|------|----------|-------|
| Alt text for images | content | major | `images_have_alt` |
| Proper heading structure | content | major | `accessible_headings` |
| Color not sole indicator | content | minor | `color_accessibility` |

---

## Custom Template (`custom`)

Users can provide their own template as a JSON file:

```bash
python3 scripts/score_project.py \
  --template custom \
  --template-file ./my-template.json \
  --project-path ./my-project
```

### Custom Template Format

```json
{
  "template_id": "my-custom",
  "display_name": "My Custom Template",
  "description": "Custom evaluation for my project type",
  "dimensions": [
    {
      "name": "Custom Dimension",
      "weight": 0.50,
      "criteria": [
        {
          "name": "Custom criterion",
          "type": "binary",
          "check": "file_exists",
          "path": "required-file.txt",
          "severity": "critical",
          "action": "Create required-file.txt with proper content"
        }
      ]
    }
  ]
}
```
