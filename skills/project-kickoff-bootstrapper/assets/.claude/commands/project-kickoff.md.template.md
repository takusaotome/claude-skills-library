---
description: Bootstrap Claude project context and quality controls for a new or existing repository. Create or refresh PROJECT_BRIEF, SKILL_ROUTING, QUALITY_GATES, and TEST_STRATEGY from repository evidence and user answers.
argument-hint: [optional-focus]
allowed-tools: Read,Write,Edit,Grep,Glob,LS,TodoRead,TodoWrite,AskUserQuestion
---

# Project Kickoff Bootstrap

プロジェクト開始時または AI 導入後追い時に、Claude 用の初期文脈と品質統制ドキュメントを整備する。

## Goals

- プロジェクトの目的・スコープ・主要リスクを明確化する
- スキルの使い分けルールを定義する
- 完了判定を明文化する
- テスト戦略と production parity 観点を定義する
- 不足情報はユーザーに確認し、推測で固定しない

## Workflow

### Phase 1: Inspect Repository
1. ルート構成を確認する
2. README、manifest、CI、テスト関連ファイルを確認する
3. 既存の `CLAUDE.md`、`.claude/rules/`、`docs/` を確認する
4. build / test / lint / typecheck / packaging 相当コマンド候補を抽出する

### Phase 2: Detect Missing Context
次の不足を洗い出す。

- 目的と成功条件
- スコープ / 非スコープ
- 高リスク領域
- 環境差分
- リリース条件
- 必要スキル

### Phase 3: Ask Targeted Questions
AskUserQuestion を使って、足りない情報だけを 2〜4 問ずつ聞く。

優先質問領域:
- プロジェクト目的
- 主要利用者 / 業務
- 本番環境との差
- 高リスク領域
- 完了判定

### Phase 4: Create / Refresh Documents
必要に応じて次を作成または更新する。

- `CLAUDE.md`
- `docs/PROJECT_BRIEF.md`
- `docs/SKILL_ROUTING.md`
- `docs/QUALITY_GATES.md`
- `docs/TEST_STRATEGY.md`
- `docs/DECISION_LOG.md`
- `docs/HIDDEN_CONTRACT_REGISTER.md`
- `docs/CROSS_MODULE_CONSISTENCY_MATRIX.md`

### Phase 5: Report Result
最後に次をまとめる。

```md
## Kickoff Summary
- Created / updated files:
- Key project risks:
- Selected mandatory skills:
- Missing information:
- Recommended next action:
```

## Rules

- 既存文書がある場合は無断で破壊せず、差分更新を優先する
- 不明な項目は `TBD` として残し、未確認で確定文にしない
- コマンドは実際の repo evidence があるものを優先し、なければ候補として示す
- 技術的高リスク領域がある場合はスキルルーティングに必ず反映する
