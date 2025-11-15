# データ分析におけるSkillsとAgentsのハイブリッド活用ガイド

**作成日**: 2025-11-11
**対象**: Claude Codeでデータ分析を実施する実務担当者

---

## 目次

1. [基本的な考え方](#基本的な考え方)
2. [4つの分析パターン](#4つの分析パターン)
3. [実践例：売上データ分析](#実践例売上データ分析)
4. [データを与える際のベストプラクティス](#データを与える際のベストプラクティス)
5. [プロンプトのベストプラクティス](#プロンプトのベストプラクティス)
6. [実装パターン集](#実装パターン集)
7. [避けるべきアンチパターン](#避けるべきアンチパターン)
8. [まとめ：黄金の組み合わせ](#まとめ黄金の組み合わせ)

---

## 基本的な考え方

### SkillsとAgentsの役割分担

**Skills**: 構造化された分析手法（統計的厳密性、再現性）
**Agents**: 探索的な発見（仮説生成、異常検出、インサイト抽出）

→ **組み合わせることで最大の価値を生む**

### なぜハイブリッド活用が必要か

- Skillsのみ：厳密だが、予想外の発見が少ない
- Agentsのみ：柔軟だが、統計的厳密性に欠ける可能性
- **両方を組み合わせ**：統計的に信頼でき、かつ創造的なインサイトを得る

---

## 4つの分析パターン

### パターン1: Sequential Flow（順次実行）

**最も一般的で推奨されるパターン**

#### Step 1: Skillで基礎分析を実施

```
例：顧客データの分析
→ Skill: data-scientist
  - auto_eda.py実行
  - データ品質チェック
  - 基本統計量
  - 相関分析
  - 可視化
  ↓
  出力: EDAレポート（standardized_eda_report.html等）
```

#### Step 2: Agentに探索的分析を依頼

```
→ Agent: general-purpose
  プロンプト例:
  「先ほどのEDA結果を踏まえて、以下の観点で深掘り分析してください：
  1. 異常値や外れ値のパターンを調査
  2. ビジネス上の仮説を3つ生成
  3. セグメント別の特徴を分析
  4. 追加で調査すべきポイントを提案」

  Agentが自律的に：
  - データを読み込み直し
  - Python/Pandasで追加分析
  - パターン発見
  - ビジネスインサイト生成
```

#### 実際のワークフロー例

```python
# ユーザー: 「顧客データ（customers.csv）を分析してインサイトを得たい」

# [Claude] Step 1: Skillで基礎分析
Skill(data-scientist)
→ 対話形式で分析実施
→ EDA完了

# [Claude] Step 2: Agentで探索的分析
Task(general-purpose, """
customers.csvのEDA結果を踏まえて、以下を実施：
1. 離脱率が高いセグメントを特定
2. 購買パターンの異常を検出
3. クロスセル機会を分析
4. 3つのビジネス仮説を生成
5. レポートをMarkdownで作成
""")
```

#### メリット

- Skillの統計的厳密性を維持
- Agentの柔軟な探索力を活用
- 段階的に深掘り可能

---

### パターン2: Parallel Analysis（並行分析）

**異なる観点から同時に分析**

```python
# 同時起動（single message with multiple Task calls）
Task(data-scientist, "統計的な分析を実施してレポート作成")
+
Task(general-purpose, "ビジネス観点でのインサイト抽出")

→ 2つの異なる視点のレポートを並行取得
→ 統合して総合的な理解を得る
```

#### 使うべき場面

- 時間が限られている
- 異なる専門性が必要（統計 vs ビジネス）
- 大規模データで処理時間がかかる

#### 注意点

- 両方のエージェント/スキルが同じファイルにアクセス可能か確認
- 結果の統合は自分で行う必要がある

---

### パターン3: Iterative Deep Dive（反復深掘り）

**段階的に仮説を検証**

```
Skill(data-scientist) → 基礎分析
  ↓
Agent → インサイト発見「売上が特定の曜日に低い」
  ↓
Skill(data-visualization-expert) → 詳細可視化
  ↓
Agent → 原因調査「配送遅延と相関がある」
  ↓
Skill(data-scientist) → 統計的検証（相関係数、有意性検定）
  ↓
Agent → アクション提案レポート作成
```

#### メリット

- 発見→検証→発見のサイクル
- 段階的に精度向上
- ビジネス価値の高いインサイト発見

---

### パターン4: Role-Based Division（役割分担）

**タスクの性質で明確に分ける**

| タスク | 使用するもの | 理由 |
|--------|------------|------|
| **データクレンジング** | Agent | 柔軟な対応が必要 |
| **基本統計量** | Skill(data-scientist) | 標準化された手法 |
| **可視化** | Skill(data-visualization-expert) | プロフェッショナルな出力 |
| **異常検出** | Agent | 探索的な調査 |
| **仮説生成** | Agent | 創造的思考が必要 |
| **統計的検定** | Skill(data-scientist) | 厳密性が必要 |
| **時系列分析** | Skill(data-scientist) | timeseries_analysis.py使用 |
| **セグメント分析** | Agent | 柔軟な切り口が必要 |
| **最終レポート** | Agent | 全体統合+ストーリーテリング |

---

## 実践例：売上データ分析

### シナリオ

「過去1年の売上データ（sales_2024.csv）から、売上改善のインサイトを得たい」

### ベストプラクティスの実行

#### Phase 1: 基礎分析（Skill）

```
Skill: data-scientist

→ 対話形式で実施：
  - データ品質チェック
  - 欠損値処理
  - 基本統計量（平均、中央値、標準偏差）
  - 相関分析
  - 分布の可視化

出力: sales_2024_eda_report.html
```

#### Phase 2: パターン発見（Agent）

```
Agent: general-purpose

プロンプト：
"""
sales_2024.csvとEDAレポートを分析して：

1. 売上の季節性パターンを特定
2. 売上が急増/急減した期間を検出
3. 商品カテゴリ別の傾向を分析
4. 地域別の特徴を抽出
5. 異常値を調査（なぜその日に売上が高い/低いのか）
6. 3つのビジネス仮説を生成

Pythonコードを書いて分析し、結果をMarkdownレポートで出力
"""

出力: sales_pattern_analysis.md
```

#### Phase 3: 詳細可視化（Skill）

```
Skill: data-visualization-expert

Phase 2で発見したパターンを可視化：
- 月別売上トレンド
- カテゴリ別構成比
- 地域別ヒートマップ

出力: sales_visualizations.html
```

#### Phase 4: 仮説検証（Agent）

```
Agent: general-purpose

Phase 2で生成した仮説を統計的に検証：
"""
以下の仮説を検証：
1. 「週末の売上は平日より30%高い」→ t検定
2. 「特定地域で特定商品が売れる」→ カイ二乗検定
3. 「プロモーション期間中は売上2倍」→ 前後比較

検証結果をレポート化
"""

出力: hypothesis_validation.md
```

#### Phase 5: アクション提案（Agent）

```
Agent: general-purpose

全分析結果を統合して経営判断用レポート作成：
"""
Phase 1-4の分析結果を統合し、以下を含むエグゼクティブサマリーを作成：
1. 主要な発見（Top 5）
2. ビジネスインパクト評価
3. 具体的なアクション提案（優先度付き）
4. 期待される効果（定量的に）
5. 次のステップ
"""

出力: sales_insights_executive_summary.md
```

---

## データを与える際のベストプラクティス

### 1. ファイルサイズに注意

```python
# 小規模データ（< 10MB）
→ そのまま渡してOK

# 中規模データ（10-100MB）
→ サンプリングして渡す
→ Agentにサンプリングコード実行させる

# 大規模データ（> 100MB）
→ 集計済みデータを渡す
→ Agentに集計処理を先に実行させる
```

### 2. コンテキストの引き継ぎ

```python
# ✅ 良い例: 明示的に前の結果を参照
Agent: general-purpose
"""
先ほどdata-scientistスキルで実施したEDA結果（ファイル: eda_report.html）を読み込み、
以下の観点で追加分析を実施：
...
"""

# ❌ 悪い例: 暗黙的な参照
Agent: general-purpose
"""
さっきの結果を使って追加分析して
"""
→ Agentは「さっきの結果」にアクセスできない可能性
```

### 3. 出力ファイルの命名規則

```python
# Phase別に明確に命名
phase1_eda_report.html
phase2_pattern_analysis.md
phase3_visualizations/
phase4_hypothesis_validation.md
phase5_executive_summary.md

→ 後続のAgentが前のフェーズの出力を簡単に参照可能
```

---

## プロンプトのベストプラクティス

### Agentに探索的分析を依頼する際の良いプロンプト

#### ✅ 優れたプロンプト

```python
Task(general-purpose, """
データファイル: customer_churn.csv
前提: data-scientistスキルで基礎分析済み（結果: eda_report.html）

以下を実施してください：

1. データ読み込み（pd.read_csv）
2. 離脱顧客（churn=1）の特徴を分析
   - 契約期間との関係
   - 利用サービスとの関係
   - 請求金額との関係
3. セグメント別の離脱率を計算
4. 離脱リスクが高いセグメントTop 3を特定
5. なぜそのセグメントが離脱しやすいか仮説を立てる
6. 離脱防止施策を3つ提案
7. 結果をMarkdownレポートで出力（ファイル名: churn_insights.md）

Pythonコードを書いて実行し、可視化も含めてください。
""")
```

**良いプロンプトの特徴**：
- データファイル名を明示
- 前提条件を明確に記載
- 実施内容を番号付きリストで具体的に指示
- 期待する出力形式とファイル名を指定
- 必要な処理（コード実行、可視化）を明記

#### ❌ 不十分なプロンプト

```python
Task(general-purpose, """
customer_churn.csvを分析してインサイトを出して
""")
```

**問題点**：
- 具体性不足
- 期待する出力が不明確
- 分析の観点が指定されていない

---

## 実装パターン集

### パターンA: EDA → 深掘り

```python
# Step 1
Skill(data-scientist)
→ 基礎的なEDA

# Step 2
Task(general-purpose, """
[先ほどのEDA結果を読み込んで]
相関が高い変数ペアTop 5について、散布図を作成し、
なぜ相関が高いのかビジネス的な理由を考察してください。
""")
```

**用途**：相関分析の結果を深掘りしたい場合

---

### パターンB: 可視化 → インサイト抽出

```python
# Step 1
Skill(data-visualization-expert)
→ 包括的な可視化

# Step 2
Task(general-purpose, """
作成された可視化（visualizations/フォルダ内）を分析し、
グラフから読み取れるビジネスインサイトを5つ抽出してください。
各インサイトについて、なぜそれが重要か、どう活用すべきかを記述。
""")
```

**用途**：可視化からビジネス的な意味を引き出したい場合

---

### パターンC: 仮説生成 → 検証

```python
# Step 1
Task(general-purpose, """
データを探索的に分析し、ビジネス上の仮説を5つ生成
""")

# Step 2
Skill(data-scientist)
→ 生成された仮説を統計的に検証
```

**用途**：探索的にアイデアを出してから、統計的に検証したい場合

---

## 避けるべきアンチパターン

### ❌ アンチパターン1: 同じことを重複実行

```python
# 悪い例
Skill(data-scientist) → 基本統計量を計算
Agent(general-purpose) → また基本統計量を計算

→ 無駄、コンテキスト消費
```

**対策**：役割分担を明確にし、Skillで実施したことはAgentに再実施させない

---

### ❌ アンチパターン2: Agentに厳密な統計分析を任せる

```python
# 悪い例
Agent: "t検定とANOVAを実施して統計的に検証"

→ Skillの方が信頼性高い（data-scientist skill）
```

**対策**：統計的検定はSkillに任せる。Agentは結果の解釈に専念

---

### ❌ アンチパターン3: Skillに自由な探索を期待

```python
# 悪い例
Skill(data-scientist): "自由に分析してインサイト発見して"

→ Skillは定型ワークフローに従う、自由な探索は不得意
```

**対策**：自由な探索はAgentに任せる。Skillには明確なタスクを与える

---

## まとめ：黄金の組み合わせ

### 最強のデータ分析ワークフロー

```
1. Skill(data-scientist)
   → データ品質、基本統計、相関分析

2. Agent(general-purpose)
   → パターン発見、異常検出、仮説生成

3. Skill(data-visualization-expert)
   → 発見したパターンの可視化

4. Agent(general-purpose)
   → 統計的検証、ビジネスインサイト統合

5. Agent(general-purpose)
   → エグゼクティブサマリー作成
```

### この組み合わせで得られるもの

- ✅ **統計的厳密性**（Skills）
- ✅ **探索的発見**（Agents）
- ✅ **プロフェッショナルな出力**（Skills）
- ✅ **ビジネス価値の高いインサイト**（Agents）
- ✅ **再現可能な分析プロセス**

---

## クイックリファレンス

### いつSkillsを使うか

- ✅ 統計的厳密性が必要
- ✅ 標準化された分析手法を適用
- ✅ プロフェッショナルな可視化が必要
- ✅ 再現可能な分析プロセスが重要

### いつAgentsを使うか

- ✅ 探索的な調査が必要
- ✅ 仮説生成が必要
- ✅ 異常検出・パターン発見
- ✅ ビジネスインサイトの統合・レポート作成
- ✅ 柔軟な切り口での分析

### 判断に迷ったら

**「再現性と厳密性が必要？」**
- YES → Skill
- NO → Agent

**「定型的なプロセス？」**
- YES → Skill
- NO → Agent

**「創造的な発見が必要？」**
- YES → Agent
- NO → Skill

---

## 参考資料

- Claude Skills Library: `/Users/takueisaotome/PycharmProjects/claude-skills-library/`
- data-scientist skill: `data-scientist/SKILL.md`
- data-visualization-expert skill: `data-visualization-expert/SKILL.md`

---

**最終更新**: 2025-11-11
**バージョン**: 1.0
**作成者**: Claude Code実務担当者向けガイド
