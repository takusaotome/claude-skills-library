---
layout: default
title: "Salesforce Report Creator"
grand_parent: English
parent: Software Development
nav_order: 28
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

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/salesforce-report-creator/references/column_limits_guide.md`
- `skills/salesforce-report-creator/references/field_naming_rules.md`
- `skills/salesforce-report-creator/references/metadata_api_vs_rest_api.md`
- `skills/salesforce-report-creator/references/report_type_configuration.md`

**Scripts:**

- `skills/salesforce-report-creator/scripts/create_reports_via_api.py`
