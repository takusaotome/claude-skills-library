# Status Update Patterns Reference

This document provides comprehensive patterns for detecting intent and extracting targets from natural language status updates in both Japanese and English.

## Intent Detection Patterns

### Completed (完了)

Indicates an action item has been finished.

**Japanese Patterns:**
- `返信した` / `返信しておいた` / `返信済み` -- Replied
- `完了` / `完了した` -- Completed
- `済み` / `済んだ` -- Done/finished
- `終わった` / `終わらせた` -- Finished
- `送った` / `送信した` -- Sent
- `対応した` / `対応完了` -- Handled
- `やっておいた` / `やった` -- Did it
- `片付けた` -- Took care of
- `処理した` -- Processed

**English Patterns:**
- `done` / `finished` / `completed`
- `sent` / `replied` / `responded`
- `handled` / `took care of`
- `resolved` / `fixed`
- `closed` / `wrapped up`

**Regex Patterns:**
```python
JP_COMPLETED = [
    r'返信し(た|ておいた|済み)',
    r'完了(した)?',
    r'済(み|んだ)',
    r'終わ(った|らせた)',
    r'送(った|信した)',
    r'対応(した|完了)',
    r'やっ(た|ておいた)',
    r'片付けた',
    r'処理した',
]

EN_COMPLETED = [
    r'\b(done|finished|completed)\b',
    r'\b(sent|replied|responded)\b',
    r'\b(handled|resolved|fixed)\b',
    r'\b(closed|wrapped\s*up)\b',
    r'took\s+care\s+of',
]
```

### Delegated (委任)

Indicates an action item has been assigned to someone else.

**Japanese Patterns:**
- `〜に依頼` / `〜にお願いした` -- Requested to ~
- `〜に任せた` / `〜に委任` -- Left to ~
- `〜に振った` / `〜に回した` -- Passed to ~
- `〜担当` -- ~ is responsible
- `〜対応予定` -- ~ will handle (when combined with name)

**English Patterns:**
- `delegated to ~` / `assigned to ~`
- `handed off to ~` / `passed to ~`
- `~ is handling` / `~ will take care`
- `asked ~ to` / `requested ~ to`

**Regex Patterns:**
```python
JP_DELEGATED = [
    r'(.+?)に(依頼|お願い)(した)?',
    r'(.+?)に(任せ|委任)(た|した)',
    r'(.+?)に(振っ|回し)(た)',
    r'(.+?)(担当|対応予定)',
]

EN_DELEGATED = [
    r'(delegated|assigned)\s+to\s+(\w+)',
    r'handed\s+off\s+to\s+(\w+)',
    r'passed\s+to\s+(\w+)',
    r'(\w+)\s+(is|will)\s+(handling|handle)',
    r'asked\s+(\w+)\s+to',
]
```

### Deferred (延期)

Indicates an action item has been postponed.

**Japanese Patterns:**
- `延期` / `延ばした` -- Postponed
- `来週` / `来月` -- Next week/month
- `後で` / `あとで` -- Later
- `保留` / `保留中` -- On hold
- `一旦止め` / `ペンディング` -- Paused/pending
- `先送り` -- Put off

**English Patterns:**
- `postponed` / `deferred`
- `later` / `next week` / `next month`
- `on hold` / `pending`
- `pushed back` / `rescheduled`
- `will do later` / `put off`

**Regex Patterns:**
```python
JP_DEFERRED = [
    r'延期(した)?',
    r'来(週|月)',
    r'(後|あと)で',
    r'保留(中)?',
    r'(一旦止め|ペンディング)',
    r'先送り',
]

EN_DEFERRED = [
    r'\b(postponed|deferred)\b',
    r'next\s+(week|month)',
    r'\blater\b',
    r'on\s+hold',
    r'pushed\s+back',
    r'put\s+off',
]
```

### In-Progress (進行中)

Indicates an action item is currently being worked on.

**Japanese Patterns:**
- `対応中` / `進行中` -- In progress
- `やってる` / `やっている` -- Working on it
- `取り組み中` -- Working on
- `作業中` -- Currently working
- `確認中` / `検討中` -- Under review

**English Patterns:**
- `working on` / `in progress`
- `handling` / `addressing`
- `reviewing` / `looking into`
- `started` / `began working`

**Regex Patterns:**
```python
JP_IN_PROGRESS = [
    r'(対応|進行|作業|確認|検討)中',
    r'やって(る|いる)',
    r'取り組み中',
]

EN_IN_PROGRESS = [
    r'working\s+on',
    r'in\s+progress',
    r'\b(handling|addressing)\b',
    r'\b(reviewing|looking\s+into)\b',
    r'\b(started|began)\b',
]
```

## Target Extraction Patterns

### Person Name Extraction

**Japanese Names:**
- `〜さん` suffix: `田中さん`, `Seanさん`
- Bare names in context: `Sean`, `Lu`, `Mike`
- Full names: `山田太郎`

**English Names:**
- Capitalized words following action verbs
- Names after prepositions: "to Sean", "from Mike"

**Regex Patterns:**
```python
JP_PERSON = [
    r'(\w+)さん',
    r'(\w+)に(返信|連絡|依頼)',
    r'(\w+)の(メール|Slack|件)',
]

EN_PERSON = [
    r'to\s+([A-Z][a-z]+)',
    r'from\s+([A-Z][a-z]+)',
    r"([A-Z][a-z]+)'s\s+(email|message|request)",
]
```

### Channel Detection

**Channels and Keywords:**

| Channel | Japanese | English |
|---------|----------|---------|
| Email | メール, Eメール | email, mail |
| Slack | Slack, スラック | Slack, DM |
| Meeting | 会議, ミーティング, MTG | meeting, call, standup |
| Teams | Teams, チームズ | Teams, MS Teams |
| Phone | 電話 | phone, call |
| Chat | チャット | chat, message |

### Description Matching

When updating existing action items, match against:

1. **Exact match**: Description contains update text
2. **Fuzzy match**: Levenshtein distance < 3 for short strings
3. **Keyword match**: Key nouns overlap (proposal, report, invoice, etc.)
4. **Person + Channel match**: Same assignee and channel

## Priority and Confidence Scoring

### Match Confidence Levels

| Score | Description |
|-------|-------------|
| 1.0 | Exact person + channel + description match |
| 0.8 | Person + channel match, fuzzy description |
| 0.6 | Person match only, recent item (< 7 days) |
| 0.4 | Channel match only, description keywords overlap |
| 0.2 | Intent detected but no clear target |

### Ambiguity Resolution

When multiple items could match:
1. Prefer items with due dates closer to today
2. Prefer items in "pending" status over "in_progress"
3. Prefer items updated more recently
4. If still ambiguous, prompt for clarification

## Examples

### Example 1: Japanese Completed Update

Input: `Seanのメールには返信しておいた`

Analysis:
- Intent: **Completed** (返信しておいた)
- Person: **Sean** (Seanの)
- Channel: **Email** (メール)

### Example 2: English Delegation

Input: `Delegated the report review to Mike`

Analysis:
- Intent: **Delegated** (Delegated ... to)
- Delegatee: **Mike**
- Description keywords: **report**, **review**

### Example 3: Japanese Deferral

Input: `田中さんの件は来週対応`

Analysis:
- Intent: **Deferred** (来週)
- Person: **田中** (田中さんの)
- Status change: pending → deferred

### Example 4: Ambiguous Update

Input: `Done`

Analysis:
- Intent: **Completed**
- Target: **Ambiguous** (no person/channel specified)
- Action: Request clarification or mark most recent pending item
