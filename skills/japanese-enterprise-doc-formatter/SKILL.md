---
name: japanese-enterprise-doc-formatter
description: Format documents for Japanese enterprise approval workflows including ringi (稟議), purchase requests (購入申請), and internal proposals. Handles bilingual requirements, proper keigo levels, required approval sections, and corporate template compliance.
---

# Japanese Enterprise Document Formatter

## Overview

This skill formats business documents for Japanese enterprise approval workflows. It ensures proper keigo (敬語) usage, required approval sections (稟議書、購入申請書、提案書), bilingual content when needed, and corporate template compliance. The skill validates documents against Japanese business writing standards and generates approval-ready output.

## When to Use

- Creating or formatting 稟議書 (ringi) approval documents
- Preparing 購入申請書 (purchase request) forms
- Drafting 提案書 (internal proposals) for management
- Converting informal notes into formal Japanese business documents
- Ensuring proper keigo levels (尊敬語, 謙譲語, 丁寧語) in documents
- Adding required approval sections (件名, 目的, 背景, 効果, リスク, 費用)
- Creating bilingual (Japanese/English) enterprise documents
- Validating document compliance with Japanese corporate standards

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library only (no third-party packages)

## Workflow

### Step 1: Analyze Input Content

Identify the document type and extract key information from the user's input:

- Document type: 稟議書 / 購入申請書 / 提案書 / 報告書 / 依頼書
- Target audience: 役員 / 部長 / 課長 / 一般
- Keigo level required: formal (役員向け) / standard (部長向け) / casual (内部)
- Bilingual requirement: Japanese only / Japanese + English summary

```bash
# Doc-type detection is handled by validate_sections.py via the --doc-type
# flag (and by format_document.py's heuristics). A standalone
# analyze_document.py was planned but never shipped — use the workflow below.
python3 scripts/validate_sections.py \
  --input user_content.md \
  --doc-type ringi \
  --output analysis.json
```

### Step 2: Validate Required Sections

Check that all required sections for the document type are present:

**稟議書 Required Sections:**
1. 件名 (Subject)
2. 起案日 (Draft Date)
3. 起案者 (Drafter)
4. 起案部署 (Department)
5. 決裁期限 (Approval Deadline)
6. 目的 (Purpose)
7. 背景 (Background)
8. 内容 (Details)
9. 効果 (Expected Benefits)
10. リスク (Risks)
11. 費用 (Cost)
12. 代替案 (Alternatives)
13. 承認欄 (Approval Section)

```bash
python3 scripts/validate_sections.py \
  --document-type ringi \
  --input draft.md \
  --output validation_report.json
```

### Step 3: Apply Keigo Transformation

Transform the text to appropriate keigo level based on target audience:

| Audience | Keigo Level | Example Transformation |
|----------|-------------|------------------------|
| 役員向け | 最上級敬語 | する → させていただきます |
| 部長向け | 標準敬語 | する → いたします |
| 課長向け | 丁寧語 | する → します |

```bash
python3 scripts/transform_keigo.py \
  --input draft.md \
  --level formal \
  --output formatted.md
```

### Step 4: Generate Formatted Document

Create the final formatted document with proper structure:

```bash
python3 scripts/format_document.py \
  --input draft.md \
  --type ringi \
  --keigo-level formal \
  --bilingual true \
  --output final_document.md
```

### Step 5: Generate Approval-Ready Output

Produce the final document in requested format:

- Markdown (for review)
- Plain text (for email submission)
- JSON (for system integration)

## Output Format

### JSON Report

```json
{
  "schema_version": "1.0",
  "document_type": "稟議書",
  "document_id": "RINGI-2024-001",
  "metadata": {
    "subject": "新規システム導入の件",
    "draft_date": "2024-01-15",
    "drafter": "山田太郎",
    "department": "情報システム部",
    "approval_deadline": "2024-01-31",
    "keigo_level": "formal",
    "bilingual": true
  },
  "sections": {
    "purpose": "...",
    "background": "...",
    "details": "...",
    "benefits": "...",
    "risks": "...",
    "cost": "...",
    "alternatives": "..."
  },
  "validation": {
    "all_sections_present": true,
    "keigo_compliance": true,
    "warnings": []
  },
  "english_summary": "..."
}
```

### Markdown Report

```markdown
# 稟議書

## 基本情報
| 項目 | 内容 |
|------|------|
| 件名 | 新規システム導入の件 |
| 起案日 | 2024年1月15日 |
| 起案者 | 山田太郎 |
| 起案部署 | 情報システム部 |
| 決裁期限 | 2024年1月31日 |

## 目的
[Purpose content with proper keigo]

## 背景
[Background content with proper keigo]

...

## 承認欄
| 役職 | 氏名 | 日付 | 印 |
|------|------|------|-----|
| 部長 |      |      |     |
| 本部長 |    |      |     |
| 役員 |      |      |     |

---
## English Summary
[English translation of key points]
```

## Resources

- `scripts/validate_sections.py` -- Validates required sections for document type (also handles type detection)
- `scripts/transform_keigo.py` -- Applies keigo transformation to text
- `scripts/format_document.py` -- Generates formatted document output
- `references/document_types.md` -- Document type specifications and requirements
- `references/keigo_guide.md` -- Keigo usage guide and transformation rules
- `references/section_templates.md` -- Template sections for each document type

## Key Principles

1. **Completeness (完全性)**: All required sections must be present for the document type
2. **Formality (格式)**: Keigo level must match the target audience and document purpose
3. **Clarity (明確性)**: Each section should have clear, unambiguous content
4. **Bilingual Consistency (二言語一貫性)**: English summaries must accurately reflect Japanese content
5. **Approval Flow (承認フロー)**: Document structure must support the enterprise approval workflow

## Document Type Quick Reference

| Type | Japanese | Primary Sections | Typical Audience |
|------|----------|-----------------|------------------|
| Ringi | 稟議書 | 目的, 背景, 効果, 費用, リスク | 役員 |
| Purchase | 購入申請書 | 品名, 数量, 金額, 理由, 納期 | 部長 |
| Proposal | 提案書 | 課題, 提案内容, 期待効果, 実施計画 | 部長/役員 |
| Report | 報告書 | 概要, 経緯, 結果, 今後の対応 | 部長 |
| Request | 依頼書 | 依頼事項, 理由, 期限, 備考 | 課長/部長 |

## Keigo Quick Reference

### 尊敬語 (Respectful Language - for actions of superiors)

| Plain | 尊敬語 |
|-------|--------|
| いる | いらっしゃる |
| 言う | おっしゃる |
| 見る | ご覧になる |
| 知る | ご存知である |
| する | なさる |

### 謙譲語 (Humble Language - for own actions)

| Plain | 謙譲語 |
|-------|--------|
| いる | おる |
| 言う | 申す / 申し上げる |
| 見る | 拝見する |
| 知る | 存じる / 存じ上げる |
| する | いたす / させていただく |

### 丁寧語 (Polite Language - general politeness)

| Plain | 丁寧語 |
|-------|--------|
| だ | です |
| する | します |
| ある | あります |
| いる | います |
