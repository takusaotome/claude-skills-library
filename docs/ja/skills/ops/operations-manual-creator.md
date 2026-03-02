---
layout: default
title: Operations Manual Creator
grand_parent: 日本語
parent: 運用・ドキュメント
nav_order: 2
lang_peer: /en/skills/ops/operations-manual-creator/
permalink: /ja/skills/ops/operations-manual-creator/
---

# Operations Manual Creator
{: .no_toc }

STEP フォーマットと ANSI Z535 準拠の注意・警告分類で構造化された操作マニュアルを作成するスキル。
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

Operations Manual Creator は、業務システムの操作マニュアルを構造化して作成するスキルです。各手順は STEP フォーマット（Specific/Target/Expected/Proceed）で記述され、一貫性と明確さを確保します。注意・警告ラベルは ANSI Z535 に準拠した分類（DANGER/WARNING/CAUTION/NOTE）を使用し、トラブルシューティングガイドとエスカレーションパスも含む包括的なマニュアルを生成します。

日本語・英語の両方で出力可能で、エンタープライズ環境に対応しています。

---

## こんなときに使う

- 業務システムの操作マニュアルを作成する
- 標準作業手順書（SOP）を作成する
- システム運用マニュアルを作成する
- エンドユーザー向けのユーザーガイドを作成する
- オンボーディング用の作業手順書を作成する

---

## 前提条件

- **Claude Code** がインストール済みであること
- **operations-manual-creator** スキルがインストール済み（`cp -r ./skills/operations-manual-creator ~/.claude/skills/`）
- 外部 API やツールは不要

---

## 仕組み

6 ステップのワークフローで進行します:

1. **スコープ・対象者定義** -- 対象システム、カバーする操作、対象者のスキルレベル（初級/中級/上級）を明確化
2. **操作一覧の棚卸し** -- 全操作を ID（OP-001, OP-002, ...）、頻度、ロール、依存関係、見積時間でリスト化
3. **手順記述** -- STEP フォーマットで各操作を記述:
   - **S**pecific: 何をするか（正確なアクション動詞）
   - **T**arget: どの UI 要素か（ボタン名、メニューパス）
   - **E**xpected: 実行後に何が起こるか
   - **P**roceed: 成功を確認し次のステップへ進む方法
4. **注意・警告の付与** -- ANSI Z535 準拠の分類（DANGER/WARNING/CAUTION/NOTE）を該当ステップの前に配置。警告を無視した場合の結果も必ず記載
5. **トラブルシューティングガイド** -- 症状-原因-解決策テーブル、デシジョンツリー、3 段階エスカレーション（L1 セルフサービス、L2 ヘルプデスク、L3 エンジニアリング）
6. **組み立て・レビュー** -- 全コンポーネントをテンプレートに組み立て、目次を生成し、品質チェックリストを実行

---

## 使い方の例

### 例 1: 在庫管理システム操作マニュアル

```
在庫管理システムの操作マニュアルを作成してください。
対象者: 倉庫スタッフ（IT リテラシー低め）。
入荷、出荷、棚卸しの操作をカバーしてください。
```

スコープ定義、操作棚卸し、STEP 形式の手順記述（スクリーンショットプレースホルダー付き）、適切な警告（出荷確定の取消不可など）、バーコード読取エラーのトラブルシューティングまで一連の工程を実行します。

### 例 2: CRM 管理画面の SOP

```
CRM 管理画面のユーザー管理 SOP を作成してください。
操作: ユーザー追加、権限変更、アカウント無効化。
対象: IT 管理者。
```

STEP 形式の個別手順書を作成し、管理者権限付与には WARNING、パスワードポリシーには NOTE を付与します。

### 例 3: クイックスタートガイド

```
経費精算システムの新入社員向けクイックスタートガイドを作成してください。
よく使う 5 つの操作に絞ってください。
```

重要な操作を選定し、初心者向けの詳細な UI ナビゲーション付き手順と、FAQ 形式のトラブルシューティングを作成します。

---

## ヒントとベストプラクティス

- **1 ステップ = 1 アクション**: 複合操作は分解します。複数のクリックや入力を 1 つのステップにまとめません。
- **UI 要素は正確に**: 「保存する」ではなく「画面右上の青い『保存』ボタンをクリック」のように正確な名称で指定します。
- **警告はステップの前に**: DANGER/WARNING/CAUTION/NOTE は該当ステップの前に配置します。後には置きません。
- **スクリーンショットプレースホルダー**: `[Screenshot: {説明}]` マーカーが含まれるため、後から実画像を差し替えられます。
- **曖昧表現の禁止**: 「適宜」「必要に応じて」などの曖昧な表現は使用しません。すべての条件を明示します。

---

## 関連スキル

- [incident-rca-specialist]({{ '/ja/skills/ops/incident-rca-specialist/' | relative_url }}) -- インシデント後の振り返りと根本原因分析
- [markdown-to-pdf]({{ '/ja/skills/ops/markdown-to-pdf/' | relative_url }}) -- 生成したマニュアルをプロフェッショナル PDF に変換
- [technical-spec-writer]({{ '/ja/skills/ops/technical-spec-writer/' | relative_url }}) -- IEEE 830 準拠の技術仕様書作成
