# CLAUDE.md

このファイルは、{{PROJECT_NAME}} に対して Claude Code / AI エージェントが継続的に従うべきプロジェクト共通ルールを定義する。

@docs/PROJECT_BRIEF.md
@docs/SKILL_ROUTING.md
@docs/QUALITY_GATES.md
@docs/TEST_STRATEGY.md

## Session Operating Mode

- すべての作業は、まず対象フェーズを `discovery / design / implementation / verification / release` のいずれかに分類する。
- 中規模以上または高リスクの変更では、実装前に `docs/SKILL_ROUTING.md` を参照し、使うべきスキルを選択する。
- 既存コード・共通関数・外部ライブラリ・他チーム提供モジュールを使うときは、挙動を推測せず、必要に応じて `hidden-contract-investigator` 相当の手順を先に実施する。
- 完了報告前に `docs/QUALITY_GATES.md` の該当ゲートを満たした証跡を確認する。
- 実装・設計・テスト方針に重要な判断が入った場合は `docs/DECISION_LOG.md` に残す。

## Default Workflow

1. 目的、対象範囲、制約、影響範囲、環境差分を明確化する。
2. `docs/SKILL_ROUTING.md` から使用スキルを選ぶ。
3. 変更前に短い作業計画を示す。
4. 小さな単位で実装・修正する。
5. `docs/TEST_STRATEGY.md` と `docs/QUALITY_GATES.md` に沿って検証する。
6. 最後に、変更内容・検証結果・残課題・リスクを明示する。

## Non-Negotiables

- 「コードを書いた」だけでは完了扱いにしない。
- 成功表示、ログ出力、関数戻り値だけで成功を断定しない。必要なら永続化・副作用・外部連携結果まで確認する。
- 認可、課金・金額、日時、タイムゾーン、ファイルI/O、DB差分、マイグレーション、ジョブ、並行実行は高リスク領域として扱う。
- 既存の危険な実装を踏襲せず、可能な限り安全側の標準パターンを優先する。
- 仮説・未確認事項・未実施テストは明確に区別して報告する。

## Project Defaults

- Primary language: `{{PRIMARY_LANGUAGE}}`
- Main stack: `{{STACK}}`
- Main source directory: `{{MAIN_SOURCE_DIR}}`
- Test directory: `{{TEST_DIR}}`
- Database / migration directory: `{{DB_DIR}}`

## Standard Commands

- Build: `{{BUILD_COMMAND}}`
- Test: `{{TEST_COMMAND}}`
- Lint: `{{LINT_COMMAND}}`
- Typecheck: `{{TYPECHECK_COMMAND}}`
- CI equivalent: `{{CI_COMMAND}}`
- Package / Deploy check: `{{PACKAGE_OR_DEPLOY_COMMAND}}`

## Output Expectations

回答や変更サマリでは、必要に応じて次を含める。

- 何を変更したか
- なぜ変更したか
- どのスキル / ルールを使ったか
- どのテストを実行したか
- 未確認事項と残リスク
- 次の推奨アクション

## Missing Information Policy

以下のどれかが欠けている場合、勝手に前提固定せず不足として明示する。

- 環境差分
- 成功条件
- 既存資産の契約
- 影響範囲
- リリース条件

## Template Maintenance Rule

この `CLAUDE.md` は短く保つ。
長くなった場合は `docs/` か `.claude/rules/` に分割し、ここには参照関係と最重要ルールだけを残す。
