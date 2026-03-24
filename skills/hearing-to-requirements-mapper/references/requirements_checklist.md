# Requirements Completeness Checklist

This checklist is used to identify gaps and missing requirements during gap analysis.

## 1. Business Requirements / ビジネス要件

### 1.1 Project Context / プロジェクト背景
- [ ] Business problem/opportunity clearly defined / ビジネス課題・機会が明確
- [ ] Strategic alignment documented / 戦略との整合性が記載
- [ ] Success metrics defined / 成功指標が定義
- [ ] Target users/customers identified / 対象ユーザー・顧客が特定
- [ ] Market or competitive context provided / 市場・競合状況が説明

### 1.2 Business Objectives / ビジネス目標
- [ ] Quantifiable goals (revenue, cost, time) / 定量的目標（売上、コスト、時間）
- [ ] Timeline for achieving goals / 目標達成期限
- [ ] Baseline measurements / 現状のベースライン数値
- [ ] ROI expectations / ROI期待値
- [ ] Risk tolerance defined / リスク許容度の定義

---

## 2. Stakeholder Requirements / ステークホルダー要件

### 2.1 User Identification / ユーザー特定
- [ ] All user roles identified / 全ユーザーロールが特定
- [ ] User personas documented / ユーザーペルソナが文書化
- [ ] User volume estimates / ユーザー数の見積もり
- [ ] Geographic distribution / 地理的分布
- [ ] Language requirements / 言語要件

### 2.2 User Needs / ユーザーニーズ
- [ ] Primary tasks for each role / 各ロールの主要タスク
- [ ] Pain points documented / 課題・問題点の文書化
- [ ] Workflow requirements / ワークフロー要件
- [ ] Device/platform needs / デバイス・プラットフォームニーズ
- [ ] Accessibility needs / アクセシビリティニーズ

---

## 3. Functional Requirements / 機能要件

### 3.1 Core Functions / コア機能
- [ ] All major features listed / 全主要機能がリスト化
- [ ] Feature prioritization (MoSCoW) / 機能優先順位（MoSCoW）
- [ ] User stories or use cases / ユーザーストーリーまたはユースケース
- [ ] Business rules documented / ビジネスルールの文書化
- [ ] Workflow/process requirements / ワークフロー・プロセス要件

### 3.2 Data Requirements / データ要件
- [ ] Data entities identified / データエンティティが特定
- [ ] Data relationships defined / データ関係が定義
- [ ] Data volume estimates / データ量の見積もり
- [ ] Data quality requirements / データ品質要件
- [ ] Data retention policies / データ保持ポリシー
- [ ] Data migration requirements / データ移行要件

### 3.3 Integration Requirements / 連携要件
- [ ] External systems listed / 外部システムがリスト化
- [ ] Integration methods specified / 連携方法が指定
- [ ] API requirements / API要件
- [ ] Data exchange formats / データ交換フォーマット
- [ ] Integration frequency / 連携頻度
- [ ] Error handling requirements / エラーハンドリング要件

### 3.4 Reporting Requirements / レポート要件
- [ ] Report types identified / レポートタイプが特定
- [ ] Report frequency / レポート頻度
- [ ] Export formats / エクスポート形式
- [ ] Dashboard requirements / ダッシュボード要件
- [ ] Ad-hoc query needs / アドホッククエリニーズ

### 3.5 Input/Output Requirements / 入出力要件
- [ ] Input data sources / 入力データソース
- [ ] Input validation rules / 入力検証ルール
- [ ] Output formats / 出力形式
- [ ] Print requirements / 印刷要件
- [ ] File import/export / ファイルインポート・エクスポート

---

## 4. Non-Functional Requirements / 非機能要件

### 4.1 Performance / パフォーマンス
- [ ] Response time requirements / 応答時間要件
- [ ] Throughput requirements / スループット要件
- [ ] Concurrent user capacity / 同時ユーザー数
- [ ] Data processing volume / データ処理量
- [ ] Batch processing requirements / バッチ処理要件
- [ ] Peak load handling / ピーク負荷対応

### 4.2 Security / セキュリティ
- [ ] Authentication requirements / 認証要件
- [ ] Authorization requirements / 認可要件
- [ ] Data encryption requirements / データ暗号化要件
- [ ] Audit logging requirements / 監査ログ要件
- [ ] Session management / セッション管理
- [ ] Password policies / パスワードポリシー
- [ ] Security compliance (PCI-DSS, HIPAA, etc.) / セキュリティ準拠
- [ ] Vulnerability assessment / 脆弱性評価
- [ ] Penetration testing requirements / ペネトレーションテスト要件

### 4.3 Availability / 可用性
- [ ] Uptime requirements / 稼働率要件
- [ ] Scheduled maintenance windows / 計画メンテナンス枠
- [ ] Recovery time objective (RTO) / 目標復旧時間
- [ ] Recovery point objective (RPO) / 目標復旧ポイント
- [ ] Disaster recovery requirements / 災害復旧要件
- [ ] Backup requirements / バックアップ要件
- [ ] Failover requirements / フェイルオーバー要件

### 4.4 Scalability / 拡張性
- [ ] Growth projections / 成長予測
- [ ] Horizontal scaling needs / 水平スケーリングニーズ
- [ ] Vertical scaling needs / 垂直スケーリングニーズ
- [ ] Multi-tenancy requirements / マルチテナント要件
- [ ] Geographic expansion plans / 地理的拡大計画

### 4.5 Usability / ユーザビリティ
- [ ] User interface standards / ユーザーインターフェース標準
- [ ] Accessibility requirements (WCAG) / アクセシビリティ要件
- [ ] Localization requirements / ローカライゼーション要件
- [ ] Help/documentation requirements / ヘルプ・ドキュメント要件
- [ ] Training requirements / 研修要件
- [ ] Error message standards / エラーメッセージ標準

### 4.6 Maintainability / 保守性
- [ ] Code standards / コーディング標準
- [ ] Documentation requirements / ドキュメント要件
- [ ] Monitoring requirements / 監視要件
- [ ] Logging requirements / ログ出力要件
- [ ] Configuration management / 構成管理
- [ ] Version control requirements / バージョン管理要件

### 4.7 Compatibility / 互換性
- [ ] Browser requirements / ブラウザ要件
- [ ] OS requirements / OS要件
- [ ] Device requirements / デバイス要件
- [ ] Legacy system compatibility / レガシーシステム互換性
- [ ] Third-party software compatibility / サードパーティソフトウェア互換性

---

## 5. Constraints / 制約条件

### 5.1 Technical Constraints / 技術制約
- [ ] Technology stack requirements / 技術スタック要件
- [ ] Existing infrastructure limitations / 既存インフラ制限
- [ ] Development environment constraints / 開発環境制約
- [ ] Deployment environment constraints / デプロイ環境制約
- [ ] Licensing constraints / ライセンス制約

### 5.2 Budget Constraints / 予算制約
- [ ] Total budget defined / 総予算の定義
- [ ] Budget breakdown by phase / フェーズ別予算
- [ ] Contingency allowance / 予備費
- [ ] Ongoing operational budget / 継続運用予算

### 5.3 Schedule Constraints / スケジュール制約
- [ ] Project start date / プロジェクト開始日
- [ ] Key milestones / 主要マイルストーン
- [ ] Hard deadlines / 絶対期限
- [ ] Dependencies on other projects / 他プロジェクトとの依存関係
- [ ] Resource availability constraints / リソース利用可能性制約

### 5.4 Regulatory Constraints / 規制制約
- [ ] Applicable regulations identified / 適用規制の特定
- [ ] Compliance requirements / コンプライアンス要件
- [ ] Audit requirements / 監査要件
- [ ] Data privacy requirements (GDPR, etc.) / データプライバシー要件
- [ ] Industry-specific regulations / 業界固有規制

### 5.5 Organizational Constraints / 組織制約
- [ ] Approval processes / 承認プロセス
- [ ] Change management requirements / 変更管理要件
- [ ] Stakeholder availability / ステークホルダー可用性
- [ ] Internal resource constraints / 社内リソース制約
- [ ] Outsourcing policies / 外注ポリシー

---

## 6. Assumptions / 前提条件

### 6.1 Technical Assumptions / 技術前提
- [ ] Infrastructure availability / インフラ利用可能性
- [ ] API stability / API安定性
- [ ] Network connectivity / ネットワーク接続性
- [ ] System integration readiness / システム連携準備状況

### 6.2 Business Assumptions / ビジネス前提
- [ ] Business process stability / ビジネスプロセス安定性
- [ ] Stakeholder commitment / ステークホルダーコミットメント
- [ ] Market conditions / 市場状況
- [ ] Regulatory stability / 規制安定性

### 6.3 Resource Assumptions / リソース前提
- [ ] Team availability / チーム可用性
- [ ] Skill availability / スキル可用性
- [ ] Budget availability / 予算可用性
- [ ] Third-party vendor availability / サードパーティベンダー可用性

---

## 7. Gap Severity Classification

### Critical (重大) - Must resolve before proceeding
- Missing core functionality requirements
- Missing security requirements for sensitive data
- Missing regulatory compliance requirements
- Conflicting high-priority requirements

### High (高) - Should resolve before development
- Missing non-functional requirements with business impact
- Ambiguous functional requirements
- Missing acceptance criteria for Must Have items
- Missing integration specifications

### Medium (中) - Should resolve before design freeze
- Incomplete stakeholder requirements
- Missing usability requirements
- Ambiguous Should Have requirements
- Missing data quality requirements

### Low (低) - Can resolve during development
- Missing Could Have requirements detail
- Nice-to-have clarifications
- Documentation gaps
- Training requirements

---

## 8. Gap Analysis Output Template

```markdown
## Gap Analysis Report

### Summary
- Total gaps identified: [N]
- Critical: [N] | High: [N] | Medium: [N] | Low: [N]

### Gap Details

#### GAP-001: [Gap Title]
- **Severity:** Critical/High/Medium/Low
- **Category:** [Missing/Ambiguous/Conflicting/Incomplete]
- **Section:** [Checklist section reference]
- **Description:** [What is missing or unclear]
- **Impact:** [Consequence if not resolved]
- **Recommendation:** [How to resolve]
- **Owner:** [Who should resolve]
- **Target Date:** [When to resolve]

[Repeat for each gap]

### Resolution Priority
1. [GAP-XXX] - [Brief description]
2. [GAP-XXX] - [Brief description]
...
```
