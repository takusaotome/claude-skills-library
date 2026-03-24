# Requirements Classification Framework

This document provides the classification framework for organizing requirements extracted from hearing sheets and meeting notes.

## Classification Categories

### 1. Business Requirements (BR)

**Definition:** High-level statements of goals, objectives, or needs that the organization wants to achieve.

**Characteristics:**
- Focus on business outcomes, not technical implementation
- Answer "why" the project exists
- Measurable in business terms (ROI, efficiency, revenue)

**Examples:**
| Japanese | English | Classification |
|----------|---------|----------------|
| 売上を20%増加させる | Increase sales by 20% | BR |
| 顧客満足度を向上させる | Improve customer satisfaction | BR |
| 業務効率を改善する | Improve operational efficiency | BR |

**Identification patterns:**
- Contains business metrics (売上、コスト、満足度 / sales, cost, satisfaction)
- References organizational goals
- Lacks technical specificity

---

### 2. Stakeholder Requirements (SR)

**Definition:** Needs of specific user groups or organizational roles that must be satisfied by the solution.

**Characteristics:**
- Tied to specific user roles or personas
- Describe what users need to accomplish
- Bridge between business requirements and functional requirements

**Examples:**
| Japanese | English | Classification |
|----------|---------|----------------|
| 営業担当者は外出先から顧客情報にアクセスできる必要がある | Sales reps need to access customer data while on the go | SR |
| 管理者は全ユーザーの権限を管理できる | Administrators can manage permissions for all users | SR |
| カスタマーサポートは通話履歴を確認できる | Customer support can view call history | SR |

**Identification patterns:**
- Contains role references (営業、管理者、ユーザー / sales, admin, user)
- "〜は〜できる必要がある" / "〜 needs to 〜"
- Describes user capabilities or needs

---

### 3. Functional Requirements (FR)

**Definition:** Specific behaviors, functions, or capabilities that the system must provide.

**Characteristics:**
- Technical or system-focused
- Describe what the system "shall do"
- Testable with clear pass/fail criteria

**Examples:**
| Japanese | English | Classification |
|----------|---------|----------------|
| システムはメールアドレス形式を検証する | System shall validate email address format | FR |
| ログイン失敗が3回でアカウントをロックする | System locks account after 3 failed login attempts | FR |
| 検索結果を10件ずつ表示する | Display search results in pages of 10 items | FR |

**Identification patterns:**
- "システムは〜する" / "System shall/will/must 〜"
- Technical verbs (検証、処理、保存、表示 / validate, process, store, display)
- Specific system behaviors

---

### 4. Non-Functional Requirements (NFR)

**Definition:** Quality attributes that define how the system performs its functions.

**Sub-categories:**

#### 4.1 Performance (PERF)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Response Time | 応答時間 | Response time | < 3秒 / < 3 seconds |
| Throughput | スループット | Throughput | 1000 TPS |
| Capacity | キャパシティ | Capacity | 同時10,000ユーザー / 10,000 concurrent users |

#### 4.2 Security (SEC)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Authentication | 認証 | Authentication | 多要素認証 / MFA required |
| Authorization | 認可 | Authorization | ロールベースアクセス制御 / RBAC |
| Encryption | 暗号化 | Encryption | AES-256, TLS 1.3 |

#### 4.3 Availability (AVAIL)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Uptime | 稼働率 | Uptime | 99.9% |
| MTTR | 平均復旧時間 | Mean time to recovery | < 1時間 / < 1 hour |
| Failover | フェイルオーバー | Failover | 自動切替 / Automatic failover |

#### 4.4 Scalability (SCALE)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Horizontal | 水平拡張 | Horizontal scaling | Auto-scaling対応 |
| Data Growth | データ増加 | Data growth | 年間20%増加対応 |

#### 4.5 Usability (USE)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Learnability | 習得容易性 | Learnability | 1時間研修で基本操作習得 |
| Accessibility | アクセシビリティ | Accessibility | WCAG 2.1 Level AA |

#### 4.6 Maintainability (MAINT)
| Attribute | Japanese | English | Metric Example |
|-----------|----------|---------|----------------|
| Modularity | モジュール性 | Modularity | マイクロサービスアーキテクチャ |
| Testability | テスト容易性 | Testability | 80%カバレッジ |

---

### 5. Constraints (CON)

**Definition:** Limitations or restrictions that constrain the solution design.

**Categories:**

| Category | Japanese | English | Examples |
|----------|----------|---------|----------|
| Technical | 技術制約 | Technical | 既存Oracle DB使用、Java 17必須 |
| Budget | 予算制約 | Budget | 初期投資1000万円以内 |
| Schedule | スケジュール制約 | Schedule | 2025年4月本番稼働必須 |
| Regulatory | 規制制約 | Regulatory | 個人情報保護法準拠、PCI-DSS対応 |
| Organizational | 組織制約 | Organizational | 社内リソース限定、外部委託禁止 |

---

### 6. Assumptions (ASM)

**Definition:** Conditions believed to be true for project planning purposes.

**Examples:**
| Japanese | English | Risk if False |
|----------|---------|---------------|
| ユーザーは安定したインターネット環境を持つ | Users have stable internet connectivity | オフライン機能追加が必要 |
| 既存システムのAPIは変更されない | Existing system APIs will not change | 追加開発・テストが必要 |
| 現行業務プロセスは変更しない | Current business processes will not change | 業務分析の再実施が必要 |

---

## Priority Classification (MoSCoW)

### Must Have (必須)

**Definition:** Absolutely essential for the solution to work. Project fails without these.

**Indicators:**
- 法規制要件 / Regulatory requirements
- 基本的なビジネス機能 / Core business functions
- セキュリティ基盤 / Security fundamentals
- "必須"、"不可欠"、"必要" / "must", "required", "essential"

### Should Have (推奨)

**Definition:** Important but not vital. Workaround exists if not included.

**Indicators:**
- 重要だが代替手段あり / Important but alternatives exist
- 効率向上機能 / Efficiency improvements
- "重要"、"推奨"、"できれば" / "important", "should", "preferably"

### Could Have (可能なら)

**Definition:** Nice to have. Included only if time and budget allow.

**Indicators:**
- 利便性向上 / Convenience features
- 将来的に価値 / Future value
- "あれば良い"、"可能なら" / "nice to have", "if possible"

### Won't Have (対象外)

**Definition:** Explicitly out of scope for this project/phase.

**Indicators:**
- 将来フェーズで検討 / Consider in future phases
- 他プロジェクトで対応 / Addressed by other projects
- "今回は対象外"、"スコープ外" / "out of scope", "not this release"

---

## Classification Decision Tree

```
Is it about business outcomes/goals?
├─ Yes → Business Requirement (BR)
└─ No
   └─ Is it tied to a specific user role?
      ├─ Yes → Stakeholder Requirement (SR)
      └─ No
         └─ Is it a system behavior/function?
            ├─ Yes → Functional Requirement (FR)
            └─ No
               └─ Is it a quality attribute?
                  ├─ Yes → Non-Functional Requirement (NFR)
                  │        └─ Sub-classify: PERF/SEC/AVAIL/SCALE/USE/MAINT
                  └─ No
                     └─ Is it a limitation/restriction?
                        ├─ Yes → Constraint (CON)
                        └─ No → Assumption (ASM)
```

---

## Requirement ID Format

**Standard format:** `{TYPE}-{SEQUENCE}`

| Type | Prefix | Example |
|------|--------|---------|
| Business Requirement | BR | BR-001 |
| Stakeholder Requirement | SR | SR-001 |
| Functional Requirement | FR | FR-001 |
| Non-Functional Requirement | NFR | NFR-001 |
| Constraint | CON | CON-001 |
| Assumption | ASM | ASM-001 |

**Extended format with category:** `{TYPE}-{CATEGORY}-{SEQUENCE}`

Examples:
- `NFR-SEC-001` (Security NFR)
- `FR-AUTH-001` (Authentication functional requirement)
- `NFR-PERF-003` (Performance NFR)

---

## Quality Criteria for Requirements

### SMART Criteria

| Criterion | Japanese | Description |
|-----------|----------|-------------|
| Specific | 具体的 | Clear, unambiguous language |
| Measurable | 測定可能 | Quantifiable success criteria |
| Achievable | 達成可能 | Technically and practically feasible |
| Relevant | 関連性 | Aligned with business objectives |
| Time-bound | 期限設定 | Has defined timeline or phase |

### Additional Quality Checks

| Check | Japanese | Description |
|-------|----------|-------------|
| Atomic | 原子性 | Single requirement per statement |
| Consistent | 一貫性 | No conflicts with other requirements |
| Traceable | 追跡可能 | Linked to source and downstream artifacts |
| Testable | テスト可能 | Clear pass/fail criteria |
| Necessary | 必要性 | Supports business objective |
| Implementation-free | 実装非依存 | Describes what, not how |

---

## Common Classification Mistakes

### 1. Mixing solution with requirement

**Wrong:** "システムはReactを使用する" (System uses React)
**Right:** "システムはモダンブラウザで動作するSPAを提供する" (System provides SPA that works on modern browsers)

### 2. Vague non-functional requirements

**Wrong:** "システムは高速に動作する" (System operates quickly)
**Right:** "平均応答時間は3秒以内とする" (Average response time shall be under 3 seconds)

### 3. Combining multiple requirements

**Wrong:** "ユーザーはログインして検索し結果をエクスポートできる"
**Right:** Split into:
- FR-001: ユーザーはログインできる
- FR-002: ユーザーは検索できる
- FR-003: ユーザーは結果をエクスポートできる

### 4. Confusing stakeholder needs with functional requirements

**Wrong (as FR):** "営業部門は売上データにアクセスしたい"
**Right:**
- SR-001: 営業部門は売上データにアクセスできる必要がある
- FR-001: システムは売上データの閲覧機能を提供する
