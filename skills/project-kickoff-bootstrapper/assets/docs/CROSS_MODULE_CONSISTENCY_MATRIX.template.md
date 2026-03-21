# CROSS_MODULE_CONSISTENCY_MATRIX

## Purpose

同一仕様が複数モジュール・複数フロー・複数ジョブに散っている場合の変更漏れを防ぐための管理表。

## Matrix

| Business Rule / Behavior | Modules / Files / Flows Affected | Shared or Duplicated? | Required Updates | Test Coverage | Owner | Status |
|---|---|---|---|---|---|---|
| Example: Refund total calculation | API, batch, admin screen, export job | Duplicated | 4箇所更新 | unit + integration |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

## Consistency Checklist

- [ ] 仕様が複数箇所に散っていないか確認した
- [ ] コピペ箇所を特定した
- [ ] 共通化候補を検討した
- [ ] 更新漏れ候補を列挙した
- [ ] テスト対象を全フローにひも付けた
- [ ] レビュー対象者に影響範囲を共有した
