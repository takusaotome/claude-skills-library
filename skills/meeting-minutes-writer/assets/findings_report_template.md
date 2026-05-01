# Self-Review Findings — Iteration {N}

**Draft file**: `{path/to/draft.md}`
**Reviewed at**: {YYYY-MM-DD HH:MM}
**Checks run**: 1) Contradictions  2) Consistency  3) Action Items  4) Speaker Names  5) Dates

## Summary

| Severity | Count |
|----------|-------|
| HIGH     | {n}   |
| MEDIUM   | {n}   |
| LOW      | {n}   |
| **Total**| {n}   |

Result: **{CLEAN PASS / FIXES NEEDED}**

---

## Findings

### Finding 1 — [HIGH | MEDIUM | LOW] — Check {1-5}: {check name}

- **Location**: §{section} / row {N} / line {N}
- **Issue**: {one-sentence description}
- **Evidence (source)**: > "{verbatim quote from source}"
- **Evidence (draft)**: > "{verbatim quote from draft}"
- **Suggested fix**: {concrete change to make}

### Finding 2 — ...

---

## Verification Commands Run (for date checks)

```bash
$ python3 -c "import datetime; print(datetime.date(2026,5,15).strftime('%Y-%m-%d %A'))"
2026-05-15 Friday
```

| Date in draft | Day in draft | Verified day | OK? |
|---------------|--------------|--------------|-----|
| 2026/05/15    | Mon          | Fri          | ❌  |

---

## Next Action

- [ ] Apply fixes 1..N to draft
- [ ] Re-run self-review (iteration {N+1})
- [ ] If iteration 3 and findings still HIGH → flag in completion report
