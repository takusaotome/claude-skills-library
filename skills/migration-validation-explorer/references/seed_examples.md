# Seed Examples

Use these as "starter seeds" to accelerate discovery. Adapt nouns to your project.

---

## Seed Set 1: Random Focus Examples (10)

### 1. Timezone + DateTime Month-End Boundaries
**Focus:** Date fields used in reporting and reminders
**Hypotheses:**
- Records dated Jan 31 23:00 PST appear as Feb 1 in UTC-based reports
- Monthly close process misses records due to timezone
- Reminders fire on wrong day

**Verify:** Query records near month boundaries, compare report vs raw data

---

### 2. Recurring Invoice Generation
**Focus:** Invoice schedules and generation logic
**Hypotheses:**
- Schedule dates shifted during migration
- Edits before send not preserved
- Generation trigger didn't fire

**Verify:** Compare pending invoice dates source vs target

---

### 3. Approval Processes
**Focus:** Approval state, history, pending work items
**Hypotheses:**
- Approval state shows "Approved" but no history
- Pending approvals lost (no work items created)
- Approval reassigned to wrong user

**Verify:** Query ApprovalHistory, ProcessInstanceWorkitem

---

### 4. Security/Sharing Effects
**Focus:** Data visibility per user role
**Hypotheses:**
- Records exist but user reports "missing"
- Report total differs from admin query
- Sharing rule not migrated correctly

**Verify:** Run same report as Admin vs Business User, compare counts

---

### 5. Retired-Field Archiving
**Focus:** Fields marked for archiving, historical data
**Hypotheses:**
- Archived data not searchable
- Restore path untested
- Audit requirements not met

**Verify:** Search for archived records, attempt restore

---

### 6. Group-Company/Cross-Department Views
**Focus:** Hierarchy-based reporting, shared data
**Hypotheses:**
- Hierarchy broken during migration
- Dedupe merged wrong records
- Sharing exposes data incorrectly

**Verify:** Run cross-department report, verify hierarchy

---

### 7. Forecast/Actual Dashboards
**Focus:** Definition alignment, drill-down
**Hypotheses:**
- Forecast definition changed, shows wrong numbers
- Drill-down doesn't match summary
- Historical forecast not migrated

**Verify:** Compare dashboard to source report, test drill-down

---

### 8. Reminder Emails
**Focus:** Scheduled notifications, idempotency
**Hypotheses:**
- Reminder sent twice (not idempotent)
- Reminder not sent ("already handled" wrongly set)
- Wrong recipient after ownership change

**Verify:** Trigger test reminder, check email logs

---

### 9. View-Edit/Bulk Update
**Focus:** UI validation, bulk operations
**Hypotheses:**
- View edit allows invalid state
- Bulk update bypasses validation rule
- Required field shows as optional

**Verify:** Attempt invalid edit via UI, bulk update

---

### 10. External Integrations
**Focus:** Idempotency, partial failure, retry
**Hypotheses:**
- Retry creates duplicate
- Partial failure not logged
- Rate limit caused silent drop

**Verify:** Resend payload, check for duplicates

---

## Seed Set 2: Cross-Pollination Examples (10)

### 1. Automation Control x Invariants
**Lens Fusion:** Keep critical constraints even in migration mode
**Hypothesis:** Validation rule disabled for migration, invalid data loaded
**Apply to:** Required fields, status transitions
**Verify:** Query for records violating business rules

---

### 2. External IDs x Cross-Company Views
**Lens Fusion:** Audit relationship chain by key continuity
**Hypothesis:** External ID reused across companies, wrong lookup
**Apply to:** Account hierarchy, intercompany transactions
**Verify:** Check External ID uniqueness across orgs

---

### 3. GMT DateTime x Monthly Close
**Lens Fusion:** Introduce "business date" if needed
**Hypothesis:** UTC storage causes records to appear in wrong month
**Apply to:** Revenue recognition, monthly reporting
**Verify:** Query month-end records, compare business date vs stored

---

### 4. Multi-Currency x Recurring Billing
**Lens Fusion:** Conversion date must be explicit and consistent
**Hypothesis:** Invoice converted at wrong rate
**Apply to:** International invoices, multi-currency accounts
**Verify:** Reconcile invoice amounts in original vs converted currency

---

### 5. Cutover Window x Web/Email Intake
**Lens Fusion:** Event ledger to guarantee zero loss
**Hypothesis:** Records created during cutover lost or duplicated
**Apply to:** Lead capture, support ticket creation
**Verify:** Compare intake logs to records created during window

---

### 6. Duplicate Rules x Cross-Department Operations
**Lens Fusion:** Detect-first, merge-after strategy
**Hypothesis:** Duplicate rule blocks legitimate record
**Apply to:** Account/Contact creation across departments
**Verify:** Attempt to create known duplicate, check behavior

---

### 7. Backup/Restore x Archive Design
**Lens Fusion:** Archive must be restorable, not just stored
**Hypothesis:** Archived data cannot be restored
**Apply to:** Compliance records, historical transactions
**Verify:** Attempt restore from archive

---

### 8. Trigger/Flow Performance x Integration Retries
**Lens Fusion:** Two-click "duplication" prevention
**Hypothesis:** Slow trigger causes timeout, retry creates duplicate
**Apply to:** Integration endpoints, batch processes
**Verify:** Monitor trigger execution time, test retry behavior

---

### 9. User Training x Data Quality SLO
**Lens Fusion:** Teach with metrics; operate with dashboards
**Hypothesis:** Users create bad data because training didn't cover edge cases
**Apply to:** Data entry processes, required field usage
**Verify:** Review data quality dashboard trends post-migration

---

### 10. Address Ambiguity x Search/Dedupe
**Lens Fusion:** Separate display address vs normalization key
**Hypothesis:** Address normalization prevents finding records
**Apply to:** Property addresses, customer addresses
**Verify:** Search for records using original vs normalized address

---

## High-Impact Convergence Set

If you must prioritize, check these first:

| Priority | Check | Why High Impact |
|----------|-------|-----------------|
| 1 | Month-end boundaries | Affects reporting, reminders, compliance |
| 2 | Invoice totals + lifecycle | Direct revenue impact |
| 3 | Cross-department views | Security and data integrity |
| 4 | Migration-mode automation | Can cause storms or dead processes |
| 5 | Integration retry idempotency | Silent duplicates or drops |
| 6 | Archive usability | Compliance, audit requirements |
