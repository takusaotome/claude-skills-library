---
name: meeting-minutes-writer
description: Generate strategic-consultant-grade meeting minutes from transcripts or notes in Japanese OR English (matching the source language), then run a self-review loop (max 3 iterations) that checks for internal contradictions, action-item omissions, speaker-name errors, and date/day-of-week mistakes before reporting completion. Use this skill whenever the user asks to draft meeting minutes, summarize a transcript, or document a meeting discussion — including Japanese-language transcripts (議事録 / 会議メモ / 文字起こし) and English-language transcripts.
---

# Meeting Minutes Writer

## Overview

Transform raw meeting content (transcripts, notes, recordings transcribed elsewhere) into concise, scannable meeting minutes that an executive can absorb in three minutes. After producing a draft, this skill runs a structured self-review loop (up to 3 passes) to detect and fix contradictions, missing action items, speaker-name errors, and date/day-of-week mistakes. Completion is only reported when a pass returns zero findings or three passes have been exhausted.

## When to Use

Trigger this skill when the user:
- Provides a meeting transcript and asks for "議事録" / "meeting minutes" / "summary"
- Asks to "format / clean up / structure" meeting notes
- Provides a `<<Transcript>>` block, raw chat log, or recording transcript
- Wants action items and decisions extracted from a discussion

**Languages supported**: Japanese and English are both first-class. The skill matches the source language by default — Japanese transcript → Japanese minutes, English transcript → English minutes. See the **Language Handling** section below for the full policy and mixed-language behavior.

## When NOT to Use

- Pure transcript cleanup with no structuring needed → just edit text directly
- Reviewing existing minutes only (no generation) → use `meeting-minutes-reviewer`
- Generating an agenda or pre-meeting brief → use `meeting-asset-preparer`
- Transcribing video/audio first → use `video2minutes` (it can call this skill afterwards)

## Core Workflow

This skill runs in **two phases**: Generation, then a Self-Review Loop. Both phases are mandatory.

### Phase 1 — Generate Draft (ultrathink)

Use ultrathink mode to analyze the source material thoroughly before writing.

**Steps**:
1. **Scan metadata** — meeting name, date, attendees. If absent, infer from content and mark `* To be confirmed`.
2. **Identify speakers** — extract a definitive speaker list with roles where derivable.
3. **Map discussion threads** to topics. Lengthy debates collapse to 2-3 key points.
4. **Extract commitments** — every "I'll do X", "we should check Y", "let's investigate Z" becomes an action item.
5. **Synthesize decisions** — explicit consensus or directives become entries under "Decisions Made".
6. **Render the draft** using the format in `references/output_format.md`.

Save the draft to a working file (e.g. `meeting_minutes_draft.md`) so the review loop can edit and re-read it.

### Phase 2 — Self-Review Loop (up to 3 iterations)

After producing the draft, run the review loop **before reporting completion**. Each iteration produces a Findings Report; if findings are non-empty, fix the draft and re-review. Stop when a clean pass occurs OR 3 iterations have run.

```
iteration = 1
while iteration <= 3:
    findings = run_review(draft)
    if findings.is_empty():
        break  # quality gate passed
    apply_fixes(draft, findings)
    iteration += 1
```

For each iteration, run the **5 Mandatory Checks** below in order. See `references/self_review_checklist.md` for full criteria and `assets/findings_report_template.md` for the report layout.

#### The 5 Mandatory Checks

1. **Internal Contradictions** — claims that conflict with each other (e.g. "Alice will lead" in §3 but "Bob will lead" in §5; deadline "Aug 20" in action table but "Aug 22" in discussion).
2. **Consistency / Coherence** — decisions reflect discussion; action items trace back to a stated commitment; numbers, dollar amounts, and counts match across sections.
3. **Action Item Omissions** — every "will do / should / need to / let's / TODO / follow up" in the source has a corresponding row in the Action Items table; ownership and due date are not silently dropped.
4. **Speaker-Name Errors** — names spelled consistently with the source (no "Tanaka" → "Tanaka-san" → "田中さん" inconsistency, no swapped first/last names, no attribution drift).
5. **Date / Day-of-Week Errors** — every concrete date is verified to match its day-of-week using the verification helper (see below). Time-zone conversions (ET↔JST etc.) are also checked.

**Date verification — MANDATORY tool use, not memory**:

```bash
python3 -c "import calendar, datetime; d=datetime.date(YYYY, MM, DD); print(d.strftime('%Y-%m-%d %A'))"
```

For ET↔JST (or any IANA timezone) conversions — including correct DST handling around the boundaries — use `zoneinfo.ZoneInfo` with the **actual meeting datetime**, never a hard-coded offset:

```bash
# Convert a specific ET datetime to JST (DST-aware)
python3 -c "
from datetime import datetime
from zoneinfo import ZoneInfo
et = datetime(2026, 3, 8, 9, 30, tzinfo=ZoneInfo('America/New_York'))  # the actual meeting datetime
jst = et.astimezone(ZoneInfo('Asia/Tokyo'))
print(f'{et:%Y-%m-%d %H:%M %Z} = {jst:%Y-%m-%d %H:%M %Z}')
"
```

Notes:
- **Always pass the real meeting date**. The DST boundary in the US (2nd Sun of Mar / 1st Sun of Nov) means a fixed +13h/+14h offset is wrong for meetings near the boundary.
- For other timezones use the IANA name: `Europe/London`, `Asia/Singapore`, `America/Los_Angeles`, etc.
- `zoneinfo` is in the Python 3.9+ standard library; no install required.
- For a quick sanity check on offset only (without DST awareness), the legacy form `python3 -c "et=14; off=14; jst=(et+off)%24"` may be used as a rough estimate, but the `zoneinfo` form above is REQUIRED whenever the meeting date crosses or sits near a DST boundary.

**Findings format** — for each finding record:
- Severity (`HIGH` blocks completion / `MEDIUM` should fix / `LOW` style)
- Location (section + line range or table row)
- Issue (what's wrong)
- Evidence (quote from source if available)
- Suggested fix

Use the structure in `assets/findings_report_template.md`.

### Completion Report

Only report completion when one of these terminates the loop:
- A review iteration returns **zero findings** → clean pass
- **Three iterations** have run

The completion report MUST include:
1. Path to the final minutes file
2. Number of review iterations run
3. Findings fixed per iteration (count + brief summary)
4. **Any HIGH-severity findings still open after iteration 3** (explicitly flagged)
5. List of items the reader should manually verify (anything tagged `* To be confirmed`)

If iteration 3 ends with HIGH-severity findings still open, do **not** silently mark the work as done — surface those open items prominently in the report.

## Output Format

The minutes follow the canonical structure below. Two language-specific templates ship with the skill — pick the one matching the source language:

- **English source** → `assets/minutes_template_en.md`
- **Japanese source** → `assets/minutes_template_ja.md`

### English structure

```markdown
### 1. Meeting Information
- **Meeting Name**: ...
- **Date**: YYYY/MM/DD (Day of Week)
- **Attendees**: ...

### 2. Action Items
| No. | Action Item | Owner | Priority | Due Date | Notes |
|-----|-------------|-------|----------|----------|-------|

### 3. Meeting Details
#### Decisions Made
#### Key Topics and Discussion Points
#### Notes for Future Meetings / Other
```

### Japanese structure (日本語構造)

```markdown
### 1. 会議情報
- **会議名**: ...
- **開催日**: YYYY/MM/DD（曜日）
- **出席者**: ...

### 2. アクションアイテム
| No. | アクション | 担当 | 優先度 | 期日 | 備考 |
|-----|-----------|------|--------|------|------|

### 3. 会議内容
#### 決定事項
#### 主要トピック・議論内容
#### 次回以降への持ち越し・その他
```

Priority legend (both languages): 🔴 High (blocking / クリティカル) / 🟡 Medium (should do / 重要) / 🟢 Low (nice to have / あれば良い).

See `references/output_format.md` for full formatting rules, inference rules, and ambiguity handling.

## Language Handling

Both Japanese and English are supported as first-class output languages. The skill **matches the source language by default**.

### Detection rules
1. If the source has a clear majority language (>70% characters), use that language for the entire output (minutes + findings report + completion report).
2. If the source is **mixed** (e.g. Japanese discussion with English technical terms, or bilingual cross-regional meeting):
   - Use the language with more substantive content for the section headings and connective text.
   - Preserve technical terms, product names, quoted statements, and proper nouns in their original form (do **not** translate "API" → "API（アプリケーション・プログラミング・インタフェース）" or "田中さん" → "Mr. Tanaka").
3. If the user explicitly requests an output language ("英語で作って" / "in Japanese please"), follow the explicit request and override auto-detection.

### What the language choice controls
- Section headings (Meeting Information vs. 会議情報, etc.) — pick the matching template
- Action verb conventions in action items
- Ambiguity markers — `* To be confirmed` (EN) / `* 要確認` (JA)
- Findings Report — use the matching half of `assets/findings_report_template.md`
- Completion Report wording

### What the language choice does NOT control
- Names of people, products, companies — always preserve verbatim from source
- Direct quotes — keep the original language; do not translate
- Date format — always `YYYY/MM/DD (Day of Week)` numerically; "(Mon)" or "（月）" depending on output language
- Time-zone abbreviations (JST, ET, UTC) — keep ASCII

### Self-review in matching language
The 5 Mandatory Checks must be run with the source-language patterns active:

- **Action-item phrases (JA)**: 「やります」「対応します」「確認します」「調べます」「フォローします」「持ち帰り」「宿題」「TODO」
- **Action-item phrases (EN)**: "I'll do", "we should", "let's check", "need to investigate", "follow up", "TODO"
- **Speaker-name errors**: be especially careful with JA honorifics (「さん」「様」「課長」) and JA↔Romaji inconsistency (「田中さん」 vs "Tanaka-san" vs "Tanaka")
- **Date format errors**: also check JA-specific formats like "令和○年" / "○月○日" / "来週火曜" before normalizing

## Examples

### Example 1: Standard transcript

**User**: "Here's today's product planning transcript: <<Transcript>>...<<End>>"

**Skill behavior**:
1. Generate draft following the 6-step generation workflow.
2. Iteration 1 review finds 2 issues: (a) "Alice owns DB migration" in action table but discussion shows Bob volunteered; (b) "next Tuesday" rendered as 8/13 but 8/13 is Wednesday.
3. Fix both, run iteration 2 → 0 findings → clean pass.
4. Report: 2 iterations, 2 findings fixed, file saved at `./meeting_minutes_2026-04-30.md`.

### Example 2: Sparse notes

**User**: "Quick notes from standup, please clean up"

**Skill behavior**:
1. Generate draft. Mark missing fields `* To be confirmed`.
2. Iteration 1 finds 1 omission (a "follow up with vendor next week" line wasn't captured as an action) → fix.
3. Iteration 2 → 0 findings.
4. Report: 2 iterations, 1 finding fixed, lists all `* To be confirmed` items for the user to fill in.

### Example 3: Loop exhausts

**User**: Provides a long, contradictory transcript.

**Skill behavior**:
1. Iteration 1 → 5 findings; iteration 2 → 2 remaining + 1 new; iteration 3 → 1 HIGH still open (a date that the source itself contradicts).
2. Report: 3 iterations run, 6 findings fixed total, **1 HIGH finding remains** (transcript itself is ambiguous about whether the launch is 2026-05-15 Friday or 2026-05-16 Saturday — flagged for user resolution).

### Example 4: 日本語トランスクリプト

**ユーザー**: 「今日の定例の文字起こしです、議事録にしてください: <<Transcript>>...<<End>>」

**スキルの挙動**:
1. ソース言語が日本語と判定 → `assets/minutes_template_ja.md` を採用
2. 日本語で議事録ドラフトを生成（「会議情報」「アクションアイテム」「決定事項」など日本語見出し）
3. 第1反復のレビューで3件検出: (a)「田中さん」と「田中課長」の表記揺れ、(b) 山田氏が「来週金曜までに」と発言した箇所が期日空欄、(c) 「5/15(金)」と書いてあるが実際は木曜
4. 修正後、第2反復で0件 → クリーンパス
5. 完了報告（日本語）: 反復2回、修正3件、出力ファイル `議事録_2026-04-30.md`、要手動確認項目なし

### Example 5: バイリンガル会議

**User**: "Cross-regional standup, mixed JP/EN. Please write minutes."

**Skill behavior**:
1. Detect majority language (e.g. 60% English) → use English template
2. Preserve Japanese names verbatim ("田中さん", not "Mr. Tanaka") and English technical terms verbatim
3. Quoted statements kept in original language: > "じゃあ来週まで" / > "Let's verify by EOW"
4. Run review loop in English; speaker-name check pays special attention to JP honorifics
5. Completion report in English; flag any `* To be confirmed` items including any JP-specific terms the user should sanity-check

## Resources

### references/
- `output_format.md` — full minutes formatting spec, inference rules, ambiguity handling
- `self_review_checklist.md` — detailed criteria for each of the 5 mandatory checks

### assets/
- `minutes_template_en.md` — blank meeting minutes template (English)
- `minutes_template_ja.md` — 議事録テンプレート（日本語）
- `findings_report_template.md` — findings report template (bilingual, EN + JA layouts)

## Best Practices

- **Never skip the review loop.** Even short minutes need at least one self-review pass before completion is reported.
- **Always verify dates with `python3 -c ...`** — never guess day-of-week from memory; LLMs are unreliable here.
- **Keep findings actionable.** Every finding must include a suggested fix, not just "this is wrong."
- **Preserve user-provided names verbatim** — if the source writes "田中さん", do not normalize to "Tanaka" in the minutes.
- **Quote evidence from the source** when raising a finding so the fix is auditable.
- **Use `* To be confirmed`** markers liberally for inferred content; surface them in the completion report.
- **Don't paraphrase decisions** — record decisions in language close to what was actually agreed, to preserve auditability.
