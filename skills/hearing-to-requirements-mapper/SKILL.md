---
name: hearing-to-requirements-mapper
description: Transform client hearing sheets and meeting notes into structured requirements documents. Use when converting raw hearing data (Japanese/English) into formal requirements, generating traceability matrices, identifying gaps/ambiguities, and mapping requirements to WBS items. Triggers include "hearing to requirements", "meeting notes to specs", "requirements traceability", "gap analysis for requirements", or requests involving hearing sheet analysis.
---

# Hearing to Requirements Mapper

## Overview

This skill transforms unstructured client hearing sheets, meeting notes, and interview transcripts into structured requirements documents. It extracts requirements, maps them to WBS items, identifies gaps and ambiguities, and generates traceability matrices. The skill supports bilingual (Japanese/English) input and output with configurable templates.

**Key Capabilities:**
- Parse and extract requirements from hearing sheets, meeting notes, and transcripts
- Classify requirements by type (functional, non-functional, business, stakeholder)
- Map requirements to WBS items for project planning
- Identify gaps, conflicts, and ambiguities in captured requirements
- Generate requirements traceability matrices (RTM)
- Support both Japanese and English input/output

## When to Use

- Converting raw client hearing sheets into formal requirements documents
- Transforming meeting notes or interview transcripts into structured specifications
- Creating requirements traceability matrices from project documentation
- Identifying gaps and ambiguities in existing requirements
- Mapping requirements to WBS items for estimation
- Preparing requirements for vendor RFQs or internal development teams
- Consolidating multiple hearing sessions into a unified requirements set

### Example Requests

1. "ヒアリングシートから要件を抽出して整理してください" (Extract and organize requirements from this hearing sheet)
2. "Convert these meeting notes into a requirements document with traceability matrix"
3. "このヒアリング結果のギャップ分析をしてください" (Analyze gaps in this hearing result)
4. "Map these requirements to WBS items for project estimation"
5. "Identify ambiguities and conflicts in these requirements from multiple stakeholders"

## Prerequisites

- Python 3.9+
- No API keys required
- Required packages: pandas, openpyxl (for Excel output)

## Workflow

### Step 1: Load and Parse Hearing Data

Load the hearing sheet, meeting notes, or interview transcript:

```bash
python3 scripts/parse_hearing.py \
  --input hearing_sheet.md \
  --format markdown \
  --language auto \
  --output parsed_requirements.json
```

**Supported input formats:**
- Markdown (.md)
- Plain text (.txt)
- CSV (.csv) - for structured hearing sheets
- JSON (.json) - for pre-parsed data

**The parser:**
1. Detects document language (Japanese/English/Mixed)
2. Identifies sections and structure
3. Extracts requirement statements
4. Tags initial requirement type (functional/non-functional/business/stakeholder)
5. Preserves source context for traceability

### Step 2: Classify and Structure Requirements

Classify extracted requirements and organize them into a structured format:

```bash
python3 scripts/classify_requirements.py \
  --input parsed_requirements.json \
  --template references/requirements_classification.md \
  --output structured_requirements.json
```

**Classification categories:**

| Category | Description | Examples |
|----------|-------------|----------|
| Business Requirements (BR) | High-level business goals | "Reduce processing time by 50%" |
| Stakeholder Requirements (SR) | Needs of specific user groups | "Sales reps need mobile access" |
| Functional Requirements (FR) | System behaviors and functions | "System shall validate email format" |
| Non-Functional Requirements (NFR) | Quality attributes | "Response time < 3 seconds" |
| Constraints (CON) | Limitations and boundaries | "Must use existing Oracle database" |
| Assumptions (ASM) | Assumed conditions | "Users have stable internet" |

**MoSCoW prioritization:**
- Must Have (必須)
- Should Have (推奨)
- Could Have (可能なら)
- Won't Have (対象外)

### Step 3: Identify Gaps and Ambiguities

Analyze requirements for completeness and clarity:

```bash
python3 scripts/gap_analyzer.py \
  --input structured_requirements.json \
  --checklist references/requirements_checklist.md \
  --output gap_analysis.json
```

**Gap detection categories:**

1. **Missing Requirements**
   - Required functional areas not covered
   - Missing non-functional requirements (security, performance, etc.)
   - Incomplete user role coverage

2. **Ambiguous Requirements**
   - Vague language ("fast", "user-friendly", "appropriate")
   - Missing quantifiable metrics
   - Undefined terms or acronyms

3. **Conflicting Requirements**
   - Contradictory statements from different stakeholders
   - Incompatible technical constraints
   - Budget vs. scope conflicts

4. **Incomplete Requirements**
   - Missing acceptance criteria
   - Undefined error handling
   - Incomplete data specifications

### Step 4: Map Requirements to WBS

Map requirements to Work Breakdown Structure items:

```bash
python3 scripts/wbs_mapper.py \
  --input structured_requirements.json \
  --wbs-template references/wbs_template.md \
  --output requirements_wbs_mapping.json
```

**WBS mapping structure:**

```
Project
├── 1. Requirements Phase
│   ├── 1.1 Requirements Analysis
│   │   └── [BR-001, BR-002, SR-001...]
│   └── 1.2 Requirements Documentation
├── 2. Design Phase
│   ├── 2.1 System Design
│   │   └── [FR-001, FR-002, NFR-001...]
│   └── 2.2 Database Design
├── 3. Development Phase
│   ├── 3.1 Core Development
│   │   └── [FR-003, FR-004...]
│   └── 3.2 Integration
├── 4. Testing Phase
│   ├── 4.1 Unit Testing
│   ├── 4.2 Integration Testing
│   └── 4.3 UAT
└── 5. Deployment Phase
```

### Step 5: Generate Traceability Matrix

Create a requirements traceability matrix (RTM):

```bash
python3 scripts/generate_rtm.py \
  --input structured_requirements.json \
  --wbs-mapping requirements_wbs_mapping.json \
  --format excel \
  --output requirements_traceability_matrix.xlsx
```

**RTM columns:**
- Requirement ID
- Source (hearing session, meeting, document)
- Description
- Type (FR/NFR/BR/SR)
- Priority (MoSCoW)
- WBS Item
- Design Reference
- Test Case Reference
- Status
- Notes

### Step 6: Generate Requirements Document

Create the final structured requirements document:

```bash
python3 scripts/generate_requirements_doc.py \
  --input structured_requirements.json \
  --gap-analysis gap_analysis.json \
  --rtm requirements_traceability_matrix.xlsx \
  --template assets/requirements_document_template_ja.md \
  --output requirements_document.md
```

**Output options:**
- `--template assets/requirements_document_template_ja.md` for Japanese
- `--template assets/requirements_document_template_en.md` for English
- `--format markdown` or `--format excel`

## Output Format

### JSON Report (structured_requirements.json)

```json
{
  "schema_version": "1.0",
  "metadata": {
    "project_name": "CRM System Renewal",
    "created_at": "2025-01-15T10:00:00Z",
    "source_documents": ["hearing_20250110.md", "meeting_20250112.md"],
    "language": "ja"
  },
  "requirements": [
    {
      "id": "FR-001",
      "type": "functional",
      "category": "user_management",
      "description": "システムはユーザーのメールアドレス形式を検証する",
      "description_en": "System shall validate user email address format",
      "priority": "must_have",
      "source": {
        "document": "hearing_20250110.md",
        "section": "2.1",
        "line": 45
      },
      "acceptance_criteria": [
        "正しいメールアドレス形式の場合、検証をパスする",
        "不正な形式の場合、エラーメッセージを表示する"
      ],
      "wbs_items": ["3.1.1", "4.1.2"],
      "status": "draft",
      "notes": ""
    }
  ],
  "gaps": [
    {
      "id": "GAP-001",
      "type": "missing",
      "severity": "high",
      "description": "パスワードポリシーが未定義",
      "recommendation": "セキュリティ要件としてパスワード複雑性ルールを定義する"
    }
  ],
  "summary": {
    "total_requirements": 45,
    "by_type": {
      "functional": 28,
      "non_functional": 12,
      "business": 3,
      "stakeholder": 2
    },
    "by_priority": {
      "must_have": 20,
      "should_have": 15,
      "could_have": 8,
      "wont_have": 2
    },
    "gaps_found": 5,
    "ambiguities_found": 8
  }
}
```

### Markdown Requirements Document

```markdown
# 要件定義書 / Requirements Specification

## 1. プロジェクト概要 / Project Overview
[Project background, objectives, scope]

## 2. 要件一覧 / Requirements List

### 2.1 ビジネス要件 / Business Requirements
| ID | 要件 | 優先度 | ソース |
|----|------|--------|--------|
| BR-001 | ... | 必須 | ヒアリング 2025/01/10 |

### 2.2 機能要件 / Functional Requirements
[Table of functional requirements]

### 2.3 非機能要件 / Non-Functional Requirements
[Table of non-functional requirements]

## 3. ギャップ分析 / Gap Analysis
[List of identified gaps and recommendations]

## 4. トレーサビリティマトリクス / Traceability Matrix
[Requirements to WBS mapping summary]

## 5. 用語集 / Glossary
[Domain-specific terms and definitions]
```

## Resources

### scripts/

- `parse_hearing.py` -- Parse hearing sheets and meeting notes into structured JSON
- `classify_requirements.py` -- Classify and organize extracted requirements
- `gap_analyzer.py` -- Identify gaps, ambiguities, and conflicts
- `wbs_mapper.py` -- Map requirements to WBS items
- `generate_rtm.py` -- Generate requirements traceability matrix
- `generate_requirements_doc.py` -- Create final requirements document

### references/

- `requirements_classification.md` -- Classification framework and guidelines
- `requirements_checklist.md` -- Completeness checklist for gap analysis
- `wbs_template.md` -- Standard WBS template for software projects
- `ambiguity_patterns.md` -- Common ambiguity patterns to detect

### assets/

- `requirements_document_template_ja.md` -- Japanese requirements document template
- `requirements_document_template_en.md` -- English requirements document template
- `rtm_template.xlsx` -- Excel template for traceability matrix

## Key Principles

1. **Preserve Source Context**: Always maintain traceability to original hearing documents
2. **Detect Ambiguity Early**: Flag vague language before it causes estimation errors
3. **Support Bilingual Workflows**: Handle Japanese/English input and output seamlessly
4. **Quantify When Possible**: Convert qualitative statements to measurable criteria
5. **Identify Gaps Proactively**: Check against standard requirements checklists
6. **Enable Vendor Communication**: Output should be suitable for RFQs and estimates

## Best Practices

### Hearing Sheet Quality

**Good hearing input:**
- Clear stakeholder identification
- Dated and attributed statements
- Specific examples and scenarios
- Quantifiable goals and metrics

**Common hearing issues:**
- Vague language ("システムを使いやすくしたい")
- Missing stakeholder context
- Conflicting statements without resolution
- Assumptions stated as requirements

### Requirements Quality Checklist

✓ Each requirement has a unique ID
✓ Requirements are atomic (one requirement per statement)
✓ Requirements are testable (clear acceptance criteria)
✓ Requirements are traceable (linked to source)
✓ Non-functional requirements have specific metrics
✓ Ambiguous terms are defined in glossary
✓ Conflicting requirements are resolved or flagged

### Gap Analysis Triggers

Perform gap analysis when:
- Initial hearing is complete
- New stakeholder requirements are added
- Scope changes are proposed
- Before sending RFQ to vendors
- Before development phase gates

## Troubleshooting

### "Too many ambiguous requirements detected"

**Root Causes:**
- Hearing conducted at too high a level
- Missing follow-up questions
- Stakeholder provided wishes, not requirements

**Solutions:**
1. Schedule follow-up hearing session
2. Prepare specific clarification questions
3. Use examples to make requirements concrete
4. Reference `references/ambiguity_patterns.md` for guidance

### "Requirements conflict detected"

**Root Causes:**
- Multiple stakeholders with different priorities
- Unclear project scope
- Changing business context

**Solutions:**
1. Document both positions clearly
2. Escalate to project sponsor for decision
3. Create separate scenarios for conflicting cases
4. Prioritize based on business value

### "Missing non-functional requirements"

**Root Causes:**
- Focus on features over quality attributes
- Stakeholders assumed defaults
- Technical discussion deferred

**Solutions:**
1. Use NFR checklist from `references/requirements_checklist.md`
2. Ask specific performance, security, availability questions
3. Propose industry-standard defaults for approval

## Version History

- **v1.0** (2025-01): Initial release
  - Hearing parsing for Markdown, Text, CSV, JSON
  - Requirements classification with MoSCoW
  - Gap analysis with 4 detection categories
  - WBS mapping support
  - Traceability matrix generation
  - Bilingual (Japanese/English) templates
