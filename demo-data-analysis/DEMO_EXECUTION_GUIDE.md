# デモ実行ガイド

**Skills & Agents ハイブリッドデータ分析デモ - 実行手順書**

**目標所要時間**: 30-60分
**作成日**: 2025-11-15

---

## 📋 デモの概要

このデモでは、Umami Wholesale Inc.の3年間の売上データ（263,040行、$47M）を分析し、5フェーズのワークフローを通じてビジネスインサイトを抽出します。

### 5フェーズワークフロー

1. **Phase 1**: 基礎分析（Skill: data-scientist）- 10分
2. **Phase 2**: パターン発見（Agent: general-purpose）- 15分
3. **Phase 3**: 詳細可視化（Skill: data-visualization-expert）- 10分
4. **Phase 4**: 仮説検証（Agent: general-purpose）- 10分
5. **Phase 5**: アクション提案（Agent: general-purpose）- 10分

**合計**: 55分（目標: 30-60分）

---

## 🚀 事前準備

### 1. データの確認

```bash
# データファイルの存在確認
ls -lh data/raw/umami_sales_2022_2024.csv

# データのサンプル確認（最初の10行）
head -10 data/raw/umami_sales_2022_2024.csv
```

**期待される結果**:
- ファイルサイズ: 約25MB
- 列数: 14列（date, product_category, product_name, region, customer_type等）

### 2. 必要なライブラリの確認

Claude CodeのSkillsには必要なライブラリが含まれていますが、念のため確認：

```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, scipy; print('All libraries available')"
```

---

## Phase 1: 基礎分析（10分）

### 目的
データ品質チェック、基本統計量、相関分析、初期可視化

### 実行方法

```
Claude Codeで以下のように依頼：

「data-scientistスキルを使って、
data/raw/umami_sales_2022_2024.csvの基礎分析（EDA）を実施してください。

以下の観点で分析：
1. データ品質チェック（欠損値、異常値、データ型）
2. 基本統計量（平均、中央値、標準偏差、四分位数）
3. 相関分析（total_salesと各変数の相関）
4. 分布の可視化（ヒストグラム、箱ひげ図）
5. 時系列プロット（月次・四半期売上トレンド）

レポートをanalysis/phase1_eda/フォルダに出力してください。」
```

### 期待される成果物

- `analysis/phase1_eda/eda_report.html` - 包括的なEDAレポート
- `analysis/phase1_eda/data_quality_report.md` - データ品質評価

### 確認ポイント

- [ ] 欠損値はないか？
- [ ] 異常値は妥当か？
- [ ] 売上の分布は正常か？
- [ ] 年次トレンドは上昇傾向か？
- [ ] どの変数が売上と相関が高いか？

**所要時間**: 約10分

---

## Phase 2: パターン発見（15分）

### 目的
季節性パターン、異常検出、セグメント分析、ビジネス仮説生成

### 実行方法

```
Claude Codeで以下のように依頼：

「Phase 1のEDA結果を踏まえて、
data/raw/umami_sales_2022_2024.csvから以下のパターンを発見してください：

1. 売上の季節性パターンを特定（月別・四半期別）
2. 売上が急増/急減した期間を検出（異常検出）
3. 商品カテゴリ別の傾向を分析
4. 地域別の特徴を抽出
5. 顧客タイプ別の購買行動を分析
6. プロモーション効果を測定
7. ビジネス仮説を3-5個生成

Pythonコードを書いて分析し、結果を以下のファイルで出力：
- analysis/phase2_patterns/pattern_analysis.md
- analysis/phase2_patterns/business_hypotheses.md」
```

### 期待される成果物

- `analysis/phase2_patterns/pattern_analysis.md` - パターン分析レポート
- `analysis/phase2_patterns/business_hypotheses.md` - ビジネス仮説リスト

### 確認ポイント

- [ ] 季節性は検出されたか？（1月、7-8月、11-12月の売上増加）
- [ ] 異常値は特定されたか？（2022年3月、2023年6月、2024年2月）
- [ ] 成長地域は特定されたか？（South地域の高成長）
- [ ] オンラインチャネルの成長は検出されたか？（+25%/年）
- [ ] ビジネス仮説は具体的で検証可能か？

**所要時間**: 約15分

---

## Phase 3: 詳細可視化（10分）

### 目的
Phase 2で発見したパターンをプロフェッショナルな可視化で表現

### 実行方法

```
Claude Codeで以下のように依頼：

「data-visualization-expertスキルを使って、
Phase 2で発見したパターンを可視化してください。

以下の可視化を作成：
1. 月別売上トレンド（折れ線グラフ、2022-2024年を重ねて表示）
2. カテゴリ別構成比（積み上げ棒グラフ、円グラフ）
3. 地域別売上推移（折れ線グラフ）
4. 顧客タイプ別トレンド（折れ線グラフ）
5. プロモーション有無別の売上比較（箱ひげ図）

データ: data/raw/umami_sales_2022_2024.csv
出力先: analysis/phase3_visualizations/」
```

### 期待される成果物

- `analysis/phase3_visualizations/sales_trends.html` - 売上トレンド可視化
- `analysis/phase3_visualizations/category_analysis.html` - カテゴリ別分析

### 確認ポイント

- [ ] グラフは読みやすいか？
- [ ] 季節性が視覚的に明確か？
- [ ] トレンドが一目で分かるか？
- [ ] カラーパレットは適切か？

**所要時間**: 約10分

---

## Phase 4: 仮説検証（10分）

### 目的
Phase 2で生成した仮説を統計的に検証

### 実行方法

```
Claude Codeで以下のように依頼：

「Phase 2で生成した仮説を統計的に検証してください。

検証する仮説（Phase 2のbusiness_hypotheses.mdから選択）:
1. 「West Coastの売上は他地域より20%以上高い」→ t検定
2. 「オンライン顧客の成長率は年間25%以上」→ トレンド分析
3. 「プロモーション期間中は売上が30%増加」→ 前後比較分析
4. 「1月の売上は平均月の1.5倍」→ 月別比較
5. 「冷凍食品は夏季（7-8月）に売上増加」→ 季節性検定

各仮説について：
- 適切な統計的検定を選択
- p値、効果量を計算
- 結果をビジネス言語で解釈

データ: data/raw/umami_sales_2022_2024.csv
出力先: analysis/phase4_validation/hypothesis_validation.md」
```

### 期待される成果物

- `analysis/phase4_validation/hypothesis_validation.md` - 仮説検証レポート

### 確認ポイント

- [ ] すべての仮説が検証されたか？
- [ ] p値は有意か？（p < 0.05）
- [ ] 効果量は実務的に意味があるか？
- [ ] ビジネス的な解釈は明確か？

**所要時間**: 約10分

---

## Phase 5: アクション提案（10分）

### 目的
Phase 1-4の全結果を統合し、経営判断用のエグゼクティブサマリーを作成

### 実行方法

```
Claude Codeで以下のように依頼：

「Phase 1-4の分析結果を統合して、
経営層向けのエグゼクティブサマリーを作成してください。

以下を含む：
1. 主要な発見（Top 5）- データで裏付け
2. ビジネスインパクト評価（売上・利益への影響を定量化）
3. 具体的なアクション提案（優先度付き）
   - 地域別の売上拡大戦略
   - 商品カテゴリの最適化
   - オンラインチャネルの成長戦略
   - 季節性を活用したプロモーション最適化
4. 期待される効果（定量的に、例：売上+15%）
5. リスクと制約条件
6. 次のステップ（短期・中期）

参照ファイル:
- analysis/phase1_eda/eda_report.html
- analysis/phase2_patterns/pattern_analysis.md
- analysis/phase4_validation/hypothesis_validation.md

出力先: analysis/phase5_summary/executive_summary.md」
```

### 期待される成果物

- `analysis/phase5_summary/executive_summary.md` - エグゼクティブサマリー

### 確認ポイント

- [ ] 主要な発見は明確か？
- [ ] アクション提案は具体的で実行可能か？
- [ ] 期待効果は定量化されているか？
- [ ] リスクは適切に記載されているか？
- [ ] 経営層が意思決定できる内容か？

**所要時間**: 約10分

---

## ✅ デモ完了後のチェックリスト

### 成果物の確認

- [ ] Phase 1: EDAレポート（HTML + MD）
- [ ] Phase 2: パターン分析 + 仮説リスト（MD）
- [ ] Phase 3: 可視化（HTML/画像）
- [ ] Phase 4: 仮説検証（MD）
- [ ] Phase 5: エグゼクティブサマリー（MD）

### 学習ポイントの確認

- [ ] SkillsとAgentsの使い分けを理解できたか？
- [ ] Sequential Flowパターンを実践できたか？
- [ ] データからビジネスインサイトを抽出できたか？
- [ ] 統計的検証とビジネス解釈の両方を実施できたか？

---

## 🎯 期待される学習成果

このデモを通じて、以下のスキルを習得：

1. **ハイブリッド分析アプローチ**
   - Skills（構造化分析）とAgents（探索的分析）の組み合わせ

2. **データ駆動型意思決定**
   - データ→パターン発見→仮説→検証→アクションの流れ

3. **ビジネスインサイト抽出**
   - 統計的結果をビジネス言語に翻訳する技術

4. **再現可能な分析プロセス**
   - 5フェーズワークフローを他のプロジェクトに適用

---

## 🔄 デモの反復

このデモは繰り返し実行可能です：

1. **異なるビジネス課題で実践**
   - 例：在庫最適化、顧客離脱分析、価格最適化

2. **データを変更して実験**
   - `scripts/generate_dummy_data.py`のパラメータを変更

3. **分析を深掘り**
   - 機械学習モデルの追加、時系列予測等

---

## 📚 参考資料

- **ベストプラクティスガイド**: `docs/data_analysis_skills_agents_best_practices.md`
- **プロジェクト計画書**: `PROJECT_PLAN.md`
- **エージェント定義**: `.agents/data-analysis-expert/AGENT.md`

---

## ❓ トラブルシューティング

### Q1: Skillが見つからない

**A**: Claude Code環境でSkillsが有効になっているか確認。`/skills list`コマンドで確認。

### Q2: Agentの応答が遅い

**A**: データサイズが大きい場合、サンプリングを検討。または、分析をPhase別に分割。

### Q3: 可視化が表示されない

**A**: HTMLファイルをブラウザで開く。または、画像ファイル（PNG）として保存。

---

**作成日**: 2025-11-15
**バージョン**: 1.0
**次回更新**: デモ実行後のフィードバックを反映
