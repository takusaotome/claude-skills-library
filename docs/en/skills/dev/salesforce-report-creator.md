---
layout: default
title: "Salesforce Report Creator"
grand_parent: English
parent: Software Development
nav_order: 29
lang_peer: /ja/skills/dev/salesforce-report-creator/
permalink: /en/skills/dev/salesforce-report-creator/
---

# Salesforce Report Creator
{: .no_toc }

SF CLI経由でSalesforceレポートを作成するスキル。Metadata APIとREST APIの使い分け、フィールド命名規則、列数制限、レポートタイプ設定を網羅。カスタムオブジェクトレポート作成時の注意点も含む。Use when creating Salesforce reports via CLI, deploying report types, or automating report generation.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/salesforce-report-creator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/salesforce-report-creator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

このスキルは以下の機能を提供します：

1. **レポートタイプの作成**: カスタムオブジェクト用レポートタイプXMLの生成
2. **レポートの作成**: Metadata APIまたはREST APIを使用したレポート作成
3. **フィールド管理**: 適切なフィールド命名規則と列数制限の適用
4. **デプロイ**: SF CLIを使用したSalesforce組織へのデプロイ

---

## 2. Prerequisites

### 必須ツール

```bash
# Salesforce CLI (sf) がインストールされていること
sf --version

# 認証済みのSalesforce組織があること
sf org list
```

### 認証

```bash
# Web認証フロー
sf org login web --alias myorg

# JWTフロー（CI/CD向け）
sf org login jwt --client-id <consumer-key> --jwt-key-file <path> --username <user>

# 既存の認証を確認
sf org display --target-org myorg
```

---

## 3. Quick Start

```bash
# フィールド一覧を取得
sf sobject describe --sobject Property__c --target-org myorg --json | \
  python3 -c "import sys,json; [print(f['name']) for f in json.load(sys.stdin)['fields']]"
```

---

## 4. How It Works

### Step 1: レポートタイプの作成（カスタムオブジェクト用）

カスタムオブジェクトのレポートを作成するには、まずレポートタイプを定義します。

```bash
# フィールド一覧を取得
sf sobject describe --sobject Property__c --target-org myorg --json | \
  python3 -c "import sys,json; [print(f['name']) for f in json.load(sys.stdin)['fields']]"
```

**レポートタイプXML例:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ReportType xmlns="http://soap.sforce.com/2006/04/metadata">
    <baseObject>Property__c</baseObject>
    <category>other</category>
    <deployed>true</deployed>
    <description>Property All Fields Report Type</description>
    <label>Property All Fields</label>
    <sections>
        <columns>
            <checkedByDefault>false</checkedByDefault>
            <field>Name</field>
            <table>Property__c</table>

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- SF CLIからSalesforceレポートを作成したい
- カスタムオブジェクト用のレポートタイプを定義したい
- 大量のフィールドを含むレポートを自動生成したい
- Metadata APIとREST APIのどちらを使うべきか判断したい
- レポートデプロイでエラーが発生し、トラブルシューティングが必要
- "Salesforceレポートを作成"

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/salesforce-report-creator/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: field_naming_rules.md, report_type_configuration.md, column_limits_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: create_reports_via_api.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/salesforce-report-creator/references/column_limits_guide.md`
- `skills/salesforce-report-creator/references/field_naming_rules.md`
- `skills/salesforce-report-creator/references/metadata_api_vs_rest_api.md`
- `skills/salesforce-report-creator/references/report_type_configuration.md`

**Scripts:**

- `skills/salesforce-report-creator/scripts/create_reports_via_api.py`
