# Database Design: {TBL_ID} — {TABLE_DISPLAY_NAME}

---

## Table Overview

| Field | Value |
|-------|-------|
| Table ID | {TBL_ID} |
| Table Name | `{TABLE_NAME}` |
| Schema | {SCHEMA_NAME} (e.g., public) |
| Description | {TABLE_DESCRIPTION} |
| Mapped Requirements | {REQ_IDS} |
| Estimated Row Count | {ESTIMATED_ROWS} |
| Retention Policy | {RETENTION_POLICY} |
| Status | Draft / Approved / Deprecated |

---

## Column Definitions

| # | Column Name | Data Type | Nullable | Default | Description | Constraints |
|---|------------|-----------|----------|---------|-------------|-------------|
| 1 | id | BIGINT | NO | AUTO_INCREMENT | Primary key, auto-generated surrogate key | PK |
| 2 | {COL_NAME_1} | {COL_TYPE_1} | {NULLABLE_1} | {DEFAULT_1} | {COL_DESC_1} | {CONSTRAINT_1} |
| 3 | {COL_NAME_2} | {COL_TYPE_2} | {NULLABLE_2} | {DEFAULT_2} | {COL_DESC_2} | {CONSTRAINT_2} |
| 4 | {COL_NAME_3} | {COL_TYPE_3} | {NULLABLE_3} | {DEFAULT_3} | {COL_DESC_3} | {CONSTRAINT_3} |
| 5 | {COL_NAME_4} | {COL_TYPE_4} | {NULLABLE_4} | {DEFAULT_4} | {COL_DESC_4} | {CONSTRAINT_4} |
| 6 | {COL_NAME_5} | {COL_TYPE_5} | {NULLABLE_5} | {DEFAULT_5} | {COL_DESC_5} | {CONSTRAINT_5} |
| 7 | created_at | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | Record creation timestamp | — |
| 8 | updated_at | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | Last modification timestamp | — |
| 9 | created_by | VARCHAR(100) | NO | — | User or system that created the record | — |
| 10 | updated_by | VARCHAR(100) | NO | — | User or system that last modified the record | — |
| 11 | deleted_at | TIMESTAMP WITH TIME ZONE | YES | NULL | Soft delete timestamp (NULL = active) | — |
| 12 | deleted_by | VARCHAR(100) | YES | NULL | User or system that deleted the record | — |

**Notes:**
- Columns 7-10 (audit columns) are mandatory for every table
- Columns 11-12 (soft delete columns) are included when soft delete is required
- Remove columns 11-12 if hard delete is used for this table

---

## Primary Key

| Constraint Name | Column(s) | Type |
|----------------|----------|------|
| pk_{TABLE_NAME} | id | PRIMARY KEY |

---

## Unique Constraints

| Constraint Name | Column(s) | Condition | Description |
|----------------|----------|-----------|-------------|
| uq_{TABLE_NAME}_{COL_1} | {UNIQUE_COL_1} | {UNIQUE_CONDITION_1} | {UNIQUE_DESC_1} |
| uq_{TABLE_NAME}_{COL_2} | {UNIQUE_COL_2} | WHERE deleted_at IS NULL | {UNIQUE_DESC_2} (active records only) |

**Note:** When using soft delete, add `WHERE deleted_at IS NULL` as a partial unique constraint to allow re-creation of deleted records.

---

## Foreign Keys

| Constraint Name | Column | References | On Delete | On Update | Description |
|----------------|--------|-----------|-----------|-----------|-------------|
| fk_{TABLE_NAME}_{REF_TABLE_1} | {FK_COL_1} | {REF_TABLE_1}(id) | {ON_DELETE_1} | CASCADE | {FK_DESC_1} |
| fk_{TABLE_NAME}_{REF_TABLE_2} | {FK_COL_2} | {REF_TABLE_2}(id) | {ON_DELETE_2} | CASCADE | {FK_DESC_2} |

**On Delete Options:**

| Option | When to Use |
|--------|------------|
| CASCADE | Child records should be deleted with parent |
| SET NULL | Child records should remain but lose parent reference |
| RESTRICT | Prevent deletion if child records exist |
| NO ACTION | Same as RESTRICT (deferred check) |

---

## Check Constraints

| Constraint Name | Column | Expression | Description |
|----------------|--------|-----------|-------------|
| ck_{TABLE_NAME}_{COL} | {CHECK_COL_1} | {CHECK_EXPR_1} | {CHECK_DESC_1} |

**Example expressions:**

```sql
-- Status enum
CHECK (status IN ('draft', 'active', 'archived', 'deleted'))

-- Non-negative amount
CHECK (amount >= 0)

-- Date range
CHECK (end_date > start_date)

-- Exclusive FK (polymorphic)
CHECK (
  (post_id IS NOT NULL)::int +
  (comment_id IS NOT NULL)::int = 1
)
```

---

## Indexes

| Index Name | Column(s) | Type | Unique | Partial Condition | Description |
|-----------|----------|------|--------|-------------------|-------------|
| pk_{TABLE_NAME} | id | B-tree | Yes | — | Primary key (auto-created) |
| idx_{TABLE_NAME}_{COL_1} | {INDEX_COL_1} | B-tree | No | — | {INDEX_DESC_1} |
| idx_{TABLE_NAME}_{COL_2} | {INDEX_COL_2} | B-tree | No | WHERE deleted_at IS NULL | {INDEX_DESC_2} (active records only) |
| idx_{TABLE_NAME}_{COL_3}_{COL_4} | {INDEX_COL_3}, {INDEX_COL_4} | B-tree | No | — | Composite index for {INDEX_DESC_3} |
| idx_{TABLE_NAME}_created_at | created_at | B-tree | No | — | Recent records sorting |

**Index Design Rationale:**

| Index | Supports Query Pattern | Expected Benefit |
|-------|----------------------|-----------------|
| idx_{TABLE_NAME}_{COL_1} | `WHERE {COL_1} = ?` | {BENEFIT_1} |
| idx_{TABLE_NAME}_{COL_2} | `WHERE {COL_2} = ? AND deleted_at IS NULL` | {BENEFIT_2} |
| idx_{TABLE_NAME}_{COL_3}_{COL_4} | `WHERE {COL_3} = ? AND {COL_4} = ?` | {BENEFIT_3} |

---

## ER Diagram

```mermaid
erDiagram
    {TABLE_NAME} {
        bigint id PK
        {COL_TYPE_1} {COL_NAME_1} {COL_KEY_1}
        {COL_TYPE_2} {COL_NAME_2} {COL_KEY_2}
        {COL_TYPE_3} {COL_NAME_3}
        {COL_TYPE_4} {COL_NAME_4}
        {COL_TYPE_5} {COL_NAME_5}
        timestamp created_at
        timestamp updated_at
        varchar created_by
        varchar updated_by
        timestamp deleted_at
        varchar deleted_by
    }

    {RELATED_TABLE_1} {
        bigint id PK
        bigint {TABLE_NAME}_id FK
    }

    {RELATED_TABLE_2} {
        bigint id PK
    }

    {TABLE_NAME} ||--o{ {RELATED_TABLE_1} : "{RELATIONSHIP_1}"
    {TABLE_NAME} }o--|| {RELATED_TABLE_2} : "{RELATIONSHIP_2}"
```

---

## Sample Data

**Purpose:** Illustrate expected data patterns and validate column definitions.

| id | {COL_NAME_1} | {COL_NAME_2} | {COL_NAME_3} | created_at | updated_at |
|----|-------------|-------------|-------------|-----------|-----------|
| 1 | {SAMPLE_1_COL1} | {SAMPLE_1_COL2} | {SAMPLE_1_COL3} | 2025-01-15 09:30:00+09 | 2025-01-15 09:30:00+09 |
| 2 | {SAMPLE_2_COL1} | {SAMPLE_2_COL2} | {SAMPLE_2_COL3} | 2025-01-16 10:00:00+09 | 2025-01-17 14:20:00+09 |
| 3 | {SAMPLE_3_COL1} | {SAMPLE_3_COL2} | {SAMPLE_3_COL3} | 2025-01-17 11:45:00+09 | 2025-01-17 11:45:00+09 |

**Notes:**
- Sample data should include edge cases (NULL values, boundary values)
- Include at least one soft-deleted record if soft delete is used
- Timestamps should use the production timezone

---

## Migration Notes

### Forward Migration (Create Table)

```sql
-- Migration: {MIGRATION_ID}
-- Description: Create {TABLE_NAME} table

CREATE TABLE {TABLE_NAME} (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    {COL_NAME_1} {COL_TYPE_1} {COL_NULLABLE_SQL_1} {COL_DEFAULT_SQL_1},
    {COL_NAME_2} {COL_TYPE_2} {COL_NULLABLE_SQL_2} {COL_DEFAULT_SQL_2},
    {COL_NAME_3} {COL_TYPE_3} {COL_NULLABLE_SQL_3} {COL_DEFAULT_SQL_3},
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) NOT NULL,
    updated_by VARCHAR(100) NOT NULL,
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by VARCHAR(100),

    CONSTRAINT uq_{TABLE_NAME}_{COL_1} UNIQUE ({UNIQUE_COL_1}),
    CONSTRAINT fk_{TABLE_NAME}_{REF_TABLE_1} FOREIGN KEY ({FK_COL_1})
        REFERENCES {REF_TABLE_1}(id) ON DELETE {ON_DELETE_1} ON UPDATE CASCADE,
    CONSTRAINT ck_{TABLE_NAME}_{CHECK_COL} CHECK ({CHECK_EXPR_1})
);

-- Indexes
CREATE INDEX idx_{TABLE_NAME}_{COL_1} ON {TABLE_NAME}({INDEX_COL_1});
CREATE INDEX idx_{TABLE_NAME}_{COL_2} ON {TABLE_NAME}({INDEX_COL_2})
    WHERE deleted_at IS NULL;
CREATE INDEX idx_{TABLE_NAME}_created_at ON {TABLE_NAME}(created_at);

-- Auto-update updated_at trigger
CREATE OR REPLACE FUNCTION update_{TABLE_NAME}_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_{TABLE_NAME}_updated_at
    BEFORE UPDATE ON {TABLE_NAME}
    FOR EACH ROW
    EXECUTE FUNCTION update_{TABLE_NAME}_updated_at();

-- Comment
COMMENT ON TABLE {TABLE_NAME} IS '{TABLE_DESCRIPTION}';
```

### Backward Migration (Rollback)

```sql
-- Rollback: {MIGRATION_ID}
DROP TRIGGER IF EXISTS trg_{TABLE_NAME}_updated_at ON {TABLE_NAME};
DROP FUNCTION IF EXISTS update_{TABLE_NAME}_updated_at();
DROP TABLE IF EXISTS {TABLE_NAME};
```

### Data Backfill

```sql
-- Required if migrating from an existing table or seeding initial data
-- {BACKFILL_DESCRIPTION}

{BACKFILL_SQL}
```

### Migration Estimates

| Metric | Value |
|--------|-------|
| Estimated table size (1 year) | {ESTIMATED_SIZE} |
| Migration duration | {MIGRATION_DURATION} |
| Requires downtime | Yes / No |
| Dependencies | {MIGRATION_DEPENDENCIES} |

---

## Related Tables

| Table ID | Table Name | Relationship | Description |
|----------|-----------|-------------|-------------|
| {RELATED_TBL_ID_1} | {RELATED_TABLE_1} | {REL_TYPE_1} (e.g., parent) | {RELATED_DESC_1} |
| {RELATED_TBL_ID_2} | {RELATED_TABLE_2} | {REL_TYPE_2} (e.g., child) | {RELATED_DESC_2} |

---

## Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|----------|----------------------|
| {DECISION_1} | {RATIONALE_1} | {ALTERNATIVES_1} |
| {DECISION_2} | {RATIONALE_2} | {ALTERNATIVES_2} |

**Example decisions to document:**
- Why a specific data type was chosen (e.g., JSONB vs separate table)
- Why denormalization was used (or avoided)
- Why a specific index strategy was chosen
- Why soft delete vs hard delete was chosen
