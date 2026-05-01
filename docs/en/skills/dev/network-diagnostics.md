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

### Phase 1: COLLECT (Data Collection)

Run the diagnostics script to collect all network metrics as JSON:

```bash
python3 scripts/network_diagnostics.py -o /tmp/network_diag.json
```

**CLI Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o FILE` | Output file (default: stdout) | stdout |
| `-t host,label` | Add custom target (repeatable) | - |
| `--skip-traceroute` | Skip traceroute | false |
| `--skip-speed` | Skip download speed tests | false |
| `--ping-count N` | Ping packet count | 10 |

**Collected Data:**

1. **Connection Info** - Interface, type (Ethernet/Wi-Fi), IP, gateway, DNS, ISP, MAC, MTU
2. **Ping Tests** - Gateway + 8.8.8.8 + 1.1.1.1 (+ custom targets) → avg/min/max/jitter/loss
3. **HTTP Timing** - DNS resolution, TCP connect, TLS handshake, TTFB, total
4. **Download Speed** - Cloudflare + OVH + Hetzner CDN endpoints → Mbps

See the skill's SKILL.md for the full end-to-end workflow.

---

## 5. Usage Examples

- Use **Network Diagnostics** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 2 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/network-diagnostics/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: network_quality_thresholds.md, deep_dive_procedures.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: network_diagnostics.py.
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
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/network-diagnostics/references/deep_dive_procedures.md`
- `skills/network-diagnostics/references/network_quality_thresholds.md`

**Scripts:**

- `skills/network-diagnostics/scripts/network_diagnostics.py`
