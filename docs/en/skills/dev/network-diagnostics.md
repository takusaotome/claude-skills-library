---
layout: default
title: "Network Diagnostics"
grand_parent: English
parent: Software Development
nav_order: 22
lang_peer: /ja/skills/dev/network-diagnostics/
permalink: /en/skills/dev/network-diagnostics/
---

# Network Diagnostics
{: .no_toc }

ネットワーク品質を総合的に診断し、ボトルネックの特定と根本原因の深堀りまで行うスキル。
接続情報、レイテンシ、ダウンロード速度、HTTP接続タイミング、経路解析を自動実行し、
品質閾値に基づく総合評価を日本語レポートとして出力する。
外部依存なし（OS標準ツールのみ使用）、macOSおよびLinux対応。

Use when diagnosing network quality, troubleshooting slow connections,
identifying network bottlenecks, measuring latency/bandwidth/jitter,
or generating network health reports.

「ネットワーク診断」「network diagnostics」「ネットワークが遅い」
「latency check」「bandwidth test」「traceroute analysis」

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/network-diagnostics.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/network-diagnostics){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

# Network Diagnostics

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

```bash
python3 scripts/network_diagnostics.py -o /tmp/network_diag.json
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

- `skills/network-diagnostics/references/deep_dive_procedures.md`
- `skills/network-diagnostics/references/network_quality_thresholds.md`

**Scripts:**

- `skills/network-diagnostics/scripts/network_diagnostics.py`
