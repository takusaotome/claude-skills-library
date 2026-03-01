# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **Claude Skills Library** - a collection of professional Claude Code skills for various domains. Each skill extends Claude's capabilities with specialized knowledge, workflows, and tools. Skills are self-contained packages that follow a standardized structure and can be distributed as `.zip` files.

## Skill Architecture

### Standard Skill Structure

Every skill follows this three-tier structure:

```
skill-name/
├── SKILL.md              # Main skill documentation (metadata + workflow)
├── scripts/              # Executable code (Python/Bash)
├── references/           # Documentation loaded on-demand to inform decisions
└── assets/               # Templates and boilerplate files used in output
```

**Progressive Disclosure Pattern:**
1. **Metadata** (in SKILL.md frontmatter): When to use the skill
2. **SKILL.md**: Core workflows and instructions
3. **Resources**: Loaded on-demand as needed (references for guidance, scripts for execution, assets for output generation)

### Resource Directory Purposes

- **`scripts/`**: Executable code that performs automation, data processing, or specific operations. May be executed without loading into context.

- **`references/`**: Documentation intended to be loaded into Claude's context to inform process and thinking. Examples: methodology guides, API references, schemas, detailed workflows.

- **`assets/`**: Files not loaded into context, but used within Claude's output. Examples: templates, boilerplate code, document templates.

### Resource Path Convention

**IMPORTANT: Always use relative paths when referencing resources within a skill.**

- **In SKILL.md**: Use `references/...` and `assets/...` (relative to skill directory)
- **In command files** (`commands/*.md`): Use `references/...` and `assets/...` (relative to skill directory), with the skill name noted for context (e.g., "`critical-code-reviewer` スキルディレクトリ内")
- **DO NOT** use repo-relative paths like `skills/skill-name/references/...` — these won't resolve when installed to `~/.claude/skills/`

## Common Development Commands

### Creating a New Skill

```bash
# Initialize new skill structure
python ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/scripts/init_skill.py <skill-name> --path ./

# This creates:
# - skill-name/ directory with standard structure
# - SKILL.md with template and structure guidance
# - Empty scripts/, references/, assets/ directories
```

### Packaging a Skill

```bash
# Package skill into distributable .zip
python3 ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/scripts/package_skill.py ./skill-name ./

# This:
# 1. Validates skill structure (checks SKILL.md exists, runs quick_validate)
# 2. Creates skill-name.zip in specified output directory
# 3. Includes all files with proper relative paths
```

### Validating a Skill

```bash
# Quick validation before packaging
python3 ~/.claude/plugins/marketplaces/anthropic-agent-skills/skills/skill-creator/scripts/quick_validate.py ./skill-name
```

## Current Skills in Library

| Skill | Version | Domain | Key Components |
|-------|---------|--------|----------------|
| ai-adoption-consultant | 1.0 | AI/LLM Adoption Strategy | 27 reference files, ROI analysis, 5-step workflow |
| ai-text-humanizer | 1.0 | Text Processing | 6-Pattern Detection, 0-100 Scoring, 3 Humanization Techniques |
| audit-control-designer | 1.0 | Audit Control Design | 7 reference files, control templates, SoD, KPIs, materiality |
| audit-doc-checker | 1.0 | Audit Quality Review | check_rules.md (12 categories), scoring_model.md |
| aws-cli-expert | 1.0 | Cloud Infrastructure | EC2, S3, IAM, Lambda, RDS, ECS operations |
| bcp-planner | 1.0 | Business Continuity | BIA, Risk Assessment, Recovery Strategies, BCP/DRP |
| bug-ticket-creator | 1.0 | Bug Reporting, QA | CLEAR Principles, severity/priority, bilingual templates |
| business-analyst | 1.0 | Business Analysis | business_analysis.py, BABOK templates, stakeholder analysis |
| business-plan-creator | 1.0 | Business Planning | 5-Phase Workflow, Financial Modeling, Industry Templates |
| change-management-consultant | 1.0 | Change Management | ADKAR, Kotter 8-Step, Stakeholder Engagement |
| codex-reviewer | 1.0 | Code Review | OpenAI Codex integration, GPT-5 high reasoning |
| competitive-intelligence-analyst | 1.0 | Competitive Analysis | Battlecards, Win/Loss, Market Landscape |
| compliance-advisor | 1.0 | Compliance | J-SOX/SOX, RCM, COSO Framework |
| contract-reviewer | 1.0 | Contract Review | Risk Analysis, Clause Review, Red Flag Detection |
| critical-code-reviewer | 1.0 | Code Review | 4-Persona parallel review (Veteran/TDD/CleanCode/BugHunter) |
| critical-document-reviewer | 1.0 | Document Review | 6-Persona parallel review (Dev/PM/Customer/QA/Security/Ops) |
| cx-error-analyzer | 1.0 | CX Error Analysis | 6-Axis CX Scoring, Impact vs Effort Matrix, ROI Calculation |
| dama-dmbok | 1.0 | Data Management | 11 Knowledge Areas, Data Governance, Quality |
| data-scientist | 1.0 | Data Science | auto_eda.py, model_comparison.py, timeseries_analysis.py |
| data-visualization-expert | 1.0 | Data Visualization | create_visualization.py, 30+ Chart Types |
| design-implementation-reviewer | 1.0 | Code Review | Bug Hunting, Correctness Focus, ultrathink |
| design-thinking | 1.0 | Innovation | 5-Phase Process, Empathy Maps, Prototyping |
| docling-converter | 1.0 | Document Conversion | PDF, DOCX, PPTX, Markdown conversion |
| dual-axis-skill-reviewer | 1.0 | Skill Quality Review | run_dual_axis_review.py, 5-dimension auto scoring, LLM merge |
| duckdb-expert | 1.0 | Data Analytics | SQL Optimization, CSV/Parquet/JSON |
| esg-reporter | 1.0 | ESG Reporting | GRI, SASB, TCFD, CDP standards |
| executive-briefing-writer | 1.0 | Executive Communication | Board Reports, So What Analysis |
| ffmpeg-expert | 1.0 | Media Processing | Video/Audio encoding, filters, streaming |
| financial-analyst | 1.0 | Financial Analysis | DCF, NPV/IRR, Comparable Analysis |
| fujisoft-presentation-creator | 1.0 | Presentations | MARP Templates, Corporate Style |
| gogcli-expert | 1.0 | Google Workspace CLI | 13 services, OAuth2/SA auth, multi-account |
| helpdesk-responder | 1.0 | Customer Support | KB-based responses, confidence scoring, escalation |
| imagemagick-expert | 1.0 | Image Processing | Convert, Resize, Effects, Batch |
| incident-rca-specialist | 1.0 | Incident Management | 5 Whys, Fishbone, FTA, 3D Prevention, bilingual templates |
| internal-audit-assistant | 1.0 | Internal Audit | IIA Standards, Audit Planning, Sampling Methods |
| iso-implementation-guide | 1.0 | ISO Standards | ISO 9001, 27001, 22301, Gap Analysis |
| it-system-roi-analyzer | 1.0 | IT Investment | ROI, TCO, NPV, Payback Period |
| itil4-consultant | 1.0 | IT Service Management | 34 Practices, Maturity Assessment, 5 workflows |
| kpi-designer | 1.0 | Performance Management | SMART KPIs, BSC, OKR, Dashboard Design |
| lean-six-sigma-consultant | 1.0 | Process Improvement | DMAIC, Value Stream Mapping, All Belt Levels |
| log-debugger | 1.0 | Log Analysis, Debugging | 4-Phase Framework, Log Patterns, RCA |
| m-and-a-advisor | 1.0 | M&A Advisory | Valuation, Due Diligence, PMI |
| ma-budget-actual-variance | 1.0 | Management Accounting | Budget variance, auto-classification, CSV analysis |
| ma-cvp-break-even | 1.0 | Management Accounting | CVP analysis, break-even, margin of safety |
| ma-standard-cost-variance | 1.0 | Management Accounting | Standard cost variance, price/quantity decomposition |
| management-accounting-navigator | 1.0 | Management Accounting | 12 domain routing, COSO/IMA framework |
| markdown-to-pdf | 2.0 | Documentation | markdown_to_pdf.py, fpdf2, Playwright, Mermaid |
| migration-validation-explorer | 2.0 | Data Migration QA | 4-Perspective hypothesis, Priority scoring |
| network-diagnostics | 1.0 | Network Quality | network_diagnostics.py, Ping/Speed/HTTP/Traceroute |
| office-script-expert | 1.0 | Office Scripts | ExcelScript API, 13 Bug Patterns, Testing |
| operations-manual-creator | 1.0 | Operations Documentation | STEP Format, ANSI Z535, Troubleshooting, bilingual templates |
| patent-analyst | 1.0 | IP Strategy | Prior Art Search, Patent Landscape |
| pci-dss-compliance-consultant | 1.0 | PCI DSS Compliance | Gap Analysis, SAQ Selection, v4.0.1 |
| presentation-reviewer | 1.0 | Presentation Review | Audience perspective, 5 evaluation axes, Marp compatibility |
| pricing-strategist | 1.0 | Pricing Strategy | Value-Based, Competitive, Price Testing |
| production-schedule-optimizer | 1.0 | Manufacturing Scheduling | Greedy Bin-Packing, Staff Estimation, PSO alerts |
| project-manager | 1.0 | Project Management | project_health_check.py, PMBOK, EVM analysis |
| project-plan-creator | 1.0 | Project Planning | Charter, WBS, Gantt, RACI, 5 Mermaid diagrams |
| qa-bug-analyzer | 1.0 | QA Testing | Quality Metrics, Trend Analysis |
| render-cli-expert | 1.0 | Cloud Deployment | Deploys, Logs, SSH, PostgreSQL |
| salesforce-cli-expert | 1.0 | Salesforce | SOQL, Metadata, Security Audit |
| salesforce-expert | 1.0 | Salesforce Development | Sharing, Apex, LWC, Architecture |
| salesforce-flow-expert | 1.0 | Salesforce Flow | Validation, Metadata Gen, Deploy |
| salesforce-report-creator | 1.0 | Salesforce Reports | Report Types, REST/Metadata API |
| shift-planner | 1.0 | Employee Scheduling | Greedy Assignment, 30-min coverage, fairness metrics |
| sox-expert | 1.0 | Audio Processing | Audio Effects, Format Conversion, Spectrogram |
| strategic-planner | 1.0 | Business Strategy | SWOT, PEST, Porter 5F, Scenario Planning |
| streamlit-expert | 1.0 | Web Development | OIDC Auth, Plotly/Altair, Caching |
| supply-chain-consultant | 1.0 | Supply Chain | Supply Chain Modeling, Optimization, S&OP |
| talent-acquisition-specialist | 1.0 | HR/Recruitment | JD Templates, Interview Evaluation, Onboarding |
| tdd-developer | 1.0 | Software Development | Red-Green-Refactor, pytest patterns |
| technical-spec-writer | 1.0 | Technical Documentation | IEEE 830, Mermaid Diagrams, API/DB/Screen Design |
| uat-testcase-generator | 1.0 | QA Testing | generate_uat_testcases.py, Excel generation |
| vendor-estimate-creator | 1.0 | Cost Estimation | WBS, 4 Estimation Methods, ROI |
| vendor-estimate-reviewer | 1.0 | Vendor Management | 12 Review Dimensions, 60+ Risk Factors |
| vendor-rfq-creator | 1.0 | RFQ Creation | 150+ Checklist Items |
| video2minutes | 1.0 | Media Processing | Transcription, Meeting Minutes |
| yt-dlp-expert | 1.0 | Media Download | 1000+ Sites, Subtitles, Formats |

## Skill Development Workflow

### 1. Initialize Skill Structure

Use `init_skill.py` to create the standardized directory structure with SKILL.md template.

### 2. Choose Structure Pattern

The SKILL.md template provides guidance on 4 structure patterns:
- **Workflow-Based**: Sequential step-by-step processes
- **Task-Based**: Different operations/capabilities
- **Reference/Guidelines**: Standards or specifications
- **Capabilities-Based**: Multiple interrelated features

Choose pattern(s) that fit your skill's purpose. Most skills combine patterns.

### 3. Develop Skill Components

**Development Policy: Test-Driven Development (TDD)**

When writing or modifying Python scripts in `scripts/`, always use the `tdd-developer` skill to follow the TDD workflow:

1. **Red**: Write failing tests first (`scripts/tests/test_*.py`)
2. **Green**: Write minimal implementation to pass the tests
3. **Refactor**: Clean up while keeping tests green

Run tests with: `uv run pytest skills/<skill-name>/scripts/tests/ -v`

**SKILL.md Guidelines:**
- Use imperative/infinitive form (verb-first instructions)
- Include clear "When to Use" section with specific scenarios
- Provide concrete examples and workflows
- Reference bundled resources appropriately

**Add Resources:**
- `scripts/`: Add executable Python/Bash scripts for automation
- `references/`: Add methodology guides, best practices, API docs
- `assets/`: Add templates, boilerplate, document templates

### 4. Package and Distribute

Use `package_skill.py` to create distributable `.zip` file. Validation runs automatically before packaging.

### 5. Install Skill to User Environment

**CRITICAL: Skills and Commands have different installation locations.**

#### Correct Installation Paths

| Type | Location | Format | Purpose |
|------|----------|--------|---------|
| **Skills** | `~/.claude/skills/skill-name/` | Directory with `SKILL.md` | Extend Claude's capabilities |
| **Commands** | `~/.claude/commands/` | `.md` files | Custom slash commands |
| **Packages** | `skill-packages/` | `.skill` files (ZIP) | Distribution only |

#### Installation Commands

```bash
# Install skill to user environment (CORRECT)
cp -r ./skills/skill-name ~/.claude/skills/

# Remove __pycache__ if present
rm -rf ~/.claude/skills/skill-name/scripts/__pycache__

# Verify installation
ls ~/.claude/skills/skill-name/SKILL.md
```

#### WRONG Installation (DO NOT DO THIS)

```bash
# WRONG: Do NOT put .skill files in commands/
cp skill-name.skill ~/.claude/commands/   # ❌ WRONG

# WRONG: Do NOT put skills in commands/
cp -r ./skills/skill-name ~/.claude/commands/   # ❌ WRONG
```

#### Summary

- **`.skill` files** = ZIP archives for distribution/upload to marketplaces
- **Local installation** = Copy the skill directory to `~/.claude/skills/`
- **Commands folder** = Only for `.md` slash command definitions

### 6. Update Repository Documentation (MANDATORY)

**CRITICAL: スキルを追加・更新したら、必ず `README.md` を更新すること。漏れ防止のため以下のチェックリストをすべて実施する。**

- [ ] **Repository Structure** のスキル数カウントを +1 する（`├── skills/ # All Claude Code skills (N skills)`）
- [ ] **Skill Catalog (N Skills)** のカウントを +1 する
- [ ] 該当カテゴリのテーブルにエントリを追加し、カテゴリのスキル数を +1 する（例: `### Software Development & IT (N skills)`）
- [ ] **Available Skills (Detailed)** セクションに概要・When to use・Key Features を追加する
- [ ] **Version History** セクションの先頭にバージョンエントリを追加する

## Key Standards and Frameworks

Skills in this library follow industry standards:

- **Data Science**: 7-phase analysis workflow, statistical rigor, proper train/test splits
- **Project Management**: PMBOK® Guide v3 (10 knowledge areas, 5 process groups)
- **Business Analysis**: BABOK® Guide v3 (6 knowledge areas)
- **Requirements**: ISO/IEC/IEEE 29148 compliant documentation
- **Process Modeling**: BPMN notation, value stream mapping

## File Organization

```
claude-skills-library/
├── README.md                    # Comprehensive skill documentation
├── CLAUDE.md                    # This file
├── skills/                      # Skill source folders
│   └── skill-name/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
└── skill-packages/              # Packaged .skill files for distribution
    └── skill-name.skill
```

**Note**: `.skill` files are ZIP archives with a different extension, compatible with Claude Desktop skill uploads.

## Python Script Patterns

Many skills include Python automation scripts. Common patterns:

### CLI Interface Pattern
```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("--output", "-o", help="Output directory")
    args = parser.parse_args()
```

### Class-Based Analyzers
```python
class FinancialAnalyzer:
    @staticmethod
    def calculate_roi(total_benefit: float, total_cost: float) -> float:
        """Calculate Return on Investment"""
        return ((total_benefit - total_cost) / total_cost) * 100
```

### Data Processing Pattern
```python
def profile_dataset(df: pd.DataFrame) -> Dict:
    """Generate comprehensive data profile with quality metrics"""
    # Analysis logic
    return profile_dict
```

## Template Standards

Templates in `assets/` directories follow professional standards:

- **BRD/Requirements**: ISO/IEC/IEEE 29148 compliant structure
- **Business Cases**: Include ROI, NPV, IRR, Payback Period calculations
- **Reports**: Structured sections with clear headers, tables, and metrics
- **Process Documentation**: BPMN notation, swimlane diagrams

## Skill Metadata Format

**IMPORTANT: SKILL.md File Structure**

The SKILL.md file MUST follow this exact structure:
1. **Frontmatter FIRST** (YAML between `---` delimiters) - NO content before this
2. **Title AFTER frontmatter** (e.g., `# Skill Name`)
3. **Content sections** follow the title

**Correct Format:**
```markdown
---
name: skill-name
description: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.
---

# Skill Name

## Overview
...
```

**WRONG Format (DO NOT DO THIS):**
```markdown
# Skill Name          <-- WRONG: Title before frontmatter

---
name: skill-name
...
---
```

The `description` field is critical - it determines when Claude Code automatically suggests the skill.

## No Personal Information in Committed Files

This is a **public repository**. Never hardcode personal information:
- **Absolute paths** containing usernames (e.g., `/Users/username/...`) — use `~` notation, relative paths, or dynamic resolution like `Path(__file__).resolve().parents[N]`
- **API keys / secrets** — use environment variables (`$FMP_API_KEY`, `$FINVIZ_API_KEY`) or `.gitignore`-listed config files (`.mcp.json`, `.envrc`)
- **Usernames, email addresses, or other PII**

Files that contain secrets (`.mcp.json`, `.envrc`) must be listed in `.gitignore` and never committed.
