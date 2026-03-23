---
layout: default
title: "Skill Idea Miner"
grand_parent: 日本語
parent: メタ・品質
nav_order: 21
lang_peer: /en/skills/meta/skill-idea-miner/
permalink: /ja/skills/meta/skill-idea-miner/
---

# Skill Idea Miner
{: .no_toc }

Mine Claude Code session logs for skill idea candidates. Use when running the skill generation pipeline to extract, score, and backlog new skill ideas from recent coding sessions.
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/skill-idea-miner.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/skill-idea-miner){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

# Skill Idea Miner

<!-- TODO: 翻訳 -->

---

## 2. 前提条件

- **API Key:** None required
- **Python 3.9+** recommended

<!-- TODO: 翻訳 -->

---

## 3. クイックスタート

### Stage 1: Session Log Mining

1. Enumerate session logs from project directories in `~/.claude/projects/`
2. Filter to past 7 days by file mtime, confirm with `timestamp` field
3. Extract user messages (`type: "user"`, `userType: "external"`)
4. Extract tool usage patterns from assistant messages
5. Run deterministic signal detection:
   - Skill usage frequency (`skills/*/` path references)
   - Error patterns (non-zero exit codes, `is_error` flags, exception keywords)
   - Repetitive tool sequences (3+ tools repeated 3+ times)

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

- `skills/skill-idea-miner/references/idea_extraction_rubric.md`

**Scripts:**

- `skills/skill-idea-miner/scripts/mine_session_logs.py`
- `skills/skill-idea-miner/scripts/score_ideas.py`
