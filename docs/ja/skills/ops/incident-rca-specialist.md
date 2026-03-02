---
layout: default
title: Incident RCA Specialist
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 1
lang_peer: /en/skills/ops/incident-rca-specialist/
permalink: /ja/skills/ops/incident-rca-specialist/
---

# Incident RCA Specialist
{: .no_toc }

インシデント発生後の振り返りと根本原因分析を体系的に実施するスキル。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API 不要</span>
<span class="badge badge-workflow">ワークフロー</span>
<span class="badge badge-bilingual">バイリンガル</span>

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 概要

Incident RCA Specialist は、組織的なインシデント管理プロセスに特化した振り返り・根本原因分析スキルです。タイムライン構築、影響評価、根本原因分析（5 Whys 分岐対応版、Fishbone、Fault Tree Analysis）、SMART 基準に基づく是正措置計画、日英バイリンガルの RCA レポート生成を提供します。

「人的エラー」で分析を止めず、必ずプロセス・システム・教育のギャップまで分解する Blame-Free カルチャーを徹底します。

**スコープ境界:** ログファイル解析や技術デバッグが必要な場合は `log-debugger` スキルを使用してください。本スキルは組織的な振り返りプロセスと是正措置の策定に特化しています。

---

## こんなときに使う

- インシデント発生後の振り返り・レトロスペクティブを実施するとき
- インシデントレポート・RCA ドキュメントを作成するとき
- 障害発生後の是正措置計画を策定するとき
- 再発防止策を策定するとき
- SLA 違反の有無を評価するとき
- 複雑なシステム障害に Fault Tree Analysis を適用するとき
- Lessons Learned を組織的に共有するとき

---

## 前提条件

- **Claude Code** がインストール済みであること
- **incident-rca-specialist** スキルがインストール済み（`cp -r ./skills/incident-rca-specialist ~/.claude/skills/`）
- 外部 API やツールは不要

---

## 仕組み

8 ステップのワークフローで進行します:

1. **情報収集** -- 構造化された質問でインシデント詳細を収集（タイムライン、影響サービス、ユーザー数、対応経緯）
2. **タイムライン構築** -- Mermaid ガントチャートで時系列を可視化し、TTD/TTR/TTM/TTRe を算出
3. **影響評価** -- 4 軸（ユーザー、サービス、ビジネス、運用）で影響を評価し、P0-P4 の重大度を判定
4. **RCA: 5 Whys** -- 分岐対応版 5 Whys。エビデンス追跡付き。人的エラーは必ずプロセス/システム/教育ギャップに分解
5. **RCA: Fishbone** -- IT 向け 6 カテゴリ（People, Process, Technology, Environment, Data, External）で石川ダイアグラムを作成
6. **RCA: Fault Tree Analysis** -- AND/OR ゲートによるトップダウン障害分析、最小カットセット、単一障害点の特定
7. **是正措置計画** -- 3 つの時間軸（即時/短期/長期）と 3D Prevention Framework（Detect, Defend, Degrade）、SMART 基準
8. **レポート生成** -- バンドルテンプレートを使用し、日本語または英語で完全な RCA レポートを出力

---

## 使い方の例

### 例 1: インシデントの全体振り返り

```
昨日、決済サービスが 2 時間ダウンしました（2/28 14:00-16:00 UTC）。
約 5,000 ユーザーが影響を受けました。監視アラートは最初のエラーから
20 分後に発報しました。RCA を実施してください。
```

情報収集からタイムライン構築、影響評価、5 Whys 分析、是正措置提案、最終レポート生成まで一連のワークフローを実行します。

### 例 2: 是正措置計画のみ

```
先週のデータベースフェイルオーバー障害の根本原因はコネクションプール
設定の誤りと判明しています。即時・短期・長期の是正措置計画を策定して
ください。
```

3D Prevention Framework（Detect/Defend/Degrade）を適用し、3 つの時間軸で SMART な是正措置を策定します。

### 例 3: Fault Tree Analysis

```
今月、CI/CD パイプラインで異なる原因による 3 回のデプロイ失敗が
発生しました。Fault Tree Analysis で単一障害点と最小カットセットを
特定してください。
```

AND/OR ゲートでトップイベントを分解し、Mermaid で FTA ツリーを生成、優先的に対処すべき SPOF を特定します。

---

## ヒントとベストプラクティス

- **Blame-Free の原則**: 分析結果は「プロセスが許容した...」のように記述し、個人の責任を追及しません。
- **エビデンスベース**: すべての因果関係にはログ・メトリクス・タイムスタンプなどの裏付けが必要です。各リンクに信頼度（High/Medium/Low）を付与します。
- **手法の使い分け**: シンプルなインシデントには 5 Whys、複数の寄与因子がある場合は Fishbone、複雑な構造的障害には FTA を使用します。組み合わせも可能です。
- **SMART な是正措置**: 「監視を強化する」のような曖昧な表現は、具体的・測定可能な項目に精緻化されます。
- **バイリンガル対応**: バンドルテンプレートを使用し、日本語・英語どちらでもレポートを生成できます。

---

## 関連スキル

- [log-debugger]({{ '/ja/skills/ops/log-debugger/' | relative_url }}) -- ログファイル解析とコードレベルの技術的根本原因調査
- [operations-manual-creator]({{ '/ja/skills/ops/operations-manual-creator/' | relative_url }}) -- 構造化された操作マニュアル・SOP の作成
- [project-manager]({{ '/ja/skills/management/project-manager/' | relative_url }}) -- プロジェクトヘルスチェックと PMBOK ベースの管理
