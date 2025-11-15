# データ分析デモプロジェクト

**Skills & Agents ハイブリッドデータ分析のベストプラクティス実践デモ**

---

## 概要

このプロジェクトは、Claude Code SkillsとAgentsを組み合わせたデータ分析のベストプラクティスを実践するデモです。

**ビジネスシナリオ**: アメリカで日本食材を販売する卸売業者（Umami Wholesale Inc.）の過去3年間の売上データを分析し、売上改善のためのアクション可能なインサイトを抽出します。

---

## プロジェクト構成

```
demo-data-analysis/
├── README.md                          # このファイル
├── PROJECT_PLAN.md                    # 詳細計画書
├── DEMO_EXECUTION_GUIDE.md            # デモ実行手順書（必読）
├── data/
│   ├── raw/                           # 生データ
│   │   └── umami_sales_2022_2024.csv  # ✅ 生成済み（263,040行、25MB）
│   └── processed/                     # 加工済みデータ
├── analysis/                          # 分析結果（5フェーズ）
│   ├── phase1_eda/
│   ├── phase2_patterns/
│   ├── phase3_visualizations/
│   ├── phase4_validation/
│   └── phase5_summary/
├── scripts/
│   └── generate_dummy_data.py         # データ生成スクリプト
└── .agents/
    └── data-analysis-expert/          # カスタムエージェント定義
        └── AGENT.md
```

---

## 📊 生成済みデータの概要

| 項目 | 値 |
|------|------|
| **総レコード数** | 263,040行 |
| **期間** | 2022-01-01 ~ 2024-12-31（3年間） |
| **総売上** | $47,085,370.57 |
| **商品数** | 23商品（8カテゴリ） |
| **地域** | 4地域（West Coast, East Coast, Midwest, South） |
| **顧客タイプ** | 3タイプ（Restaurant, Retail Store, Online） |

---

## 🚀 デモの実行方法

### ステップ1: データの確認（✅ 完了）

```bash
# データが正常に生成されたか確認
ls -lh data/raw/umami_sales_2022_2024.csv
```

### ステップ2: 5フェーズ分析ワークフロー

**詳細な実行手順**: `DEMO_EXECUTION_GUIDE.md` を参照（**必読**）

**目標所要時間**: 30-60分

---

## 分析ワークフロー（5フェーズ）

1. **Phase 1: 基礎分析（Skill）** - EDA、データ品質チェック
2. **Phase 2: パターン発見（Agent）** - 季節性、異常検出、仮説生成
3. **Phase 3: 詳細可視化（Skill）** - 発見したパターンの可視化
4. **Phase 4: 仮説検証（Agent）** - 統計的検証
5. **Phase 5: アクション提案（Agent）** - エグゼクティブサマリー作成

---

## 参考資料

- **ベストプラクティスガイド**: `docs/data_analysis_skills_agents_best_practices.md`
- **詳細計画書**: `PROJECT_PLAN.md`
- **エージェント定義**: `.agents/data-analysis-expert/AGENT.md`

---

## ステータス

### 準備完了 ✅

- [x] プロジェクト計画作成（PROJECT_PLAN.md）
- [x] エージェント定義作成（.agents/data-analysis-expert/AGENT.md）
- [x] フォルダ構造構築
- [x] ダミーデータ生成（263,040行、$47M売上）
- [x] デモ実行ガイド作成（DEMO_EXECUTION_GUIDE.md）

### 次のステップ

**Phase 1-5の分析実行**

詳細な手順は `DEMO_EXECUTION_GUIDE.md` を参照してください。

---

**作成日**: 2025-11-15
**最終更新**: 2025-11-15
**バージョン**: 1.0（デモ準備完了）
