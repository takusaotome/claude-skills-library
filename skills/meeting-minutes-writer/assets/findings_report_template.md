# Self-Review Findings — Iteration {N} / 自己レビュー指摘 — 第{N}反復

> Use this template in the language matching the minutes draft (English minutes → English report; Japanese minutes → Japanese report). Both layouts are shown side-by-side; pick one and delete the other when generating the actual report.
>
> 議事録ドラフトの言語に合わせて使用してください（英語議事録→英語レポート、日本語議事録→日本語レポート）。下に英語版・日本語版を併記してあるので、生成時はどちらかを選び、もう片方を削除してください。

---

## English layout

**Draft file**: `{path/to/draft.md}`
**Reviewed at**: {YYYY-MM-DD HH:MM}
**Checks run**: 1) Contradictions  2) Consistency  3) Action Items  4) Speaker Names  5) Dates

### Summary

| Severity | Count |
|----------|-------|
| HIGH     | {n}   |
| MEDIUM   | {n}   |
| LOW      | {n}   |
| **Total**| {n}   |

Result: **{CLEAN PASS / FIXES NEEDED}**

### Findings

#### Finding 1 — [HIGH | MEDIUM | LOW] — Check {1-5}: {check name}

- **Location**: §{section} / row {N} / line {N}
- **Issue**: {one-sentence description}
- **Evidence (source)**: > "{verbatim quote from source}"
- **Evidence (draft)**: > "{verbatim quote from draft}"
- **Suggested fix**: {concrete change to make}

#### Finding 2 — ...

### Verification Commands Run (for date checks)

```bash
$ python3 -c "import datetime; print(datetime.date(2026,5,15).strftime('%Y-%m-%d %A'))"
2026-05-15 Friday
```

| Date in draft | Day in draft | Verified day | OK? |
|---------------|--------------|--------------|-----|
| 2026/05/15    | Mon          | Fri          | ❌  |

### Next Action

- [ ] Apply fixes 1..N to draft
- [ ] Re-run self-review (iteration {N+1})
- [ ] If iteration 3 and findings still HIGH → flag in completion report

---

## 日本語版レイアウト

**ドラフトファイル**: `{path/to/draft.md}`
**レビュー日時**: {YYYY-MM-DD HH:MM}
**実施チェック**: 1) 内部矛盾  2) 整合性  3) アクション漏れ  4) 発言者名  5) 日付・曜日

### サマリ

| 重要度 | 件数 |
|--------|------|
| HIGH   | {n}  |
| MEDIUM | {n}  |
| LOW    | {n}  |
| **合計** | {n} |

結果: **{クリーンパス / 要修正}**

### 指摘一覧

#### 指摘 1 — [HIGH | MEDIUM | LOW] — チェック{1-5}: {チェック名}

- **場所**: §{セクション} / 行 {N} / テーブル {N} 行目
- **問題**: {1文で簡潔に}
- **根拠（ソース）**: > 「{ソースからの逐語引用}」
- **根拠（ドラフト）**: > 「{ドラフトからの逐語引用}」
- **修正案**: {具体的な修正内容}

#### 指摘 2 — ...

### 実行した検証コマンド（日付チェック）

```bash
$ python3 -c "import datetime; print(datetime.date(2026,5,15).strftime('%Y-%m-%d %A'))"
2026-05-15 Friday
```

| ドラフト中の日付 | ドラフト記載の曜日 | 検証結果の曜日 | 整合 |
|------------------|-------------------|---------------|------|
| 2026/05/15       | Mon               | Fri           | ❌   |

### 次のアクション

- [ ] 指摘1〜Nの修正をドラフトに反映
- [ ] 自己レビューを再実行（第{N+1}反復）
- [ ] 第3反復でHIGH指摘が残る場合は完了報告でフラグ
