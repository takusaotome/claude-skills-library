---
layout: default
title: "Docling Converter"
grand_parent: 日本語
parent: ソフトウェア開発
nav_order: 16
lang_peer: /en/skills/dev/docling-converter/
permalink: /ja/skills/dev/docling-converter/
---

# Docling Converter
{: .no_toc }

docling CLIを使用したドキュメント変換スキル。PDF、DOCX、PPTX、HTML、画像、Excel等のあらゆるドキュメントをMarkdown、JSON、YAML、HTML、テキストに変換。OCR対応で画像内テキストも抽出可能。Use when converting documents to Markdown or other formats, extracting text from PDFs, processing scanned documents with OCR, or converting office documents.

Argument hint: [file_path] [--to md|json|yaml|html|text] [--ocr-lang ja] [--output output_dir]

{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/docling-converter.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/docling-converter){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

doclingは、あらゆるドキュメント形式をMarkdown、JSON、YAML等に変換するための強力なCLIツールです。PDFのテキスト抽出、スキャンドキュメントのOCR、テーブル構造の認識、音声/動画の文字起こしなど、多様なドキュメント処理に対応しています。

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

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

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

```bash
docling $ARGUMENTS
```

<!-- TODO: 翻訳 -->

---

## 4. 仕組み

<!-- TODO: 翻訳 -->

---

## 5. 使用例

<!-- TODO: 翻訳 -->

---

## 6. 出力の読み方

<!-- TODO: 翻訳 -->

---

## 7. Tips & ベストプラクティス

<!-- TODO: 翻訳 -->

---

## 8. 他スキルとの連携

<!-- TODO: 翻訳 -->

---

## 9. トラブルシューティング

<!-- TODO: 翻訳 -->

---

## 10. リファレンス

**References:**

- `skills/docling-converter/references/docling_options.md`
