---
paths:
  - "src/api/**/*"
  - "src/backend/**/*"
  - "app/api/**/*"
  - "server/**/*"
  - "{{MAIN_SOURCE_DIR}}/**/*.py"
  - "{{MAIN_SOURCE_DIR}}/**/*.ts"
---

# Backend / API Rules

- 既存サービス、共通関数、ラッパーを流用する場合は、必要に応じて `hidden-contract-investigator` 相当の手順を先に行う。
- 認可、機微データ、ファイルI/O、外部API、SQL を含む場合は `safe-by-default-architect` の観点で実装方針を選ぶ。
- 成功レスポンスや UI メッセージだけで成功とみなさず、必要に応じて永続化・副作用・外部連携結果まで確認する。
- 入力バリデーション、認可判定、エラー処理、監査可能性を考慮する。
- 高リスク変更では integration test 以上を必須候補とする。
