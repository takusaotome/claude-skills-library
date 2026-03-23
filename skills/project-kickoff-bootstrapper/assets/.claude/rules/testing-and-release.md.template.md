---
paths:
  - "tests/**/*"
  - ".github/workflows/**/*"
  - "ci/**/*"
  - "scripts/**/*"
  - "Makefile"
  - "package.json"
  - "pyproject.toml"
---

# Testing / Release Rules

- テスト設計では unit / integration / e2e / production parity の責務を混同しない。
- 高リスク変更で happy path だけしかない場合は不十分として扱う。
- `QUALITY_GATES.md` に定義した必須証跡とテスト結果を結びつける。
- packaging / container build / runtime dependency がある場合は、本番同等確認を検討する。
- リリース判定では、通ったテストだけでなく未実施テストと残リスクも明示する。
