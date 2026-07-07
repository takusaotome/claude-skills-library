---
layout: default
title: "Fable Thinking"
grand_parent: 日本語
parent: メタ・品質
nav_order: 14
lang_peer: /en/skills/meta/fable-thinking/
permalink: /ja/skills/meta/fable-thinking/
---

# Fable Thinking
{: .no_toc }

Fable Thinking に関する日本語ガイドです。`skills/fable-thinking/SKILL.md` をもとに、利用開始手順、参照ファイル、補助スクリプトへの入口を日本語で整理しています。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/fable-thinking.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/fable-thinking){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

このページは **Fable Thinking** スキルの日本語サマリーです。
- スキル本体: `skills/fable-thinking/SKILL.md`
- 参照ガイド: 3 件
- 補助スクリプト: なし
- 詳細な背景説明や判断基準は英語版ガイドを参照してください。

---

## 2. 前提条件

- APIキーは不要です
- Python 3.9 以上を推奨します
- 詳細な実行条件は英語版ガイドまたは `SKILL.md` を参照してください。

---

## 3. クイックスタート

思考は8つのフェーズを順に通る。各フェーズにはゲートがあり、満たすまで次に進まない。
フェーズの実行は thinking 内、または下書きメモとして行い、ユーザーへの出力に
フェーズ見出しをそのまま出さない。詳細な質問バンクと実例は
`references/thinking-protocol.md` を読むこと。視点を変えるレンズ集は
`references/lenses.md`、避けるべき失敗パターンは `references/anti-patterns.md` にある。

---

## 4. 進め方

1. `skills/fable-thinking/SKILL.md` を開き、対象タスクと期待する成果物を確認します。
2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。
3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。
4. スキルの手順に沿って対話またはドキュメント作成を進めます。
5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。

---

## 5. リソース

**参照ガイド:**

- `skills/fable-thinking/references/anti-patterns.md`
- `skills/fable-thinking/references/lenses.md`
- `skills/fable-thinking/references/thinking-protocol.md`

---

## 6. 英語版ガイド

- 詳細な背景説明、判断基準、実装例は [English version]({{ '/en/skills/meta/fable-thinking/' | relative_url }}) を参照してください。
