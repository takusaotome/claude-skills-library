---
name: meeting-asset-preparer
description: Prepare comprehensive meeting assets including agendas, reference materials, decision logs, and action items. Use when preparing for project meetings, cross-regional sessions, or creating bilingual (Japanese/English) meeting documentation.
---

# Meeting Asset Preparer

## Overview

This skill prepares comprehensive meeting assets by gathering project context, generating structured agendas, compiling relevant reference materials, and creating templates for decision logs and action items. It supports bilingual (Japanese/English) output for cross-regional meetings and integrates with project artifacts such as estimates, implementation documents, and prior meeting notes.

## When to Use

- Preparing assets for an upcoming project meeting or status review
- Creating bilingual meeting documentation for cross-regional teams
- Compiling reference materials from estimates, specs, and implementation docs
- Generating structured agendas with time allocations
- Setting up decision log and action item tracking templates
- Preparing follow-up documentation after a meeting concludes

## Prerequisites

- Python 3.9+
- No API keys required
- Standard library plus `pyyaml` for configuration parsing

## Workflow

### Step 1: Gather Meeting Context

Collect meeting metadata including title, date/time, attendees, objectives, and language preferences. Create a meeting configuration file.

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

### Step 2: Compile Reference Materials

Scan project directories for relevant documents (estimates, specs, prior meeting notes) and generate a reference index.

```bash
python3 scripts/prepare_meeting.py compile-refs \
  --config meeting_config.yaml \
  --project-dir ./project \
  --output references_index.md
```

### Step 3: Generate Meeting Agenda

Create a structured agenda with time allocations, discussion topics, and presenter assignments.

```bash
python3 scripts/prepare_meeting.py generate-agenda \
  --config meeting_config.yaml \
  --topics "Sprint Goals,Demo,Retrospective" \
  --durations "15,30,15" \
  --output meeting_agenda.md
```

### Step 4: Create Decision Log Template

Generate a decision log template pre-populated with meeting metadata for tracking decisions made during the meeting.

```bash
python3 scripts/prepare_meeting.py create-decision-log \
  --config meeting_config.yaml \
  --output decision_log.md
```

### Step 5: Create Action Items Template

Generate an action items template with columns for task, owner, due date, and status.

```bash
python3 scripts/prepare_meeting.py create-action-items \
  --config meeting_config.yaml \
  --output action_items.md
```

### Step 6: Generate Meeting Package

Bundle all assets into a meeting package directory with an index document.

```bash
python3 scripts/prepare_meeting.py package \
  --config meeting_config.yaml \
  --agenda meeting_agenda.md \
  --references references_index.md \
  --decision-log decision_log.md \
  --action-items action_items.md \
  --output-dir ./meeting_package
```

## Output Format

### Meeting Configuration (YAML)

```yaml
meeting:
  title: "Sprint Review Meeting"
  date: "2026-03-15"
  time: "14:00"
  timezone: "JST"
  duration_minutes: 60
  attendees:
    - name: "Alice"
      role: "Product Owner"
    - name: "Bob"
      role: "Developer"
  objectives:
    - "Review sprint deliverables"
    - "Discuss blockers"
  language: "bilingual"  # en, ja, or bilingual
```

### Agenda Template (Markdown)

```markdown
# Meeting Agenda / 会議アジェンダ

**Title / タイトル**: Sprint Review Meeting
**Date / 日時**: 2026-03-15 14:00 JST
**Duration / 所要時間**: 60 minutes

## Attendees / 参加者
- Alice (Product Owner)
- Bob (Developer)

## Agenda Items / 議題

| # | Topic / 議題 | Duration / 時間 | Presenter / 担当 |
|---|-------------|-----------------|------------------|
| 1 | Sprint Goals / スプリント目標 | 15 min | Alice |
| 2 | Demo / デモ | 30 min | Bob |
| 3 | Retrospective / 振り返り | 15 min | All |
```

### Decision Log Template (Markdown)

```markdown
# Decision Log / 決定事項ログ

**Meeting**: Sprint Review Meeting
**Date**: 2026-03-15

| # | Decision / 決定事項 | Rationale / 理由 | Owner / 担当 | Date / 日付 |
|---|---------------------|------------------|--------------|-------------|
| 1 |                     |                  |              |             |
```

### Action Items Template (Markdown)

```markdown
# Action Items / アクションアイテム

**Meeting**: Sprint Review Meeting
**Date**: 2026-03-15

| # | Task / タスク | Owner / 担当 | Due Date / 期限 | Status / 状態 |
|---|--------------|--------------|-----------------|---------------|
| 1 |              |              |                 | Open          |
```

## Resources

- `scripts/prepare_meeting.py` -- Main CLI for meeting asset preparation
- `references/meeting-best-practices.md` -- Best practices for effective meeting preparation
- `assets/agenda_template.md` -- Bilingual agenda template
- `assets/decision_log_template.md` -- Bilingual decision log template
- `assets/action_items_template.md` -- Bilingual action items template

## Key Principles

1. **Context Integration**: Pull relevant project documents (estimates, specs, prior notes) to inform meeting discussions
2. **Bilingual Support**: All templates support Japanese/English bilingual output for cross-regional teams
3. **Structured Templates**: Use consistent formats for agendas, decision logs, and action items to ensure traceability
4. **Time Awareness**: Include time allocations in agendas to keep meetings focused and efficient
5. **Actionable Outputs**: Every meeting should produce clear decisions and action items with owners and due dates
