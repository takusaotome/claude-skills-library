# Skill vs Subagent Design Guide

Claude Code でワークフローを設計する際の、スキルとサブエージェントの使い分けガイド。

## 目次

1. [本質的な違い](#本質的な違い)
2. [判断フローチャート](#判断フローチャート)
3. [設計パターン](#設計パターン)
4. [判断軸の詳細](#判断軸の詳細)
5. [具体例での比較](#具体例での比較)
6. [実践的な設計指針](#実践的な設計指針)

---

## 本質的な違い

### スキル (Skill) とサブエージェント (Task) の比較

| 観点 | スキル (Skill) | サブエージェント (Task) |
|------|---------------|----------------------|
| **実行場所** | メインコンテキスト内 | 独立したサブプロセス |
| **コンテキスト** | 会話履歴を共有 | 隔離（渡した情報のみ） |
| **ユーザー可視性** | プロセスが見える | 結果のみ返る |
| **並列実行** | 不可（順次展開） | 可能 |
| **コンテキスト消費** | 増加する | しない（独立） |
| **対話性** | ユーザーと対話可能 | 一方向（結果のみ） |
| **再実行** | 会話内で再利用 | 毎回新規プロセス |

### 図解：実行モデルの違い

```mermaid
flowchart TB
    subgraph skill["スキル実行モデル"]
        direction TB
        U1[ユーザー] --> MC1[メインコンテキスト]
        MC1 --> SK[スキル展開]
        SK --> MC1
        MC1 --> U1
        note1[/"コンテキストを共有
        対話可能"/]
    end

    subgraph agent["サブエージェント実行モデル"]
        direction TB
        U2[ユーザー] --> MC2[メインコンテキスト]
        MC2 -->|タスク指示| SA[サブエージェント]
        SA -->|結果のみ| MC2
        MC2 --> U2
        note2[/"独立プロセス
        コンテキスト隔離"/]
    end
```

---

## 判断フローチャート

タスクを受けたときに、以下のフローチャートで最適なアプローチを判断できます。

### メイン判断フロー

```mermaid
flowchart TD
    START([タスク開始]) --> Q1{ユーザーとの<br/>対話が必要？}

    Q1 -->|Yes| SKILL_BASE[スキルをベースに設計]
    Q1 -->|No| Q2{探索・検索が<br/>多い？}

    Q2 -->|Yes| AGENT_DELEGATE[サブエージェントに委任]
    Q2 -->|No| Q3{並列化で<br/>高速化できる？}

    Q3 -->|Yes| MULTI_AGENT[複数サブエージェント<br/>並列実行]
    Q3 -->|No| Q4{繰り返し使う<br/>パターン？}

    Q4 -->|Yes| DEFINE_WORKFLOW[スキル or CLAUDE.md<br/>にワークフロー定義]
    Q4 -->|No| Q5{深い専門知識が<br/>必要？}

    Q5 -->|Yes| Q6{単一ドメイン？<br/>複数ドメイン？}
    Q5 -->|No| SIMPLE[シンプルな実装<br/>直接実行]

    Q6 -->|単一| SPECIALIZED_AGENT[専門サブエージェント]
    Q6 -->|複数| SKILL_INTEGRATE[スキルで統合]

    %% スタイル
    style START fill:#e1f5fe
    style SKILL_BASE fill:#c8e6c9
    style AGENT_DELEGATE fill:#fff3e0
    style MULTI_AGENT fill:#fff3e0
    style DEFINE_WORKFLOW fill:#c8e6c9
    style SPECIALIZED_AGENT fill:#fff3e0
    style SKILL_INTEGRATE fill:#c8e6c9
    style SIMPLE fill:#f5f5f5
```

### サブ判断：スキルベース設計の詳細

```mermaid
flowchart TD
    SKILL_START([スキルベース設計]) --> SQ1{重い処理<br/>フェーズがある？}

    SQ1 -->|Yes| SQ2{その処理は<br/>独立している？}
    SQ1 -->|No| PURE_SKILL[純粋スキル<br/>単体で完結]

    SQ2 -->|Yes| SKILL_ORCHESTRATOR[スキル＋サブエージェント<br/>オーケストレーター型]
    SQ2 -->|No| SKILL_SEQUENTIAL[スキル内で<br/>順次処理]

    %% スタイル
    style SKILL_START fill:#c8e6c9
    style PURE_SKILL fill:#a5d6a7
    style SKILL_ORCHESTRATOR fill:#81c784
    style SKILL_SEQUENTIAL fill:#a5d6a7
```

### サブ判断：ワークフロー定義の詳細

```mermaid
flowchart TD
    WF_START([ワークフロー定義]) --> WQ1{プロジェクト<br/>固有？}

    WQ1 -->|Yes| CLAUDE_MD[CLAUDE.mdに定義<br/>プロジェクト専用]
    WQ1 -->|No| WQ2{ユーザーが<br/>明示的に呼び出す？}

    WQ2 -->|Yes| SLASH_CMD[スラッシュコマンド<br/>として定義]
    WQ2 -->|No| SKILL_REUSABLE[再利用可能スキル<br/>として定義]

    %% スタイル
    style WF_START fill:#c8e6c9
    style CLAUDE_MD fill:#b39ddb
    style SLASH_CMD fill:#90caf9
    style SKILL_REUSABLE fill:#a5d6a7
```

---

## 設計パターン

### パターンA: スキル → サブエージェント（オーケストレーター型）

```mermaid
flowchart TB
    USER[ユーザー] --> SKILL[スキル<br/>オーケストレーター]

    SKILL --> AG1[サブエージェント1<br/>探索]
    SKILL --> AG2[サブエージェント2<br/>分析]
    SKILL --> AG3[サブエージェント3<br/>検証]

    AG1 --> SKILL
    AG2 --> SKILL
    AG3 --> SKILL

    SKILL -->|統合結果| USER

    note[/"並列実行可能
    スキルが結果を統合"/]

    style SKILL fill:#c8e6c9
    style AG1 fill:#fff3e0
    style AG2 fill:#fff3e0
    style AG3 fill:#fff3e0
```

**適用場面**:
- 専門的なワークフロー + 重い処理の組み合わせ
- 結果の統合・解釈に専門知識が必要
- 例: `migration-validation-explorer`

**メリット**:
- スキルの専門知識でサブエージェントを適切に指示
- 結果の統合・解釈にスキルの知識を活用
- コンテキスト節約しつつ専門性を確保

### パターンB: サブエージェント → スキル（委任型）

```mermaid
flowchart TB
    USER[ユーザー] --> AGENT[サブエージェント<br/>作業者]

    AGENT --> SK1[スキルA<br/>専門知識]
    AGENT --> SK2[スキルB<br/>別の専門知識]

    SK1 --> AGENT
    SK2 --> AGENT

    AGENT -->|処理結果| USER

    note[/"重い探索 + 専門判断
    メインコンテキスト影響なし"/]

    style AGENT fill:#fff3e0
    style SK1 fill:#c8e6c9
    style SK2 fill:#c8e6c9
```

**適用場面**:
- 重い探索 + 途中で専門判断が必要
- コンテキストを消費せずに専門知識を活用したい

**注意点**:
- サブエージェント内でスキルを呼ぶとサブエージェントのコンテキストで展開
- メインコンテキストは影響を受けない

### パターンC: CLAUDE.md / スラッシュコマンド（ワークフロー型）

```mermaid
flowchart TB
    USER[ユーザー<br/>一言の依頼] --> WORKFLOW[CLAUDE.md<br/>定義フロー]

    WORKFLOW --> P1[Phase 1<br/>サブエージェント<br/>調査]
    P1 --> P2[Phase 2<br/>スキルA<br/>分析]
    P2 --> P3[Phase 3<br/>サブエージェント群<br/>並列処理]
    P3 --> P4[Phase 4<br/>スキルB<br/>レポート生成]

    P4 --> USER

    style WORKFLOW fill:#b39ddb
    style P1 fill:#fff3e0
    style P2 fill:#c8e6c9
    style P3 fill:#fff3e0
    style P4 fill:#c8e6c9
```

**適用場面**:
- プロジェクト固有の定型ワークフロー
- 繰り返し実行するパイプライン
- 複数ドメインを横断する複合タスク

**メリット**:
- 最も柔軟な組み合わせが可能
- プロジェクトコンテキストに最適化できる
- 一言で複雑なワークフローを起動

### パターンD: 階層的サブエージェント（分散型）

```mermaid
flowchart TB
    USER[ユーザー] --> COORD[コーディネーター<br/>サブエージェント]

    COORD --> WORKER1[ワーカー1<br/>サブエージェント]
    COORD --> WORKER2[ワーカー2<br/>サブエージェント]
    COORD --> WORKER3[ワーカー3<br/>サブエージェント]

    WORKER1 --> COORD
    WORKER2 --> COORD
    WORKER3 --> COORD

    COORD -->|統合結果| USER

    note[/"完全にコンテキスト隔離
    大規模並列処理向き"/]

    style COORD fill:#ffcc80
    style WORKER1 fill:#fff3e0
    style WORKER2 fill:#fff3e0
    style WORKER3 fill:#fff3e0
```

**適用場面**:
- 非常に大規模な処理
- 完全なコンテキスト隔離が必要
- メインコンテキストの汚染を完全に防ぎたい

---

## 判断軸の詳細

### 軸1: 「何を隠すか」の観点

| シナリオ | 推奨 | 理由 |
|---------|------|------|
| 探索の試行錯誤 | サブエージェント | ユーザーに見せる必要なし |
| 中間的な分析プロセス | サブエージェント | 結果だけが重要 |
| 意思決定の根拠説明 | スキル | 透明性が重要 |
| 教育的なプロセス | スキル | 過程を見せることに価値 |

### 軸2: 「コンテキストのコスト」の観点

| シナリオ | 推奨 | 理由 |
|---------|------|------|
| 100ファイル探索→3ファイル発見 | サブエージェント | 97ファイル分のコンテキスト節約 |
| 試行錯誤が多い調査 | サブエージェント | 失敗の履歴が不要 |
| 確定した手順の実行 | スキル | 手順自体に価値 |
| テンプレート展開 | スキル | テンプレートを共有 |

### 軸3: 「並列性」の観点

| シナリオ | 推奨 | 理由 |
|---------|------|------|
| 独立した複数タスク | 複数サブエージェント | 同時実行で高速化 |
| 異なる専門分野の同時分析 | 複数サブエージェント | 専門性の並列活用 |
| 順次依存のあるワークフロー | スキル | 前の結果が次に影響 |
| A/Bテスト的な比較 | 複数サブエージェント | 同条件で並列実行 |

### 軸4: 「専門性の粒度」の観点

| シナリオ | 推奨 | 理由 |
|---------|------|------|
| 深い単一ドメイン分析 | 専門サブエージェント | 集中した専門性 |
| 複数ドメインの統合判断 | スキル | 広い視野での統合 |
| 標準化されたフォーマット出力 | スキル | テンプレート活用 |
| 探索的な調査 | Explore サブエージェント | 汎用的な探索能力 |

---

## 具体例での比較

### 例1: コードレビュー

#### アプローチA（スキル主導）

```mermaid
flowchart LR
    USER[ユーザー] -->|/code-review| SKILL[コードレビュースキル]
    SKILL --> READ[コード読み込み]
    READ --> ANALYZE[分析・判断]
    ANALYZE --> DIALOG[対話的フィードバック]
    DIALOG --> USER

    style SKILL fill:#c8e6c9
```

- **メリット**: 対話的、基準の説明が可能、追加質問に即座に対応
- **デメリット**: 大規模コードでコンテキスト消費

#### アプローチB（サブエージェント主導）

```mermaid
flowchart LR
    USER[ユーザー] --> AGENT[design-implementation-reviewer]
    AGENT --> EXPLORE[独立して探索・分析]
    EXPLORE --> RESULT[結果レポート]
    RESULT --> USER

    style AGENT fill:#fff3e0
```

- **メリット**: コンテキスト節約、深い分析、大規模コードベース対応
- **デメリット**: 途中経過が見えない、追加質問は新規実行

### 例2: データ分析

#### アプローチA（スキル単体）

```mermaid
flowchart LR
    USER[ユーザー] -->|/data-scientist| SKILL[データサイエンティストスキル]
    SKILL --> EDA[探索的データ分析]
    EDA --> MODEL[モデリング]
    MODEL --> REPORT[レポート生成]
    REPORT --> USER

    style SKILL fill:#c8e6c9
```

- **適用**: 中規模データ、対話的な分析

#### アプローチB（スキル + サブエージェント）

```mermaid
flowchart TB
    USER[ユーザー] -->|/data-scientist| SKILL[データサイエンティストスキル]
    SKILL --> AG1[サブエージェント<br/>データプロファイリング]
    SKILL --> AG2[サブエージェント<br/>モデル比較]
    AG1 --> SKILL
    AG2 --> SKILL
    SKILL --> INTERPRET[結果解釈・統合]
    INTERPRET --> USER

    style SKILL fill:#c8e6c9
    style AG1 fill:#fff3e0
    style AG2 fill:#fff3e0
```

- **適用**: 大規模データ、複数モデルの並列比較

### 例3: マイグレーション検証

#### 現在の `migration-validation-explorer` 設計

```mermaid
flowchart TB
    USER[ユーザー] -->|/migration-validation-explorer| SKILL[検証スキル<br/>方法論・フレームワーク]

    SKILL --> HYPOTHESIS[仮説生成フェーズ]
    HYPOTHESIS --> AG_EXPLORE[Explore サブエージェント<br/>データ探索]

    AG_EXPLORE --> SKILL
    SKILL --> PRIORITIZE[優先順位付け<br/>スキルの専門知識で]
    PRIORITIZE --> BACKLOG[QAバックログ生成]
    BACKLOG --> USER

    style SKILL fill:#c8e6c9
    style AG_EXPLORE fill:#fff3e0
```

- **設計理由**:
  - スキルが検証方法論を提供
  - 重い探索はサブエージェントに委任
  - 結果の優先順位付けはスキルの専門知識で判断

---

## 実践的な設計指針

### スキル設計時のチェックリスト

```markdown
## スキル設計チェックリスト

### サブエージェント呼び出しを組み込むべきか？
- [ ] 探索フェーズがある → サブエージェントに
- [ ] 重い処理フェーズがある → サブエージェントに
- [ ] 並列化できる独立タスクがある → 複数サブエージェントに

### 純粋にスキルだけで完結させるべきか？
- [ ] 手順が明確で試行錯誤が少ない
- [ ] ユーザーとの対話が重要
- [ ] テンプレート展開が主目的
- [ ] プロセスの透明性が重要
```

### サブエージェント設計時のチェックリスト

```markdown
## サブエージェント設計チェックリスト

### スキルを使わせるべきか？
- [ ] 専門知識を注入したい
- [ ] 標準化されたフォーマットで出力させたい
- [ ] 特定のワークフローに従わせたい

### 純粋にサブエージェントだけにするか？
- [ ] 探索・検索が主目的
- [ ] 汎用的な分析で十分
- [ ] 結果の形式に柔軟性が必要
```

### ワークフロー定義の配置判断

```mermaid
flowchart TD
    Q1{このワークフローは<br/>どこで使う？} --> |単一プロジェクト| CLAUDE[CLAUDE.md]
    Q1 --> |複数プロジェクト| Q2{ユーザーが<br/>明示的に呼び出す？}

    Q2 --> |Yes| SLASH[スラッシュコマンド<br/>スキルとして定義]
    Q2 --> |No| AGENT[サブエージェント<br/>agents.tomlに定義]

    style CLAUDE fill:#b39ddb
    style SLASH fill:#90caf9
    style AGENT fill:#fff3e0
```

---

## クイックリファレンス

### 状況別推奨アプローチ

| 状況 | 推奨アプローチ | 理由 |
|------|--------------|------|
| 対話重視 | スキル | ユーザーとの双方向コミュニケーション |
| 探索重視 | サブエージェント | コンテキスト節約 |
| 並列化したい | 複数サブエージェント | 同時実行で高速化 |
| 専門知識の統合 | スキル→サブエージェント | オーケストレーター型 |
| 定型ワークフロー | CLAUDE.md/スラッシュコマンド | 再利用性 |
| コンテキスト節約 | サブエージェント | 隔離された実行 |
| 透明性重視 | スキル | プロセスの可視化 |
| 大規模処理 | 階層的サブエージェント | 完全な隔離 |

### 核心原則

> **「コンテキストのコスト」と「ユーザー可視性のニーズ」のバランスで決める。**
>
> 重い処理は隠し、重要な判断は見せる。

---

## 関連ドキュメント

- [CLAUDE.md](../CLAUDE.md) - プロジェクト全体の設計指針
- [README.md](../README.md) - スキルカタログと使用方法
- [agents/agents.toml](../agents/agents.toml) - サブエージェント定義

---

*Last updated: 2025-12-29*
