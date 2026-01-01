# プロジェクトスケジュール（Gantt Chart）
# Claude Code Skills 全自動化プロジェクト

**プロジェクトコード**: PRJ-2025-SKILLS
**作成日**: 2025年12月29日
**バージョン**: 1.0

---

## 目次

1. [スケジュール概要](#1-スケジュール概要)
2. [マイルストーン一覧](#2-マイルストーン一覧)
3. [全体Ganttチャート](#3-全体ganttチャート)
4. [フェーズ別詳細Ganttチャート](#4-フェーズ別詳細ganttチャート)
5. [クリティカルパス](#5-クリティカルパス)
6. [リソース配分](#6-リソース配分)

---

## 1. スケジュール概要

### 1.1 プロジェクト期間

| 項目 | 内容 |
|------|------|
| **開始日** | 2025年1月6日（月） |
| **完了予定日** | 2026年6月30日（火） |
| **総期間** | 18ヶ月（約78週） |
| **総工数** | 1,350人日 |

### 1.2 フェーズ別期間

| フェーズ | 開始日 | 終了日 | 期間 | 工数 |
|---------|--------|--------|------|------|
| 1. 基盤整備 | 2025/01/06 | 2025/03/31 | 12週 | 180人日 |
| 2. プリセールス・要件定義 | 2025/04/01 | 2025/06/30 | 13週 | 250人日 |
| 3. 設計・開発 | 2025/07/01 | 2025/09/30 | 13週 | 280人日 |
| 4. テスト・QA | 2025/10/01 | 2025/12/26 | 13週 | 230人日 |
| 5. PM・運用保守 | 2026/01/05 | 2026/03/31 | 12週 | 250人日 |
| 6. 統合・最終検証 | 2026/04/01 | 2026/06/30 | 13週 | 160人日 |

---

## 2. マイルストーン一覧

| ID | マイルストーン名 | 予定日 | 達成基準 |
|----|-----------------|--------|---------|
| M0 | プロジェクト開始 | 2025/01/06 | キックオフ完了 |
| M1 | 基盤整備完了 | 2025/03/31 | 標準・環境整備完了、21既存スキル分析完了 |
| M2 | プリセールス・要件スキル完了 | 2025/06/30 | 9スキル開発・検証完了 |
| M3 | 設計・開発スキル完了 | 2025/09/30 | 11スキル開発・検証完了 |
| M4 | テスト・QAスキル完了 | 2025/12/26 | 9スキル開発・検証完了 |
| M5 | PM・運用保守スキル完了 | 2026/03/31 | 16スキル開発・検証完了 |
| M6 | プロジェクト完了 | 2026/06/30 | 全45スキル統合・リリース完了 |

---

## 3. 全体Ganttチャート

### 3.1 プロジェクト全体スケジュール

```mermaid
gantt
    title Claude Code Skills 全自動化プロジェクト - マスタースケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section マイルストーン
    M0: プロジェクト開始          :milestone, m0, 2025-01-06, 0d
    M1: 基盤整備完了              :milestone, m1, 2025-03-31, 0d
    M2: プリセールス・要件完了     :milestone, m2, 2025-06-30, 0d
    M3: 設計・開発完了            :milestone, m3, 2025-09-30, 0d
    M4: テスト・QA完了            :milestone, m4, 2025-12-26, 0d
    M5: PM・運用保守完了          :milestone, m5, 2026-03-31, 0d
    M6: プロジェクト完了          :milestone, m6, 2026-06-30, 0d

    section フェーズ1: 基盤整備
    プロジェクト立上げ            :p1a, 2025-01-06, 3w
    既存スキル分析               :p1b, after p1a, 4w
    標準・ガイドライン策定        :p1c, after p1b, 4w
    開発環境整備                 :p1d, after p1b, 5w

    section フェーズ2: プリセールス・要件定義
    プリセールススキル開発        :p2a, 2025-04-01, 7w
    要件定義スキル開発           :p2b, 2025-04-21, 9w
    フェーズ2検証               :p2c, after p2b, 3w

    section フェーズ3: 設計・開発
    設計スキル開発               :p3a, 2025-07-01, 10w
    開発スキル開発               :p3b, 2025-07-21, 7w
    フェーズ3検証               :p3c, after p3a, 3w

    section フェーズ4: テスト・QA
    テストスキル開発             :p4a, 2025-10-01, 8w
    品質管理スキル開発           :p4b, 2025-10-20, 6w
    フェーズ4検証               :p4c, after p4a, 3w

    section フェーズ5: PM・運用保守
    PMスキル開発                 :p5a, 2026-01-05, 6w
    運用保守スキル開発           :p5b, 2026-01-19, 7w
    データ分析・共通スキル       :p5c, 2026-02-09, 4w
    フェーズ5検証               :p5d, after p5b, 3w

    section フェーズ6: 統合・最終検証
    統合テスト                   :p6a, 2026-04-01, 5w
    ドキュメント整備             :p6b, 2026-04-28, 4w
    リリース準備                 :p6c, after p6b, 3w
    プロジェクト完了             :p6d, after p6c, 1w
```

---

## 4. フェーズ別詳細Ganttチャート

### 4.1 フェーズ1: 基盤整備（2025年1月〜3月）

```mermaid
gantt
    title フェーズ1: 基盤整備 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section プロジェクト立上げ
    キックオフ会議               :a1, 2025-01-06, 2d
    詳細計画策定                 :a2, after a1, 10d
    ステークホルダー分析         :a3, after a1, 5d
    リスク初期評価               :a4, after a2, 8d
    コミュニケーション計画       :a5, after a3, 5d

    section 既存スキル分析
    既存スキル棚卸し             :b1, after a1, 15d
    ギャップ分析                 :b2, after b1, 10d
    統合・拡張計画               :b3, after b2, 10d
    依存関係マッピング           :b4, after b2, 5d

    section 標準・ガイドライン
    スキル設計標準               :c1, after b1, 15d
    コーディング規約             :c2, after c1, 10d
    テスト基準                   :c3, after c1, 10d
    ドキュメント標準             :c4, after c1, 10d
    レビュープロセス             :c5, after c3, 5d

    section 開発環境整備
    リポジトリ構成整備           :d1, after c1, 10d
    CI/CDパイプライン           :d2, after d1, 20d
    テスト環境構築               :d3, after d1, 15d
    ドキュメント基盤             :d4, after d1, 10d
    パイロット検証               :d5, after d3, 5d

    section マイルストーン
    基盤整備完了                 :milestone, m1, 2025-03-31, 0d
```

### 4.2 フェーズ2: プリセールス・要件定義（2025年4月〜6月）

```mermaid
gantt
    title フェーズ2: プリセールス・要件定義 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section プリセールススキル
    proposal-creator設計         :ps1, 2025-04-01, 8d
    proposal-creator実装         :ps2, after ps1, 22d
    competitor-analyzer設計      :ps3, 2025-04-01, 5d
    competitor-analyzer実装      :ps4, after ps3, 15d
    既存スキル統合               :ps5, 2025-04-14, 20d
    プリセールステスト           :ps6, after ps2, 20d

    section 要件定義スキル
    requirements-elicitor設計    :rd1, 2025-04-21, 10d
    requirements-elicitor実装    :rd2, after rd1, 25d
    use-case-creator設計         :rd3, 2025-04-21, 5d
    use-case-creator実装         :rd4, after rd3, 15d
    brd-creator設計              :rd5, 2025-05-05, 8d
    brd-creator実装              :rd6, after rd5, 22d
    business-analyst拡張         :rd7, 2025-05-19, 15d
    要件定義テスト               :rd8, after rd2, 30d

    section フェーズ2検証
    統合テスト                   :v1, after rd8, 15d
    パイロット適用               :v2, after v1, 10d
    完了レビュー                 :v3, after v2, 5d

    section マイルストーン
    プリセールス・要件完了        :milestone, m2, 2025-06-30, 0d
```

### 4.3 フェーズ3: 設計・開発（2025年7月〜9月）

```mermaid
gantt
    title フェーズ3: 設計・開発 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section 設計スキル
    architecture-designer設計    :ds1, 2025-07-01, 12d
    architecture-designer実装    :ds2, after ds1, 28d
    database-designer設計        :ds3, 2025-07-01, 8d
    database-designer実装        :ds4, after ds3, 17d
    api-designer設計             :ds5, 2025-07-14, 8d
    api-designer実装             :ds6, after ds5, 17d
    ui-ux-reviewer設計           :ds7, 2025-07-21, 5d
    ui-ux-reviewer実装           :ds8, after ds7, 15d
    security-architect設計       :ds9, 2025-07-28, 10d
    security-architect実装       :ds10, after ds9, 25d

    section 開発スキル
    code-generator設計           :dv1, 2025-07-21, 8d
    code-generator実装           :dv2, after dv1, 17d
    refactoring-assistant設計    :dv3, 2025-08-04, 5d
    refactoring-assistant実装    :dv4, after dv3, 15d
    documentation-generator設計  :dv5, 2025-08-11, 5d
    documentation-generator実装  :dv6, after dv5, 15d
    既存開発スキル統合           :dv7, 2025-08-18, 15d
    開発スキルテスト             :dv8, after dv6, 15d

    section フェーズ3検証
    設計スキルテスト             :v1, after ds10, 15d
    統合テスト                   :v2, after v1, 15d
    パイロット適用               :v3, after v2, 5d
    完了レビュー                 :v4, after v3, 5d

    section マイルストーン
    設計・開発完了               :milestone, m3, 2025-09-30, 0d
```

### 4.4 フェーズ4: テスト・QA（2025年10月〜12月）

```mermaid
gantt
    title フェーズ4: テスト・QA 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section テストスキル
    test-plan-creator設計        :ts1, 2025-10-01, 8d
    test-plan-creator実装        :ts2, after ts1, 17d
    test-automation-designer設計 :ts3, 2025-10-06, 10d
    test-automation-designer実装 :ts4, after ts3, 20d
    既存テストスキル統合         :ts5, 2025-10-20, 25d
    テストスキルテスト           :ts6, after ts4, 30d

    section 品質管理スキル
    quality-audit-assistant設計  :qa1, 2025-10-20, 5d
    quality-audit-assistant実装  :qa2, after qa1, 15d
    process-improvement設計      :qa3, 2025-10-27, 5d
    process-improvement実装      :qa4, after qa3, 15d
    既存QAスキル統合             :qa5, 2025-11-10, 20d
    品質管理スキルテスト         :qa6, after qa4, 20d

    section フェーズ4検証
    統合テスト                   :v1, after ts6, 20d
    パイロット適用               :v2, after v1, 15d
    完了レビュー                 :v3, after v2, 5d

    section マイルストーン
    テスト・QA完了               :milestone, m4, 2025-12-26, 0d
```

### 4.5 フェーズ5: PM・運用保守（2026年1月〜3月）

```mermaid
gantt
    title フェーズ5: PM・運用保守 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section PMスキル
    progress-reporter設計        :pm1, 2026-01-05, 5d
    progress-reporter実装        :pm2, after pm1, 15d
    meeting-facilitator設計      :pm3, 2026-01-12, 5d
    meeting-facilitator実装      :pm4, after pm3, 15d
    既存PMスキル統合             :pm5, 2026-01-26, 20d
    PMスキルテスト               :pm6, after pm4, 20d

    section 運用保守スキル
    incident-manager設計         :om1, 2026-01-19, 8d
    incident-manager実装         :om2, after om1, 17d
    change-manager設計           :om3, 2026-01-26, 8d
    change-manager実装           :om4, after om3, 17d
    knowledge-curator設計        :om5, 2026-02-09, 5d
    knowledge-curator実装        :om6, after om5, 15d
    既存運用スキル統合           :om7, 2026-02-23, 10d
    運用保守スキルテスト         :om8, after om6, 15d

    section データ分析・共通
    bi-report-creator設計        :da1, 2026-02-09, 5d
    bi-report-creator実装        :da2, after da1, 15d
    technical-writer設計         :da3, 2026-02-16, 5d
    technical-writer実装         :da4, after da3, 10d
    既存分析スキル統合           :da5, 2026-02-23, 10d

    section フェーズ5検証
    統合テスト                   :v1, after om8, 15d
    パイロット適用               :v2, after v1, 10d
    完了レビュー                 :v3, after v2, 5d

    section マイルストーン
    PM・運用保守完了             :milestone, m5, 2026-03-31, 0d
```

### 4.6 フェーズ6: 統合・最終検証（2026年4月〜6月）

```mermaid
gantt
    title フェーズ6: 統合・最終検証 詳細スケジュール
    dateFormat YYYY-MM-DD
    excludes weekends

    section 統合テスト
    全スキル統合テスト           :it1, 2026-04-01, 30d
    E2Eシナリオテスト           :it2, after it1, 20d
    パフォーマンステスト         :it3, after it1, 10d

    section ドキュメント整備
    スキルカタログ作成           :doc1, 2026-04-28, 15d
    開発者ドキュメント           :doc2, 2026-05-05, 15d
    ベストプラクティス集         :doc3, after it2, 10d
    READMEアップデート           :doc4, after doc1, 10d

    section リリース準備
    パッケージング               :rel1, after it3, 10d
    リリースノート作成           :rel2, after rel1, 5d
    本番環境デプロイ             :rel3, after rel1, 10d
    トレーニング準備             :rel4, after doc1, 10d

    section プロジェクト完了
    最終レビュー                 :fin1, after rel3, 5d
    教訓収集                     :fin2, after fin1, 5d
    完了報告                     :fin3, after fin2, 5d

    section マイルストーン
    プロジェクト完了             :milestone, m6, 2026-06-30, 0d
```

---

## 5. クリティカルパス

### 5.1 クリティカルパス分析

プロジェクトのクリティカルパス（最長経路）は以下の通りです：

```mermaid
graph LR
    A[キックオフ] --> B[既存スキル分析]
    B --> C[スキル設計標準]
    C --> D[architecture-designer]
    D --> E[security-architect]
    E --> F[test-automation-designer]
    F --> G[incident-manager]
    G --> H[全スキル統合テスト]
    H --> I[E2Eテスト]
    I --> J[リリース]
    J --> K[プロジェクト完了]

    style A fill:#ff6b6b,color:#fff
    style B fill:#ff6b6b,color:#fff
    style C fill:#ff6b6b,color:#fff
    style D fill:#ff6b6b,color:#fff
    style E fill:#ff6b6b,color:#fff
    style F fill:#ff6b6b,color:#fff
    style G fill:#ff6b6b,color:#fff
    style H fill:#ff6b6b,color:#fff
    style I fill:#ff6b6b,color:#fff
    style J fill:#ff6b6b,color:#fff
    style K fill:#ff6b6b,color:#fff
```

### 5.2 クリティカルパス詳細

| 順序 | タスク | 工数 | 開始日 | 終了日 |
|-----|--------|------|--------|--------|
| 1 | キックオフ | 2d | 2025/01/06 | 2025/01/07 |
| 2 | 既存スキル分析 | 40d | 2025/01/08 | 2025/02/28 |
| 3 | スキル設計標準 | 15d | 2025/02/10 | 2025/02/28 |
| 4 | architecture-designer | 40d | 2025/07/01 | 2025/08/22 |
| 5 | security-architect | 35d | 2025/07/28 | 2025/09/12 |
| 6 | test-automation-designer | 30d | 2025/10/06 | 2025/11/14 |
| 7 | incident-manager | 25d | 2026/01/19 | 2026/02/20 |
| 8 | 全スキル統合テスト | 30d | 2026/04/01 | 2026/05/08 |
| 9 | E2Eテスト | 20d | 2026/05/11 | 2026/06/05 |
| 10 | リリース | 25d | 2026/06/02 | 2026/06/30 |

### 5.3 フロート（余裕）分析

| カテゴリ | スキル/タスク | フロート |
|---------|-------------|---------|
| クリティカル | architecture-designer | 0日 |
| クリティカル | security-architect | 0日 |
| 準クリティカル | database-designer | 5日 |
| 準クリティカル | api-designer | 7日 |
| 余裕あり | ui-ux-reviewer | 15日 |
| 余裕あり | mermaid-to-pdf統合 | 20日 |

---

## 6. リソース配分

### 6.1 フェーズ別リソース配分

```mermaid
pie title リソース配分（工数ベース）
    "フェーズ1: 基盤整備" : 180
    "フェーズ2: プリセールス・要件" : 250
    "フェーズ3: 設計・開発" : 280
    "フェーズ4: テスト・QA" : 230
    "フェーズ5: PM・運用保守" : 250
    "フェーズ6: 統合・最終検証" : 160
```

### 6.2 役割別リソース配分

| 役割 | 人数 | 稼働率 | フェーズ1 | フェーズ2 | フェーズ3 | フェーズ4 | フェーズ5 | フェーズ6 |
|------|------|--------|----------|----------|----------|----------|----------|----------|
| PM | 1 | 100% | 40% | 20% | 15% | 15% | 20% | 30% |
| TL | 1 | 100% | 30% | 25% | 35% | 25% | 25% | 25% |
| SE | 3 | 100% | 25% | 35% | 40% | 35% | 35% | 30% |
| BA | 1 | 80% | 5% | 30% | 20% | 15% | 25% | 30% |
| QA | 1 | 100% | 10% | 25% | 25% | 40% | 25% | 40% |

### 6.3 月別工数推移

> **注記**: 本表はWBS詳細（03_wbs_detailed.md）の総工数1,350人日と整合しています。

| 月 | PM | TL | SE(3名) | BA | QA | 合計 |
|----|----|----|---------|----|----|------|
| 2025/01 | 18 | 13 | 27 | 4 | 4 | 66 |
| 2025/02 | 13 | 18 | 27 | 4 | 9 | 71 |
| 2025/03 | 9 | 13 | 18 | 4 | 9 | 53 |
| 2025/04 | 13 | 18 | 35 | 13 | 13 | 92 |
| 2025/05 | 9 | 13 | 31 | 13 | 18 | 84 |
| 2025/06 | 9 | 9 | 18 | 9 | 13 | 58 |
| 2025/07 | 9 | 22 | 40 | 13 | 13 | 97 |
| 2025/08 | 9 | 18 | 35 | 9 | 13 | 84 |
| 2025/09 | 9 | 18 | 27 | 9 | 18 | 81 |
| 2025/10 | 9 | 18 | 31 | 9 | 22 | 89 |
| 2025/11 | 9 | 13 | 27 | 9 | 22 | 80 |
| 2025/12 | 9 | 9 | 18 | 4 | 18 | 58 |
| 2026/01 | 13 | 18 | 31 | 13 | 13 | 88 |
| 2026/02 | 9 | 13 | 27 | 13 | 13 | 75 |
| 2026/03 | 9 | 13 | 22 | 9 | 18 | 71 |
| 2026/04 | 13 | 13 | 22 | 13 | 22 | 83 |
| 2026/05 | 13 | 13 | 18 | 13 | 18 | 75 |
| 2026/06 | 18 | 9 | 13 | 9 | 13 | 62 |
| **合計** | **190** | **261** | **467** | **160** | **269** | **1,347** |

> **差分調整**: WBS合計1,350人日との差分3人日はコンティンジェンシーとして管理予備に含む。

---

**文書管理**:
- 作成日: 2025年12月29日
- 最終更新日: 2025年12月29日
- バージョン: 1.0
