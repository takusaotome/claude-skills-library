---
layout: default
title: "Docling Converter"
grand_parent: English
parent: Software Development
nav_order: 16
lang_peer: /ja/skills/dev/docling-converter/
permalink: /en/skills/dev/docling-converter/
---

# Docling Converter
{: .no_toc }

docling CLIを使用したドキュメント変換スキル。PDF、DOCX、PPTX、HTML、画像、Excel等のあらゆるドキュメントをMarkdown、JSON、YAML、HTML、テキストに変換。OCR対応で画像内テキストも抽出可能。Use when converting documents to Markdown or other formats, extracting text from PDFs, processing scanned documents with OCR, or converting office documents.

Argument hint: [file_path] [--to md|json|yaml|html|text] [--ocr-lang ja] [--output output_dir]

{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/docling-converter.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/docling-converter){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

doclingは、あらゆるドキュメント形式をMarkdown、JSON、YAML等に変換するための強力なCLIツールです。PDFのテキスト抽出、スキャンドキュメントのOCR、テーブル構造の認識、音声/動画の文字起こしなど、多様なドキュメント処理に対応しています。

---

## 2. Prerequisites

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

---

## 3. Quick Start

```bash
docling $ARGUMENTS
```

---

## 4. How It Works

1. **入力確認**: ユーザーからファイルパスとオプションを受け取る
2. **引数解析**: ファイルパスとオプション（`--to`, `--ocr-lang`, `--output`等）を解析
3. **デフォルト設定**: `--to` が未指定の場合は `md`（Markdown）を使用
4. **docling実行**: 解析した引数でコマンドを実行
   ```bash
   docling $ARGUMENTS
   ```
5. **結果報告**: 変換完了後、出力ファイルのパスをユーザーに報告

---

## 5. Usage Examples

- PDFをMarkdownやJSONに変換したい
- スキャンされたPDFからテキストを抽出したい（OCR）
- Word、PowerPoint、Excelドキュメントを変換したい
- 画像からテキストを抽出したい
- 複数のドキュメントを一括変換したい
- URLからドキュメントを取得して変換したい

---

## 6. Understanding the Output

このスキルは **ファイル生成型** です。docling CLIを実行し、変換されたファイル（Markdown、JSON、YAML、HTML、テキスト等）を指定ディレクトリに出力します。

- **デフォルト出力**: 入力ファイルと同じディレクトリに `.md` ファイルを生成
- **カスタム出力**: `--output` オプションで出力先を指定可能
- **複数形式**: `--to` を複数指定して複数形式を同時生成可能

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/docling-converter/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: docling_options.md.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.

---

## 10. Reference

**References:**

- `skills/docling-converter/references/docling_options.md`
