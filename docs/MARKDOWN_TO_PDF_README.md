# Markdown to PDF スキル - 使用ガイド

## 概要

**markdown-to-pdf**スキルは、Markdownドキュメントを高品質なPDFに変換するためのツールです。2つのレンダリングモードを提供します：

1. **Playwrightモード** — HTML/CSSベースのPDF変換。Mermaid図のサポート付き。技術文書に最適。
2. **fpdf2モード** — プロフェッショナルなPDF生成。カバーページ、テーマ、スタイル付きテーブル、CJKフォント対応。ビジネス文書（見積書、提案書、レポート）に最適。

## スキルの配置場所

- **パッケージファイル**: `skill-packages/markdown-to-pdf.skill`
- **インストール済み**: `~/.claude/skills/markdown-to-pdf/`

## 機能

### 1. Markdown to PDF変換（Playwrightモード）
- Markdownファイル内のMermaidコードブロックを自動検出
- 各Mermaid図を高品質な画像に変換
- 画像を埋め込んだPDFを生成
- カスタムCSSスタイルのサポート

### 2. プロフェッショナルPDF生成（fpdf2モード）
- YAMLフロントマターによるメタデータ管理
- カバーページ自動生成
- テーマ対応（navy / gray）
- プロフェッショナルなテーブルスタイル（交互行色、ヘッダー色）
- CJKフォント自動探索（macOS / Windows / Linux）

### 3. Mermaid to 画像変換
- Mermaid図をPNG/SVG形式で出力
- テーマ選択（default, forest, dark, neutral）
- カスタム背景色と画像サイズ

## 前提条件

### システム要件

**✅ クロスプラットフォーム対応**
- **macOS** ✅ 完全対応
- **Windows** ✅ 完全対応
- **Linux** ✅ 完全対応

### 必須依存関係

**macOS / Linux:**
```bash
# Python依存関係（必須）
pip3 install markdown2 playwright

# Chromiumブラウザのインストール
python3 -m playwright install chromium

# Mermaid変換用（どちらか一方を選択）
# オプション1: mermaid-cli（高速変換、推奨）
npm install -g @mermaid-js/mermaid-cli

# オプション2: Playwright（上記で既にインストール済み）
# 追加のインストールは不要
```

**Windows (PowerShell):**
```powershell
# Python依存関係（必須）
pip install markdown2 playwright

# Chromiumブラウザのインストール
python -m playwright install chromium

# Mermaid変換用（どちらか一方を選択）
# オプション1: mermaid-cli（高速変換、推奨）
npm install -g @mermaid-js/mermaid-cli

# オプション2: Playwright（上記で既にインストール済み）
# 追加のインストールは不要
```

### システム依存関係

**✅ 不要！** このスキルはPythonパッケージのみで動作し、システムライブラリ（pango/cairo等）は一切不要です。Windows、macOS、Linuxで全く同じ手順でインストールできます。

## 使用方法

### fpdf2モード（プロフェッショナルPDF）

#### 依存関係

```bash
pip install fpdf2 mistune pyyaml
```

#### 基本的な使い方

```bash
# 基本変換
python3 scripts/markdown_to_fpdf.py input.md output.pdf

# テーマ指定
python3 scripts/markdown_to_fpdf.py input.md output.pdf --theme navy
python3 scripts/markdown_to_fpdf.py input.md output.pdf --theme gray --confidential

# カバーページなし
python3 scripts/markdown_to_fpdf.py input.md output.pdf --no-cover

# フォント手動指定
python3 scripts/markdown_to_fpdf.py input.md output.pdf --font-regular /path/to/font.ttc --font-bold /path/to/bold.ttc
```

#### YAMLフロントマター

Markdownファイルの先頭にYAMLフロントマターを追加して、カバーページやテーマを制御できます：

```yaml
---
title: 御見積書
subtitle: AI プラットフォーム PoC サポート
theme: navy
document_number: FSAI-2026-0001
date: 2026年2月17日
author: 山田 太郎
company: Example Corp.
recipient: Client Inc.
confidential: false
cover: true
---
```

詳しいフィールド仕様は `references/fpdf_styling_guide.md` を参照してください。

### Playwrightモード（Mermaid図対応PDF）

#### 基本的な使い方

##### 1. Markdown → PDF変換

**macOS / Linux:**
```bash
# スキルディレクトリに移動
cd ~/.claude/skills/markdown-to-pdf

# 基本的な変換（PNG形式）
python3 scripts/markdown_to_pdf.py sample_design_document.md output.pdf

# SVG形式で変換（推奨：最高品質）
python3 scripts/markdown_to_pdf.py sample_design_document.md output.pdf --image-format svg

# テーマを指定
python3 scripts/markdown_to_pdf.py sample_design_document.md output.pdf --theme dark --image-format svg

# カスタムCSSを適用
python3 scripts/markdown_to_pdf.py sample_design_document.md output.pdf --css custom.css --image-format svg
```

**Windows (PowerShell):**
```powershell
# スキルディレクトリに移動
cd $env:USERPROFILE\.claude\skills\markdown-to-pdf

# 基本的な変換（PNG形式）
python scripts\markdown_to_pdf.py sample_design_document.md output.pdf

# SVG形式で変換（推奨：最高品質）
python scripts\markdown_to_pdf.py sample_design_document.md output.pdf --image-format svg

# テーマを指定
python scripts\markdown_to_pdf.py sample_design_document.md output.pdf --theme dark --image-format svg

# カスタムCSSを適用
python scripts\markdown_to_pdf.py sample_design_document.md output.pdf --css custom.css --image-format svg
```

#### 2. Mermaid図 → 画像変換

**macOS / Linux:**
```bash
# .mmdファイルからPNG生成
python3 scripts/mermaid_to_image.py diagram.mmd diagram.png

# SVG形式で出力
python3 scripts/mermaid_to_image.py diagram.mmd diagram.svg --format svg

# コード文字列から直接変換
python3 scripts/mermaid_to_image.py --code "graph TD; A-->B" output.png

# デフォルトで高解像度（1600x1200）
python3 scripts/mermaid_to_image.py diagram.mmd output.png
```

**Windows (PowerShell):**
```powershell
# .mmdファイルからPNG生成
python scripts\mermaid_to_image.py diagram.mmd diagram.png

# SVG形式で出力
python scripts\mermaid_to_image.py diagram.mmd diagram.svg --format svg

# コード文字列から直接変換
python scripts\mermaid_to_image.py --code "graph TD; A-->B" output.png

# デフォルトで高解像度（1600x1200）
python scripts\mermaid_to_image.py diagram.mmd output.png
```

## サンプルファイル

### sample_design_document.md

プロジェクト内の`sample_design_document.md`には、以下のMermaid図が含まれています：

1. **システムアーキテクチャ図** - クライアント/サーバー/データ層の構成
2. **シーケンス図** - ユーザーとシステム間のデータフロー
3. **ER図** - データベーススキーマとリレーション
4. **ステート図** - リード管理のステート遷移
5. **フロー図** - 商談管理プロセス
6. **アクセス制御図** - セキュリティ設計
7. **Ganttチャート** - プロジェクトスケジュール
8. **円グラフ** - 課題優先度分布

### 変換例

```bash
# サンプル文書をPDFに変換
cd ~/.claude/skills/markdown-to-pdf
python scripts/markdown_to_pdf.py \
    ~/sample_design_document.md \
    ~/design_document.pdf

# Dark テーマで変換
python scripts/markdown_to_pdf.py \
    ~/sample_design_document.md \
    ~/design_document_dark.pdf \
    --theme dark

# 任意のMarkdownファイルを変換
python scripts/markdown_to_pdf.py \
    /path/to/your/document.md \
    /path/to/output.pdf
```

## 設定オプション

### Markdown to PDF

| オプション | 値 | 説明 |
|-----------|-----|------|
| `--theme` | default, forest, dark, neutral | Mermaid図のテーマ |
| `--background` | white, transparent, #color | 背景色 |
| `--image-format` | png, svg | 図の画像形式 |
| `--css` | ファイルパス | カスタムCSSファイル |
| `--keep-temp` | - | 一時ファイルを保持（デバッグ用） |

### Mermaid to Image

| オプション | 値 | 説明 |
|-----------|-----|------|
| `--format` | png, svg | 出力形式 |
| `--theme` | default, forest, dark, neutral | テーマ |
| `--background` | white, transparent, #color | 背景色 |
| `--width` | 数値（ピクセル） | 画像幅（PNG用、デフォルト: 1600） |
| `--height` | 数値（ピクセル） | 画像高さ（PNG用、デフォルト: 1200） |
| `--use-playwright` | - | Playwrightを強制使用 |

**注意:** デフォルトの解像度は1600x1200に設定されており、小さな文字も読みやすい高品質な画像を生成します。

## トラブルシューティング

### 問題: Mermaid図が変換されない

**原因:**
- mermaid-cliまたはPlaywrightがインストールされていない
- Node.jsがインストールされていない

**解決策:**
```bash
# mermaid-cliをインストール
npm install -g @mermaid-js/mermaid-cli

# または Playwrightをインストール
pip install playwright
playwright install chromium
```

### 問題: PDF生成に失敗する

**原因:**
- Playwrightがインストールされていない
- Chromiumブラウザがインストールされていない

**解決策:**
```bash
# Playwrightをインストール
pip install playwright

# Chromiumブラウザをインストール
playwright install chromium
```

### 問題: 図のテキストが読みにくい、または重なる

**✅ 推奨解決策: SVG形式を使用**
```bash
# SVG形式で変換（ベクター形式、無限スケール可能、最高品質）
python scripts/markdown_to_pdf.py input.md output.pdf --image-format svg
```

**PNG形式を使う場合の高解像度オプション:**
デフォルト解像度: 3200x2400（高品質）

さらに高解像度が必要な場合:
```bash
# 超高解像度で変換（4800x3600）
python scripts/mermaid_to_image.py diagram.mmd output.png --width 4800 --height 3600
```

**その他の解決策:**
1. **SVG形式を使用（最優先）**: `--image-format svg` - 完全に鮮明、拡大しても劣化しない
2. ラベルを短くする
3. 図の向きを変更する（TD → LR）
4. フォントサイズを調整（Mermaidコード内で指定）

## 高度な使用例

### 複数ファイルの一括変換

```bash
# カレントディレクトリの全Markdownファイルを変換
for file in *.md; do
    python scripts/markdown_to_pdf.py "$file" "${file%.md}.pdf"
done
```

### カスタムスタイルの適用

```css
/* custom.css */
body {
    font-family: "Hiragino Sans", "Yu Gothic", sans-serif;
    font-size: 11pt;
}

h1 {
    color: #003366;
    border-bottom: 3px solid #003366;
}

img {
    border: 1px solid #ddd;
    padding: 10px;
    background: #fafafa;
}
```

```bash
python scripts/markdown_to_pdf.py input.md output.pdf --css custom.css
```

### SVG形式での最高品質出力（推奨）

```bash
# すべての図をSVGとして出力（ベクター形式、無限スケール可能）
python scripts/markdown_to_pdf.py input.md output.pdf --image-format svg

# SVGとdarkテーマを組み合わせ
python scripts/markdown_to_pdf.py input.md output.pdf --image-format svg --theme dark

# SVGとカスタムCSS
python scripts/markdown_to_pdf.py input.md output.pdf --image-format svg --css custom.css
```

**SVG形式の利点:**
- テキストが完全に鮮明（拡大しても劣化しない）
- エッジがシャープで美しい
- ファイルサイズが小さい
- PDF印刷時も高品質を維持

## 参考資料

### スキル内リソース
- `SKILL.md` - スキルの詳細な使用方法
- `references/mermaid_guide.md` - Mermaid図の完全ガイド
- `references/fpdf_styling_guide.md` - fpdf2スタイリングガイド
- `scripts/markdown_to_fpdf.py` - プロフェッショナルPDF変換（fpdf2）
- `scripts/markdown_to_pdf.py` - Mermaid対応PDF変換（Playwright）
- `scripts/mermaid_to_image.py` - 画像変換スクリプト
- `scripts/themes.py` - テーマ定義 + フォント探索
- `assets/sample_frontmatter.yaml` - フロントマターサンプル

### 外部リンク
- [Mermaid公式ドキュメント](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/) - 図のプレビューとテスト
- [WeasyPrint ドキュメント](https://doc.courtbouillon.org/weasyprint/)

## よくある質問（FAQ）

### Q: どのMermaid図がサポートされていますか？
A: すべてのMermaid図タイプをサポートしています（フローチャート、シーケンス図、ER図、Ganttチャート、クラス図、ステート図、パイチャート、Git graphなど）。

### Q: 日本語は正しく表示されますか？
A: はい、UTF-8エンコーディングで日本語を完全サポートしています。

### Q: PDFのファイルサイズを小さくするには？
A: `--image-format svg`を使用すると、通常PNGよりもファイルサイズが小さくなります。

### Q: SVG形式とPNG形式、どちらを使うべきですか？
A: **SVG形式を強く推奨**します。SVGはベクター形式のため：
- テキストが完全に鮮明（拡大しても劣化しない）
- ファイルサイズが小さい
- PDF内でも高品質を維持
PNG形式は互換性は高いですが、ビットマップのため拡大すると品質が劣化します。

### Q: 商用プロジェクトで使用できますか？
A: はい、スクリプトは自由に使用できます。ただし、依存ライブラリ（mermaid-cli、WeasyPrint等）のライセンスを確認してください。

## サポート

問題が発生した場合は、以下を確認してください：

1. **依存関係のインストール** - すべての必須ライブラリがインストールされているか
2. **Mermaid構文** - [mermaid.live](https://mermaid.live/)で図の構文をテスト
3. **一時ファイル** - `--keep-temp`オプションで中間ファイルを確認

---

**バージョン**: 2.0
**最終更新**: 2026-02-19
**作成者**: Claude Code + skill-creator
