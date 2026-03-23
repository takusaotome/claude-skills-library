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

<!-- TODO: Describe the internal pipeline/algorithm -->

---

## 5. Usage Examples

<!-- TODO: Add 4-6 real-world usage scenarios -->

---

## 6. Understanding the Output

<!-- TODO: Describe output file format and field definitions -->

---

## 7. Tips & Best Practices

<!-- TODO: Add expert advice for getting the most value -->

---

## 8. Combining with Other Skills

<!-- TODO: Add multi-skill workflow table -->

---

## 9. Troubleshooting

<!-- TODO: Add common errors and fixes -->

---

## 10. Reference

**References:**

- `skills/docling-converter/references/docling_options.md`
