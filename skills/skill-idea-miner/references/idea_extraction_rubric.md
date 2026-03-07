# Idea Extraction Rubric

Criteria and scoring framework for mining skill ideas from Claude Code session logs.

## Signal Detection Rules

### 1. Skill Usage Signals

Detect references to existing skills in tool arguments:

- **Pattern:** File paths containing `skills/*/` in Read, Edit, Write, Glob, Grep, Bash tools
- **Threshold:** Any reference counts as a signal
- **Interpretation:** Frequently used skills indicate adjacent needs; skills used together suggest workflow gaps

### 2. Error Detection Signals

Identify pain points from failed operations:

| Signal | Detection Method |
|--------|-----------------|
| Non-zero exit code | Bash tool_result with `exitCode != 0` |
| Explicit error flag | `tool_result` content block with `is_error: true` |
| Error text patterns | Regex match: `Error:`, `Exception:`, `Traceback`, `FAILED`, `ModuleNotFoundError` |

- **Interpretation:** Recurring errors on similar tasks suggest automation or tooling gaps

### 3. Repetitive Pattern Signals

Detect repetitive tool sequences that indicate manual workflows:

- **Definition:** A sequence of 3+ consecutive tool calls (by tool name)
- **Threshold:** Same sequence appearing 3+ times in a session
- **Extraction:** Record the tool sequence and associated file/command arguments
- **Interpretation:** Repetitive sequences are strong candidates for workflow automation

### 4. Automation Request Signals

Keyword detection in user messages:

**English keywords:**
- `skill`, `create`, `automate`, `workflow`, `pipeline`, `generate`, `template`, `script`

**Japanese keywords:**
- `スキル`, `作成`, `自動化`, `ワークフロー`, `パイプライン`, `生成`, `テンプレート`

- **Matching:** Case-insensitive, partial word match
- **Interpretation:** Direct user intent to automate; highest signal value

### 5. Unresolved Request Signals

Detect user messages that did not result in tool actions:

- **Definition:** User message (`type: "user"`) followed by 5+ minutes without any `tool_use`
- **Measurement:** Compare timestamps between user message and next tool_use
- **Edge cases:** End-of-session messages (no subsequent entries) are excluded
- **Interpretation:** May indicate requests beyond current capabilities

## LLM Abstraction Prompt

When invoking Claude CLI for idea abstraction, use this prompt structure:

```
You are analyzing Claude Code session logs to extract skill idea candidates
for a business/professional skill repository.

Given the following signals detected from recent sessions:
{signals_json}

And sample user messages from these sessions:
{user_messages}

Extract 0-5 skill idea candidates. For each candidate:
1. Abstract the idea (do not copy verbatim user messages)
2. Assign a category: software-development, business-analysis, project-management,
   compliance-audit, data-analytics, documentation, workflow-automation, cloud-infrastructure
3. Describe the pain point it addresses
4. Note which signals support this idea

Return JSON with this structure:
{
  "candidates": [
    {
      "title": "Short descriptive name",
      "raw_description": "What the skill would do",
      "category": "one of the categories above",
      "evidence": {
        "user_requests": ["abstracted summaries, not verbatim"],
        "pain_points": ["what problem this solves"],
        "frequency": <number of times this pattern appeared>
      }
    }
  ]
}

Rules:
- Return 0 candidates if no clear skill ideas emerge
- Do not suggest skills that already exist (provided in context)
- Abstract user requests (e.g., "generate project charter" not "create charter for X project")
- Focus on business/professional domain relevance
```

## Scoring Rubric

### Novelty (0-100)

| Score Range | Criteria |
|------------|---------|
| 80-100 | No existing skill covers this domain; fills a clear gap |
| 60-79 | Partially overlaps with existing skills but adds significant new capability |
| 40-59 | Moderate overlap; could be a feature of an existing skill |
| 20-39 | High overlap; mostly duplicates existing functionality |
| 0-19 | Near-identical to an existing skill |

### Feasibility (0-100)

| Score Range | Criteria |
|------------|---------|
| 80-100 | Can be built with existing tools (WebSearch, Read, Bash); no paid API required |
| 60-79 | Requires commonly available APIs or libraries |
| 40-59 | Requires new API integration or complex parsing logic |
| 20-39 | Requires significant infrastructure (databases, real-time feeds) |
| 0-19 | Not feasible as a Claude skill (needs persistent state, GUI, etc.) |

### Work Utility (0-100)

| Score Range | Criteria |
|------------|---------|
| 80-100 | Directly supports business decisions with actionable outputs |
| 60-79 | Provides valuable professional insights or automates key workflows |
| 40-59 | Useful for research but not directly actionable |
| 20-39 | Tangentially related to professional work |
| 0-19 | No clear business/professional application |

### Composite Score

```
composite = 0.3 * novelty + 0.3 * feasibility + 0.4 * work_utility
```

Work utility is weighted higher (0.4) because the repository's primary purpose
is to serve business professionals with practical, high-impact skills.

## Category Taxonomy

| Category | Description | Examples |
|----------|-------------|---------|
| `software-development` | Code generation, review, testing, debugging | TDD developer, code reviewer |
| `business-analysis` | Business requirements, stakeholder analysis | BABOK analysis, process modeling |
| `project-management` | Planning, tracking, reporting | WBS, Gantt, RACI, EVM |
| `compliance-audit` | Regulatory compliance, audit support | SOX, J-SOX, ISO standards |
| `data-analytics` | Data processing, visualization, ML | EDA, statistical analysis |
| `documentation` | Technical writing, spec generation | API docs, runbooks |
| `workflow-automation` | Multi-step process automation | Pipeline orchestration, batch processing |
| `cloud-infrastructure` | Cloud ops, deployment, monitoring | AWS, render, network diagnostics |

## Privacy and Data Handling

- Session logs contain user interactions already sent to Claude; no additional privacy concern for LLM processing
- Raw user messages must be abstracted before storage in backlog (no verbatim copies)
- File paths with usernames must be stripped from output artifacts
- Source session UUIDs are stored in `logs/` (gitignored) for audit purposes only
- Committed files (SKILL.md, references) must not contain personal information
