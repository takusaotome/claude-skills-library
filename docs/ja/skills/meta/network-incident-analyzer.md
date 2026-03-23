---
layout: default
title: "Network Incident Analyzer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 17
lang_peer: /en/skills/meta/network-incident-analyzer/
permalink: /ja/skills/meta/network-incident-analyzer/
---

# Network Incident Analyzer
{: .no_toc }

Analyze network device logs to identify connectivity issues, latency problems, and outages. Correlate timestamps across timezones, detect anomaly patterns, and generate incident reports with root cause hypotheses. Use when troubleshooting network incidents from log files.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/network-incident-analyzer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/network-incident-analyzer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

Analyzes network device logs (routers, switches, firewalls, load balancers) to identify connectivity issues, latency problems, and service outages. Automatically correlates events across multiple log files with different timestamp formats and timezones, detects anomaly patterns within specified time windows, and generates comprehensive incident reports with root cause hypotheses and remediation recommendations.

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- Python 3.9+
- No API keys required
- Standard library only (datetime, re, json, collections, pathlib)

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
python3 scripts/analyze_network_logs.py \
  --logs /path/to/router.log /path/to/firewall.log \
  --start "2024-01-15 10:00:00" \
  --end "2024-01-15 12:00:00" \
  --timezone "America/New_York" \
  --output-dir ./incident-report
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

- `skills/network-incident-analyzer/references/anomaly-patterns.md`
- `skills/network-incident-analyzer/references/log-formats.md`

**Scripts:**

- `skills/network-incident-analyzer/scripts/analyze_network_logs.py`
