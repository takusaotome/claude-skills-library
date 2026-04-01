# Skill Template Validation Rules

This document defines all validation rules, error codes, and fix suggestions for the skill-template-validator.

## Error Code Format

Error codes follow the pattern: `{CATEGORY}{NUMBER}`

- **STRUCT**: Structure validation (001-099)
- **FRONT**: Frontmatter validation (001-099)
- **PATH**: Path validation (001-099)
- **CONTENT**: Content quality validation (001-099)

## Structure Validation Rules (STRUCT)

### STRUCT001: Missing SKILL.md

- **Severity**: Error
- **Condition**: SKILL.md file does not exist in skill directory
- **Message**: "SKILL.md not found in skill directory"
- **Suggestion**: "Create SKILL.md with YAML frontmatter as the first content"

### STRUCT002: Invalid Directory Name

- **Severity**: Error
- **Condition**: Directory name contains uppercase letters, underscores, or special characters
- **Message**: "Directory name '{name}' is invalid"
- **Suggestion**: "Use lowercase letters and hyphens only (e.g., 'my-skill-name')"

### STRUCT003: Missing scripts/ Directory

- **Severity**: Warning
- **Condition**: scripts/ directory does not exist
- **Message**: "scripts/ directory not found"
- **Suggestion**: "Create scripts/ directory or mark as knowledge-only skill"

### STRUCT004: Missing references/ Directory

- **Severity**: Warning
- **Condition**: references/ directory does not exist
- **Message**: "references/ directory not found"
- **Suggestion**: "Create references/ directory with at least one documentation file"

### STRUCT005: Empty scripts/ Directory

- **Severity**: Warning
- **Condition**: scripts/ directory exists but contains no .py or .sh files
- **Message**: "scripts/ directory is empty"
- **Suggestion**: "Add executable scripts or remove empty directory"

### STRUCT006: Empty references/ Directory

- **Severity**: Warning
- **Condition**: references/ directory exists but contains no files
- **Message**: "references/ directory is empty"
- **Suggestion**: "Add reference documentation or remove empty directory"

### STRUCT007: Missing tests/ Directory

- **Severity**: Warning
- **Condition**: scripts/ exists but scripts/tests/ does not
- **Message**: "scripts/tests/ directory not found"
- **Suggestion**: "Create scripts/tests/ with conftest.py and test files"

### STRUCT008: Empty tests/ Directory

- **Severity**: Warning
- **Condition**: scripts/tests/ exists but contains no test_*.py files
- **Message**: "No test files found in scripts/tests/"
- **Suggestion**: "Add at least 3 test files with meaningful test coverage"

### STRUCT009: Missing conftest.py

- **Severity**: Warning
- **Condition**: scripts/tests/ exists but conftest.py does not
- **Message**: "conftest.py not found in scripts/tests/"
- **Suggestion**: "Create conftest.py with sys.path setup for imports"

### STRUCT010: Unexpected Top-Level Files

- **Severity**: Info
- **Condition**: Files other than SKILL.md found at top level
- **Message**: "Unexpected file at top level: '{filename}'"
- **Suggestion**: "Move to appropriate subdirectory (scripts/, references/, assets/)"

## Frontmatter Validation Rules (FRONT)

### FRONT001: Missing Frontmatter

- **Severity**: Error
- **Condition**: SKILL.md does not start with `---`
- **Message**: "YAML frontmatter not found"
- **Suggestion**: "Add YAML frontmatter at the very beginning of SKILL.md"

### FRONT002: Content Before Frontmatter

- **Severity**: Error
- **Condition**: Any content (including title) appears before opening `---`
- **Message**: "Content found before frontmatter"
- **Suggestion**: "Move all content after the closing `---` of frontmatter"

### FRONT003: Unclosed Frontmatter

- **Severity**: Error
- **Condition**: Opening `---` found but no closing `---`
- **Message**: "Frontmatter not properly closed"
- **Suggestion**: "Add closing `---` after frontmatter fields"

### FRONT004: Invalid YAML Syntax

- **Severity**: Error
- **Condition**: Content between `---` delimiters is not valid YAML
- **Message**: "Invalid YAML syntax in frontmatter"
- **Suggestion**: "Check YAML syntax: proper indentation, colon-space separators"

### FRONT005: Missing name Field

- **Severity**: Error
- **Condition**: `name:` field not present in frontmatter
- **Message**: "Required field 'name' not found in frontmatter"
- **Suggestion**: "Add 'name: skill-name' matching the directory name"

### FRONT006: Name Mismatch

- **Severity**: Error
- **Condition**: `name:` value does not match directory name exactly
- **Message**: "Frontmatter name '{fm_name}' does not match directory name '{dir_name}'"
- **Suggestion**: "Change name to exactly match directory: 'name: {dir_name}'"

### FRONT007: Missing description Field

- **Severity**: Error
- **Condition**: `description:` field not present in frontmatter
- **Message**: "Required field 'description' not found in frontmatter"
- **Suggestion**: "Add 'description: ...' explaining when to trigger the skill"

### FRONT008: Description Too Short

- **Severity**: Warning
- **Condition**: `description:` value is less than 20 characters
- **Message**: "Description is too short ({length} chars, minimum 20)"
- **Suggestion**: "Expand description to clearly explain trigger conditions"

### FRONT009: Description Too Long

- **Severity**: Warning
- **Condition**: `description:` value exceeds 500 characters
- **Message**: "Description is too long ({length} chars, maximum 500)"
- **Suggestion**: "Condense description; move details to Overview section"

### FRONT010: Empty Field Value

- **Severity**: Error
- **Condition**: Required field has empty or whitespace-only value
- **Message**: "Field '{field}' has empty value"
- **Suggestion**: "Provide a meaningful value for '{field}'"

## Path Validation Rules (PATH)

### PATH001: Hardcoded Absolute Path

- **Severity**: Error
- **Condition**: Path starting with `/` found in SKILL.md or scripts
- **Message**: "Hardcoded absolute path found: '{path}'"
- **File/Line**: Specific location in file
- **Suggestion**: "Use relative paths (e.g., 'scripts/...' or 'references/...')"

### PATH002: Username in Path

- **Severity**: Error
- **Condition**: Path containing `/Users/`, `/home/`, or similar patterns
- **Message**: "Personal username in path: '{path}'"
- **Suggestion**: "Remove personal paths; use relative paths or $HOME"

### PATH003: Non-Existent Resource Reference

- **Severity**: Warning
- **Condition**: SKILL.md references a file in scripts/ or references/ that doesn't exist
- **Message**: "Referenced file does not exist: '{path}'"
- **Suggestion**: "Create the file or update the reference"

### PATH004: Incorrect Path Prefix

- **Severity**: Warning
- **Condition**: Path uses repo-relative prefix like `skills/skill-name/`
- **Message**: "Repo-relative path found: '{path}'"
- **Suggestion**: "Use skill-relative paths (e.g., 'scripts/...' not 'skills/name/scripts/...')"

### PATH005: Windows-Style Path

- **Severity**: Warning
- **Condition**: Path uses backslashes or drive letters
- **Message**: "Windows-style path found: '{path}'"
- **Suggestion**: "Use Unix-style forward slashes for cross-platform compatibility"

### PATH006: Path Traversal

- **Severity**: Warning
- **Condition**: Path contains `../` traversal outside skill directory
- **Message**: "Path traversal detected: '{path}'"
- **Suggestion**: "Keep all references within the skill directory"

## Content Quality Validation Rules (CONTENT)

### CONTENT001: Missing Overview Section

- **Severity**: Warning
- **Condition**: No `## Overview` heading in SKILL.md
- **Message**: "Overview section not found"
- **Suggestion**: "Add '## Overview' with 2-3 sentences describing the skill"

### CONTENT002: Missing When to Use Section

- **Severity**: Warning
- **Condition**: No `## When to Use` heading in SKILL.md
- **Message**: "When to Use section not found"
- **Suggestion**: "Add '## When to Use' with bullet list of trigger conditions"

### CONTENT003: Missing Workflow Section

- **Severity**: Warning
- **Condition**: No `## Workflow` heading in SKILL.md
- **Message**: "Workflow section not found"
- **Suggestion**: "Add '## Workflow' with numbered steps using imperative verbs"

### CONTENT004: Missing Prerequisites Section

- **Severity**: Warning
- **Condition**: No `## Prerequisites` heading in SKILL.md
- **Message**: "Prerequisites section not found"
- **Suggestion**: "Add '## Prerequisites' listing Python version, API keys, dependencies"

### CONTENT005: Missing Output Format Section

- **Severity**: Warning
- **Condition**: No `## Output Format` heading in SKILL.md
- **Message**: "Output Format section not found"
- **Suggestion**: "Add '## Output Format' showing expected output structure"

### CONTENT006: Non-Imperative Workflow Steps

- **Severity**: Info
- **Condition**: Workflow steps don't start with imperative verbs
- **Message**: "Step '{step}' may not use imperative form"
- **Suggestion**: "Start steps with action verbs: Run, Create, Analyze, Generate"

### CONTENT007: Missing Resources Section

- **Severity**: Warning
- **Condition**: No `## Resources` heading listing scripts and references
- **Message**: "Resources section not found"
- **Suggestion**: "Add '## Resources' listing all scripts and reference files"

### CONTENT008: Empty When to Use Section

- **Severity**: Warning
- **Condition**: When to Use section has no bullet points
- **Message**: "When to Use section has no trigger conditions"
- **Suggestion**: "Add at least 3 specific scenarios when the skill should be used"

## Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| Error | Blocking issue preventing skill from working | Must fix before use |
| Warning | Quality issue that may cause problems | Should fix |
| Info | Improvement suggestion | Consider fixing |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (no errors) |
| 1 | One or more errors found |
| 2 | Invalid arguments or skill path |

## Validation Order

1. **Structure** -- Verify files and directories exist
2. **Frontmatter** -- Parse and validate YAML metadata
3. **Paths** -- Check for hardcoded or invalid paths
4. **Content** -- Analyze SKILL.md quality

Validation stops early if SKILL.md is missing (STRUCT001) since other checks depend on it.
