---
paths:
  - "db/**/*"
  - "database/**/*"
  - "migrations/**/*"
  - "alembic/**/*"
  - "prisma/**/*"
  - "**/*.sql"
---

# DB / Migration Rules

- クエリやマイグレーション変更時は、ターゲット DB 方言と transaction 挙動を明示する。
- 本番と開発で DB が異なる場合は `production-parity-test-designer` 相当の観点を必ず入れる。
- schema change が 2 モジュール以上に影響する場合は `cross-module-consistency-auditor` 相当の確認を行う。
- forward だけでなく rollback、再実行、データ整合性も確認対象に含める。
- 生SQLを使う場合は、パラメータ化、方言依存、インデックス影響、NULL/集計挙動を明示する。
