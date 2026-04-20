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

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/markdown-to-pdf.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/markdown-to-pdf){: .btn .fs-5 .mb-4 .mb-md-0 }
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

### エンジン比較

| 機能 | fpdf2 (`markdown_to_fpdf.py`) | Playwright (`markdown_to_pdf.py`) |
|:-----|:------------------------------|:----------------------------------|
| **適用領域** | ビジネス文書（見積書、提案書、レポート） | カスタム CSS 付き技術文書 |
| **カバーページ** | YAML フロントマターで内蔵 | 非対応 |
| **テーマ** | navy, gray（ヘッダー/フッター/テーブル） | カスタム CSS ファイル |
| **テーブルスタイリング** | 交互行色、色付きヘッダー、info-table モード | 標準 HTML テーブル |
| **Mermaid 対応** | mmdc で PNG レンダリング後 PDF に埋込 | mmdc または Playwright バックエンドで完全対応 |
| **CJK フォント** | TrueType 優先の自動検出 | ブラウザのシステムフォントを使用 |
| **ページ区切り** | `<!-- pagebreak -->` コメント | CSS `page-break-before` |
| **依存パッケージ** | `fpdf2`, `mistune`, `pyyaml` | `markdown2`, `playwright`, `chromium` |
| **機密マーク** | `--confidential` フラグ | CSS で手動設定 |

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

### Mermaid ダイアグラム対応

両エンジンとも Mermaid コードブロックを画像に変換できます。レンダリングパイプライン:

1. Markdown ソース内の Mermaid コードブロック（` ```mermaid `）を検出
2. 各ブロックを `mermaid_renderer.py` で PNG（Playwright モードでは SVG）にレンダリング
3. レンダリングされた画像がコードブロックに置き換わり、最終 PDF に埋め込み
4. SHA256 ベースのキャッシュにより、変更のないダイアグラムの再レンダリングを回避

対応する Mermaid ダイアグラムの種類: フローチャート、シーケンス図、ガントチャート、クラス図、状態遷移図、ER 図、円グラフ。変換前に [mermaid.live](https://mermaid.live/) でプレビューを推奨します。

**strict モード vs. permissive モード**: デフォルトでは Mermaid の構文エラーで PDF 生成が停止します。`--no-strict-mermaid` を指定すると、エラー時にコードブロックをそのまま表示するフォールバック動作に切り替わります。

### ページ区切りと特殊構文

| 構文 | モード | 効果 |
|:-----|:-------|:-----|
| `<!-- pagebreak -->` | fpdf2 | ページ区切りを挿入 |
| `<!-- info-table -->` | fpdf2 | 次のテーブルをキーバリュー info-table スタイルで表示 |
| `<!-- col-widths: 10,45,45 -->` | fpdf2 | 次のテーブルの列幅を指定（比率・%・mm を受付。ページ幅に正規化） |
| `---` | fpdf2 | 水平線 |
| ` ```mermaid ` | 両方 | Mermaid ダイアグラムを画像としてレンダリング |

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

### 例 4: 社内レポート（gray テーマ）

```
この月次運用レポートを PDF に変換してください。
gray テーマ（社内文書）を使用し、セクション間にページ区切りを入れてください。
カバーページは不要です。
```

`markdown_to_fpdf.py --theme gray --no-cover` を実行し、`<!-- pagebreak -->` マーカーでセクションを区切り、gray テーマで社内文書スタイリングを適用します。

---

## トラブルシューティング

### fpdf2 モードで CJK 文字が文字化けする

**症状**: 日本語・中国語・韓国語の文字が PDF 上で四角や意味不明な記号として表示される。テキスト抽出ツールでは正しい文字が得られる場合がある。

**解決策**: CFF アウトラインフォント（macOS の Hiragino Sans など）が原因です。TrueType CJK フォントをインストールしてください: macOS は `brew install --cask font-udev-gothic`、Linux は `sudo apt install fonts-noto-cjk`。stderr に "Warning: Using CFF-outline font" が出力されていないか確認してください。インストール後に再変換し、CFF 警告が表示されないことを確認します。

### strict モードで Mermaid 変換が失敗する

**症状**: Mermaid の構文エラーやツール不足により PDF 生成が途中で停止する。

**解決策**: 出力のエラーカテゴリを確認してください。`mmdc_not_found` の場合は mermaid-cli をインストール: `npm install -g @mermaid-js/mermaid-cli`。`syntax_error` の場合は [mermaid.live](https://mermaid.live/) でダイアグラムを検証。`browser_launch_failed` の場合は Playwright をインストール: `pip install playwright && playwright install chromium`。エラー時にコードブロック表示へフォールバックさせるには `--no-strict-mermaid` を追加してください。

### リスト項目内のテーブルが表示されない

**症状**: リスト項目（`- item`）やブロック引用（`>`）の下にインデントされた Markdown テーブルが PDF に出力されない。

**解決策**: fpdf2 モードの mistune パーサーはインデントされたテーブルを認識できません。テーブルをトップレベル（インデントなし）に移動してください。これは fpdf2 モードの既知の制限事項です。

---

## ヒントとベストプラクティス

- **ビジネス文書**: fpdf2 モードで YAML フロントマターを使用し、カバーページとテーマ付きスタイリングを適用
- **ダイアグラム付き技術文書**: Playwright モードで `--image-format svg` を指定し、高品質な出力を実現
- **ページ区切り**: fpdf2 モードでは `<!-- pagebreak -->` でセクション間を区切る
- **キーバリューテーブル**: fpdf2 モードではテーブルの前に `<!-- info-table -->` を記述して info-table スタイルを適用
- **テーブル列幅の制御**: `<!-- col-widths: 10,45,45 -->` をテーブル直前に置くと、比率／％／mm で列幅を指定可能（自動幅計算を上書き）
- **CJK フォント**: TrueType CJK フォント（UDEVGothic または Noto Sans JP）をインストールして文字化けを防止。Hiragino などの CFF アウトラインフォントはレンダリングの問題を引き起こす可能性あり。
- **Mermaid プレビュー**: 変換前に [mermaid.live](https://mermaid.live/) でダイアグラムをプレビュー
- **テーマ**: クライアント向け文書は `navy`、社内文書は `gray`

---

## 関連スキル

- [operations-manual-creator]({{ '/ja/skills/ops/operations-manual-creator/' | relative_url }}) -- 操作マニュアルを作成し、本スキルで PDF に変換
- **technical-spec-writer** -- Mermaid ダイアグラム付き技術仕様書の作成
- **presentation-reviewer** -- PDF 変換前のプレゼンテーションレビュー
