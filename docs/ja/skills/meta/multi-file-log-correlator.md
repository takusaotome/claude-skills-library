---
layout: default
title: "Multi File Log Correlator"
grand_parent: 日本語
parent: メタ・品質
nav_order: 16
lang_peer: /en/skills/meta/multi-file-log-correlator/
permalink: /ja/skills/meta/multi-file-log-correlator/
---

# Multi File Log Correlator
{: .no_toc }

Correlate events across multiple log files from different sources, systems, or time periods.
Build unified timelines, identify causal relationships between events, and highlight anomalies
that span multiple data sources. Supports timezone normalization and gap detection.

Use when analyzing logs from multiple systems (frontend, backend, database, infrastructure),
investigating distributed system failures, or building event timelines across services.

Triggers: "correlate these logs", "build timeline from multiple logs", "cross-system analysis",
"find related events across logs", "multi-source log analysis", "distributed trace analysis"

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/multi-file-log-correlator.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/multi-file-log-correlator){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

This skill correlates events across multiple log files from different sources, systems, or time periods. It builds unified timelines, identifies causal relationships between events, and highlights anomalies that span multiple data sources. The skill handles timezone normalization, timestamp format differences, and gap detection to provide a comprehensive view of distributed system behavior.

**Key Capabilities:**
- Unified timeline construction from heterogeneous log sources
- Causal relationship inference between events across systems
- Timezone normalization and timestamp alignment
- Gap and anomaly detection across multiple data sources
- Correlation ID tracking and distributed trace reconstruction

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Dependencies: pandas, python-dateutil (for timezone handling)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
# List available log files
ls -la /path/to/logs/

# Check first few lines to identify format
head -5 app.log nginx.log database.log
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

- `skills/multi-file-log-correlator/references/correlation_methodology.md`
- `skills/multi-file-log-correlator/references/timestamp_formats.md`

**Scripts:**

- `skills/multi-file-log-correlator/scripts/correlate_logs.py`
