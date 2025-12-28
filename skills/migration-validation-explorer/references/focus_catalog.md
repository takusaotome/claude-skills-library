# Focus Catalog

Build a catalog of >= 20 candidate focus areas. Keep it diverse so random selection works.

## Category Buckets

### Keys/IDs
- External IDs: uniqueness, formatting, nullability
- Legacy key retention and mapping
- Cross-system ID synchronization
- Composite key handling

### Relationships
- Parent/child integrity (Account-Contact, Invoice-LineItems)
- Many-to-many junction objects
- Circular reference detection
- Load order dependencies
- Orphan records (children without parents)

### Normalization
- Names: casing, whitespace, special characters
- Addresses: unit numbers, city/state inference, postal codes
- Phone/email formatting and validation
- International character handling

### Status/Stage
- Picklist value mapping
- Default fallbacks for unmapped values
- "Unknown" bucket handling
- Status lifecycle consistency

### Ownership & Security
- OwnerId mapping and fallbacks
- Queue assignments
- Licensing constraints
- Sharing rule implications
- Role hierarchy effects

### Dates/Time
- Date vs DateTime field types
- Timezone conversion and storage
- Month-end boundaries
- DST transitions
- Lifecycle date consistency (Created <= Modified <= Closed)

### Money
- Currency parsing and precision
- Rounding rules
- Rollups vs raw values
- Negative value handling
- Multi-currency conversion dates
- Exchange rate application

### Volume/Dedup
- Record counts by segment
- Exact duplicate detection
- Near-duplicate/fuzzy matching
- Merge strategy validation
- Historical duplicate cleanup

### Documents
- PDF/template generation
- Attachment migration
- File link integrity
- Legacy document mapping
- Size/format constraints

### Automation
- Triggers/flows: suppressed vs active during migration
- Approval processes: state reconstruction
- Scheduled jobs/reminders
- Notification rules
- "Migration mode" switch behavior

### Integrations
- Idempotency key handling
- Retry behavior and deduplication
- Partial failure recovery
- Backfill completeness
- Rate limit handling
- Error log correlation

### Reporting
- Report filter compatibility
- Rollup/summary accuracy
- Drill-down consistency
- Per-user visibility effects
- Dashboard refresh timing

### Archiving
- Retired field handling
- History retention rules
- Restore path verification
- Audit trail requirements
- Searchability of archived data

### Operations
- Monitoring and alerting
- Reconciliation procedures
- Runbook completeness
- Cutover window drift control
- Rollback procedures
