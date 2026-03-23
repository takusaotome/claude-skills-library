---
layout: default
title: "Log Debugger"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 21
lang_peer: /en/skills/dev/log-debugger/
permalink: /ja/skills/dev/log-debugger/
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

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/log-debugger.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/log-debugger){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このスキルは、システムログを体系的に分析し、エラーの根本原因を特定するデバッグ専門家です。

**対応ログタイプ:**
- アプリケーションログ（Python/Java/Node.js例外、スタックトレース）
- システムログ（Linux syslog, journald, Windows Event Log）
- クラウドサービスログ（AWS CloudWatch, Azure Monitor, GCP Logging）
- Webサーバーログ（Apache, Nginx）
- Kubernetesログ

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

- `skills/log-debugger/references/debugging_strategies.md`
- `skills/log-debugger/references/log_format_guide.md`
- `skills/log-debugger/references/log_patterns.md`
- `skills/log-debugger/references/rca_methodology.md`

**Scripts:**

- `skills/log-debugger/scripts/log_analyzer.py`
