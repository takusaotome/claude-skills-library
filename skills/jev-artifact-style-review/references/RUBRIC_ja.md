# 評価ルーブリック v1.0.0

これは読者向け編集の独自ルーブリックです。AIの執筆確率・人間らしさの科学的測定値ではありません。
基準文は英語で定義し、日本語・英語の原文をそのままJevに評価させます。例示句に一致しただけでは減点しません。
公式の日本語評価ベンチマークではなく、実際の日本語業務文書での人手校正が必要です。

## 文体8軸

### stock_phrasing — 決まり文句・汎用的な前置き / Stock phrasing

**評価対象:** Unnecessary stock phrases and generic opening/closing sentences substitute for a direct message.
**除外・慎重に扱う場合:** Do not penalize ordinary greetings, thanks, contract boilerplate, required disclaimers or a phrase merely because it is common.
**返す編集方針:** 意思決定に寄与しない前置き・定型句を削り、要件から始める。挨拶や必要な免責は残す。
**基本重み:** 15
**例（単語ブラックリストではない）:** 昨今の急速に変化する環境において／包括的なアプローチが重要です / In today’s rapidly evolving landscape; it is important to note

### redundancy — 同義反復・冗長さ / Redundancy

**評価対象:** The passage repeats substantially the same point without adding useful information.
**除外・慎重に扱う場合:** An executive summary, safety repetition, definition or intentionally repeated procedural step may be appropriate. Do not count occurrences; judge added meaning.
**返す編集方針:** 同じ意味の文を統合する。条件、例外、注意事項は削らない。
**基本重み:** 20
**例（単語ブラックリストではない）:** 重要です／不可欠です／欠かせません、と同じ主張を重ねる / Restating the same benefit in multiple adjacent sentences

### mechanical_structure — 型にはめすぎた構成 / Over-templated structure

**評価対象:** Headings, numbered groups, symmetric sections or list items impose a structure that is disproportionate to the message.
**除外・慎重に扱う場合:** Do not penalize mandated templates, accessibility headings, technical procedures, checklists, comparison tables or slide bullets that help the reader.
**返す編集方針:** 見出しや項目を目的に合わせて減らす。指定テンプレート、手順の順序、比較軸は維持する。
**基本重み:** 15
**例（単語ブラックリストではない）:** 短い返信を「背景・現状・課題・方向性・まとめ」の五章に分ける / A two-sentence update expanded into a five-section framework

### uniform_rhythm — 文型・語尾の機械的な反復 / Mechanical sentence rhythm

**評価対象:** Repeated sentence patterns or endings create conspicuously monotonous prose where variation would improve readability.
**除外・慎重に扱う場合:** Consistent terminology, controlled language, parallel safety instructions and short messages are not defects. Do not inject random variation.
**返す編集方針:** 読みにくい部分だけ文を統合・分割する。専門用語や手順文の一貫性は崩さない。
**基本重み:** 10
**例（単語ブラックリストではない）:** 各文が「〜することができます」で続き、情報の強弱がない / Every paragraph follows the identical opening, explanation and closing pattern

### register_mismatch — 敬語・距離感・口調の不一致 / Register mismatch

**評価対象:** The level of formality, politeness or interpersonal warmth does not fit the stated reader and purpose.
**除外・慎重に扱う場合:** Japanese business greetings, honorifics and requests are normal. Do not equate fluent, formal or non-native English with machine authorship. If reader context is missing, abstain unless the mismatch is self-evident.
**返す編集方針:** 相手との関係に合う口調に整える。社外メールの敬意は維持し、過剰なへりくだりだけを調整する。
**基本重み:** 15
**例（単語ブラックリストではない）:** 社内の短い連絡に「ご確認いただけますと幸甚に存じ上げます」を重ねる / Effusive praise in a routine technical incident update

### translationese — 直訳調・不自然な連語 / Translation-like awkwardness

**評価対象:** Collocations, word order or nominalizations are unnatural in the original language and impede comprehension.
**除外・慎重に扱う場合:** Read the original without translation. Accepted technical terms, loanwords, legitimate bilingual usage and a non-native writer identity are not defects.
**返す編集方針:** 原文の意味を保ち、自然な動詞・語順に直す。無理に和語化せず、専門用語は維持する。
**基本重み:** 10
**例（単語ブラックリストではない）:** 課題をアドレスするための価値をアンロックする / Make an implementation of the confirmation

### inflated_rhetoric — 誇張・過剰な装飾や共感 / Inflated rhetoric

**評価対象:** Grand claims, decorative metaphors or emotional amplification are disproportionate to the actual content and purpose.
**除外・慎重に扱う場合:** Persuasive copy or empathetic responses can be appropriate when requested. Judge excess in context, not the existence of emotion or metaphor.
**返す編集方針:** 根拠のない強調や比喩を外し、実際に伝えられる効果・限界へ戻す。新しい数値や実績は作らない。
**基本重み:** 10
**例（単語ブラックリストではない）:** 定例の設定変更を「革新的で圧倒的な変革」と表現する / Calling a minor configuration change a game-changing revolution

### assistant_residue — 成果物に残った対話AIの応答定型 / Conversational assistant residue

**評価対象:** The deliverable contains unsolicited chat-assistant framing, self-reference or follow-up offers that do not belong in the final artifact.
**除外・慎重に扱う場合:** Quotes, documentation about AI systems, customer-service offers requested by the brief and actual dialog transcripts are not defects.
**返す編集方針:** 完成成果物に不要な対話の前置き・後置きを除く。引用や実際のサービス案内は残す。
**基本重み:** 5
**例（単語ブラックリストではない）:** 素晴らしい質問です／以下にご依頼の文章を作成します／ご希望であればさらに / Certainly! Here is your requested email; let me know if you would like me to refine it

## 内容品質4軸（指数には加算しない）

### context_specificity — 文脈・具体性の不足 / Missing context-specific information

**評価対象:** Required case-specific information available in the brief is missing or replaced by generic statements.
**除外・慎重に扱う場合:** Do not request fabricated examples, names, dates or numbers. Generic educational material may be correct for its purpose.
**返す編集方針:** 提供された事実・背景のうち必要なものを反映する。不明点は作成者に確認し、推測で補わない。
**必要な文脈:** brief。該当するbriefがなければ評価から外す。

### action_clarity — 依頼・担当・次の行動の不足 / Unclear next action

**評価対象:** A next action required by the brief is unclear to the reader.
**除外・慎重に扱う場合:** Do not require an owner or deadline for a greeting, narrative, informational note or a task that does not call for action. Never invent an owner or deadline.
**返す編集方針:** 依頼内容・次の行動を明示する。担当や期限が未確定なら確認事項として残す。
**必要な文脈:** action。該当するbriefがなければ評価から外す。

### support_alignment — 根拠に対する断定の強さ / Certainty beyond supplied support

**評価対象:** The passage presents a claim more definitively than the supplied source facts or explicit uncertainty warrant.
**除外・慎重に扱う場合:** This compares only the supplied evidence. It is not external fact checking. Missing external evidence alone does not prove a claim false.
**返す編集方針:** 提供根拠の強さに合わせて断定を調整する。外部の真偽検証は別工程へ返す。
**必要な文脈:** facts。該当するbriefがなければ評価から外す。

### instruction_fit — 指示・制約との不一致 / Mismatch with explicit instructions

**評価対象:** An explicit requirement in the supplied brief is violated by the evaluated passage.
**除外・慎重に扱う場合:** Judge a visible conflict, not an omission elsewhere in a chunked document. Other chunks may satisfy a requirement. Use an independent final checklist for completeness.
**返す編集方針:** 明示された制約・要件への不一致を修正する。長文全体の網羅性は別チェックで確認する。
**必要な文脈:** constraints。該当するbriefがなければ評価から外す。

## 段階と集計

各軸で評価可能性のChoiceと、0〜4のScoreを分ける。評価可能性は`assessable` / `not_applicable` / `insufficient_context`。問題がないことは、それだけでは適用外の意味ではない。

| 段階 | 読者への影響 |
|---:|---|
| 0 | この軸の問題を認めない |
| 1 | 軽微。局所的な任意修正 |
| 2 | 気になる。狙いを定めた修正で読みやすくなる |
| 3 | 強い。理解・用途適合性を損なう |
| 4 | 支配的。この問題が伝達を繰り返し妨げる |

JevのScoreは段階番号に対する確率加重値をそのまま使う。0始まりなので最大4であり、5で割らない。[1]

各軸の深刻度 = 確信度条件を満たす断片の文字数加重平均。
文体違和感指数 = 25 × Σ(用途補正後の重み × 文体軸深刻度) / Σ(集計対象の文体軸重み)。
同じ文字列の頻出回数や見出し数は補助メトリクスのみで、機械的に点へ変換しない。

用途中立の深刻度平均を文書全体の真の読者反応と解釈しない。長文は局所評価の集計である。
少なくとも3文体軸、対象重みの70%以上、文字範囲の70%以上が評価条件を満たすことを暫定の指数計算条件とする。
日本語・mixedは空白を除く80文字未満、英語は簡易単語数35語未満で総合指数を保留する。短文中の明瞭な指摘候補を出すこと自体は許容する。

## 閾値はすべて試運用値

評価可能性confidence 0.45、Score confidence 0.40、根拠Choice confidence 0.45、修正候補の深刻度1.5。
比較の変化目安は5ポイント。これらは測定済みの最適値でも、正答率保証でもない。
confidenceは応答分布から計算される統計値であり、本用途の正答率ではない。[2]

## 用途補正

| Profile | 考慮すること |
|---|---|
| email | Business email. Prefer a direct purpose, appropriate courtesy and an explicit request only when needed. |
| chat | Short work message. Brevity is normal. Do not force introductions, conclusions or rich detail. |
| report | Analytical report. Headings, executive summaries and tables are useful; retain caveats and sources. |
| proposal | Business proposal. Persuasion is appropriate but unsupported grandiosity is not. Preserve scope and commercial terms. |
| technical | Technical document, specification or README. Consistent terms, procedural repetition and code are appropriate. |
| slides | Slide text only. Short fragments, bullets, headings and parallel structure are appropriate. Visual layout is not evaluated. |
| formal | Formal policy or contract-like text. Required terminology, boilerplate and defined terms must not be casually rewritten. |

基本重みとの差分は`assets/rubric.json`。重みを変更するとrubricハッシュが変わり、以前の結果とは同条件比較できなくなる。

## 参照
[1] https://docs.typesafe.ai/primitives/score
[2] https://docs.typesafe.ai/confidence
