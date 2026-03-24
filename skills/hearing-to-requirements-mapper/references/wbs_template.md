# WBS Template for Software Projects

This template provides a standard Work Breakdown Structure for mapping requirements to project tasks.

## Standard WBS Structure

```
1. Requirements Phase (要件定義フェーズ)
├── 1.1 Requirements Analysis (要件分析)
│   ├── 1.1.1 Business Requirements Analysis (ビジネス要件分析)
│   ├── 1.1.2 Stakeholder Requirements Analysis (ステークホルダー要件分析)
│   ├── 1.1.3 Functional Requirements Analysis (機能要件分析)
│   └── 1.1.4 Non-Functional Requirements Analysis (非機能要件分析)
├── 1.2 Requirements Documentation (要件文書化)
│   ├── 1.2.1 Requirements Specification (要件仕様書作成)
│   ├── 1.2.2 Use Case Documentation (ユースケース文書化)
│   └── 1.2.3 Requirements Review (要件レビュー)
└── 1.3 Requirements Approval (要件承認)
    └── 1.3.1 Stakeholder Sign-off (ステークホルダー承認)

2. Design Phase (設計フェーズ)
├── 2.1 System Design (システム設計)
│   ├── 2.1.1 Architecture Design (アーキテクチャ設計)
│   ├── 2.1.2 Component Design (コンポーネント設計)
│   ├── 2.1.3 Integration Design (連携設計)
│   └── 2.1.4 Security Design (セキュリティ設計)
├── 2.2 Database Design (データベース設計)
│   ├── 2.2.1 Data Model Design (データモデル設計)
│   ├── 2.2.2 Schema Design (スキーマ設計)
│   └── 2.2.3 Data Migration Design (データ移行設計)
├── 2.3 UI/UX Design (UI/UX設計)
│   ├── 2.3.1 Wireframes (ワイヤーフレーム)
│   ├── 2.3.2 Mockups (モックアップ)
│   ├── 2.3.3 Prototype (プロトタイプ)
│   └── 2.3.4 Style Guide (スタイルガイド)
├── 2.4 API Design (API設計)
│   ├── 2.4.1 API Specification (API仕様)
│   └── 2.4.2 API Documentation (APIドキュメント)
└── 2.5 Design Review (設計レビュー)
    └── 2.5.1 Design Approval (設計承認)

3. Development Phase (開発フェーズ)
├── 3.1 Environment Setup (環境構築)
│   ├── 3.1.1 Development Environment (開発環境)
│   ├── 3.1.2 Test Environment (テスト環境)
│   └── 3.1.3 CI/CD Pipeline (CI/CDパイプライン)
├── 3.2 Core Development (コア開発)
│   ├── 3.2.1 Backend Development (バックエンド開発)
│   ├── 3.2.2 Frontend Development (フロントエンド開発)
│   ├── 3.2.3 Database Development (データベース開発)
│   └── 3.2.4 API Development (API開発)
├── 3.3 Feature Development (機能開発)
│   ├── 3.3.1 [Feature Module 1] (機能モジュール1)
│   ├── 3.3.2 [Feature Module 2] (機能モジュール2)
│   └── 3.3.N [Feature Module N] (機能モジュールN)
├── 3.4 Integration Development (連携開発)
│   ├── 3.4.1 External System Integration (外部システム連携)
│   └── 3.4.2 Internal System Integration (内部システム連携)
└── 3.5 Data Migration (データ移行)
    ├── 3.5.1 Data Extraction (データ抽出)
    ├── 3.5.2 Data Transformation (データ変換)
    └── 3.5.3 Data Loading (データロード)

4. Testing Phase (テストフェーズ)
├── 4.1 Unit Testing (単体テスト)
│   ├── 4.1.1 Backend Unit Tests (バックエンド単体テスト)
│   └── 4.1.2 Frontend Unit Tests (フロントエンド単体テスト)
├── 4.2 Integration Testing (結合テスト)
│   ├── 4.2.1 API Integration Tests (API結合テスト)
│   ├── 4.2.2 System Integration Tests (システム結合テスト)
│   └── 4.2.3 External Integration Tests (外部連携テスト)
├── 4.3 System Testing (システムテスト)
│   ├── 4.3.1 Functional Testing (機能テスト)
│   ├── 4.3.2 Performance Testing (性能テスト)
│   ├── 4.3.3 Security Testing (セキュリティテスト)
│   └── 4.3.4 Usability Testing (ユーザビリティテスト)
├── 4.4 User Acceptance Testing (受入テスト)
│   ├── 4.4.1 UAT Planning (UAT計画)
│   ├── 4.4.2 UAT Execution (UAT実施)
│   └── 4.4.3 UAT Sign-off (UAT承認)
└── 4.5 Bug Fixing (バグ修正)
    └── 4.5.1 Defect Resolution (不具合解消)

5. Deployment Phase (導入フェーズ)
├── 5.1 Deployment Planning (導入計画)
│   ├── 5.1.1 Release Planning (リリース計画)
│   ├── 5.1.2 Rollback Planning (ロールバック計画)
│   └── 5.1.3 Communication Planning (コミュニケーション計画)
├── 5.2 Production Environment (本番環境)
│   ├── 5.2.1 Infrastructure Setup (インフラ構築)
│   ├── 5.2.2 Security Configuration (セキュリティ設定)
│   └── 5.2.3 Monitoring Setup (監視設定)
├── 5.3 Deployment Execution (デプロイ実施)
│   ├── 5.3.1 Pre-deployment Checklist (デプロイ前チェック)
│   ├── 5.3.2 Deployment (デプロイ)
│   └── 5.3.3 Smoke Testing (スモークテスト)
├── 5.4 Data Migration Execution (データ移行実施)
│   ├── 5.4.1 Migration Rehearsal (移行リハーサル)
│   ├── 5.4.2 Production Migration (本番移行)
│   └── 5.4.3 Data Verification (データ検証)
└── 5.5 Go-Live (本番稼働)
    ├── 5.5.1 Go-Live Monitoring (本番監視)
    └── 5.5.2 Issue Resolution (問題解決)

6. Training & Documentation Phase (研修・文書化フェーズ)
├── 6.1 User Training (ユーザー研修)
│   ├── 6.1.1 Training Material Development (研修資料作成)
│   ├── 6.1.2 Training Delivery (研修実施)
│   └── 6.1.3 Training Evaluation (研修評価)
├── 6.2 Admin Training (管理者研修)
│   └── 6.2.1 System Administration Training (システム管理者研修)
└── 6.3 Documentation (文書化)
    ├── 6.3.1 User Manual (ユーザーマニュアル)
    ├── 6.3.2 Admin Manual (管理者マニュアル)
    └── 6.3.3 Technical Documentation (技術ドキュメント)

7. Project Management (プロジェクト管理)
├── 7.1 Planning & Control (計画・管理)
│   ├── 7.1.1 Project Planning (プロジェクト計画)
│   ├── 7.1.2 Progress Monitoring (進捗監視)
│   └── 7.1.3 Risk Management (リスク管理)
├── 7.2 Communication (コミュニケーション)
│   ├── 7.2.1 Stakeholder Communication (ステークホルダー連絡)
│   └── 7.2.2 Status Reporting (状況報告)
├── 7.3 Quality Assurance (品質保証)
│   ├── 7.3.1 Code Review (コードレビュー)
│   └── 7.3.2 Quality Audits (品質監査)
└── 7.4 Change Management (変更管理)
    └── 7.4.1 Change Request Processing (変更要求処理)
```

---

## Requirements to WBS Mapping Rules

### Business Requirements (BR)
| Requirement Type | Primary WBS Items | Secondary WBS Items |
|-----------------|-------------------|---------------------|
| Business goals | 1.1.1 | 7.1.1 |
| Success metrics | 1.1.1, 1.3.1 | 4.3.1 |
| ROI requirements | 1.1.1, 7.1.1 | - |

### Stakeholder Requirements (SR)
| Requirement Type | Primary WBS Items | Secondary WBS Items |
|-----------------|-------------------|---------------------|
| User roles | 1.1.2 | 2.1.4 |
| User workflows | 1.1.2, 2.3.x | 4.4.x |
| Training needs | 6.1.x, 6.2.x | - |
| Accessibility | 2.3.x | 4.3.4 |

### Functional Requirements (FR)
| Requirement Type | Primary WBS Items | Secondary WBS Items |
|-----------------|-------------------|---------------------|
| Core features | 3.3.x | 4.1.x, 4.3.1 |
| Data processing | 3.2.3 | 2.2.x |
| Integration | 3.4.x | 2.1.3, 4.2.x |
| Reports | 3.3.x | 4.3.1 |
| User interface | 3.2.2 | 2.3.x |

### Non-Functional Requirements (NFR)
| Requirement Type | Primary WBS Items | Secondary WBS Items |
|-----------------|-------------------|---------------------|
| Performance | 2.1.1, 4.3.2 | 5.2.x |
| Security | 2.1.4, 4.3.3 | 5.2.2 |
| Availability | 2.1.1, 5.2.x | 4.3.x |
| Scalability | 2.1.1 | 5.2.1 |
| Usability | 2.3.x, 4.3.4 | 6.1.x |
| Maintainability | 7.3.x | 6.3.x |

### Constraints (CON)
| Constraint Type | Primary WBS Items | Secondary WBS Items |
|-----------------|-------------------|---------------------|
| Technical | 2.1.1, 3.1.x | - |
| Budget | 7.1.1 | - |
| Schedule | 7.1.1, 7.1.2 | - |
| Regulatory | 2.1.4, 4.3.3 | 7.3.x |

---

## Feature Module Template

For each feature module in WBS 3.3.x, create sub-items based on the feature's requirements:

```
3.3.X [Feature Name] (機能名)
├── 3.3.X.1 Feature Analysis (機能分析)
├── 3.3.X.2 Feature Design (機能設計)
├── 3.3.X.3 Feature Development (機能開発)
│   ├── 3.3.X.3.1 Backend Implementation (バックエンド実装)
│   ├── 3.3.X.3.2 Frontend Implementation (フロントエンド実装)
│   └── 3.3.X.3.3 Data Model Implementation (データモデル実装)
├── 3.3.X.4 Feature Testing (機能テスト)
│   ├── 3.3.X.4.1 Unit Tests (単体テスト)
│   └── 3.3.X.4.2 Feature Tests (機能テスト)
└── 3.3.X.5 Feature Documentation (機能ドキュメント)
```

---

## WBS Mapping Output Format

```json
{
  "requirement_id": "FR-001",
  "wbs_items": [
    {
      "wbs_code": "3.3.1",
      "wbs_name": "User Authentication Module",
      "relationship": "primary",
      "notes": "Core implementation"
    },
    {
      "wbs_code": "4.1.2",
      "wbs_name": "Frontend Unit Tests",
      "relationship": "secondary",
      "notes": "Test coverage"
    }
  ],
  "estimated_effort_distribution": {
    "3.3.1": 0.7,
    "4.1.2": 0.3
  }
}
```

---

## Effort Distribution Guidelines

### By Project Phase (Typical)
| Phase | Percentage |
|-------|------------|
| Requirements | 10-15% |
| Design | 15-20% |
| Development | 35-40% |
| Testing | 20-25% |
| Deployment | 5-10% |
| PM | 10-15% |

### By Requirement Type
| Type | Design | Development | Testing |
|------|--------|-------------|---------|
| FR (Simple) | 10% | 70% | 20% |
| FR (Complex) | 20% | 50% | 30% |
| NFR (Performance) | 15% | 45% | 40% |
| NFR (Security) | 20% | 40% | 40% |
| Integration | 20% | 40% | 40% |
