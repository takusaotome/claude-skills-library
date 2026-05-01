---
layout: default
title: "Design Thinking"
grand_parent: English
parent: Project & Business
nav_order: 11
lang_peer: /ja/skills/management/design-thinking/
permalink: /en/skills/management/design-thinking/
---

# Design Thinking
{: .no_toc }

人間中心のイノベーション・問題解決スキル（Design Thinking）。Stanford d.school / IDEOが体系化した
5フェーズ（共感→定義→発想→試作→検証）で、曖昧な課題を具体的な解決策に変換する。
Use when: 新サービス企画、UX改善、顧客理解、問題の再定義、イノベーション創出、ワークショップ設計。
Triggers: "ペルソナを作りたい", "顧客の課題を理解したい", "アイデア出しをしたい",
"ジャーニーマップを作成", "プロトタイプを作りたい", "design thinking", "HMW", "エンパシーマップ"

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/design-thinking.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/design-thinking){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Design Thinking（デザイン思考）は、デザイナーの思考プロセスを体系化した問題解決手法です。
「ユーザーにとって本当に価値のあるもの」を生み出すために、共感から始まり、反復的に解決策を磨いていきます。

**核心原則:**
- **Human-Centered（人間中心）**: ユーザーの真のニーズから出発する
- **Iterative（反復的）**: 失敗から学び、素早く改善する
- **Bias Toward Action（行動重視）**: 考えるより作る、作って学ぶ
- **Radical Collaboration（徹底的な協働）**: 多様な視点を統合する

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Design Thinking Process                         │
│                                                                     │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   │          │   │          │   │          │   │          │   │          │
│   │ EMPATHIZE│──▶│  DEFINE  │──▶│  IDEATE  │──▶│PROTOTYPE │──▶│   TEST   │
│   │   共感   │   │   定義   │   │   発想   │   │   試作   │   │   検証   │
│   │          │   │          │   │          │   │          │   │          │
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
│        │                                                           │
│        └───────────────────── 反復 ─────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────┘
```

---

---

## 2. Prerequisites

- **必須ではない**: このスキルはナレッジベースのガイダンススキルのため、特別な前提条件はありません
- **推奨環境**: チームワークショップの場合、ホワイトボードや付箋などの可視化ツールがあると効果的

---

---

## 3. Quick Start

1. **コンテキスト確認**: ユーザーの課題・状況を把握する
2. **適切なフェーズ特定**: 5フェーズ（共感→定義→発想→試作→検証）のどこにいるかを判断
3. **手法提案**: 該当フェーズに適した手法・テンプレートを提案
4. **対話的ガイダンス**: 質問に回答しながら、次のステップへ導く
5. **イテレーション**: 必要に応じて前のフェーズに戻り、反復的に改善

---

## 4. How It Works

1. **コンテキスト確認**: ユーザーの課題・状況を把握する
2. **適切なフェーズ特定**: 5フェーズ（共感→定義→発想→試作→検証）のどこにいるかを判断
3. **手法提案**: 該当フェーズに適した手法・テンプレートを提案
4. **対話的ガイダンス**: 質問に回答しながら、次のステップへ導く
5. **イテレーション**: 必要に応じて前のフェーズに戻り、反復的に改善

---

## 5. Usage Examples

- **新サービス・新製品の企画**
- 「顧客が本当に求めているものは何か」を探索したい
- 既存の解決策では満足されていない課題がある
- **顧客体験（CX/UX）の改善**
- カスタマージャーニーを可視化したい
- タッチポイントごとのペインポイントを特定したい

---

## 6. Understanding the Output

**このスキルの出力形式**: 対話的なガイダンス（Conversational Guidance）

- ファイル生成は行わず、会話を通じて Design Thinking の各フェーズをガイドします
- 必要に応じて、`assets/` 内のテンプレートを参照し、ユーザーが自身でドキュメントを作成できるよう支援します
- ワークショップ設計、手法選択、フィードバック解釈などのアドバイスを提供します

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/design-thinking/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: empathize_methods.md, define_methods.md, test_methods.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/management/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.

---

## 10. Reference

**References:**

- `skills/design-thinking/references/define_methods.md`
- `skills/design-thinking/references/design_thinking_overview.md`
- `skills/design-thinking/references/empathize_methods.md`
- `skills/design-thinking/references/ideate_methods.md`
- `skills/design-thinking/references/prototype_methods.md`
- `skills/design-thinking/references/test_methods.md`
