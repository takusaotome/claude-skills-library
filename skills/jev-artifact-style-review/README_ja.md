# Jev Artifact Style Review

**日本語中心・英語対応の「AIっぽさ」を、修正可能な文体・伝達品質として扱うAgent Skillです。**
執筆者判定器ではありません。文体の8軸と内容品質の4軸を分離し、作成担当者へ具体的に返す用途です。

Version 1.0.0 · 2026-09-20 · Python 3.10+ · Jev実APIによる本用途の精度検証は未実施。

## 最初に使う方法

ZIPを展開し、`jev-artifact-style-review`フォルダをそのままClaude Codeの
`.claude/skills/`へ配置します。`SKILL.md`だけでなく、フォルダ一式が必要です。
Agent Skills仕様を採用する別のホストでも、スキルディレクトリへの配置とPythonの実行権限を確認して使えます。
各ホストでの実機ロード検証は未実施です。[1][2]

```bash
# プロジェクトのルートで実行。既存の同名skillがある場合は退避してから配置する。
mkdir -p .claude/skills
cp -R /path/to/jev-artifact-style-review .claude/skills/
```

Claude Codeへの依頼例:

> jev-artifact-style-reviewを使って、draft.mdを顧客向けの日本語メールとして評価してください。
> brief.jsonに目的・確認済みの事実を入れてあります。文体評価は品質評価の一軸として扱い、
> 作成担当者へ返す主要3件の具体的な改善案を作ってください。まだ全面改稿はしないでください。

生成担当エージェントに改善まで依頼する場合:

> この成果物をJevで評価し、具体的な局所修正、事実・要件の保持確認、同条件での再評価まで進めてください。
> 改稿は最大2回。スコアが下がっても内容を損なった変更は採用しないでください。

外部APIへの送信が許可されていない場合はdry runまでです。APIキーはユーザー自身の環境変数に設定してください。

## CLIを直接実行する

テキスト・Markdown・HTML・JSONは標準ライブラリだけで動きます。PDF/DOCX/PPTXを使う場合だけ追加依存が必要です。

```bash
cd jev-artifact-style-review
python3 -m venv .venv
source .venv/bin/activate
# PDF / Word / PowerPointのテキスト抽出を使う場合:
python -m pip install -r requirements.txt
```

APIキーをチャットに貼らず、ターミナルで非表示入力して環境変数に設定する例:

```bash
# bash / zsh共通。入力内容は画面表示されない。
read -s TYPESAFE_API_KEY
export TYPESAFE_API_KEY
printf '\n'
```

### 1. 外部通信なしの確認

```bash
python scripts/review.py examples/email_ja_before.md \
  --context assets/context.example.json --language ja --profile email \
  --dry-run --out runs/preview
```

`extracted.json`と`request_preview.json`で、抽出の範囲・原文・送信予定のbriefを確認できます。
**dry runは採点しません。ダミーのAIっぽさスコアも出しません。**

### 2. 実際のJev評価

```bash
python scripts/review.py examples/email_ja_before.md \
  --context assets/context.example.json --language ja --profile email \
  --model jev-1.13.0 --allow-remote --out runs/v1
```

1断片なら通常は採点1回＋根拠選択0〜1回です。長文は全ての評価対象断片を処理し、省略抽出やサンプリングはしません。
全体の呼出上限は `断片数 + min(top-k, 断片数)`。リトライは各論理呼出につき最大2回追加です。
HTTP要求の失敗時には課金済み使用量が不明な場合があるため、使用量表示は成功応答に含まれる分のみです。

### 3. 改稿後の再評価・比較

```bash
python scripts/review.py examples/email_ja_after.md \
  --context assets/context.example.json --language ja --profile email \
  --model jev-1.13.0 --allow-remote --out runs/v2

python scripts/compare.py runs/v1/review.json runs/v2/review.json \
  --out runs/comparison.json
```

比較は同じモデル・brief・rubric・profile・言語・抽出方式・設定でのみ有効です。
変更した評価軸、評価範囲の大きな変化、保留された指数などは比較不能にします。
例文の前後は説明用であり、改善がJevで実証された例ではありません。

### 4. 英文

```bash
python scripts/review.py examples/email_en.md \
  --language en --profile email --allow-remote --out runs/en-v1
```

英文の説明と改善指示を出力します。日本語文を英訳して採点する方法は採りません。
`--language auto`は文字種による簡易判定なので、再評価時は`ja`または`en`の明示を推奨します。
`mixed`も選べますが、日英別々の評価・校正を優先してください。

## 評価設計

| 分類 | 評価対象 |
|---|---|
| 文体の8軸 | 決まり文句、同義反復、過剰な構造化、文型・語尾の単調さ、口調・敬語の不一致、直訳調、誇張・装飾、対話AIの応答定型の残存 |
| 内容品質の4軸 | 必要な文脈・具体性の不足、次の行動の不明瞭さ、提供根拠以上の断定、明示的指示との不一致 |

0〜100の「文体違和感指数」は8文体軸だけを集計します。内容品質とは混ぜません。
これはAI執筆確率でも、実際の読者が違和感を覚える割合でもありません。
`confidence`も本タスクの正答率ではなく、モデル出力分布から算出される指標です。[3]

指数・重み・閾値・レベル記述は`assets/rubric.json`に集約しました。
日本語の精度と過剰指摘率を測定してから業務ごとに調整してください。
日本語を含む非英語はJevの最得意言語ではないと公式が説明しています。[4]

### 用途別profile

`email` / `chat` / `report` / `proposal` / `technical` / `slides` / `formal`

例: スライドでは箇条書きや並列構造を評価対象から外し、技術資料では文型の一貫性を欠点にしません。
formalは契約・規程風の文章で定型を強く保護しますが、法的妥当性の評価はしません。
既定値はCLIでは`email`ですが、skillは用途に合ったprofileを選びます。

## 文脈ファイル

`assets/context.example.json`は例です。実際の案件の確認済み情報へ置き換えてください。
`schemas/context.schema.json`に形式定義があります。

| フィールド | 役割 |
|---|---|
| `purpose`, `audience` | 目的・読者。未知なら省略 |
| `action_expected` | 読者に行動を求める文書か |
| `constraints` | 明示的な形式・口調・内容制約 |
| `source_facts` | 断定の強さを照合するための提供済み事実 |
| `required_information` | 最終的に保持する要件。全文の充足確認はホストの別工程 |
| `protected_fragments` | 完全一致で保持確認する語句・金額・識別子 |
| `style_reference` | 求める口調や、送信が許可された短い参考文 |
| `locked_sections` | 編集対象から外す正確な本文。該当行・文は除外扱い |

未知のフィールドは拒否します。source_factsは必要最小限にし、外部サイト取得やRAGはこの版では行いません。
required_informationの全件を満たしたかはJev指数だけでは保証できません。

## 出力

| ファイル | 内容 |
|---|---|
| `review.md` | 人向けの採点・原文引用・編集方針。CLIの編集方針は定型であり、具体案はホストが補う |
| `review.json` | 次元別値、確信度、引用位置、使用量、モデル、rubric、raw応答・要求ハッシュ |
| `writer_handoff.json` | 作成者向けの修正候補、保持条件、応答欄。書き換え前はpending |
| `extracted.json` | 正規化した原文全文、セグメント、文字位置、除外理由、抽出警告 |
| `context.json`, `plan.json` | 実行条件の記録 |
| `run_status.json` | 実行完了・失敗。いずれも自動公開承認はfalse |
| `reviewer_feedback.md` | SKILLの手順に従ってホストが生成する具体的な原文→修正文と判断理由。CLI単体は生成しない |

位置の`start`/`end`は正規化した`extracted.json`の本文に対するPythonの文字位置（endは含まない）です。
文書の`sha256`は正規化テキストのcanonical JSON表現のハッシュで、元ファイルのバイト列ハッシュではありません。
PDFではページ、PPTXではスライド、DOCXでは本文ブロックの位置も記録します。

出力ディレクトリは新規または空である必要があります。既存評価の上書きはしません。
JSON・Markdownの保存権限はPOSIX環境で600、出力ディレクトリは700です。
ローカル出力は本文と引用を含むため、Git・共有ドライブに不用意に登録しないでください。

## 対応範囲と留意点

| 入力 | この版の評価範囲 |
|---|---|
| MD/TXT | 本文。Markdownのコードフェンスとblockquote、指定locked sectionを除外 |
| HTML | script等・一部の非表示要素を除いた近似テキスト。CSSの計算済み表示ではない |
| JSON | `{"text":"本文"}`または`{"blocks":[{"locator":"message 123","text":"本文"}]}` |
| PDF | テキスト層のみ。空ページ・スキャンの欠落を警告。OCRなし |
| DOCX | 本文・表のテキスト。ヘッダー、フッター、コメント、変更履歴の意味は未評価 |
| PPTX | テキスト枠・表。図、画像、ノート、視覚的配置は未評価 |

巨大文書は断片別評価の集計であり、全体構成・遠く離れた重複・論旨の通りを完全には評価しません。
画像中心の成果物、実行コードの正しさ、スプレッドシートの計算、デザインのAIっぽさは対象外です。
テキスト抽出形式へ変換して評価する場合も、変換で失った範囲を別途確認してください。

入力上限: ファイル30MB、抽出本文50万文字、既定128断片、既定150論理API呼出。
状態＋質問はUTF-8バイトによる保守的な上限を設けていますが、正確なモデルのトークン数ではありません。
実際のトークン制限はTypeSafe側が適用します。[4]

モデルのprompt injection耐性を保証するものではありません。埋込指示の簡易検知、明示的なデータ境界、
固定のAPI送信先、リダイレクト拒否、出力検証を施していますが、攻撃文を含む入力は独立した確認が必要です。[5]
自動PII除去、完全な意味保持検証、実サービスへの投稿、常駐キュー・定期実行は実装していません。

## テスト

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

実行結果は`TEST_REPORT.md`を参照してください。テストは契約に沿う合成応答を使います。
Jev実APIの品質、日本語の精度、実運用のfalse positive、各エージェントのロードを証明するものではありません。
試運用用の合成ケースは`examples/pilot_cases.jsonl`です。人手校正の手順は`references/CALIBRATION.md`にあります。

## 公式根拠

[1] Agent Skills specification: https://agentskills.io/specification

[2] Claude Code skills: https://code.claude.com/docs/en/skills

[3] Confidence: https://docs.typesafe.ai/confidence

[4] Models / language / text-only / context limits: https://docs.typesafe.ai/models

[5] Jev 1.13 jaggedness: https://docs.typesafe.ai/model-jaggedness/jev-1.13

API契約の詳細・参照日は`references/API_AND_SOURCES.md`。このskillの重みや評価基準は独自設計で、TypeSafe公式のAI検出器ではありません。
