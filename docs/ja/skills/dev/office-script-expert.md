---
layout: default
title: "Office Script Expert"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 23
lang_peer: /en/skills/dev/office-script-expert/
permalink: /ja/skills/dev/office-script-expert/
---

# Office Script Expert
{: .no_toc }

Office Scripts (Excel Online / Microsoft 365) development expert skill. Covers platform limitations, ExcelScript API patterns, testing strategy (lib + Vitest), and 13 real-world bug patterns discovered during production development. Trigger words: Office Scripts, ExcelScript, Excel Online, Office Script development, TypeScript Excel, Excel automation, CalculateRequirements, ImportCsvData

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/office-script-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/office-script-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

Office Scripts are TypeScript-based automation scripts for Excel on the web (Microsoft 365).
They are fundamentally different from VBA and Power Automate:

| Aspect | Office Scripts | VBA | Power Automate |
|--------|---------------|-----|----------------|
| Language | TypeScript (subset) | VBA | Low-code / expressions |
| Runtime | Server-side (Excel Online) | Client-side (Desktop) | Cloud service |
| Module system | **None** (no import/export) | Modules | Connectors |
| External libs | **Not available** | COM references | Connectors |
| Timeout | **120 seconds** | None | 30 min (premium) |
| Testing | Indirect (lib extraction) | Manual | Manual |

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **API Key:** None required
- **Python 3.9+** recommended

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

Invoke this skill by describing your analysis needs to Claude.

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

- `skills/office-script-expert/references/common_bug_patterns.md`
- `skills/office-script-expert/references/excel_api_patterns.md`
- `skills/office-script-expert/references/platform_limitations.md`
- `skills/office-script-expert/references/testing_strategy.md`
