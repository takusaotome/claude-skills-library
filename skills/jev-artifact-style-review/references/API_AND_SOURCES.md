# API・設計根拠・検証範囲

確認日: **2026-09-20**。以下は公開公式ドキュメントを参照した内容です。
配布コードの閾値・採点軸・重みは独自の編集ルーブリックで、TypeSafeが認証した検出法ではありません。

## 利用する契約

TypeSafeのJev評価APIは`POST https://api.typesafe.ai/v1/systemone`。
Bearer認証を使用し、`model`、`state`、`questions`を送信します。[1]
`state`は文字列・オブジェクト・配列のテキストデータ。
回答は質問IDをキーにした`answers`、実際の`model`、`usage`を返します。

このskillでは`Choice`を評価可否と原文ID選択に、`Score`を独立した深刻度評価に使います。
Scoreの`criteria`はレベル説明の順序配列。応答は0始まりのレベルに基づく確率加重`score`と分布を含みます。[1][2]
Jevは自由記述の修正案を生成する用途のモデルではないため、理由・リライトはホストの生成エージェントへ渡します。[3]

`confidence`は分布から計算される統計量であり、選択肢の確率そのものとは異なります。[4]
特に本skillの日本語文体レビューにおける正答確率と見なさないでください。

## モデル・入出力

確認時点のモデルは`jev-1.13.0`。`jev-latest`などの別名は将来変わり得るため、比較のために固定IDを既定としました。[5]
テキストのみが入力対象です。日本語などCJKは扱うものの、英語が最も得意であり、対象文書による検証が必要です。[5]

公式上限は状態＋全質問64k tokens、状態＋最長質問32k tokensです。[5]
実装では正確なtokenizerを推測せず、状態＋全質問58,000 UTF-8 bytes、状態＋最長質問28,000 bytesという
保守的な事前検査を行います。これはモデルのトークン使用量を保証する式ではありません。
実際の使用量はAPIの`usage`から記録します。

公式に、複雑な推論・数え上げ・数値比較・長い無関連文脈・敵対的な本文に弱点が記されています。[3]
このため、算術や文字位置はPythonで処理し、1問1軸、小さめの状態、明示的な例外を使います。
prompt injectionへの完全な防御は主張しません。

## エラーの扱い

HTTP 401/422などは停止。429/529および一部の一時障害は回数制限付きリトライ。
無効な応答、欠けた質問ID、範囲外のscore、分布不整合、根拠ID不整合は評価失敗です。
失敗を「0点」「合格」に置き換えません。エラーボディはログに出しません。
送信先は公式HTTPSエンドポイント固定で、リダイレクトは許可しません。

## Agent Skillの形式

標準の`SKILL.md`、YAML frontmatter、`scripts/`、`references/`構成を使います。[6]
Claude Codeのプロジェクトスキル配置例は`.claude/skills/<name>/SKILL.md`。[7]
TypeSafe自身もエージェントスキルを公開していますが、このパッケージはそのコピーや改変版ではありません。[8]

## 未検証

実API認証・レイテンシ・料金の実測、日本語・英語のタスク精度、閾値の校正、各ホストのロード、
複雑な実業務PDF/Word/PowerPointの抽出忠実度は未検証です。
配布時のPython試験は構造・境界条件・合成応答を使うオフライン試験です。

## 公式参照

[1] HTTP API: https://docs.typesafe.ai/api

[2] Score: https://docs.typesafe.ai/primitives/score

[3] Jev 1.13 jaggedness (last reviewed 2026-09-17): https://docs.typesafe.ai/model-jaggedness/jev-1.13

[4] Confidence: https://docs.typesafe.ai/confidence

[5] Models, language support, input and limits: https://docs.typesafe.ai/models

[6] Agent Skills specification: https://agentskills.io/specification

[7] Claude Code skills: https://code.claude.com/docs/en/skills

[8] Official TypeSafe agent skill: https://docs.typesafe.ai/agent-skill
