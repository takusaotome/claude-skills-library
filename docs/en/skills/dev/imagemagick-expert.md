---
layout: default
title: "Imagemagick Expert"
grand_parent: English
parent: Software Development
nav_order: 20
lang_peer: /ja/skills/dev/imagemagick-expert/
permalink: /en/skills/dev/imagemagick-expert/
---

# Imagemagick Expert
{: .no_toc }

ImageMagick CLIを使用した画像処理の専門家スキル。フォーマット変換、リサイズ、トリミング、回転、フィルタ適用、アニメーションGIF作成、PDF処理、バッチ処理を支援。Use when processing images via CLI, converting formats, resizing, cropping, applying filters, creating animations, or batch processing images.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/imagemagick-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/imagemagick-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

ImageMagickは画像の作成、編集、合成、変換を行うための強力なCLIツールセットです。200以上の画像フォーマットをサポートし、リサイズ、回転、トリミング、色調整、フィルタ適用、アニメーション作成など幅広い画像処理が可能です。

### Primary Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `magick` | メインコマンド（v7+）、画像変換・処理 | `magick input.png output.jpg` |
| `convert` | 画像変換・処理（レガシー、v6互換） | `convert input.png output.jpg` |
| `identify` | 画像情報の取得 | `identify -verbose image.png` |
| `mogrify` | 画像のインプレース変換 | `mogrify -resize 50% *.jpg` |
| `composite` | 画像の合成 | `composite overlay.png base.png result.png` |
| `montage` | 複数画像のモンタージュ作成 | `montage *.jpg -tile 3x3 montage.jpg` |

---

## 2. Prerequisites

```bash
# Check installation
magick --version

# macOS (Homebrew)
brew install imagemagick

# Linux (Ubuntu/Debian)
sudo apt-get install imagemagick

# Linux (CentOS/RHEL)
sudo yum install ImageMagick
```

---

## 3. Quick Start

1. **Identify Requirements** - Determine the desired operation (convert, resize, filter, etc.) and output format
2. **Select Command** - Choose appropriate ImageMagick command (`magick`, `mogrify`, `identify`, etc.)
3. **Build Command** - Construct command with options and parameters based on Core Operations examples
4. **Execute** - Run the command via Bash tool
5. **Verify Output** - Check the result using `identify` or visual inspection
6. **Iterate** - Adjust parameters if needed based on output quality

---

## 4. How It Works

1. **Identify Requirements** - Determine the desired operation (convert, resize, filter, etc.) and output format
2. **Select Command** - Choose appropriate ImageMagick command (`magick`, `mogrify`, `identify`, etc.)
3. **Build Command** - Construct command with options and parameters based on Core Operations examples
4. **Execute** - Run the command via Bash tool
5. **Verify Output** - Check the result using `identify` or visual inspection
6. **Iterate** - Adjust parameters if needed based on output quality

For batch operations, use `mogrify` for in-place edits or shell loops for custom naming patterns.

---

## 5. Usage Examples

- 画像フォーマットの変換（PNG↔JPEG↔WebP↔GIF等）
- 画像のリサイズ、トリミング、回転
- バッチ処理で複数画像を一括変換
- 画像へのエフェクト・フィルタ適用
- アニメーションGIFの作成・編集
- PDF↔画像の相互変換

---

## 6. Understanding the Output

This skill provides conversational guidance and ImageMagick CLI command examples. No files are automatically generated - you execute the suggested commands via the Bash tool to process images according to your requirements.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/imagemagick-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: batch_processing.md, image_manipulation.md, format_conversion.md.
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

---

## 10. Reference

**References:**

- `skills/imagemagick-expert/references/batch_processing.md`
- `skills/imagemagick-expert/references/format_conversion.md`
- `skills/imagemagick-expert/references/image_manipulation.md`
