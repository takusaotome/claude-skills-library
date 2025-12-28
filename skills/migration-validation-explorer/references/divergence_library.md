# Divergence Library

Use this library to force variety during the Diverge phase. Generate 6-12 hypotheses per cycle.

## Failure Mode Categories

### 1. Value Correctness
- Range violations (min/max, business rules)
- Unit/scale errors (cents vs dollars, bytes vs KB)
- Rounding discrepancies
- Precision loss in conversion
- Encoding issues (UTF-8, special chars)

### 2. Nullability/Required Fields
- Required field missing after transform
- Null vs empty string handling
- Default value not applied
- Conditional required logic not enforced

### 3. Type/Format Errors
- String to number parsing failures
- Date format mismatches (MM/DD vs DD/MM)
- Boolean representation differences (Y/N, 1/0, true/false)
- Enum/picklist value case sensitivity

### 4. Relationship Integrity
- Missing lookup targets (orphaned references)
- Incorrect lookup resolution (wrong parent)
- Cardinality violations (1:1 became 1:N)
- Circular reference creation
- Self-referential loop

### 5. Identity/Dedup Issues
- Duplicate keys created
- Near-duplicate not detected
- Merge logic created data loss
- External ID collision across sources

### 6. Temporal Boundary Issues
- Month-end date assignment errors
- DST transition handling
- Timezone conversion errors
- Business date vs system date mismatch
- Leap year edge cases

### 7. Automation Side-Effects
- Trigger fired unexpectedly during load
- Trigger didn't fire when expected
- Workflow created duplicate records
- Approval process in wrong state
- Notification storm generated
- Performance degradation from automation

### 8. Security Visibility Issues
- Record "missing" due to sharing rules
- Report shows different count than query
- User sees stale cached data
- Profile permission blocking access
- Cross-department visibility broken

### 9. Report Consistency Issues
- Filter logic changed after migration
- Rollup calculation differs
- Drill-down doesn't match summary
- Currency conversion in report differs
- Historical report broken

### 10. Integration Behavior Issues
- Idempotency failure (duplicates on retry)
- Payload schema drift
- Partial success not handled
- Error not logged/alerted
- Rate limit caused silent drops

### 11. Archive/Restore Issues
- Archived data not searchable
- Restore path broken
- Audit history incomplete
- Retention policy violated

### 12. Usability Regressions
- View edit allows invalid states
- Bulk update bypasses validation
- Required field shows as optional
- Picklist shows obsolete values

---

## Minimal Experiment Patterns

Use these fast convergence patterns to verify hypotheses:

### Boundary Sampling
- Month-end records (28th-1st)
- DST transition dates
- Leap year dates (Feb 29)
- Midnight boundary (00:00-01:00)
- Year-end (Dec 31 - Jan 1)

### Orphan Scan
```sql
-- Children without parents
SELECT COUNT(*) FROM Child__c
WHERE Parent__c IS NULL OR Parent__c NOT IN (SELECT Id FROM Parent__c)

-- Parents without children (where required)
SELECT COUNT(*) FROM Parent__c
WHERE Id NOT IN (SELECT Parent__c FROM Child__c)
```

### Reconciliation
- Count by segment (status, type, region)
- Sum by segment (amount, quantity)
- Compare source totals vs target totals
- Verify audit trail continuity

### Duplicate Scan
```sql
-- Exact duplicates
SELECT ExternalId__c, COUNT(*)
FROM Object__c
GROUP BY ExternalId__c
HAVING COUNT(*) > 1

-- Fuzzy duplicates (name similarity)
-- Use matching rules or custom similarity function
```

### Two-Lens Check
- Admin query vs business user report
- API response vs UI display
- System of record vs integration log
- Report total vs drill-down sum

### Replay Test
- Resend integration payload
- Verify no duplicate created
- Confirm idempotency key respected

### Output Diff
- PDF generated vs source fields
- Email template vs record data
- Report export vs query results
