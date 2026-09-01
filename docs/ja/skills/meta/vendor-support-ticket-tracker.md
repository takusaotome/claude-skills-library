---
layout: default
title: "Vendor Support Ticket Tracker"
grand_parent: 日本語
parent: メタ・品質
nav_order: 32
lang_peer: /en/skills/meta/vendor-support-ticket-tracker/
permalink: /ja/skills/meta/vendor-support-ticket-tracker/
---

# Vendor Support Ticket Tracker
{: .no_toc }

複数ベンダーのサポートチケットとRMAケースを、ローカルのYAMLデータベースで一元管理します。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/vendor-support-ticket-tracker.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/vendor-support-ticket-tracker){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

STX、Dell、HP など複数ベンダーにまたがるサポートチケットとRMAケースを追跡します。チケットの状態、やり取りのタイムライン、保留中のアクション、エスカレーション状況を保持し、ベンダーからのメール返信を反映してステータスを更新できます。フォローアップが必要なチケットを洗い出すステータスレポートも生成します。

チケットは8段階の状態を遷移します。`open` から `acknowledged`、`in-progress` と進み、RMAでは `awaiting-parts`、ベンダー側が顧客対応待ちなら `awaiting-customer`、必要に応じて `escalated`、最後に `resolved` から `closed` へ至ります。

優先度ごとにSLA目標を持ちます。critical は4時間、high は24時間、medium は72時間、low は5営業日です。営業時間は9:00から18:00で、休日を除外して計算します。

## 2. 利用シーン

- 新規のベンダーサポートチケットまたはRMAケースを登録するとき
- ベンダーからのメール返信を基にステータスを更新するとき
- オープンチケットのステータスレポートを生成するとき
- 一定期間動きのないチケットを洗い出すとき
- 特定チケットのエスカレーション履歴を確認するとき
- ベンダー間のSLA遵守状況を追跡するとき

---

## 3. 前提条件

- APIキーは不要です
- Python 3.9 以上を推奨します
- 詳細な実行条件は英語版ガイドまたは `SKILL.md` を参照してください。

---

## 4. クイックスタート

```bash
python3 scripts/ticket_manager.py init \
  --db-path ./tickets.yaml
```

---

## 5. 進め方

1. `skills/vendor-support-ticket-tracker/SKILL.md` を開き、対象タスクと期待する成果物を確認します。
2. クイックスタートのコマンドや最小サンプルで、手順が通ることを先に確認します。
3. 必要な観点に応じて `references/` 配下のガイドを確認し、判断基準を揃えます。
4. 補助スクリプトがある場合は小さな入力で実行し、出力形式を確認してから本番データへ広げます。
5. 仕上げ時に、出力内容と前提条件が依頼内容に合っているか見直します。

---

## 6. リソース

**参照ガイド:**

- `skills/vendor-support-ticket-tracker/references/ticket-lifecycle.md`

**補助スクリプト:**

- `skills/vendor-support-ticket-tracker/scripts/ticket_manager.py`

---

## 7. 英語版ガイド

- 詳細な背景説明、判断基準、実装例は [English version]({{ '/en/skills/meta/vendor-support-ticket-tracker/' | relative_url }}) を参照してください。
