---
layout: default
title: "QA Bug Analyzer"
grand_parent: 日本語
parent: プロジェクト・経営
nav_order: 19
lang_peer: /en/skills/management/qa-bug-analyzer/
permalink: /ja/skills/management/qa-bug-analyzer/
---

# QA Bug Analyzer
{: .no_toc }

This skill should be used when analyzing bug ticket data to identify quality trends, assess software quality status, and provide improvement recommendations. Use when a user provides bug lists (CSV, Excel, JSON, or Markdown format) and needs comprehensive quality analysis from a QA manager perspective. Generates statistical analysis, identifies quality hotspots, provides actionable recommendations, and produces professional Markdown reports suitable for project managers and executive leadership. Ideal for IT system development, migration, and implementation projects.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/qa-bug-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/qa-bug-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill enables comprehensive bug ticket analysis from a QA management perspective. Analyze bug data to identify quality trends, assess project health, pinpoint problem areas, and generate actionable improvement recommendations. The skill produces professional Markdown reports suitable for project managers, development managers, and executive leadership.

**Key capabilities:**
- Statistical analysis of bug distributions (severity, category, module, resolution time)
- Quality trend identification and hotspot detection
- Root cause pattern analysis
- Prioritized improvement recommendations
- Professional report generation for stakeholders

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **API Key:** None required
- **Python 3.9+** recommended

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
User provides bug data
    │
    ├─→ Data in CSV/JSON format
    │   └─→ Use Automated Analysis Workflow (Section 3)
    │
    ├─→ Data in multiple Markdown files (from bug-ticket-creator)
    │   └─→ Use Markdown Aggregation Workflow (Section 4)
    │
    └─→ User wants custom analysis or specific focus
        └─→ Use Custom Analysis Workflow (Section 5)
```

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/qa-bug-analyzer/references/analysis_methodology.md`
- `skills/qa-bug-analyzer/references/quality_metrics_guide.md`

**Scripts:**

- `skills/qa-bug-analyzer/scripts/analyze_bugs.py`
