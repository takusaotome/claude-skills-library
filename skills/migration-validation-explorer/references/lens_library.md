# Lens Library for Cross-Pollination

Pick **two lenses** and fuse them to create hypotheses that standard checklists won't generate.

## Available Lenses

### CRM Migration Pitfalls
- External ID conflicts across source systems
- Picklist value drift (source vs target mappings)
- Lookup cardinality changes (1:1 vs 1:N)
- Ownership/licensing constraints
- Record type mapping gaps
- Currency field precision loss
- Activity history completeness

### Real-Estate Domain Pitfalls
- Lease lifecycle state machines
- Unit/address ambiguity (Suite vs Unit vs #)
- Broker/agent role hierarchies
- Property hierarchy (Building > Floor > Unit)
- Rent roll calculations
- Vacancy vs occupied status timing
- Square footage rounding

### Data Pipeline Pitfalls
- Join key reuse across loads
- Normalization side effects (address standardization breaking matches)
- Schema drift between runs
- Incremental vs full load conflicts
- CDC (Change Data Capture) gaps
- Backfill overlap with live data

### QA Pitfalls
- Sampling bias (only testing happy paths)
- Over-reliance on target system constraints
- Silent fallback logic hiding issues
- "Admin-only truth" (missing user perspective)
- Assuming source is authoritative
- Testing with sanitized data only

### Automation Pitfalls
- Approval state not reconstructed
- Notification storms on bulk load
- Scheduler drift after migration
- "Migration mode" left enabled
- Trigger order dependencies
- Flow interview limits

### Finance Pitfalls
- Rounding accumulation errors
- Currency conversion date ambiguity
- Invoice lifecycle state mismatch
- Tax calculation timing
- Revenue recognition cutoff
- Intercompany elimination

### Security Pitfalls
- Sharing rules vs reporting visibility gap
- Cross-org data exposure
- Role hierarchy reporting effects
- Field-level security blocking migration
- Guest user access after migration

---

## Cross-Pollination Examples

### Lens A + Lens B -> Hypothesis

1. **CRM Migration + Finance**
   - External ID reuse might cause invoice double-counting in reports

2. **Real-Estate + Data Pipeline**
   - Address normalization might break lease-to-property joins

3. **QA + Security**
   - Admin test passed but business user sees different data due to sharing

4. **Automation + CRM Migration**
   - Approval history not migrated leaves workflows in limbo state

5. **Finance + Automation**
   - Currency conversion trigger fires on load, applying wrong rate

6. **Data Pipeline + Real-Estate**
   - Incremental load misses lease renewals due to status filter

7. **Security + Reporting**
   - Cross-department report shows different totals per user

8. **QA + Data Pipeline**
   - Test data normalization differs from production normalization

9. **CRM Migration + Automation**
   - Record Type change triggers unexpected flow

10. **Finance + QA**
    - Rounding tested with small numbers, fails at scale

---

## Salesforce-Specific Watchlist

Use these as forced prompts during cross-pollination:

### Date vs DateTime + Timezone
- Month-end boundaries shift across timezones
- DST transitions create 23/25 hour days
- Per-locale display differs from stored value
- Report grouping by date may shift records

### Automation During Import
- What must fire vs must NOT fire?
- Document "migration mode" strategy explicitly
- Test with automation on AND off

### Validation Rules
- Which invariants are non-negotiable?
- Which can be temporarily relaxed?
- Re-enable validation post-migration

### Duplicate/Matching Rules
- Block vs warn vs report-only mode
- Affects both load success and cleanup
- Test with rules enabled

### Multi-Currency
- Conversion date: when is rate applied?
- Rounding rules: per line vs total
- Report sums: converted currency vs original
- Test reconciliation explicitly

### Approvals & Reminders
- Approval state is behavioral data, not just fields
- Pending approvals need work item reconstruction
- Scheduled actions may not transfer
- Test BEHAVIOR, not just field values

### Security & Reporting
- Per-user visibility changes report totals
- Verify with persona-based access checks
- Admin query != business user report

### Governor Limits
- Batch size during load
- Trigger recursion limits
- Flow interview limits
- API call limits during integration test
