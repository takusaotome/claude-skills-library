---
layout: default
title: "Timezone Aware Event Tracker"
grand_parent: 日本語
parent: メタ・品質
nav_order: 22
lang_peer: /en/skills/meta/timezone-aware-event-tracker/
permalink: /ja/skills/meta/timezone-aware-event-tracker/
---

# Timezone Aware Event Tracker
{: .no_toc }

Track and correlate events across multiple timezones with automatic conversion. Use when analyzing distributed system incidents, coordinating cross-regional operations, or creating time-normalized reports from logs/events spanning PST/CST/EST/JST or other timezones. Handles daylight saving transitions automatically.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/timezone-aware-event-tracker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/timezone-aware-event-tracker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill tracks, converts, and correlates events occurring across multiple timezones with automatic timezone detection and conversion. It maintains awareness of regional time differences (PST/CST/EST/JST and others), handles daylight saving time (DST) transitions, and generates time-normalized reports. Essential for distributed team incident analysis, cross-regional operations coordination, and multi-timezone log correlation.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Dependencies: `pytz` (or use standard library `zoneinfo` on Python 3.9+)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
python3 scripts/timezone_event_tracker.py parse \
  --input events.csv \
  --output normalized_events.json \
  --reference-tz UTC
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

- `skills/timezone-aware-event-tracker/references/timezone-conversion-guide.md`

**Scripts:**

- `skills/timezone-aware-event-tracker/scripts/timezone_event_tracker.py`
