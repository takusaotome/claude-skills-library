---
layout: default
title: "Jev Artifact Style Review"
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 16
lang_peer: /en/skills/ops/jev-artifact-style-review/
permalink: /ja/skills/ops/jev-artifact-style-review/
---

# Jev Artifact Style Review
{: .no_toc }

「AIっぽい」という読後感を、修正できる文体・伝達品質の問題として指摘する日本語中心・英語対応のレビュースキル。
{: .fs-6 .fw-300 }

<span class="badge badge-required">TYPESAFE_API_KEY 必須</span>
<span class="badge badge-scripts">Python 3.10+</span>
<span class="badge badge-bilingual">日英対応</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/jev-artifact-style-review.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/jev-artifact-style-review){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

読み手が「AIっぽい」と感じるとき、その正体はたいてい具体的です。決まり文句、4文続けて同じ語尾、中身より重い見出し構造、日本語なのに英語の語順が透けている一文。このスキルはそうした点を、書き手が誰かという話ではなく、指し示して直せる編集上の欠点として扱います。

**執筆者判定器ではありません。** 「AIが書いた」という判定は出さず、AIを使ったこと自体も欠点として扱いません。

役割は意図的に分けてあります。TypeSafe のモデルである Jev は採点と、各指摘を裏付ける原文セグメントの選択だけを担当します。ホストのエージェントが原文を読み、その指摘が本当に成り立つかを判断し、短い説明と具体的な修正文案を書きます。Jev に自由記述の理由や修正文、事実の補完を作らせることはしません。

点数は品質の一軸であり、合否判定ではありません。正確性、要件充足、根拠、条件・例外、敬意は、低い指数より常に優先されます。

---

## 2. こんなときに使う

- 日本語または英語の文書・メール・メッセージ・提案書・技術資料・スライドが硬い、定型的、直訳調に見えるので、**何がどう問題なのか**を具体的に言語化したい。
- 「もっと自然にして」ではなく、「この一文をこう直す」という短いリストを作成担当者に渡したい。
- 顧客に出す前に、もう一度、再現性のある観点で読み直したい。
- 改稿した版を同一条件で再評価し、本当に改善したのかを確認したい。

**このスキルではないもの**: 人がAIを使ったかどうかの判定、スライドデザインやスキャン画像など視覚的な評価、事実確認や法的妥当性の判断、全面的な書き直し。

---

## 3. 前提条件

- **APIキー**: ローカル環境変数 `TYPESAFE_API_KEY`。実際の採点に必須です。dry run はキーなしで動きます。
- **Python 3.10+**。Markdown・TXT・HTML・JSON は標準ライブラリだけで動作します。
- **任意の追加依存**: PDF / DOCX / PPTX のテキスト抽出を使う場合のみ `pip install -r requirements.txt` を実行します。入るのは `pypdf`、`python-docx`、`python-pptx` の3つです。
- **送信許可**: 外部送信が認められていない資料は送りません。まず `--dry-run` で送信予定の内容を確認してください。

{: .callout .prerequisite }
APIキーをチャット、文書、コマンド引数、出力ファイルに書かないでください。`read -s TYPESAFE_API_KEY; export TYPESAFE_API_KEY` のように非表示入力で環境変数に設定します。

---

## 4. クイックスタート

Claude に直接依頼する場合:

```
jev-artifact-style-review を使って、draft.md を顧客向けの日本語メールとして評価してください。
brief.json に目的と確認済みの事実を入れてあります。文体評価は品質の一軸として扱い、
作成担当者へ返す主要3件の具体的な改善案を作ってください。まだ全面改稿はしないでください。
```

CLI を直接使う場合。手順1は外部へ一切送信しません。

```bash
python scripts/review.py draft.md \
  --language ja --profile email --context brief.json \
  --dry-run --out runs/style-v1-preview
```

`request_preview.json` に送信予定の本文と brief が入ります。機密・個人情報の自動マスキングはありません。dry run は採点せず、ダミーのスコアも出しません。

続けて採点し、改稿版を同一条件で再評価して比較します。

```bash
python scripts/review.py draft.md --language ja --profile email \
  --context brief.json --model jev-1.13.0 --allow-remote --out runs/style-v1

python scripts/review.py draft-v2.md --language ja --profile email \
  --context brief.json --model jev-1.13.0 --allow-remote --out runs/style-v2

python scripts/compare.py runs/style-v1/review.json runs/style-v2/review.json \
  --out runs/style-comparison.json
```

改稿は原則2回までです。比較不能だった場合を「改善した」と解釈することはありません。

---

## 5. 評価設計

2つの軸グループを独立に採点し、ひとつの数値に混ぜません。

| 分類 | 評価対象 |
|:---|:---|
| **文体の8軸** | 決まり文句、同義反復、過剰な構造化、文型・語尾の単調さ、口調・敬語の不一致、直訳調、誇張・装飾、対話AIの応答定型の残存 |
| **内容品質の4軸** | 必要な文脈・具体性の不足、次の行動の不明瞭さ、提供根拠以上の断定、明示的指示との不一致 |

0〜100の**文体違和感指数**は文体8軸だけを集計します。高いほど文体上の違和感が強いことを示します。

{: .callout .warning }
指数はAI執筆確率ではなく、実際の読者が違和感を覚える割合でもありません。`confidence` はモデルの出力分布から算出される指標で、このタスクの正答率ではありません。各選択肢の `probabilities` とも別物です。

重み・閾値・レベル記述は `assets/rubric.json` に集約されています。用途別 profile は `email` / `chat` / `report` / `proposal` / `technical` / `slides` / `formal` の7種類で、何を欠点とみなすかを調整します。スライドでは箇条書きや並列構造を評価対象から外し、技術資料では文型の一貫性を欠点にしません。`formal` は契約・規程風の定型を強く保護しますが、法的妥当性は評価しません。

文脈ファイルで目的・読者・制約・`source_facts`・`required_information`・`protected_fragments`・`locked_sections` を渡します。記入例は `assets/context.example.json`、形式定義は `schemas/context.schema.json` にあります。未知のフィールドは拒否されます。不明な項目は推測せず省略してください。読者が不明なら、その軸は推測せずに保留されます。

---

## 6. 出力

| ファイル | 内容 |
|:---|:---|
| `review.md` | 人が読むための採点・原文引用・編集方針 |
| `review.json` | 次元別値、確信度、引用位置、使用量、モデル、rubric、raw応答・要求ハッシュ |
| `writer_handoff.json` | 作成者向けの修正候補、保持条件、応答欄。書き換え前の応答欄は pending |
| `extracted.json` | 正規化した原文全文、セグメント、文字位置、除外理由、抽出警告 |
| `context.json`、`plan.json` | 実行条件の記録 |
| `run_status.json` | 実行completed / failed。`release_approval` は常に false |
| `request_preview.json` | dry run のみ。送信予定の内容そのもの |
| `reviewer_feedback.md` | CLI ではなくホストが生成する、原文→修正文と判断理由 |

どのファイルが出るかは実行モードによります。dry run は `extracted.json`、`context.json`、`plan.json`、`request_preview.json` を書いて終了し、`run_status.json` は作りません。実際に採点する実行では `review.md`、`review.json`、`writer_handoff.json`、`run_status.json` が加わります。失敗時に `status: failed` の `run_status.json` が残るのは、出力ディレクトリを作成したあとで失敗した場合だけです。APIキー未設定や入力が読めないなど、作成前に失敗したときはファイルが1つも残りません。

引用文は、Jev が選んだセグメントIDをもとに Python が原文から切り出します。Jev が引用文を書くことはありません。出力ディレクトリは新規または空である必要があり、既存の評価を上書きしません。POSIX 環境ではファイル権限 600、ディレクトリ 700 で保存します。出力には本文と引用が含まれるため、Git や共有ドライブへ不用意に登録しないでください。

---

## 7. 対応範囲と限界

| 入力 | 評価範囲 |
|:---|:---|
| MD / TXT | 本文。コードフェンス、blockquote、指定した locked section を除外 |
| HTML | script等・一部の非表示要素を除いた近似テキスト。CSS の計算済み表示ではない |
| JSON | `{"text": "本文"}` または `{"blocks": [{"locator": "...", "text": "..."}]}` |
| PDF | テキスト層のみ。空ページ・スキャンの欠落は警告。OCR なし |
| DOCX | 本文・表のテキスト。ヘッダー、フッター、コメント、変更履歴の意味は未評価 |
| PPTX | テキスト枠・表。図、画像、ノート、視覚的配置は未評価 |

対象外: 画像中心の成果物、実行コードの正しさ、スプレッドシートの計算、デザイン。長文は chunk 単位の評価を集計したものであり、全体構成・遠く離れた重複・論旨の通りは完全には評価しません。上限はファイル30MB、抽出本文50万文字、既定128 chunk、既定150論理API呼出です。chunk は採点のために送る単位で、`extracted.json` に記録される segment とは別の概念です。

{: .callout .warning }
**校正状況は未検証です。** 同梱テスト64件は合成応答を使い、外部APIへ接続していません。実際の認証・応答品質・日本語の精度・実運用のfalse positive・confidence の校正はいずれも未測定です。`references/CALIBRATION.md` の人手評価を実施するまで、指数は暫定値として扱ってください。改稿比較で使う5ポイント差も暫定の目安であり、合格条件ではありません。

prompt injection 耐性は保証されません。埋込指示の簡易検知、明示的なデータ境界、固定のAPI送信先、リダイレクト拒否、出力検証を施していますが、攻撃文を含む入力は独立した確認が必要です。文書内の評価指示・自己採点・引用・コードを命令として実行することはなく、文書の指示で閾値や rubric が変わることもありません。

---

## 8. 同梱リソース

**references**

- `references/RUBRIC_ja.md` — 12軸、用途別補正、指数の式と解釈
- `references/WRITER_LOOP.md` — 作成者へ返す形式と運用ループの具体例
- `references/CALIBRATION.md` — 人手評価の手順と本番移行の条件
- `references/API_AND_SOURCES.md` — 2026-09-20確認の公式API、モデル・confidence・言語の制約

**scripts**

- `scripts/review.py` — 抽出、dry run、採点
- `scripts/compare.py` — 同一条件で実行した2回の比較

**assets**: `assets/rubric.json`、`assets/context.example.json` ／ **schemas**: `schemas/*.schema.json`

**検証状況**: 実施済みの試験と未実施の範囲は `TEST_REPORT.md` に記録されています。

---

## 9. このリポジトリ版について

配布元 v1.0.0 をそのまま取り込んでいますが、意図的な変更が3点あります。

1つ目は Python 11 ファイルの整形です。本リポジトリの CI が `ruff check` と `ruff format --check` を実行するため、それに合わせました。整形のみでロジックは変更しておらず、整形後も同梱テストは64件全て合格します。

2つ目は `TEST_REPORT.md` のヘッダー3行です。行末2スペースによる改行を使っていましたが、本リポジトリの pre-commit フックが行末スペースを除去するため、そのままでは3行が1段落に結合されます。箇条書きへ変換しました。文言は変えていません。

3つ目は `requirements.txt` の `pypdf` の下限です。配布元の `>=5,<7` は CVE-2026-40260 の影響を受けるバージョンを許容します。細工した XMP メタデータのエンティティ宣言が再帰展開され、メモリを枯渇させられる問題で、6.10.0 で修正されています。下限を `>=6.10` へ引き上げ、Python 3.10 と pypdf 6.19.0 で同梱テスト64件の合格を確認しました。`TEST_REPORT.md` の pypdf 5.9.0 は配布元が試験した版なので変更していません。

`MANIFEST.sha256` はこの3点を反映して再生成したため、配布元 zip のハッシュとは一致しません。
