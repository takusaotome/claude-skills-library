# Persona Selection Matrix

文書タイプに応じたペルソナ選定マトリクス。
各ペルソナの詳細定義は `references/agents/*.md` を参照。

---

| 文書タイプ | 必須ペルソナ | 推奨ペルソナ | オプション |
|-----------|-------------|-------------|-----------|
| 設計文書 | Developer, QA | Security, Ops | PM, Customer |
| 不具合分析レポート | Developer, QA, PM | Ops | Security, Customer |
| 要件定義書 | Developer, PM, Customer | QA | Security, Ops |
| 提案書・企画書 | PM, Customer | Developer | Security, Ops, QA |
| セキュリティ設計 | Security, Developer | Ops | PM, QA, Customer |
| 運用設計 | Ops, Developer | Security | PM, QA, Customer |
| テスト計画・結果 | Developer, QA, PM | - | Security, Ops, Customer |
| 移行計画 | Developer, Ops, PM | - | Security, QA, Customer |
| **汎用（デフォルト）** | Developer, PM, Customer | QA, Security, Ops | - |

## ペルソナ一覧

| ペルソナ | 一言概要 |
|---------|---------|
| Developer | 実装者視点: 技術的正確性、実装可能性 |
| PM | プロジェクト管理視点: リスク、整合性、実現性 |
| Customer | 顧客/ステークホルダー視点: 要件充足、ビジネス価値 |
| QA | 品質保証視点: テスト可能性、受入基準の明確性 |
| Security | セキュリティ/コンプライアンス視点: 脆弱性、データ保護 |
| Ops | 運用/SRE視点: 運用準備度、監視、障害対応 |

## 選定ガイドライン

- 最低3ペルソナ、最大6ペルソナまで選定可能
- 文書タイプに応じて適切な組み合わせを選択
- セキュリティ・運用の考慮が必要な文書は対応ペルソナを必ず含める
- ユーザーが「徹底レビュー」を指示した場合は全6ペルソナを使用
