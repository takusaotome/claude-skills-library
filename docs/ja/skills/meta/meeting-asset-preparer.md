---
layout: default
title: "Meeting Asset Preparer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 15
lang_peer: /en/skills/meta/meeting-asset-preparer/
permalink: /ja/skills/meta/meeting-asset-preparer/
---

# Meeting Asset Preparer
{: .no_toc }

Prepare comprehensive meeting assets including agendas, reference materials, decision logs, and action items. Use when preparing for project meetings, cross-regional sessions, or creating bilingual (Japanese/English) meeting documentation.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-asset-preparer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-asset-preparer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill prepares comprehensive meeting assets by gathering project context, generating structured agendas, compiling relevant reference materials, and creating templates for decision logs and action items. It supports bilingual (Japanese/English) output for cross-regional meetings and integrates with project artifacts such as estimates, implementation documents, and prior meeting notes.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Standard library plus `pyyaml` for configuration parsing

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
python3 scripts/prepare_meeting.py init \
  --title "Sprint Review Meeting" \
  --date "2026-03-15" \
  --time "14:00" \
  --timezone "JST" \
  --attendees "Alice,Bob,Carol" \
  --language "bilingual" \
  --output meeting_config.yaml
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

- `skills/meeting-asset-preparer/references/meeting-best-practices.md`

**Scripts:**

- `skills/meeting-asset-preparer/scripts/prepare_meeting.py`
