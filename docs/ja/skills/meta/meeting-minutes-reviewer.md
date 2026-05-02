---
layout: default
title: "Meeting Minutes Reviewer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 31
lang_peer: /en/skills/meta/meeting-minutes-reviewer/
permalink: /ja/skills/meta/meeting-minutes-reviewer/
---

# Meeting Minutes Reviewer
{: .no_toc }

議事録ドキュメントを完全性・アクションアイテム明瞭性・決定事項記録・ソース素材（ヒアリングシート、トランスクリプト等）との整合性の観点でレビューするスキル。5 ディメンションの品質スコアと、具体的な改善提案つきの構造化フィードバックを生成します。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/meeting-minutes-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

既存の議事録ドキュメントを品質基準と（任意で）ソース素材に対してレビューします。5 ディメンション（重み付き）でスコアリング — 完全性 (25%)、アクションアイテム (25%)、決定事項 (20%)、整合性 (15%)、明瞭性 (15%) — し、具体的な改善案つきの構造化指摘リストを出力します。

このスキルはレビュー専用です。トランスクリプトから議事録を**生成**したい場合は `meeting-minutes-writer`（独自の自己レビューループ付き）、会議資料を**事前準備**したい場合は `meeting-asset-preparer` を使ってください。

---

## 2. 前提条件

- Python 3.9 以上
- API キー不要
- 標準ライブラリのみ（json、re、pathlib）

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=meeting-minutes-reviewer

# または .skill パッケージを取得
curl -L -o meeting-minutes-reviewer.skill \
  https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/meeting-minutes-reviewer.skill

# サンプルでレビュー実行
python3 skills/meeting-minutes-reviewer/scripts/review_minutes.py \
  --minutes path/to/minutes.md \
  --output review_report.md
```

---

## 4. 進め方

1. **入力収集** — 議事録ドキュメント、加えて突合したいソース素材（ヒアリングシート、トランスクリプト、過去決定ログ、アジェンダ）
2. **5 ディメンションスコアリング** — 各 0-100 点、重み付きで合計に寄与:
   - 完全性 (25%) — 必須セクション（日付、出席者、アジェンダ、決定、アクション、Next Steps）の有無
   - アクションアイテム (25%) — 各アクションに担当者・期日・曖昧でない説明
   - 決定事項 (20%) — 背景、根拠、代替案検討の記録
   - 整合性 (15%) — ソース素材と一致、自己矛盾なし
   - 明瞭性 (15%) — 曖昧な表現、未定義略語、不明瞭な代名詞をフラグ
3. **指摘** — 重要度（HIGH / MEDIUM / LOW）と修正案つきの構造化リスト
4. **出力** — 機械処理用 JSON ＋ 人間向け Markdown

---

## 5. 使用例

- 議事録ドラフト後、配布前のレビュー
- 他者が作成した議事録の品質保証
- ソース素材（ヒアリングシート、トランスクリプト）との整合性検証
- アクションアイテムが追跡可能な品質基準を満たしているか確認（プロジェクトトラッカー登録前）
- 監査証跡や正式プロジェクト文書化の準備

---

## 6. 出力の読み方

```
スコア:               78/100
  完全性:              85/100  (良好 — 軽微: "Next Steps" セクション薄い)
  アクションアイテム:  65/100  (3 件で担当者欠落、1 件で説明が曖昧)
  決定事項:            80/100
  整合性:              85/100  (ソースと矛盾なし)
  明瞭性:              75/100  (未定義略語 3 件)
指摘:                 7 件 (HIGH 1, MEDIUM 4, LOW 2)
```

Markdown レポートは各指摘に場所（行／セクション）、重要度、具体的な修正案を含めて列挙します。JSON レポートは同じデータを構造化形式で持ち、後段ツール連携に使えます。

---

## 7. ベストプラクティス

- 可能であればソース素材を渡してください — 整合性スコアの精度がぐっと上がります
- HIGH 指摘は配布前ブロッカーとして扱い、MEDIUM は「今版で直す」、LOW は「あれば直す」程度に
- このスキル内で議事録を手書き直さないでください — 生成側ワークフロー（または `meeting-minutes-writer` の自己レビューループ）に戻して再レビュー
- 監査証跡では議事録とレビューレポートを一緒にアーカイブ
- スコアはガイダンスでありゲートではありません。HIGH を直した 60 点のほうが、アクション漏れが埋まった 85 点より良い

---

## 8. 他スキルとの連携

- `meeting-minutes-writer` と組合せ — 生成側で 3 反復セルフレビュー後、本スキルで独立した二次レビュー
- 確定したアクションアイテムを `project-artifact-linker` に渡して WBS／要件にスレッド
- `video2minutes` の後に使い、文字起こし議事録にも同じ QA プロセスを適用
- 関連ワークフローを探す場合は同カテゴリ一覧を参照: [カテゴリ一覧]({{ '/ja/skills/meta/' | relative_url }})
- 日本語スキルカタログ全体: [スキルカタログ]({{ '/ja/skill-catalog/' | relative_url }})

---

## 9. トラブルシューティング

- **スコアが不自然に高い** — ソース素材を渡し忘れていないか確認。なしの場合 整合性は寛容なベースラインに落ちる
- **アクションアイテムで指摘ゼロ** — アクションが平文で書かれていないか確認。パーサは明示的なリスト／テーブル構造を期待
- **「曖昧な表現」が誤検知** — ドメイン固有語彙が明瞭性フラグを誘発することあり、提案として扱う
- **JSON 出力が空** — 入力が有効な Markdown か確認。軽微な issue は許容するが、完全に非 Markdown は不可

---

## 10. リファレンス

**参照ガイド:**

- `skills/meeting-minutes-reviewer/references/review-criteria.md` — 詳細スコア基準と品質標準
- `skills/meeting-minutes-reviewer/references/meeting-minutes-checklist.md` — 議事録チェックリスト

**スクリプト:**

- `skills/meeting-minutes-reviewer/scripts/review_minutes.py` — 5 ディメンション品質分析メインスクリプト
- `skills/meeting-minutes-reviewer/scripts/test_minutes_sample.md` — スモークテスト用サンプル入力

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/meeting-minutes-reviewer/' | relative_url }}) を参照してください。
