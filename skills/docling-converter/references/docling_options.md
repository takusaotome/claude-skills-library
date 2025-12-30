# Docling CLI Options Reference

## Input Formats (`--from`)

| Format | Extensions | Description | Notes |
|--------|------------|-------------|-------|
| pdf | .pdf | PDFドキュメント | テキスト抽出、OCR、テーブル認識対応 |
| docx | .docx | Microsoft Word | スタイル、テーブル、画像を保持 |
| pptx | .pptx | Microsoft PowerPoint | スライドごとにセクション分割 |
| xlsx | .xlsx | Microsoft Excel | シートごとにテーブルとして抽出 |
| html | .html, .htm | Webページ | CSSスタイルを考慮した構造抽出 |
| image | .png, .jpg, .jpeg, .tiff, .bmp | 画像ファイル | OCRでテキスト抽出 |
| md | .md | Markdown | 構造を保持して再変換 |
| csv | .csv | CSVファイル | テーブルとして処理 |
| asciidoc | .adoc, .asciidoc | AsciiDoc | ドキュメント構造を保持 |
| xml_uspto | .xml | USPTO特許XML | 特許文書専用パーサー |
| xml_jats | .xml | JATS学術論文XML | 学術論文専用パーサー |
| mets_gbs | .xml | Google Books METS | デジタル書籍メタデータ |
| json_docling | .json | Docling JSON | 再インポート用 |
| audio | .mp3, .wav, .m4a, .flac | 音声ファイル | ASRパイプラインで文字起こし |
| vtt | .vtt | WebVTT字幕 | タイムスタンプ付きテキスト |

## Output Formats (`--to`)

| Format | Description | Use Case |
|--------|-------------|----------|
| md | Markdown | 汎用ドキュメント、README、ブログ記事 |
| json | JSON形式 | プログラムでの処理、データ分析 |
| yaml | YAML形式 | 設定ファイル、可読性重視 |
| html | HTMLページ | Webでの表示 |
| html_split_page | ページ分割HTML | 大きなドキュメントのWeb表示 |
| text | プレーンテキスト | シンプルなテキスト抽出 |
| doctags | ドキュメントタグ | ML/AI用のアノテーション形式 |

## OCR Engines (`--ocr-engine`)

| Engine | Description | Pros | Cons |
|--------|-------------|------|------|
| auto | 自動選択 | 環境に応じて最適なエンジンを選択 | - |
| ocrmac | macOS Vision Framework | macOSで最高性能、日本語優秀 | macOS専用 |
| rapidocr | ONNX Runtime OCR | 高速、クロスプラットフォーム | 精度はやや劣る |
| easyocr | PyTorch OCR | 多言語対応、高精度 | 速度が遅い、GPU推奨 |
| tesserocr | Tesseract Python binding | 安定、広く使われている | インストールが複雑 |
| tesseract | Tesseract CLI | シンプル | 別途インストール必要 |

### OCR Language Codes (`--ocr-lang`)

| Code | Language |
|------|----------|
| en | English |
| ja | Japanese |
| zh | Chinese |
| ko | Korean |
| de | German |
| fr | French |
| es | Spanish |
| it | Italian |
| pt | Portuguese |
| ru | Russian |
| ar | Arabic |

複数言語: `--ocr-lang en,ja,zh`

## Pipeline Options (`--pipeline`)

| Pipeline | Description | Best For |
|----------|-------------|----------|
| standard | 標準パイプライン | 通常のPDF、Word、PowerPoint |
| vlm | Vision Language Model | 画像が多いドキュメント、複雑なレイアウト |
| asr | Automatic Speech Recognition | 音声/動画ファイルの文字起こし |
| legacy | 旧バージョン互換 | 互換性が必要な場合 |

## VLM Models (`--vlm-model`)

| Model | Description |
|-------|-------------|
| granite_docling | Granite Docling（デフォルト） |
| granite_docling_vllm | Granite Docling (vLLM backend) |
| granite_vision | Granite Vision |
| granite_vision_vllm | Granite Vision (vLLM) |
| granite_vision_ollama | Granite Vision (Ollama) |
| smoldocling | SmolDocling（軽量） |
| smoldocling_vllm | SmolDocling (vLLM) |
| got_ocr_2 | GOT-OCR2 |

## ASR Models (`--asr-model`)

### Standard Models

| Model | Size | Description |
|-------|------|-------------|
| whisper_tiny | 39M | 最小、最速 |
| whisper_base | 74M | 基本モデル |
| whisper_small | 244M | バランス型 |
| whisper_medium | 769M | 高精度（推奨） |
| whisper_large | 1550M | 最高精度 |
| whisper_turbo | - | 高速版 |

### macOS MLX Models (Apple Silicon最適化)

| Model | Description |
|-------|-------------|
| whisper_tiny_mlx | MLXバックエンド、高速 |
| whisper_small_mlx | MLXバックエンド |
| whisper_medium_mlx | MLXバックエンド（推奨） |
| whisper_base_mlx | MLXバックエンド |
| whisper_large_mlx | MLXバックエンド |
| whisper_turbo_mlx | MLXバックエンド |

### Native Models

| Model | Description |
|-------|-------------|
| whisper_tiny_native | ネイティブ実装 |
| whisper_small_native | ネイティブ実装 |
| whisper_medium_native | ネイティブ実装 |
| whisper_base_native | ネイティブ実装 |
| whisper_large_native | ネイティブ実装 |
| whisper_turbo_native | ネイティブ実装 |

## PDF Backend (`--pdf-backend`)

| Backend | Description |
|---------|-------------|
| dlparse_v4 | 最新パーサー（デフォルト） |
| dlparse_v2 | 安定版パーサー |
| dlparse_v1 | 旧バージョン |
| pypdfium2 | pypdfium2ライブラリ |

## Image Export Mode (`--image-export-mode`)

| Mode | Description | Output |
|------|-------------|--------|
| embedded | Base64埋め込み（デフォルト） | 単一ファイル、サイズ大 |
| referenced | 別ファイル参照 | 画像は別ファイル、サイズ小 |
| placeholder | 位置マークのみ | 画像なし、最小サイズ |

## Table Mode (`--table-mode`)

| Mode | Description | Speed | Accuracy |
|------|-------------|-------|----------|
| accurate | 精度優先（デフォルト） | 遅い | 高い |
| fast | 速度優先 | 速い | 標準 |

## Device Options (`--device`)

| Device | Description |
|--------|-------------|
| auto | 自動選択（デフォルト） |
| cpu | CPU使用（メモリ節約） |
| cuda | NVIDIA GPU |
| mps | Apple Silicon GPU |

## Performance Tuning

### Memory-Constrained Environment

```bash
docling document.pdf \
  --device cpu \
  --num-threads 2 \
  --page-batch-size 2
```

### High-Performance Environment

```bash
docling document.pdf \
  --device mps \
  --num-threads 8 \
  --page-batch-size 8
```

### Large Document

```bash
docling large-document.pdf \
  --document-timeout 600 \
  --page-batch-size 4 \
  --abort-on-error
```

## Enrichment Options

| Option | Description |
|--------|-------------|
| --enrich-code | コードブロックの認識・強調 |
| --enrich-formula | 数式の認識・変換 |
| --enrich-picture-classes | 画像の分類 |
| --enrich-picture-description | 画像の説明生成 |

## Debug Visualization

| Option | Description |
|--------|-------------|
| --debug-visualize-cells | PDFセルの可視化 |
| --debug-visualize-ocr | OCR結果の可視化 |
| --debug-visualize-layout | レイアウトクラスターの可視化 |
| --debug-visualize-tables | テーブルセルの可視化 |
| --show-layout | バウンディングボックスを表示 |

## Example Combinations

### Japanese Business Document

```bash
docling business-report.pdf \
  --ocr-engine ocrmac \
  --ocr-lang ja \
  --table-mode accurate \
  --to md \
  --output ./output/
```

### Academic Paper with Formulas

```bash
docling paper.pdf \
  --enrich-formula \
  --to json \
  --output ./output/
```

### Meeting Recording (macOS)

```bash
docling meeting.mp4 \
  --pipeline asr \
  --asr-model whisper_medium_mlx \
  --to md \
  --output ./transcripts/
```

### Batch Processing

```bash
docling ./documents/ \
  --from pdf \
  --to json \
  --num-threads 4 \
  --output ./converted/
```
