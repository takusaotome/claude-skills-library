---
layout: default
title: "Task Runner"
grand_parent: English
parent: Project & Business
nav_order: 32
lang_peer: /ja/skills/management/task-runner/
permalink: /en/skills/management/task-runner/
---

# Task Runner
{: .no_toc }

Pick up one folder-based task ticket per run, do the work, write the result back to the ticket, and refresh a kanban dashboard.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>
<span class="badge badge-scripts">Python 3</span>
<span class="badge badge-workflow">Scheduled Runs</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/task-runner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/task-runner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Each task is one Markdown file in a `tasks/` folder. The folder a file sits in is its status. On each run, Claude takes the oldest due task from `todo/`, writes a plan card, does the work, checks the completion condition, and moves the file to `done/` or `blocked/`. Every run also regenerates `tasks/dashboard.html`, a kanban board that shows the state of all tasks.

The skill is designed to be called on a schedule, for example every hour from Cowork's scheduled tasks. It handles one task per run and stops when in doubt, so a person can decide in about a minute and send the task back.

The skill content (instructions, templates, samples) is written in Japanese.

---

## 2. When to Use

- You want routine work, such as reports, summaries, or drafts, to be done in the background one ticket at a time.
- You want a person to approve anything that touches the outside world before it happens.
- You want a single page that shows what is waiting, running, blocked, and done.

Typical requests: 「タスクを1件処理して」「tasksフォルダをチェックして」「タスク管理の初期設定」「タスクの状況を見せて」「看板ボード」.

---

## 3. Prerequisites

- No API key.
- Python 3 for `scripts/build_dashboard.py`. If Python is not available, Claude writes an equivalent HTML file directly.
- A scheduler that can call Claude regularly, such as Cowork scheduled tasks. Scheduled runs do not fire while the computer sleeps or the app is closed.

---

## 4. Quick Start

1. Install the skill.
2. In your working folder, ask: 「task-runnerの初期設定をして」. This creates `tasks/`, the config file, the ticket template, and 3 sample tasks. The mode starts as `dry-run`.
3. Run 「task-runnerでタスクを1件処理して」 three times. In `dry-run`, each task gets a plan card and goes back to `todo/`.
4. Change `mode` in `tasks/_config.md` to `live` and run three more times. Two samples go to `done/`. The email sample goes to `blocked/` because its external action is not allowed.
5. Register the prompt 「task-runnerスキルで tasks フォルダのタスクを1件処理して」 as an hourly scheduled task.
6. Open `tasks/dashboard.html` in a browser.

---

## 5. Folder Layout

```
tasks/
  _config.md      # mode: dry-run or live
  _template.md    # template for new tickets
  log.md          # one line per run
  dashboard.html  # regenerated on every run; do not edit by hand
  todo/           # not started
  doing/          # running (also acts as a lock)
  blocked/        # needs a person: approval, missing info, or failure
  done/YYYY-MM/   # completed, by month
  output/         # default place for deliverables
```

Status lives only in the folder. Ticket files have no status field, so the two can never disagree.

| Folder | What a person does |
|:-------|:-------------------|
| `todo/` | Add tickets |
| `doing/` | Usually nothing |
| `blocked/` | Read the reason, respond, move the ticket back to `todo/` |
| `done/YYYY-MM/` | Check the result |

---

## 6. Writing a Ticket

File name: `YYYYMMDD_priority_title.md`, for example `20260923_1_請求書チェック.md`. Only tickets dated today or earlier run. On the same date, the lower priority number runs first. Files that start with `_` are ignored.

The template fields:

| Field | Meaning |
|:------|:--------|
| 目的 | Why the task exists |
| 入力 | Files or information to use |
| 手順メモ | Any instructions on how to do it |
| 完了条件 | A concrete, checkable end state. Vague conditions cannot be judged. |
| 出力先 | Where deliverables go (default `tasks/output/`) |
| 外部操作 | `不可` (default) or `許可`. Only `許可` lets the task send mail, delete files, or write to external systems. |
| 計画確認 | `要` stops for plan approval before work. Empty means stop only when `外部操作: 許可`. `不要` never stops. |

You can also ask 「〇〇のタスクを追加して」 and Claude creates the file from the template.

---

## 7. How a Run Works

1. **Lock check.** If a ticket in `doing/` started less than 60 minutes ago, the run logs `skip` and ends. If it is older, the run marks it as interrupted and moves it to `blocked/`. It is not re-run automatically, to avoid doing a half-finished action twice.
2. **Pick.** The first due ticket in `todo/`, by file name. If none, the run logs `idle` and ends quietly.
3. **Plan card.** Before working, Claude writes a `## 計画カード` into the ticket: what will be produced, 3 to 7 tagged steps, what it will and will not touch outside, assumptions it made, at most 3 questions for you, and the end conditions as checkboxes.
4. **Approval stop.** If the ticket needs plan approval and has no `計画承認:` line, the ticket goes to `blocked/` with `計画の確認待ち` as the first result line. Reply with the title and "OK", for example 「未返信メールの下書き作成 OK」, and the ticket runs on the next cycle.
5. **Work.** In `live` mode, Claude follows the plan. If the plan must change, if information is missing, or if an external action is not allowed, the ticket goes to `blocked/` with the reason and what a person must do.
6. **Done check.** Claude verifies the completion condition against the real output before moving the ticket to `done/YYYY-MM/`.
7. **Log and dashboard.** One line is added to `tasks/log.md`, and the dashboard is regenerated, even on `idle` and `skip` runs.

Claude only appends to tickets: start and end times, the plan card, the result, the run log, and your approvals. The parts you wrote are never rewritten.

---

## 8. Dashboard

`tasks/dashboard.html` is a single HTML file with no external CDN, in light and dark themes.

- Four columns: todo, doing, blocked, and done (last 14 days).
- A summary row with counts and the current mode.
- Card badges for scheduled (future date), possibly stalled (doing for more than 60 minutes), external action, waiting for plan approval, and the number of open questions.
- Blocked cards show the stop reason in red.
- Clicking a card opens the plan card, with the steps drawn as a flow and external steps outlined in red.
- A search box, and the last 8 lines of `log.md`.

Regenerate it by hand:

```bash
python3 scripts/build_dashboard.py tasks
python3 scripts/build_dashboard.py tasks --done-days 30 --out ~/Desktop/board.html
```

The script only reads the task files.

---

## 9. Resources

- `SKILL.md` — run procedure, plan card format, dashboard, setup, and how requests are handled
- `README.md` — setup guide for end users (Japanese)
- `scripts/build_dashboard.py` — kanban dashboard generator
- `assets/config.md`, `assets/task_template.md` — copied into `tasks/` at setup
- `assets/samples/` — 3 sample tickets and their sample data
