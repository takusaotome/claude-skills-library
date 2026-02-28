# Database Design Guide

This reference provides comprehensive guidance for relational database design in technical specification documents. Use this guide when creating database design specifications (Workflow 4).

## 1. Naming Conventions

### General Rules

| Element | Convention | Example |
|---------|-----------|---------|
| Table name | snake_case, singular | `user`, `order_item` |
| Column name | snake_case | `first_name`, `created_at` |
| Primary key | `id` | `id` (BIGINT, auto-increment) |
| Foreign key | `{referenced_table}_id` | `user_id`, `department_id` |
| Junction table | `{table1}_{table2}` (alphabetical) | `project_user`, `order_tag` |
| Index | `idx_{table}_{columns}` | `idx_user_email` |
| Unique constraint | `uq_{table}_{columns}` | `uq_user_email` |
| Check constraint | `ck_{table}_{column}` | `ck_order_status` |
| Boolean column | `is_` or `has_` prefix | `is_active`, `has_permission` |
| Timestamp column | `_at` suffix | `created_at`, `deleted_at` |
| Date column | `_on` or `_date` suffix | `hired_on`, `birth_date` |

### Naming Anti-Patterns

| Anti-Pattern | Problem | Correct |
|-------------|---------|---------|
| `tbl_user` or `t_user` | Unnecessary prefix | `user` |
| `users` (plural) | Inconsistent with SQL conventions | `user` |
| `userID` or `userId` | camelCase | `user_id` |
| `fk_user_id` | Prefix exposes implementation | `user_id` |
| `data`, `info`, `value` | Too generic | Use specific names |
| `status` without context | Ambiguous type | Define allowed values |

### Reserved Words to Avoid

Avoid using these as table or column names (they are SQL reserved words):
`user`, `order`, `group`, `table`, `index`, `key`, `select`, `from`, `where`, `join`, `name`, `type`, `status`, `role`, `level`, `action`, `comment`

**Workaround strategies:**
- Prefix with domain context: `app_user`, `sales_order`
- Use more specific names: `account`, `purchase_order`
- Quote if unavoidable (not recommended): `"user"`, `"order"`

## 2. Data Type Selection Guide

### String Types

| Type | Use Case | Max Length | Notes |
|------|---------|-----------|-------|
| `VARCHAR(n)` | Known max length | Varies by DB | Use for emails (254), names (100), codes (50) |
| `TEXT` | Variable/long text | 65,535+ chars | Descriptions, notes, comments |
| `CHAR(n)` | Fixed-length codes | Fixed | Country codes (2), currency codes (3) |
| `UUID` | Globally unique IDs | 36 chars | Use native UUID type if available |

### Numeric Types

| Type | Use Case | Range | Notes |
|------|---------|-------|-------|
| `BIGINT` | Primary keys, counters | -2^63 to 2^63-1 | Default for PKs |
| `INTEGER` | Bounded counts | -2^31 to 2^31-1 | Quantities, ages |
| `SMALLINT` | Small enumerations | -32,768 to 32,767 | Status codes |
| `DECIMAL(p,s)` | Monetary values | Exact | `DECIMAL(12,2)` for currency |
| `FLOAT` / `DOUBLE` | Scientific data | Approximate | Never use for money |
| `BOOLEAN` | True/false flags | true/false | `is_active`, `has_verified` |

### Temporal Types

| Type | Use Case | Format | Notes |
|------|---------|--------|-------|
| `TIMESTAMP WITH TIME ZONE` | Events, audit trails | ISO 8601 | Always use TZ-aware |
| `TIMESTAMP` | DB-local timestamps | ISO 8601 | Only if TZ not needed |
| `DATE` | Calendar dates | YYYY-MM-DD | Birth dates, deadlines |
| `TIME` | Time of day | HH:MM:SS | Business hours |
| `INTERVAL` | Duration | Varies | SLA thresholds |

### Special Types

| Type | Use Case | Notes |
|------|---------|-------|
| `JSONB` (PostgreSQL) | Semi-structured data | Metadata, config, flexible attributes |
| `ARRAY` | Multi-valued columns | Tags, permissions (use junction table if queried) |
| `ENUM` | Fixed value sets | Prefer CHECK constraint or lookup table for flexibility |
| `BYTEA` / `BLOB` | Binary data | Avoid; use object storage + URL reference |

### Type Selection Decision Tree

1. Is it a unique identifier? -> `BIGINT` (sequential) or `UUID` (distributed)
2. Is it money? -> `DECIMAL(p,s)` (never FLOAT)
3. Is it a point in time? -> `TIMESTAMP WITH TIME ZONE`
4. Is it a calendar date? -> `DATE`
5. Is it true/false? -> `BOOLEAN`
6. Is it a count or quantity? -> `INTEGER` or `BIGINT`
7. Is it a short string with known max? -> `VARCHAR(n)`
8. Is it free-form text? -> `TEXT`
9. Is it semi-structured? -> `JSONB` (PostgreSQL) or `TEXT` + application parsing

## 3. Normalization

### First Normal Form (1NF)

**Rule:** Every column contains atomic (indivisible) values; no repeating groups.

**Violation:**
```
| id | name  | phone_numbers          |
|----|-------|------------------------|
| 1  | Taro  | 090-1111-2222, 080-3333-4444 |
```

**Correction:** Create a separate `phone_number` table:
```
user: id, name
phone_number: id, user_id (FK), number, type (mobile/home/work)
```

### Second Normal Form (2NF)

**Rule:** No partial dependency — every non-key column depends on the entire primary key (relevant for composite PKs).

**Violation (composite PK: student_id + course_id):**
```
| student_id | course_id | student_name | grade |
```
`student_name` depends only on `student_id`, not on the full composite key.

**Correction:** Separate student data:
```
student: id, name
enrollment: student_id (FK), course_id (FK), grade
```

### Third Normal Form (3NF)

**Rule:** No transitive dependency — non-key columns depend only on the primary key, not on other non-key columns.

**Violation:**
```
| id | department_id | department_name | department_location |
```
`department_name` and `department_location` depend on `department_id`, not on `id`.

**Correction:** Separate department data:
```
employee: id, department_id (FK)
department: id, name, location
```

### When to Denormalize

Denormalization introduces controlled redundancy for performance. Use sparingly and document the rationale.

| Scenario | Technique | Trade-off |
|----------|----------|-----------|
| Read-heavy dashboards | Materialized views | Stale data risk |
| Reporting tables | Star/snowflake schema | Write complexity |
| Frequently joined lookups | Embed as column | Update anomalies |
| Audit/history tables | Full snapshot per event | Storage cost |
| Search/autocomplete | Denormalized search table | Sync overhead |

**Documentation requirement:** When denormalizing, always document:
1. Which normal form is violated
2. Why the violation is acceptable
3. How data consistency is maintained (triggers, application logic, ETL)

## 4. Index Strategy

### Index Types

| Type | Use Case | Notes |
|------|---------|-------|
| B-tree (default) | Equality, range, sorting | Most common; default in PostgreSQL/MySQL |
| Hash | Exact equality only | Faster for `=` but no range support |
| GIN | Full-text search, JSONB, arrays | PostgreSQL specific |
| GiST | Geometric, range, full-text | PostgreSQL specific |
| Partial | Subset of rows | `WHERE is_active = true` |
| Covering | Include non-key columns | Index-only scans |

### Composite Index Column Order

The column order in a composite index determines which queries it can serve.

**Rule: Put the most selective (highest cardinality) column first, and follow the query's WHERE/ORDER BY clause.**

```sql
-- Query: WHERE status = 'active' AND department_id = 5 ORDER BY created_at DESC
-- Index: idx_user_status_dept_created (status, department_id, created_at DESC)
```

**Leftmost prefix rule:** A composite index `(A, B, C)` supports queries on:
- `A` alone
- `A, B` together
- `A, B, C` together

It does NOT support queries on `B` alone, `C` alone, or `B, C` together.

### Index Decision Matrix

| Query Pattern | Index Type | Example |
|--------------|-----------|---------|
| `WHERE col = value` | B-tree (single column) | `idx_user_email` |
| `WHERE col1 = v AND col2 = v` | B-tree (composite) | `idx_order_user_status` |
| `WHERE col BETWEEN a AND b` | B-tree | `idx_order_created_at` |
| `WHERE col LIKE 'prefix%'` | B-tree | `idx_product_name` |
| `WHERE col LIKE '%substr%'` | GIN + trigram | `idx_product_name_trgm` |
| `WHERE json_col @> '{"key":"val"}'` | GIN | `idx_metadata_gin` |
| `ORDER BY col` | B-tree | `idx_user_created_at` |
| `COUNT(*)` with filter | Partial index | `idx_order_active` |

### Indexes to Always Create

1. **Primary key** — Automatically indexed
2. **Foreign keys** — Index every FK column (prevents table scans on JOINs and cascading deletes)
3. **Unique constraints** — Automatically indexed (email, employee_code, etc.)
4. **Frequently filtered columns** — `status`, `is_active`, `type`
5. **Sort columns** — `created_at`, `updated_at` (for recent-first queries)

### Indexes to Avoid

1. **Low-cardinality columns alone** — `boolean` columns (use partial index instead)
2. **Rarely queried columns** — Indexes have write overhead
3. **Small tables** — Tables under 1000 rows rarely benefit from indexes
4. **Too many indexes** — Each index slows INSERT/UPDATE/DELETE

## 5. Audit Columns Standard

### Required Audit Columns

Every table MUST include these columns:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `created_at` | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | Record creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NO | CURRENT_TIMESTAMP | Last modification timestamp |
| `created_by` | VARCHAR(100) or BIGINT | NO | — | User/system that created the record |
| `updated_by` | VARCHAR(100) or BIGINT | NO | — | User/system that last modified the record |

### Soft Delete Columns (Optional)

For tables that require soft delete:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `deleted_at` | TIMESTAMP WITH TIME ZONE | YES | NULL | Deletion timestamp (NULL = not deleted) |
| `deleted_by` | VARCHAR(100) or BIGINT | YES | NULL | User/system that deleted the record |

**Soft delete query pattern:**
```sql
-- Active records only
SELECT * FROM user WHERE deleted_at IS NULL;

-- All records including deleted
SELECT * FROM user;

-- Deleted records only
SELECT * FROM user WHERE deleted_at IS NOT NULL;
```

**Unique constraint with soft delete:**
```sql
-- Partial unique index (PostgreSQL)
CREATE UNIQUE INDEX uq_user_email_active ON user(email) WHERE deleted_at IS NULL;
```

### Version Column (Optional)

For optimistic locking:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `version` | INTEGER | NO | 1 | Optimistic lock version counter |

## 6. Common Design Patterns

### Polymorphic Associations

When multiple tables reference a shared entity:

**Approach 1: Shared FK with type discriminator**
```
comment: id, commentable_type ('post'/'product'/'order'), commentable_id, body
```

**Approach 2: Separate FK columns (preferred for referential integrity)**
```
comment: id, post_id (FK, nullable), product_id (FK, nullable), order_id (FK, nullable), body
CHECK (
  (post_id IS NOT NULL)::int +
  (product_id IS NOT NULL)::int +
  (order_id IS NOT NULL)::int = 1
)
```

### Self-Referential Relationships

For hierarchies (org chart, categories, comments):

```
category: id, name, parent_id (FK -> category.id, nullable)
```

**Query pattern (recursive CTE):**
```sql
WITH RECURSIVE tree AS (
  SELECT id, name, parent_id, 0 AS depth
  FROM category WHERE parent_id IS NULL
  UNION ALL
  SELECT c.id, c.name, c.parent_id, t.depth + 1
  FROM category c JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

### Many-to-Many with Junction Table

Always model many-to-many relationships with an explicit junction table:

```
project: id, name
user: id, name
project_member: id, project_id (FK), user_id (FK), role, joined_at
  UNIQUE(project_id, user_id)
```

**Junction table rules:**
1. Has its own surrogate PK (`id`)
2. Contains FKs to both related tables
3. Has a unique constraint on the FK pair
4. May contain relationship attributes (role, joined_at, etc.)

### Enum Columns vs Lookup Tables

**Enum column (CHECK constraint):**
```sql
status VARCHAR(20) NOT NULL CHECK (status IN ('draft', 'active', 'archived'))
```
**Use when:** Values are fixed and rarely change.

**Lookup table:**
```
order_status: id, code, display_name, sort_order, is_active
```
**Use when:** Values may change, need display names, or are referenced across multiple tables.

### Temporal Tables (History/Audit Trail)

For tracking changes over time:

```
user: id, name, email, status (current state)
user_history: id, user_id (FK), name, email, status, changed_at, changed_by, change_type ('INSERT'/'UPDATE'/'DELETE')
```

**Implementation:** Use database triggers or application-level event sourcing.

## 7. Migration Considerations

### Forward Migration Checklist

When designing schema changes, document:

- [ ] New tables: CREATE TABLE statements with all constraints
- [ ] New columns: ALTER TABLE ADD COLUMN with defaults for existing rows
- [ ] New indexes: CREATE INDEX CONCURRENTLY (to avoid locks)
- [ ] Data backfill: UPDATE statements for existing rows
- [ ] Foreign keys: Ensure referenced data exists before adding FK constraints
- [ ] Application code changes: Deploy code that handles both old and new schema

### Backward-Compatible Changes (Online Migration Safe)

| Change | Safe? | Notes |
|--------|-------|-------|
| Add nullable column | Yes | No lock, no data change |
| Add column with default | Yes* | *PostgreSQL 11+ only |
| Add index concurrently | Yes | Use CONCURRENTLY keyword |
| Create new table | Yes | No existing data affected |
| Rename column | No | Breaks existing queries |
| Drop column | No | Requires code change first |
| Change column type | No | Requires data migration |
| Add NOT NULL constraint | No | Requires backfill first |

### Migration Documentation Template

```markdown
## Migration: {MIGRATION_ID} — {Description}

### Changes
- Add column `phone` (VARCHAR(20), nullable) to `user` table
- Create index `idx_user_phone` on `user(phone)`

### Forward Migration
1. ALTER TABLE user ADD COLUMN phone VARCHAR(20);
2. CREATE INDEX CONCURRENTLY idx_user_phone ON user(phone);

### Backward Migration (Rollback)
1. DROP INDEX idx_user_phone;
2. ALTER TABLE user DROP COLUMN phone;

### Data Backfill
- None required (nullable column)

### Estimated Duration
- Table size: ~1M rows
- Add column: < 1 second
- Create index: ~30 seconds
```

## 8. Database Design Checklist

Before finalizing any database design specification, verify:

- [ ] All tables use singular, snake_case names
- [ ] All columns use snake_case names
- [ ] Every table has a `BIGINT id` primary key (or documented alternative)
- [ ] Every foreign key column has an index
- [ ] Every table has audit columns (`created_at`, `updated_at`, `created_by`, `updated_by`)
- [ ] Soft delete tables have `deleted_at` and `deleted_by` columns
- [ ] Data types are appropriate (DECIMAL for money, TIMESTAMP WITH TIME ZONE for events)
- [ ] Normalization level is documented (with denormalization rationale if applicable)
- [ ] Unique constraints are defined for natural keys (email, code, etc.)
- [ ] CHECK constraints are defined for enum columns
- [ ] Junction tables are used for many-to-many relationships
- [ ] ER diagram matches the column definitions
- [ ] Index strategy is documented with rationale
- [ ] Migration path is documented (forward and rollback)
