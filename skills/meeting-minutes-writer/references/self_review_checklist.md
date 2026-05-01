# Self-Review Checklist — Meeting Minutes

This document defines the **5 Mandatory Checks** the self-review loop runs on every iteration. The loop runs up to 3 times; it stops early when a pass returns zero findings.

For each check, the reviewer must:
1. Examine the entire draft (not just the section being checked).
2. Compare the draft against the original source material.
3. Record findings using the format in `assets/findings_report_template.md`.

Severity:
- **HIGH** — factually wrong, contradicts source, or blocks completion
- **MEDIUM** — likely wrong, or important context missing
- **LOW** — style / wording / minor formatting

---

## Check 1: Internal Contradictions

**Question**: Does any claim in the draft contradict another claim in the same draft?

**Look for**:
- [ ] Same action item appears with different owners in different sections
- [ ] Same deadline rendered differently (e.g. "Aug 20" in table, "Aug 22" in discussion)
- [ ] A decision contradicts the action items derived from it
- [ ] Numbers, dollar amounts, percentages, counts that disagree across sections
- [ ] Status of a topic stated as both "agreed" and "deferred"
- [ ] Attendee list inconsistent with speakers attributed in discussion

**How to fix**: Identify the authoritative version (usually the source) and align all references to it.

---

## Check 2: Consistency with Source / Coherence

**Question**: Does the draft accurately reflect the source, and do its parts cohere?

**Look for**:
- [ ] Every "Decision Made" has corresponding discussion or context in the source
- [ ] Every Action Item traces back to a stated commitment in the source
- [ ] Numbers/data points match the source verbatim (no rounding errors)
- [ ] No fabricated content (quotes, names, dates not present in source)
- [ ] Topic ordering / emphasis reflects what actually got airtime in the meeting
- [ ] Tone and terminology match the source register (formal/casual, JP/EN)

**How to fix**: For invented content, either remove it or mark it `* To be confirmed` with a note. For mismatched data, restore the source value.

---

## Check 3: Action Item Omissions

**Question**: Did we capture every commitment from the source?

**Source phrases that MUST become action items**:

English:
- "I'll do X" / "I will X" / "I can take that"
- "We should X" / "we ought to X" / "let's X"
- "Let's X by [date]" / "X by EOW / by next Tuesday"
- "Need to check / investigate / confirm / verify"
- "Follow up with [person]" / "circle back on X"
- "TODO: X" / "AI: [person] to X"

Japanese (日本語):
- 「やっておきます」「やります」「対応します」「進めます」「巻き取ります」
- 「Xすべき」「Xしたほうがいい」「Xしましょう」
- 「[date]までにXします」「来週までに」「次回までに」「月内に」
- 「確認します」「調べます」「検証します」「裏取りします」
- 「[person]にフォローします」「[person]に連絡します」「持ち帰り」「宿題」
- 「TODO」「ToDo」「課題」「未決事項」「アクション」

**Look for**:
- [ ] Commitments mentioned in the source but not in the Action Items table
- [ ] Action items missing an owner (every row needs one, even if `(To be confirmed)`)
- [ ] Action items missing a due date (`TBD` is acceptable; blank is not)
- [ ] Action items missing priority
- [ ] Multi-step commitments collapsed into one ambiguous row

**How to fix**: Add missing rows. For ambiguous owners/dates, use `(To be confirmed)` / `TBD` and add to the "manual verification" list in the completion report.

---

## Check 4: Speaker-Name Errors

**Question**: Are all names spelled and attributed correctly?

**Look for**:
- [ ] Inconsistent spelling of the same person across the draft (e.g. "Tanaka" / "Tanaka-san" / "田中さん" mixed)
- [ ] Swapped first/last names
- [ ] Honorifics dropped or added inconsistently
- [ ] Quoted statements attributed to the wrong person
- [ ] Owner field references someone not on the attendee list
- [ ] Department / role used as a name when an individual is identified in the source
- [ ] Romanization inconsistency (e.g. "Sato" vs "Satoh")

**Japanese-specific patterns to watch (日本語固有の注意点)**:
- 「田中」「田中さん」「田中課長」「田中部長」など敬称・役職の揺れ
- 漢字／ひらがな／カタカナ／ローマ字の表記揺れ（「斎藤」「斉藤」「サイトウ」「Saito」「Saitoh」）
- 同姓 attendee がいる場合、姓のみだと曖昧になるので fullname または役職併記を維持する
- 敬語表現で発言者が省略された箇所（「〜だそうです」「〜とのことです」）の attribution 漏れ
- 出席者一覧と登場発言者リストの差分（「[name] については議事録に出ているが attendees に含まれていない」など）

**How to fix**: Pick one canonical form per person (preferring the source's own spelling) and apply globally. If the source itself is inconsistent, choose one form and add a note.

---

## Check 5: Date / Day-of-Week Errors

**Question**: Is every date in the draft real, and does its day-of-week match?

**MANDATORY**: For every concrete date, run:

```bash
python3 -c "import datetime; d=datetime.date(YYYY,MM,DD); print(d.strftime('%Y-%m-%d %A'))"
```

Compare the printed day-of-week against what the draft says.

**Look for**:
- [ ] Date + day-of-week mismatches (e.g. "2026/05/15 (Mon)" but it's actually Friday)
- [ ] "Next Tuesday" / "next week" resolved to the wrong calendar date
- [ ] Year typos (e.g. "2025" written when meeting is in 2026)
- [ ] Month/day swapped (US vs JP/EU date order confusion)
- [ ] Time-zone conversion errors (ET ↔ JST: +13h summer / +14h winter)
- [ ] Dates earlier than the meeting date used for future deadlines
- [ ] DST boundary errors (US DST ends 1st Sun of Nov; JP has no DST)

**Japanese-specific date patterns (日本語固有の日付表現)**:
- 「来週火曜」「再来週」「月末」「来月初」などの相対表現が会議日に対して正しく解決されているか
- 和暦表記（「令和○年」「平成」）→西暦変換が正しいか（令和8年 = 2026年）
- 「○月○日（火）」の曜日表記が `python3 -c "import datetime..."` 検証と一致しているか
- 「金曜まで」「金曜中に」が EOD/EOW どちらの解釈か明示されているか
- 「JST」「日本時間」「現地時間」の使い分けが一貫しているか

**How to fix**: Recompute the correct date and update both the date and day-of-week fields.

---

## Iteration Decision Logic

After running all 5 checks:

```
findings = {HIGH: [...], MEDIUM: [...], LOW: [...]}

if len(findings.HIGH) + len(findings.MEDIUM) + len(findings.LOW) == 0:
    → CLEAN PASS — exit loop, report completion
elif iteration < 3:
    → Apply fixes, increment iteration, re-review
else:  # iteration == 3 and findings still exist
    → Apply what fixes are possible
    → Exit loop with FINAL_REPORT_OPEN_ITEMS
    → Surface remaining HIGH findings in completion report
```

## Anti-Patterns to Avoid in the Review

- ❌ Confirming "looks good" without running the date verification command
- ❌ Skipping a check because the draft "seems fine"
- ❌ Marking a finding "fixed" without re-checking after the edit
- ❌ Suppressing findings to reach "0" faster — the loop terminates at 3 anyway
- ❌ Treating reviewer-introduced changes as findings (only flag draft-vs-source / draft-vs-self issues)
