---
layout: default
title: "Log Debugger"
grand_parent: English
parent: Software Development
nav_order: 21
lang_peer: /ja/skills/dev/log-debugger/
permalink: /en/skills/dev/log-debugger/
---

# Log Debugger
{: .no_toc }

システムログを分析してエラーの根本原因を特定し、段階的に深堀りしていくデバッグ専門家スキル。
アプリケーションログ、システムログ、クラウドサービスログなど様々な形式に対応。
5 Whys、タイムライン分析、Fishbone分析などのRCA（根本原因分析）手法を用いて
問題の本質を突き止め、再発防止策まで提案する。

Use when analyzing system logs to find error root causes, debugging application issues,
or performing technical post-mortem analysis with log data.
For organizational incident management processes (post-incident review,
corrective action plans, incident reports without log data),
use incident-rca-specialist instead.

Triggers: "analyze this log", "find the root cause", "debug this error",
"why is this failing", "log analysis",
"what caused this crash", "troubleshoot this issue"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/log-debugger.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/log-debugger){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

このスキルは、システムログを体系的に分析し、エラーの根本原因を特定するデバッグ専門家です。

**対応ログタイプ:**
- アプリケーションログ（Python/Java/Node.js例外、スタックトレース）
- システムログ（Linux syslog, journald, Windows Event Log）
- クラウドサービスログ（AWS CloudWatch, Azure Monitor, GCP Logging）
- Webサーバーログ（Apache, Nginx）
- Kubernetesログ

---

## 2. Prerequisites

- **API Key:** None required
- **Python 3.9+** recommended

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

Follow the skill's SKILL.md workflow step by step, starting from a small validated input.

---

## 5. Usage Examples

- Use **Log Debugger** when you need a structured workflow rather than an ad-hoc answer.
- Start with a small representative input before applying the workflow to production data or assets.
- Review the helper scripts and reference guides to tailor the output format to your project.

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 4 guide file(s).
- Script-assisted execution using 1 helper command(s) where applicable.
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/log-debugger/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: log_format_guide.md, debugging_strategies.md, rca_methodology.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: log_analyzer.py.
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

- `skills/log-debugger/references/debugging_strategies.md`
- `skills/log-debugger/references/log_format_guide.md`
- `skills/log-debugger/references/log_patterns.md`
- `skills/log-debugger/references/rca_methodology.md`

**Scripts:**

- `skills/log-debugger/scripts/log_analyzer.py`
