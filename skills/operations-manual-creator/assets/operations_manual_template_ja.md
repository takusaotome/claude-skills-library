# {SYSTEM_NAME} 操作マニュアル

---

## 表紙

| 項目 | 内容 |
|------|------|
| **文書名** | {SYSTEM_NAME} 操作マニュアル |
| **文書番号** | {DOCUMENT_ID} |
| **バージョン** | {VERSION} |
| **作成日** | {CREATED_DATE} |
| **最終更新日** | {UPDATED_DATE} |
| **作成者** | {AUTHOR_NAME}（{AUTHOR_DEPARTMENT}） |
| **承認者** | {APPROVER_NAME}（{APPROVER_TITLE}） |
| **配布管理** | {DISTRIBUTION_LEVEL}（社外秘 / 部門内限定 / 一般） |
| **対象システムバージョン** | {SYSTEM_VERSION} |

### 配布先

| # | 部門 | 担当者 | 配布日 |
|---|------|--------|--------|
| 1 | {DEPARTMENT_1} | {RECIPIENT_1} | {DISTRIBUTION_DATE_1} |
| 2 | {DEPARTMENT_2} | {RECIPIENT_2} | {DISTRIBUTION_DATE_2} |

---

## 改訂履歴

| バージョン | 改訂日 | 改訂者 | 改訂内容 |
|-----------|--------|--------|----------|
| 1.0 | {CREATED_DATE} | {AUTHOR_NAME} | 初版作成 |
| {NEXT_VERSION} | {REVISION_DATE} | {REVISER_NAME} | {REVISION_DESCRIPTION} |

---

## 目次

1. [はじめに](#1-はじめに)
   1.1 本書の目的
   1.2 対象者
   1.3 前提条件
   1.4 関連文書
   1.5 本書の読み方
2. [システム概要](#2-システム概要)
   2.1 システムの目的
   2.2 システム構成
   2.3 アクセス方法
   2.4 動作環境
3. [操作一覧](#3-操作一覧)
4. [操作手順](#4-操作手順)
5. [トラブルシューティング](#5-トラブルシューティング)
   5.1 よくある問題と対処法
   5.2 判断フローチャート
   5.3 エスカレーション手順
6. [FAQ](#6-faq)
7. [用語集](#7-用語集)
8. [問い合わせ先](#8-問い合わせ先)
9. [承認欄](#9-承認欄)

---

## 1. はじめに

### 1.1 本書の目的

本書は、{SYSTEM_NAME}の操作手順を体系的にまとめた操作マニュアルです。{TARGET_AUDIENCE}が日常業務で{SYSTEM_NAME}を正しく・安全に操作するために必要な情報を提供します。

### 1.2 対象者

| 対象者 | スキルレベル | 主な利用シーン |
|--------|-------------|---------------|
| {AUDIENCE_1} | {SKILL_LEVEL_1}（初級 / 中級 / 上級） | {USE_CASE_1} |
| {AUDIENCE_2} | {SKILL_LEVEL_2} | {USE_CASE_2} |
| {AUDIENCE_3} | {SKILL_LEVEL_3} | {USE_CASE_3} |

### 1.3 前提条件

本マニュアルを利用するにあたり、以下の前提条件を満たしていることを確認してください。

- [ ] {SYSTEM_NAME}のユーザーアカウントが発行されていること
- [ ] {REQUIRED_SOFTWARE}がインストールされていること
- [ ] {NETWORK_REQUIREMENT}（社内ネットワーク / VPN接続 等）が利用可能であること
- [ ] {PRIOR_TRAINING}（基礎研修 等）を受講済みであること
- [ ] {ACCESS_RIGHTS}（必要な権限）が付与されていること

### 1.4 関連文書

| 文書名 | 文書番号 | 概要 |
|--------|---------|------|
| {RELATED_DOC_1} | {DOC_ID_1} | {DOC_DESCRIPTION_1} |
| {RELATED_DOC_2} | {DOC_ID_2} | {DOC_DESCRIPTION_2} |
| {RELATED_DOC_3} | {DOC_ID_3} | {DOC_DESCRIPTION_3} |

### 1.5 本書の読み方

#### 表記規則

| 表記 | 意味 |
|------|------|
| **太字** | 画面上のボタン名、メニュー名、フィールド名 |
| `等幅フォント` | 入力値、コマンド、URL |
| Menu > Submenu > Item | メニュー階層の操作パス |
| [Screenshot: 説明] | スクリーンショットの挿入位置 |
| OP-xxx | 操作手順のID |
| T-xxx | トラブルシューティングのID |

#### 注意・警告の表記

> [!DANGER]
> **危険**: 取り返しのつかないデータ破壊や重大な影響を及ぼす操作

> [!WARNING]
> **警告**: 複数ユーザーやシステム全体に影響する操作

> [!CAUTION]
> **注意**: 予期しない結果やデータ不整合が生じる可能性がある操作

> [!NOTE]
> **補足**: 操作のヒント、ベストプラクティス、補足情報

---

## 2. システム概要

### 2.1 システムの目的

{SYSTEM_NAME}は、{SYSTEM_PURPOSE}を目的として導入されたシステムです。

主な機能：
- {FUNCTION_1}
- {FUNCTION_2}
- {FUNCTION_3}

### 2.2 システム構成

```
{SYSTEM_ARCHITECTURE_DIAGRAM}
```

| コンポーネント | 説明 | URL/アクセス先 |
|--------------|------|---------------|
| {COMPONENT_1} | {COMPONENT_DESC_1} | {COMPONENT_URL_1} |
| {COMPONENT_2} | {COMPONENT_DESC_2} | {COMPONENT_URL_2} |

### 2.3 アクセス方法

| 環境 | URL | 用途 |
|------|-----|------|
| 本番環境 | `{PROD_URL}` | 通常業務 |
| 検証環境 | `{STAGING_URL}` | テスト・検証 |
| 開発環境 | `{DEV_URL}` | 開発・デバッグ |

### 2.4 動作環境

| 項目 | 推奨環境 | 最低要件 |
|------|---------|---------|
| ブラウザ | {RECOMMENDED_BROWSER} | {MINIMUM_BROWSER} |
| OS | {RECOMMENDED_OS} | {MINIMUM_OS} |
| 画面解像度 | {RECOMMENDED_RESOLUTION} | {MINIMUM_RESOLUTION} |
| ネットワーク | {RECOMMENDED_NETWORK} | {MINIMUM_NETWORK} |

---

## 3. 操作一覧

### 操作一覧表

| OP-ID | 操作名 | カテゴリ | 頻度 | 対象ロール | 所要時間 | 前提操作 |
|-------|--------|---------|------|-----------|---------|---------|
| OP-001 | {OPERATION_NAME_1} | {CATEGORY_1} | {FREQUENCY_1} | {ROLE_1} | {TIME_1} | - |
| OP-002 | {OPERATION_NAME_2} | {CATEGORY_2} | {FREQUENCY_2} | {ROLE_2} | {TIME_2} | OP-001 |
| OP-003 | {OPERATION_NAME_3} | {CATEGORY_3} | {FREQUENCY_3} | {ROLE_3} | {TIME_3} | OP-001 |

### カテゴリ凡例

| カテゴリ | 説明 |
|---------|------|
| 初期設定 | システム利用開始時に1回のみ実施 |
| 日次業務 | 毎日実施する定型操作 |
| 週次業務 | 毎週実施する定型操作 |
| 月次業務 | 毎月実施する定型操作 |
| 随時業務 | 必要に応じて実施する操作 |
| 管理業務 | 管理者が実施するシステム管理操作 |

### 操作依存関係マップ

```
{DEPENDENCY_MAP}
例:
OP-001 (ログイン)
  ├── OP-002 (データ登録) ── OP-004 (データ承認)
  ├── OP-003 (データ検索) ── OP-005 (レポート出力)
  └── OP-006 (設定変更)
```

---

## 4. 操作手順

<!-- 以下、各操作手順をOP-IDごとに記述する。procedure_template.mdを使用 -->

### OP-001: {OPERATION_NAME_1}

#### 基本情報

| 項目 | 内容 |
|------|------|
| **操作ID** | OP-001 |
| **操作名** | {OPERATION_NAME_1} |
| **概要** | {OPERATION_DESCRIPTION_1} |
| **カテゴリ** | {CATEGORY_1} |
| **実行頻度** | {FREQUENCY_1} |
| **所要時間** | 約{TIME_1} |
| **対象ロール** | {ROLE_1} |
| **前提条件** | {PREREQUISITES_1} |

#### 手順

| Step | 操作（Specific） | 対象（Target） | 期待結果（Expected） | 確認・次へ（Proceed） |
|------|-----------------|---------------|--------------------|--------------------|
| 1 | {ACTION_1} | {TARGET_1} | {EXPECTED_1} | {PROCEED_1} |
| 2 | {ACTION_2} | {TARGET_2} | {EXPECTED_2} | {PROCEED_2} |
| 3 | {ACTION_3} | {TARGET_3} | {EXPECTED_3} | {PROCEED_3} |

#### 確認チェックポイント

- [ ] {CHECKPOINT_1}
- [ ] {CHECKPOINT_2}

#### 関連操作

- 次の操作: OP-002（{NEXT_OP_NAME}）
- 関連トラブルシューティング: T-001

---

### OP-002: {OPERATION_NAME_2}

<!-- 同様のフォーマットで記述 -->

---

## 5. トラブルシューティング

### 5.1 よくある問題と対処法

| ID | 症状 | 想定原因 | 対処方法 | 関連OP | 重要度 |
|----|------|---------|---------|--------|--------|
| T-001 | {SYMPTOM_1} | {CAUSE_1} | {RESOLUTION_1} | OP-{xxx} | {SEVERITY_1} |
| T-002 | {SYMPTOM_2} | {CAUSE_2} | {RESOLUTION_2} | OP-{xxx} | {SEVERITY_2} |
| T-003 | {SYMPTOM_3} | {CAUSE_3} | {RESOLUTION_3} | OP-{xxx} | {SEVERITY_3} |

### 5.2 判断フローチャート

```
{DECISION_TREE}
```

### 5.3 エスカレーション手順

| レベル | 対応範囲 | 連絡先 | 対応時間 |
|--------|---------|--------|---------|
| L1（自己解決） | 本マニュアル記載の対処法で解決可能な問題 | - | 即時 |
| L2（ヘルプデスク） | アカウント管理、権限変更、設定変更 | {HELPDESK_CONTACT} | {L2_RESPONSE_TIME} |
| L3（開発チーム） | システム障害、データ復旧、セキュリティ | {ENGINEERING_CONTACT} | {L3_RESPONSE_TIME} |

#### エスカレーション時に準備する情報

1. 発生日時（YYYY-MM-DD HH:MM）
2. ユーザーID
3. エラーメッセージ（全文）
4. 発生時の操作手順（何をしていたか）
5. スクリーンショット
6. 自己解決で試みた内容と結果

---

## 6. FAQ

### アカウント・ログイン

**Q1: パスワードを忘れた場合はどうすればよいですか？**

A: {FAQ_ANSWER_1}

---

**Q2: アカウントがロックされました。どうすればよいですか？**

A: {FAQ_ANSWER_2}

---

### データ操作

**Q3: 誤って削除したデータを復元できますか？**

A: {FAQ_ANSWER_3}

---

**Q4: データのエクスポートで文字化けが発生します。**

A: {FAQ_ANSWER_4}

---

### システム全般

**Q5: 推奨ブラウザは何ですか？**

A: {FAQ_ANSWER_5}

---

## 7. 用語集

| 用語 | 読み | 定義 | 関連OP |
|------|------|------|--------|
| {TERM_1} | {READING_1} | {DEFINITION_1} | OP-{xxx} |
| {TERM_2} | {READING_2} | {DEFINITION_2} | OP-{xxx} |
| {TERM_3} | {READING_3} | {DEFINITION_3} | OP-{xxx} |

---

## 8. 問い合わせ先

| 問い合わせ種別 | 連絡先 | 対応時間 |
|--------------|--------|---------|
| 操作方法に関する質問 | {SUPPORT_CONTACT_1} | {SUPPORT_HOURS_1} |
| システム障害の報告 | {SUPPORT_CONTACT_2} | {SUPPORT_HOURS_2} |
| 機能改善の要望 | {SUPPORT_CONTACT_3} | {SUPPORT_HOURS_3} |
| セキュリティインシデント | {SECURITY_CONTACT} | 24時間365日 |

---

## 9. 承認欄

| 役割 | 氏名 | 部署 | 承認日 | 署名 |
|------|------|------|--------|------|
| 作成者 | {AUTHOR_NAME} | {AUTHOR_DEPARTMENT} | {CREATED_DATE} | |
| レビュー者 | {REVIEWER_NAME} | {REVIEWER_DEPARTMENT} | {REVIEW_DATE} | |
| 承認者 | {APPROVER_NAME} | {APPROVER_DEPARTMENT} | {APPROVAL_DATE} | |

---

*本文書は{ORGANIZATION_NAME}の機密文書です。許可なく複製・配布することを禁じます。*
