---
layout: default
title: "Meeting Minutes Writer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 23
lang_peer: /en/skills/meta/meeting-minutes-writer/
permalink: /ja/skills/meta/meeting-minutes-writer/
---

# Meeting Minutes Writer
{: .no_toc }

トランスクリプトやメモから戦略コンサル品質の議事録を生成し、その後「自己レビューループ（最大3反復）」で議事録内の矛盾・整合性・アクションアイテムの漏れ・発言者名の誤り・日時/曜日のズレをチェックしてから完了報告するスキルです。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-writer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-minutes-writer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このスキルは、生のミーティング素材（トランスクリプト、メモ、別ツールで起こした録音テキストなど）を、エグゼクティブが3分で把握できる構造化議事録に変換します。ドラフト生成後は、ソース素材とドラフト自身を突き合わせる**自己レビューループ（最大3反復）**を実行し、5つの必須チェックを通過するか3反復が尽きるまで繰り返したうえで完了報告します。完了時にHIGH指摘が残っている場合は、その項目を明示的にフラグします。

**対応言語**: 日本語と英語の両方を一級市民として扱います。ソース言語に合わせて出力言語を自動決定し、日本語素材→日本語議事録（「会議情報」「アクションアイテム」「決定事項」など日本語見出し）、英語素材→英語議事録を生成します。バイリンガル会議の場合は多数派言語を採用し、固有名詞・引用・技術用語は元の言語のまま保持します。

近接するスキルとの位置づけ:
- `meeting-minutes-reviewer` — レビュー専用（既存議事録の品質評価）
- `video2minutes` — 動画→文字起こし。生成時に本スキルへ渡せます

---

## 2. 前提条件

- Python 3.9 以上（必須の日付検証コマンドにのみ使用）
- APIキーは不要
- 追加パッケージは不要（標準ライブラリの `datetime` のみ）

---

## 3. クイックスタート

`<<Transcript>>` タグで素材を渡すか、トランスクリプトファイルを添付して「議事録を作って」と依頼してください。スキルは次を実行します。

1. 6ステップの生成ワークフローでドラフト作成
2. 自己レビューループ（最大3反復）
3. 完了報告（出力パス／反復回数／反復ごとの修正件数／残存HIGH指摘／要手動確認項目）

ドラフト中の各日付に対し、曜日を以下で必ず検証します。

```bash
python3 -c "import datetime; d=datetime.date(2026,5,15); print(d.strftime('%Y-%m-%d %A'))"
# 2026-05-15 Friday
```

---

## 4. 進め方

スキルは **2フェーズ** で動きます。

### Phase 1 — ドラフト生成（ultrathink）

1. メタデータ（会議名・日付・出席者）を抽出。欠落していれば推論し `* To be confirmed` を付与
2. 発言者と役割を特定
3. 議論スレッドをトピックに整理。長い議論は2〜3点のキーポイントへ要約
4. 「やります／確認します／対応します／調べます」などのコミットメントは全てアクションアイテム化
5. 明確な合意・指示は決定事項として抽出
6. `references/output_format.md` の正準構造でドラフト出力

### Phase 2 — 自己レビューループ（最大3反復）

```
iteration = 1
while iteration <= 3:
    findings = run_review(draft)
    if findings.is_empty():
        break  # クリーンパスで終了
    apply_fixes(draft, findings)
    iteration += 1
```

各反復で5つの必須チェックを実行します。

1. **内部矛盾** — オーナー／期日／数値の自己矛盾
2. **整合性** — ソースに対する忠実性、捏造内容なし
3. **アクションアイテムの漏れ** — ソース中のコミットメントが全てテーブルに記載されている
4. **発言者名の誤り** — 表記の一貫性、誤帰属、敬称ミス
5. **日時／曜日の誤り** — 全ての具体的な日付について Python `datetime` で曜日検証

各指摘は重要度で分類：**HIGH**（完了をブロック）／**MEDIUM**／**LOW**。指摘には場所・ソース引用・修正案を含めます（テンプレート: `assets/findings_report_template.md`）。

### 完了報告

ループ終了時のみ完了を報告します。報告には以下を含めます。

- 最終議事録ファイルのパス
- 実行した反復回数
- 反復ごとに修正した指摘件数（件数＋簡潔なサマリ）
- **3反復後にHIGH指摘が残っている場合は明示的にフラグ**
- ユーザーに手動確認を要する `* To be confirmed` 項目一覧

---

## 5. 使用例

- 長い製品計画ミーティングのトランスクリプトを、検証済み日付と完全なアクションアイテム付き議事録に変換
- スタンドアップの簡潔メモを品質ゲート済み議事録にクリーンアップ
- ソース言語に合わせたバイリンガル対応（日本語素材→日本語議事録）
- 全ての決定とアクションがソースに遡及可能な、監査対応議事録の作成
- LLMがやりがちな「来週火曜＝間違った日付」の検出・修正

---

## 6. 出力の読み方

### 議事録の構造

```markdown
### 1. Meeting Information
- **Meeting Name**: ...
- **Date**: 2026/04/30 (Thu)
- **Attendees**: ...

### 2. Action Items
| No. | Action Item | Owner | Priority | Due Date | Notes |
|-----|-------------|-------|----------|----------|-------|

### 3. Meeting Details
#### Decisions Made
#### Key Topics and Discussion Points
#### Notes for Future Meetings / Other
```

優先度: 🔴 High（ブロッカー）／🟡 Medium（実施すべき）／🟢 Low（あれば良い）

### 反復ごとの Findings Report

各レビュー反復は、重要度・場所・引用・修正案を含む指摘リストを生成します。完了報告ではその合計を要約します。

### 曖昧マーカー

- `* To be confirmed` — 推論内容、ユーザー側で要確認
- `[Details unclear]` — ソースが不明瞭・断片的
- `(To be confirmed)` — 担当者欄に付与する場合、オーナー未確定

---

## 7. ベストプラクティス

- **レビューループは絶対にスキップしない** — 短い議事録でも最低1回は実行してから完了報告
- **日付は必ず Python コマンドで検証** — LLMの記憶ベースは不確実なので絶対に頼らない
- **ユーザー指定の名前は表記そのまま保持** — 「田中さん」を勝手に「Tanaka」に正規化しない
- **指摘にはソースを引用** — 修正の根拠が監査可能になるように
- **決定事項は言い換えない** — 実際に合意された言葉に近い形で記録
- 完了報告では `* To be confirmed` を必ず可視化し、ユーザーが追って確認できるようにする

---

## 8. 他スキルとの連携

- `video2minutes` と組み合わせて、動画→文字起こし→レビュー済み議事録 を一気通貫で実行
- 生成後にさらに深い品質スコアリングを行いたい場合は `meeting-minutes-reviewer` を後段に配置
- アクションアイテムを `project-manager` や `project-artifact-linker` に渡し、プロジェクト計画への追跡性を確保
- 関連ワークフローを探す場合は同カテゴリの一覧を参照: [カテゴリ一覧]({{ '/ja/skills/meta/' | relative_url }})

---

## 9. トラブルシューティング

- **ドラフト中の日付・曜日がおかしい** — `python3 -c "import datetime..."` の検証が走っていない可能性。明示的に再実行を依頼してください
- **アクションアイテムが漏れている** — ソース内の「should / will / TODO / 確認 / 対応 / フォロー」をgrepし、Check 3（漏れ）にフォーカスして再反復させてください
- **発言者名がセクション間で揺れている** — Check 4 のみで再反復。スキルはソースの表記に正規化します
- **3反復終了時にHIGH指摘が残る** — 多くはソース自身に矛盾があるケース（トランスクリプト自体が食い違う等）。報告内のソース引用を見て手動解決してください
- **完了報告に `* To be confirmed` の一覧がない** — 通常は完了報告の末尾に出力されます。表示されない場合は、ソースに推論対象の欠落がなかった可能性があります

---

## 10. リファレンス

**参照ガイド:**

- `skills/meeting-minutes-writer/references/output_format.md` — 議事録の正準構造、推論ルール、曖昧マーカー
- `skills/meeting-minutes-writer/references/self_review_checklist.md` — 5つの必須チェックと反復ロジックの詳細基準

**アセット:**

- `skills/meeting-minutes-writer/assets/minutes_template_ja.md` — 議事録テンプレート（日本語）
- `skills/meeting-minutes-writer/assets/minutes_template_en.md` — 議事録テンプレート（英語）
- `skills/meeting-minutes-writer/assets/findings_report_template.md` — 反復ごとの指摘レポートテンプレート（日英バイリンガル）

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/meeting-minutes-writer/' | relative_url }}) を参照してください。
