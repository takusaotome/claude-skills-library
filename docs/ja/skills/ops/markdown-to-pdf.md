---
layout: default
title: Markdown to PDF
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 3
lang_peer: /en/skills/ops/markdown-to-pdf/
permalink: /ja/skills/ops/markdown-to-pdf/
---

# Markdown to PDF
{: .no_toc }

2 つのレンダリングエンジンで Markdown をプロフェッショナル PDF に変換。Playwright は技術文書向け、fpdf2 はビジネス文書向け。
{: .fs-6 .fw-300 }

<span class="badge badge-scripts">Python スクリプト</span>
<span class="badge badge-workflow">ワークフロー</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Markdown to PDF は、Markdown から PDF への変換に 2 つのレンダリングエンジンを提供します:

1. **Playwright モード** -- HTML/CSS ベースのレンダリング。Mermaid ダイアグラム対応。カスタム CSS スタイリングが可能な技術文書に最適。
2. **fpdf2 モード** -- カバーページ、テーマ付きヘッダー/フッター、スタイル付きテーブル、CJK フォント対応のプロフェッショナル PDF 生成。見積書、提案書、レポートなどのビジネス文書に最適。

両モードとも Mermaid ダイアグラム変換、コードブロック、標準 Markdown フォーマットに対応しています。

---

## こんなときに使う

- Markdown ファイルを PDF に変換する
- カバーページ付きのプロフェッショナルなビジネス文書（見積書、提案書、レポート）を作成する
- Mermaid ダイアグラムを含む技術文書を PDF に変換する
- コーポレートスタイリング（navy / gray テーマ）でテーマ付き PDF を生成する
- Mermaid ダイアグラムを PNG/SVG 画像として書き出す

---

## 前提条件

- **Claude Code** がインストール済みであること
- **markdown-to-pdf** スキルがインストール済み（`cp -r ./skills/markdown-to-pdf ~/.claude/skills/`）

**fpdf2 モード（ビジネス PDF）:**
```bash
pip install fpdf2 mistune pyyaml
```

**Playwright モード（Mermaid 付き技術文書）:**
```bash
pip install markdown2 playwright
playwright install chromium
npm install -g @mermaid-js/mermaid-cli
```

---

## 仕組み

### モードの選び方

| 要件 | モード | スクリプト |
|:-----|:-------|:-----------|
| カバーページ、プロフェッショナルスタイリング | fpdf2 | `markdown_to_fpdf.py` |
| ビジネス文書（見積書、レポート） | fpdf2 | `markdown_to_fpdf.py` |
| テーマ付きヘッダー/フッター | fpdf2 | `markdown_to_fpdf.py` |
| スタイル付きテーブル（交互行色） | fpdf2 | `markdown_to_fpdf.py` |
| カスタム CSS 付き技術文書 | Playwright | `markdown_to_pdf.py` |
| Mermaid ダイアグラムが主要コンテンツ | Playwright | `markdown_to_pdf.py` |

### fpdf2 モードのワークフロー

1. Markdown ファイルに YAML フロントマター（タイトル、サブタイトル、テーマなど）を追加
2. 変換を実行:
   ```bash
   python scripts/markdown_to_fpdf.py input.md output.pdf --theme navy
   ```
3. 出力 PDF を確認

### Playwright モードのワークフロー

1. 変換を実行:
   ```bash
   python scripts/markdown_to_pdf.py input.md output.pdf
   ```
2. Mermaid コードブロックは自動的に画像に変換
3. 出力 PDF を確認

---

## 使い方の例

### 例 1: プロフェッショナルな見積書

```
この見積書をカバーページ付きのプロフェッショナル PDF に変換してください。
navy テーマで、機密扱いにしてください。
```

フロントマターを追加し、`markdown_to_fpdf.py --theme navy --confidential` を実行して洗練されたビジネス PDF を生成します。

### 例 2: ダイアグラム付き技術文書

```
API 設計ドキュメントを PDF に変換してください。
Mermaid のシーケンスダイアグラムが複数含まれています。
```

高品質なダイアグラムレンダリングのため、Playwright モード + SVG フォーマットを使用します。

### 例 3: Mermaid ダイアグラムの書き出し

```
この Mermaid フローチャートを PNG 画像として書き出してください:

graph TD
    A[開始] --> B{判断}
    B -->|はい| C[実行]
    B -->|いいえ| D[終了]
```

`mermaid_to_image.py` を使用してスタンドアロン PNG を生成します。

---

## ヒントとベストプラクティス

- **ビジネス文書**: fpdf2 モードで YAML フロントマターを使用し、カバーページとテーマ付きスタイリングを適用
- **ダイアグラム付き技術文書**: Playwright モードで `--image-format svg` を指定し、高品質な出力を実現
- **ページ区切り**: fpdf2 モードでは `<!-- pagebreak -->` でセクション間を区切る
- **キーバリューテーブル**: fpdf2 モードではテーブルの前に `<!-- info-table -->` を記述して info-table スタイルを適用
- **CJK フォント**: TrueType CJK フォント（UDEVGothic または Noto Sans JP）をインストールして文字化けを防止。Hiragino などの CFF アウトラインフォントはレンダリングの問題を引き起こす可能性あり。
- **Mermaid プレビュー**: 変換前に [mermaid.live](https://mermaid.live/) でダイアグラムをプレビュー
- **テーマ**: クライアント向け文書は `navy`、社内文書は `gray`

---

## 関連スキル

- [operations-manual-creator]({{ '/ja/skills/ops/operations-manual-creator/' | relative_url }}) -- 操作マニュアルを作成し、本スキルで PDF に変換
- [technical-spec-writer]({{ '/ja/skills/ops/technical-spec-writer/' | relative_url }}) -- Mermaid ダイアグラム付き技術仕様書の作成
- [presentation-reviewer]({{ '/ja/skills/ops/presentation-reviewer/' | relative_url }}) -- PDF 変換前のプレゼンテーションレビュー
