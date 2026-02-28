---
name: technical-spec-writer
description: >
  要件定義と実装の間を埋める技術仕様書を体系的に作成するスキル。
  画面設計、API設計、DB設計、シーケンス図、状態遷移図をMermaid形式で生成し、
  IEEE 830/ISO 29148準拠の仕様書を出力する。Use when creating functional
  specifications, API design documents, database design documents, screen design
  specifications, or sequence/state diagrams from requirements. Triggers:
  "technical specification", "functional spec", "API design", "database design",
  "screen design", "画面設計書", "API設計書", "DB設計書", "技術仕様書",
  "シーケンス図", "状態遷移図"
---

# Technical Spec Writer（技術仕様書作成）

## Overview

This skill bridges the gap between requirements definition (BRD/User Stories) and implementation by producing structured, standards-compliant technical specification documents. It generates screen designs, API specifications, database designs, sequence diagrams, and state transition diagrams using Mermaid notation, following IEEE 830 and ISO/IEC/IEEE 29148 standards.

## When to Use

- 要件定義（BRD）から技術仕様書を作成する
- 画面設計書を作成する
- API設計書を作成する
- DB設計書を作成する
- シーケンス図や状態遷移図を作成する
- 既存仕様書のレビューや改善を行う
- 要件からトレーサビリティマトリクスを作成する

## Workflows

### Workflow 1: Requirements Intake（要件取り込み）

**Purpose**: Gather and structure input requirements to determine document scope.

1. **Receive input** — Accept BRD, user stories, verbal requirements, or existing partial specs
2. **Determine document scope** — Classify the requested output:
   - 全体仕様書（Full functional specification）
   - 画面設計書（Screen design specification）
   - API設計書（API design specification）
   - DB設計書（Database design specification）
   - 個別ダイアグラム（Individual diagram）
3. **Create document outline** — Establish the ID numbering scheme:
   - SCR-xxx for screens
   - API-xxx for endpoints
   - TBL-xxx for tables
   - SEQ-xxx for sequence diagrams
   - STS-xxx for state diagrams
4. **Establish traceability** — Build a REQ-xxx to SCR/API/TBL mapping table to ensure every requirement is addressed
5. **Confirm scope with user** — Present the outline and confirm before proceeding
6. **Load** `references/spec_writing_standards.md` for ID conventions and quality criteria

### Workflow 2: Screen Design Specification（画面設計）

**Purpose**: Produce detailed screen design documents with UI elements, events, and transitions.

1. **Assign SCR-IDs** — Number each screen sequentially (SCR-001, SCR-002, ...)
2. **Define UI elements table** for each screen:

   | Element ID | Type | Label | Validation Rules | Default Value | Notes |
   |-----------|------|-------|-----------------|--------------|-------|
   | SCR-001-E01 | text | User Name | Required, max 50 chars | — | — |

3. **Define event table** for each screen:

   | Event ID | Trigger Element | Event Type | Action | Target |
   |----------|----------------|------------|--------|--------|
   | SCR-001-EV01 | btn_submit | click | POST /api/v1/users | SCR-002 |

4. **Create screen transition diagram** — Use Mermaid `stateDiagram-v2` to visualize navigation flow
5. **Add responsive breakpoint notes** — Document layout changes at standard breakpoints (mobile 375px, tablet 768px, desktop 1024px+)
6. **Reference** `references/mermaid_diagram_patterns.md` for diagram syntax
7. **Output** using `assets/functional_spec_template_ja.md` or `assets/functional_spec_template_en.md`

### Workflow 3: API Design Specification（API設計）

**Purpose**: Produce REST API specifications with endpoints, schemas, and sequence diagrams.

1. **Assign API-IDs** — Number each endpoint sequentially (API-001, API-002, ...)
2. **Define each endpoint**:
   - HTTP Method and Path
   - Description and authentication requirements
   - Request parameters, headers, and body (JSON schema)
   - Response body (success and error)
   - Error codes with business error code mapping
3. **Provide request/response JSON examples** — Include realistic sample data
4. **Standardize error codes** — Use the error envelope pattern from `references/api_design_guide.md`
5. **Create sequence diagrams** — For multi-service or complex flows, produce Mermaid `sequenceDiagram`
6. **Load** `references/api_design_guide.md` for REST conventions
7. **Output** using `assets/api_spec_template.md` for per-endpoint detail

### Workflow 4: Database Design Specification（DB設計）

**Purpose**: Produce database design documents with table definitions, ER diagrams, and indexes.

1. **Assign TBL-IDs** — Number each table sequentially (TBL-001, TBL-002, ...)
2. **Define column definition table** for each table:

   | Column Name | Data Type | Nullable | Default | Description | Constraints |
   |------------|-----------|----------|---------|-------------|-------------|
   | id | BIGINT | NO | AUTO_INCREMENT | Primary key | PK |

3. **Create ER diagram** — Use Mermaid `erDiagram` to visualize relationships
4. **Define index table** — Document all indexes with type, columns, and purpose
5. **Include audit columns** — Ensure every table has: `created_at`, `updated_at`, `created_by`, `updated_by`
6. **Add soft delete support** where appropriate — `deleted_at` column
7. **Load** `references/db_design_guide.md` for naming conventions and normalization guidance
8. **Output** using `assets/db_design_template.md` for per-table detail

### Workflow 5: Sequence Diagram Creation（シーケンス図）

**Purpose**: Produce Mermaid sequence diagrams for system interaction flows.

1. **Identify participants** — Categorize actors:
   - Actor (user)
   - Frontend (browser/app)
   - Backend (API server)
   - Database
   - External API / Third-party services
2. **Map message flow** — Document request/response patterns for the target scenario
3. **Add conditional branches** — Use `alt`, `opt`, `loop` fragments as needed
4. **Add notes and activations** — Clarify processing steps and active lifelines
5. **Output** Mermaid `sequenceDiagram` code block
6. **Reference** `references/mermaid_diagram_patterns.md` for syntax patterns

### Workflow 6: State Transition Diagram Creation（状態遷移図）

**Purpose**: Produce state machines for entities with lifecycle behavior.

1. **Build state inventory table**:

   | State ID | Name | Description | Entry Condition | Exit Condition |
   |----------|------|-------------|----------------|----------------|
   | STS-001 | Draft | Initial state | Record created | Submit action |

2. **Build transition table**:

   | From State | Event/Trigger | Guard Condition | Action | To State |
   |-----------|--------------|----------------|--------|----------|
   | Draft | Submit | All required fields filled | Validate & save | Pending Review |

3. **Create state transition matrix** — States as rows, events as columns, target state in cells
4. **Output** Mermaid `stateDiagram-v2` code block
5. **Reference** `references/mermaid_diagram_patterns.md` for state diagram syntax

### Workflow 7: Document Assembly（ドキュメント組み立て）

**Purpose**: Assemble individual sections into a complete specification document.

1. **Generate table of contents** — Auto-generate from section headers
2. **Cross-reference validation** — Verify all IDs are referenced correctly:
   - Every REQ-xxx maps to at least one SCR/API/TBL
   - Every SCR-xxx event references a valid API-xxx or screen target
   - Every API-xxx references valid TBL-xxx tables
3. **Quality checklist** — Verify the document meets IEEE 830 criteria:
   - [ ] Completeness — All requirements addressed
   - [ ] Consistency — No contradictions between sections
   - [ ] Traceability — Bidirectional mapping maintained
   - [ ] Unambiguity — No vague language ("appropriate", "etc.", "as needed")
   - [ ] Verifiability — Each requirement can be tested
   - [ ] Modifiability — Modular structure with clear cross-references
4. **Select output template** — Use the appropriate template from `assets/`:
   - Full spec: `functional_spec_template_ja.md` or `functional_spec_template_en.md`
   - API only: `api_spec_template.md`
   - DB only: `db_design_template.md`
5. **Fill template placeholders** — Replace all `{PLACEHOLDER}` values with actual content

## Resources

| File | Purpose | When to Load |
|------|---------|-------------|
| `references/spec_writing_standards.md` | IEEE 830/ISO 29148 standards, ID conventions, quality criteria | Workflow 1 (Requirements Intake), Workflow 7 (Document Assembly) |
| `references/mermaid_diagram_patterns.md` | Mermaid syntax patterns for all diagram types | Workflow 2, 5, 6 (any diagram creation) |
| `references/api_design_guide.md` | REST design principles, error formats, pagination | Workflow 3 (API Design) |
| `references/db_design_guide.md` | Naming conventions, normalization, index strategy | Workflow 4 (DB Design) |
| `assets/functional_spec_template_ja.md` | Full functional spec template (Japanese) | Workflow 7 when output language is Japanese |
| `assets/functional_spec_template_en.md` | Full functional spec template (English) | Workflow 7 when output language is English |
| `assets/api_spec_template.md` | Per-endpoint API specification template | Workflow 3, 7 for API-focused output |
| `assets/db_design_template.md` | Per-table database design template | Workflow 4, 7 for DB-focused output |

---

## Best Practices

### Do's
- 各設計要素にIDを採番し、要件とのトレーサビリティを維持する
- 曖昧な用語（「適切な」「必要に応じて」「等」）を避け、SHALL/SHOULD/MAYで記述する
- 画面・API・DBの相互参照を検証してから出力する
- Mermaidダイアグラムは方向・命名規則を統一する
- テンプレートのプレースホルダーを一つ残らず置換する

### Don'ts
- 要件の取りこぼしを放置しない（トレーサビリティマトリクスで確認）
- 1つの画面設計に複数の関心事を混在させない
- APIの正常系だけ記述してエラー系を省略しない
- インデックス戦略なしにテーブル定義だけ書かない

---

## Examples

### 例1: ECサイト商品管理画面の技術仕様書

```
User: 商品管理画面の技術仕様書を作成してください。
      要件: 商品CRUD、カテゴリ管理、画像アップロード、在庫管理

Claude:
1. [Workflow 1] 要件取り込み → SCR-001〜003、API-001〜008、TBL-001〜004 を採番
2. [Workflow 2] 画面設計 → 商品一覧(SCR-001)、商品登録/編集(SCR-002)、カテゴリ管理(SCR-003)
3. [Workflow 3] API設計 → GET/POST/PUT/DELETE /api/v1/products、POST /api/v1/images
4. [Workflow 4] DB設計 → products、categories、product_images、inventory テーブル + ER図
5. [Workflow 7] 組み立て → functional_spec_template_ja.md で出力
```

### 例2: API設計書のみ作成

```
User: 認証APIの設計書だけ作ってください。JWT認証です。

Claude:
1. [Workflow 1] スコープ: API設計のみ → API-001〜003（login, refresh, logout）
2. [Workflow 3] 各エンドポイントの詳細設計（リクエスト/レスポンス/エラー）
3. [Workflow 5] 認証フローのシーケンス図（Client → API → DB → JWT発行）
4. [Workflow 7] api_spec_template.md で出力
```
