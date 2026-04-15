---
layout: default
title: "AWS CLI Expert"
grand_parent: English
parent: Software Development
nav_order: 12
lang_peer: /ja/skills/dev/aws-cli-expert/
permalink: /en/skills/dev/aws-cli-expert/
---

# AWS CLI Expert
{: .no_toc }

AWS CLIの専門家スキル。EC2, S3, IAM, Lambda, RDS, ECS等の主要サービスのCLI操作を支援。IAMポリシー設計、クロスアカウント運用、セキュリティ設定、コスト最適化のベストプラクティスを提供。Use when working with AWS services via CLI, designing IAM policies, managing infrastructure, or automating cloud operations.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/aws-cli-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/aws-cli-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

AWS CLIは、Amazon Web Servicesの200以上のサービスをコマンドラインから操作するための公式ツールです。このスキルは、企業環境で頻出するサービスのCLI操作、IAMポリシー設計、セキュリティベストプラクティスを提供します。

---

## 2. Prerequisites

### Installation

```bash
# macOS (Homebrew)
brew install awscli

# pip
pip install awscli

# バージョン確認
aws --version
```

### Authentication Setup

```bash
# 対話式設定
aws configure

# プロファイル指定で設定
aws configure --profile <profile-name>

# 設定ファイルの場所
# ~/.aws/credentials - 認証情報
# ~/.aws/config - 設定
```

### Profile Management

```bash
# デフォルトプロファイルを使用
aws s3 ls

# 特定プロファイルを使用
aws s3 ls --profile production

# 環境変数でプロファイル指定
export AWS_PROFILE=production
aws s3 ls
```

---

## 3. Quick Start

Invoke this skill by describing your analysis needs to Claude.

---

## 4. How It Works

Follow the skill's SKILL.md workflow step by step, starting from a small validated input.

---

## 5. Usage Examples

- AWS CLIコマンドの構文を知りたい
- IAMポリシーやロールを設計・確認したい
- EC2、S3、Lambdaなどのリソースを管理したい
- クロスアカウントアクセスを設定したい
- セキュリティ設定を確認・強化したい
- AWS操作を自動化したい

---

## 6. Understanding the Output

- A structured response or artifact aligned to the skill's workflow.
- Reference support from 3 guide file(s).
- Reusable output that can be reviewed, refined, and incorporated into a wider project workflow.

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/aws-cli-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: security_best_practices.md, iam_guide.md, aws_cli_essentials.md.
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

- `skills/aws-cli-expert/references/aws_cli_essentials.md`
- `skills/aws-cli-expert/references/iam_guide.md`
- `skills/aws-cli-expert/references/security_best_practices.md`
