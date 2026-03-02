---
layout: default
title: 日本語
nav_order: 2
has_children: true
lang_peer: /en/
permalink: /ja/
---

<div class="hero">
  <div class="hero-tagline">Claude Skills Library</div>
  <p class="hero-mantra">あらゆる業務領域をカバーする 78 のプロフェッショナルスキル</p>
</div>

## Claude Skills Library とは

Claude Skills Library は、[Claude Code](https://docs.anthropic.com/en/docs/claude-code) の機能を拡張する **78 のすぐに使えるスキル** を収録したオープンソースコレクションです。各スキルは専門知識・ワークフロー・自動化スクリプトを備えた自己完結型パッケージで、数秒でインストールできます。

コードレビューやデータサイエンスから、コンプライアンス支援、財務分析、プロジェクト管理まで幅広い領域をカバー。個人開発者からエンタープライズチームまで、業務を加速するスキルが見つかります。

---

## スキルカテゴリ

<div class="category-cards">

  <a href="{{ '/ja/skill-catalog/#ソフトウェア開発--it' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>ソフトウェア開発 & IT</h3>
    <p>16 スキル -- コードレビュー、TDD、データサイエンス、クラウド CLI、デバッグなど。</p>
  </a>

  <a href="{{ '/ja/skill-catalog/#プロジェクト--ビジネス' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>プロジェクト & ビジネス</h3>
    <p>18 スキル -- 戦略立案、M&A、価格戦略、プロジェクト計画、管理会計。</p>
  </a>

  <a href="{{ '/ja/skill-catalog/#オペレーション--ドキュメンテーション' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>オペレーション & ドキュメンテーション</h3>
    <p>10 スキル -- 技術文書、プレゼン、PDF 変換、議事録作成。</p>
  </a>

  <a href="{{ '/ja/skill-catalog/#コンプライアンス-財務--ガバナンス' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>コンプライアンス、財務 & ガバナンス</h3>
    <p>12 スキル -- SOX、ISO、PCI DSS、ESG、監査、財務分析。</p>
  </a>

  <a href="{{ '/ja/skill-catalog/#qa-テスト--ベンダー管理' | relative_url }}" class="category-card" style="text-decoration:none;color:inherit;">
    <h3>QA、テスト & ベンダー管理</h3>
    <p>9 スキル -- UAT、移行検証、ベンダー見積、ヘルプデスク、CX 分析。</p>
  </a>

</div>

---

## 3 ステップで始める

<div class="steps">

  <div class="step">
    <div class="step-number">1</div>
    <h4>Claude Code をインストール</h4>
    <p>Claude Code CLI をセットアップします。</p>
  </div>

  <div class="step">
    <div class="step-number">2</div>
    <h4>スキルをコピー</h4>
    <p><code>cp -r ./skills/skill-name ~/.claude/skills/</code></p>
  </div>

  <div class="step">
    <div class="step-number">3</div>
    <h4>使う</h4>
    <p>Claude はインストール済みスキルを自動検出し、関連するタスクで適用します。</p>
  </div>

</div>

[はじめにガイド]({{ '/ja/getting-started/' | relative_url }}){: .btn .btn-primary }

---

## 注目スキル

| スキル | カテゴリ | 特徴 |
|:------|:---------|:-----|
| [critical-code-reviewer]({{ '/ja/skills/dev/critical-code-reviewer/' | relative_url }}) | 開発 | 4 ペルソナ並列コードレビュー |
| [data-scientist]({{ '/ja/skills/dev/data-scientist/' | relative_url }}) | 開発 | 自動 EDA、ML モデル比較、時系列分析 |
| [project-plan-creator]({{ '/ja/skills/management/project-plan-creator/' | relative_url }}) | PM | PMBOK 準拠チャーター、WBS、ガント、RACI |
| [financial-analyst]({{ '/ja/skills/finance/financial-analyst/' | relative_url }}) | 財務 | DCF、NPV/IRR、類似企業比較分析 |
| [markdown-to-pdf]({{ '/ja/skills/ops/markdown-to-pdf/' | relative_url }}) | Ops | Mermaid 対応プロフェッショナル PDF |

[全 78 スキルを見る]({{ '/ja/skill-catalog/' | relative_url }}){: .btn }
