---
name: docling-converter
description: |
  docling CLIを使用したドキュメント変換スキル。PDF、DOCX、PPTX、HTML、画像、Excel等のあらゆるドキュメントをMarkdown、JSON、YAML、HTML、テキストに変換。OCR対応で画像内テキストも抽出可能。Use when converting documents to Markdown or other formats, extracting text from PDFs, processing scanned documents with OCR, or converting office documents.

  Argument hint: [file_path] [--to md|json|yaml|html|text] [--ocr-lang ja] [--output output_dir]
allowed-tools: Bash(docling:*), Bash(~/Library/Python/3.12/bin/docling:*)
---

# Docling Converter

## Slash Command Usage

```
/docling-converter <ファイルパス> [オプション]
```

### Examples

```bash
# 基本（Markdownに変換）
/docling-converter document.pdf

# JSON形式で出力
/docling-converter document.pdf --to json

# 日本語OCR付き
/docling-converter scanned.pdf --ocr-lang ja

# 出力先指定
/docling-converter document.pdf --output ./converted/

# 複合オプション
/docling-converter report.pdf --to json --ocr-lang ja --output ./output/
```

## Execution Flow

スラッシュコマンドが実行されたら、以下の手順で処理を行う：

1. **引数を解析**: ファイルパスとオプションを取得
2. **デフォルト設定**: `--to` が未指定の場合は `md`（Markdown）を使用
3. **docling実行**: 以下のコマンドを実行

```bash
docling $ARGUMENTS
```

4. **結果報告**: 変換完了後、出力ファイルのパスをユーザーに報告

## Overview

doclingは、あらゆるドキュメント形式をMarkdown、JSON、YAML等に変換するための強力なCLIツールです。PDFのテキスト抽出、スキャンドキュメントのOCR、テーブル構造の認識、音声/動画の文字起こしなど、多様なドキュメント処理に対応しています。

## When to Use This Skill

このスキルを使用するタイミング：

- PDFをMarkdownやJSONに変換したい
- スキャンされたPDFからテキストを抽出したい（OCR）
- Word、PowerPoint、Excelドキュメントを変換したい
- 画像からテキストを抽出したい
- 複数のドキュメントを一括変換したい
- URLからドキュメントを取得して変換したい
- 会議の音声/動画を文字起こししたい

**Example triggers:**
- "このPDFをMarkdownに変換して"
- "PDFからテキストを抽出して"
- "このスキャンしたドキュメントをOCRで読み取って"
- "WordファイルをJSONに変換して"
- "このフォルダ内のPDFを全部Markdownに変換して"

## Prerequisites

### Installation Check

```bash
# doclingがインストールされているか確認
docling --version

# インストールされていない場合
python3.12 -m pip install --user --break-system-packages docling

# PATHに追加（.zshrcに追記）
echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Quick Start

### Basic Conversion

```bash
# PDF → Markdown（デフォルト）
docling document.pdf

# 出力先を指定
docling document.pdf --output ./output/

# 出力形式を指定
docling document.pdf --to json
docling document.pdf --to yaml
docling document.pdf --to html
docling document.pdf --to text
```

## Supported Formats

### Input Formats (`--from`)

| Format | Extension | Description |
|--------|-----------|-------------|
| pdf | .pdf | PDFドキュメント |
| docx | .docx | Microsoft Word |
| pptx | .pptx | Microsoft PowerPoint |
| xlsx | .xlsx | Microsoft Excel |
| html | .html | Webページ |
| image | .png, .jpg, .tiff | 画像ファイル |
| md | .md | Markdown |
| csv | .csv | CSVファイル |
| asciidoc | .adoc | AsciiDoc |
| audio | .mp3, .wav, .m4a | 音声ファイル |
| vtt | .vtt | WebVTT字幕 |

### Output Formats (`--to`)

| Format | Description |
|--------|-------------|
| md | Markdown（デフォルト） |
| json | JSON形式（構造化データ） |
| yaml | YAML形式 |
| html | HTMLページ |
| html_split_page | ページ分割HTML |
| text | プレーンテキスト |
| doctags | ドキュメントタグ形式 |

## Core Commands

### 1. Basic Conversion

```bash
# PDF → Markdown
docling document.pdf

# 特定の出力形式
docling document.pdf --to json --output ./output/

# 複数の出力形式を同時に生成
docling document.pdf --to md --to json --output ./output/
```

### 2. OCR Processing

```bash
# OCR有効（デフォルト）
docling scanned.pdf

# OCR無効化
docling document.pdf --no-ocr

# 強制OCR（既存テキストを上書き）
docling document.pdf --force-ocr

# OCRエンジンを指定
docling document.pdf --ocr-engine ocrmac    # macOS最適化
docling document.pdf --ocr-engine rapidocr  # 高速
docling document.pdf --ocr-engine tesseract # 多言語対応

# OCR言語を指定
docling document.pdf --ocr-lang ja          # 日本語
docling document.pdf --ocr-lang en,ja       # 英語+日本語
```

### 3. Table Extraction

```bash
# テーブル抽出（デフォルト有効）
docling table-document.pdf

# テーブル抽出無効化
docling document.pdf --no-tables

# テーブルモード（精度優先）
docling document.pdf --table-mode accurate

# テーブルモード（速度優先）
docling document.pdf --table-mode fast
```

### 4. Batch Conversion

```bash
# ディレクトリ内の全ドキュメントを変換
docling ./documents/ --output ./converted/

# 特定形式のみ変換
docling ./documents/ --from pdf --output ./converted/
```

### 5. URL Conversion

```bash
# URLからドキュメントを取得して変換
docling https://example.com/document.pdf

# カスタムヘッダー付き
docling https://example.com/document.pdf --headers '{"Authorization": "Bearer token"}'
```

### 6. Password-Protected PDF

```bash
docling protected.pdf --pdf-password "secret123"
```

### 7. Audio/Video Transcription

```bash
# 音声/動画の文字起こし
docling meeting.mp4 --pipeline asr

# Whisperモデルを指定
docling meeting.mp4 --pipeline asr --asr-model whisper_medium

# macOS最適化（MLXバックエンド）
docling meeting.mp4 --pipeline asr --asr-model whisper_medium_mlx
```

## Advanced Options

### Pipeline Selection

| Pipeline | Use Case |
|----------|----------|
| standard | 通常のドキュメント変換（デフォルト） |
| vlm | 画像認識モデルによる高精度変換 |
| asr | 音声/動画の文字起こし |
| legacy | 旧バージョン互換 |

```bash
# VLMパイプライン（画像が多いドキュメント）
docling image-heavy.pdf --pipeline vlm

# ASRパイプライン（音声/動画）
docling meeting.mp4 --pipeline asr
```

### Image Export Mode

```bash
# 画像を埋め込み（デフォルト）
docling document.pdf --image-export-mode embedded

# 画像を別ファイルとして参照
docling document.pdf --image-export-mode referenced

# 画像位置のみマーク（プレースホルダー）
docling document.pdf --image-export-mode placeholder
```

### Performance Options

```bash
# スレッド数を指定
docling document.pdf --num-threads 8

# デバイスを指定
docling document.pdf --device auto  # 自動選択
docling document.pdf --device cpu   # CPU使用
docling document.pdf --device mps   # Apple Silicon GPU

# タイムアウト設定（秒）
docling large-document.pdf --document-timeout 300

# ページバッチサイズ
docling document.pdf --page-batch-size 8
```

### Debug Options

```bash
# 詳細ログ
docling document.pdf -v      # info
docling document.pdf -vv     # debug

# レイアウト可視化
docling document.pdf --show-layout

# デバッグ出力
docling document.pdf --debug-visualize-cells
docling document.pdf --debug-visualize-ocr
docling document.pdf --debug-visualize-layout
docling document.pdf --debug-visualize-tables
```

## Common Patterns

### Pattern 1: PDF to Markdown with Japanese OCR

```bash
docling japanese-document.pdf \
  --ocr-engine ocrmac \
  --ocr-lang ja \
  --output ./output/
```

### Pattern 2: Batch Convert All PDFs to JSON

```bash
docling ./pdfs/ \
  --from pdf \
  --to json \
  --output ./converted/ \
  --num-threads 4
```

### Pattern 3: High-Quality Table Extraction

```bash
docling financial-report.pdf \
  --table-mode accurate \
  --to json \
  --output ./output/
```

### Pattern 4: Meeting Recording Transcription

```bash
docling meeting-recording.mp4 \
  --pipeline asr \
  --asr-model whisper_medium_mlx \
  --output ./transcripts/
```

### Pattern 5: Scanned Document OCR

```bash
docling scanned-contract.pdf \
  --force-ocr \
  --ocr-engine ocrmac \
  --ocr-lang en,ja \
  --output ./extracted/
```

### Pattern 6: URL Document Conversion

```bash
docling https://arxiv.org/pdf/xxxx.xxxxx.pdf \
  --to md \
  --output ./papers/
```

## Troubleshooting

### Issue: OCR not working

**Solution:**
```bash
# OCRエンジンを確認
docling --help | grep ocr-engine

# macOSの場合、ocrmacが最適
docling document.pdf --ocr-engine ocrmac
```

### Issue: Table extraction inaccurate

**Solution:**
```bash
# 精度優先モードを使用
docling document.pdf --table-mode accurate

# VLMパイプラインを試す
docling document.pdf --pipeline vlm
```

### Issue: Processing timeout

**Solution:**
```bash
# タイムアウトを延長
docling large-document.pdf --document-timeout 600

# ページバッチサイズを小さく
docling document.pdf --page-batch-size 2
```

### Issue: Out of memory

**Solution:**
```bash
# CPUを使用
docling document.pdf --device cpu

# スレッド数を減らす
docling document.pdf --num-threads 2
```

### Issue: Japanese text garbled

**Solution:**
```bash
# 日本語OCRを明示的に指定
docling document.pdf --ocr-lang ja --force-ocr
```

## Resources

### Official Documentation

- [Docling GitHub](https://github.com/DS4SD/docling)
- [Docling Documentation](https://ds4sd.github.io/docling/)

### References

詳細なオプションリファレンスは `references/docling_options.md` を参照してください。

## Tips

1. **macOSユーザー**: `--ocr-engine ocrmac` で最高のOCR性能を得られます
2. **大量ドキュメント**: `--num-threads` でCPUコア数に応じて並列処理
3. **メモリ節約**: `--device cpu` と `--page-batch-size 2` を組み合わせ
4. **日本語ドキュメント**: `--ocr-lang ja` を必ず指定
5. **構造化データ**: テーブルが多いドキュメントは `--to json` が便利
6. **会議録**: `--pipeline asr --asr-model whisper_medium_mlx` がmacOSで高速
