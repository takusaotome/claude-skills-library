# 作成担当者へ返す形式と改善ループ

## 誰が何をするか

Jevは独立した評価値・確信度・根拠候補IDを返す。
PythonはAPI契約、元テキストとの対応、集計、保護語句・数値差分を扱う。
ホストの生成エージェントは指摘の妥当性と具体的な修正文を考える。
作成者は必要な修正だけを行い、事実・要件を確認する。
最終レビュー担当は、文体以外の品質基準を含めて成果物を判断する。

同じモデルが作成と修正を担当してもよいが、原文・brief・修正版の照合は採点とは独立した工程にする。
人がレビューできる場合は、日本語の口調・敬語・案件文脈の判断を優先する。

## フィードバック例（合成例。Jevの実測結果ではない）

**評価対象:** 法人顧客への移行作業の進捗連絡。

**原文:**
> 円滑かつ確実な移行を実現することは非常に重要であり、関係者間の連携を通じて最適な対応を推進していくことが不可欠です。

**指摘:** 移行が重要という一般論が先に来ており、顧客が知りたい現在の停止理由と次の対応が後ろに隠れています。

**修正案:**
> システム移行用のライセンスキーが一部未着のため、訪問日はまだ確定していません。必要なキーが揃い次第、A店舗から対応する日程をご相談いたします。

**この修正を成立させる根拠:** 一部キーが未着、キーが揃い次第日程調整、初回はA店舗、訪問日未確定という情報がbriefにある。
その情報がなければ上記修正は作らず、「未確定の理由・次の対応を確認してください」と返す。

**保持するもの:** A店舗、未着の範囲、訪問日の未確定性、顧客への丁寧さ。

**確認条件:** 読者が「なぜまだ訪問できないか」「次に何が起きるか」を読み取れる。具体的な到着日や担当者を追加していない。

## reviewer_feedback.mdのテンプレート

```markdown
# 作成担当者向けレビュー

対象: <artifact>
用途・読者: <confirmed context>
Jev実測の文体違和感指数: <value or withheld> / 100
これは執筆者判定・AI生成確率ではありません。

## 優先修正（最大3件）

### F01 — <dimension>
位置: <locator and segment ID>
原文: <exact quote>
読者への影響: <specific explanation by host reviewer>
修正案: <concrete replacement preserving available facts>
保持条件: <facts, caveats, required structure>
確認条件: <observable success criterion>
未確定事項: <questions, or none>

## 採用しなかった指摘
<finding ID and rationale; do not modify raw Jev audit>

## 内容品質の別チェック
<required-information checklist; numbers/dates/terms preserved?>

## 次の対応
<targeted author revision, or no change, or clarification>
```

## 機械連携

`writer_handoff.json`の`event`は`editorial_review_available`。
`revision_candidates`が原文引用・位置・評価軸・深刻度を持ち、`preserve`が既知事実・必須情報を持つ。
`writer_response`は未対応時`pending`。作成者が対応したら、元のhandoffを監査用に残し、応答を別ファイルに保存する。

例:

```json
{
  "status": "revised",
  "edits": [
    {
      "finding_id": "F01",
      "before": "<original exact span>",
      "after": "<replacement>",
      "reason": "<specific reader benefit>"
    }
  ],
  "unresolved_questions": [],
  "fact_and_meaning_preservation": "reviewed_by_author; independent_check_pending",
  "requirement_checklist": [
    {"requirement": "<brief requirement>", "status": "preserved", "evidence": "<new text>"}
  ]
}
```

作成・レビューを分けたエージェント運用では、レビュー担当から作成担当へこのファイルを渡せばよい。
この版には外部キュー、Slack/Gmail送信、PR投稿、特定エージェントSDKへの結合は含めない。

## 止める条件

改稿は最大2回。重要な指摘が解消された、修正の実益が小さい、校閲者が正当な定型だと判断した、
内容保持に疑義が生じた、または比較条件が変わった場合には停止または人へ戻す。

「総合指数が0になるまで」「一定点未満なら自動納品」は設定しない。
Jevの指数が上がっても、必要な説明を戻した結果ならその方が正しい場合がある。
文体・事実・要件・利用目的の優先順位を保つ。
