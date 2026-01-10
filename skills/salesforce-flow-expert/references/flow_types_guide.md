# Flow Types Guide

Complete guide for choosing and implementing the right Flow type for your use case.

## Flow Type Decision Matrix

| Flow Type | Trigger | User Interaction | Best For | Runs As |
|-----------|---------|------------------|----------|---------|
| **Screen Flow** | User action | Yes | Guided processes, data entry, wizards | Current user |
| **Record-Triggered** | Record change | No | Automated logic, field updates | System context |
| **Schedule-Triggered** | Time-based | No | Batch processing, cleanup, reports | System context |
| **Autolaunched** | Called by code | No | Reusable logic, subflows | System context |

---

## Screen Flow

### When to Use
- User needs to input data through guided steps
- Multi-step wizards or forms
- Display information and collect decisions
- Interactive processes requiring user confirmation

### Key Components
- **Screens**: Display fields, text, and collect input
- **Navigation**: Next/Previous buttons, pause/resume
- **Validation**: Required fields, format validation
- **Output**: Return values to calling component

### Common Patterns

**Pattern 1: Data Entry Wizard**
```
Screen 1 (Select Type) → Decision (Type) → Screen 2A/2B (Type-specific) → Assignment → Create Records → Screen 3 (Confirmation)
```

**Pattern 2: Approval Request**
```
Screen 1 (Request Details) → Get Records (Manager) → Screen 2 (Review & Submit) → Create Record (Approval) → Screen 3 (Success)
```

**Pattern 3: Lookup & Update**
```
Screen 1 (Enter ID) → Get Records (Lookup) → Decision (Found?) → Screen 2 (Display & Edit) → Update Records → Screen 3 (Confirmation)
```

### Best Practices
- ✅ Keep screens simple (3-5 fields per screen)
- ✅ Use helpText for field guidance
- ✅ Validate inputs before DML operations
- ✅ Provide clear success/error messages
- ✅ Use Progress Indicator for multi-step flows

### Common Pitfalls
- ❌ Too many fields on one screen (breaks mobile experience)
- ❌ No validation (leads to bad data)
- ❌ Complex formulas in screen fields (hard to debug)
- ❌ No error handling (users see cryptic messages)

---

## Record-Triggered Flow

### When to Use
- Automate business logic when records change
- Replace Workflow Rules and Process Builder
- Field updates, validations, related record creation
- Cross-object updates based on record changes

### Trigger Types

**Before-Save (Fast Field Updates)**
- Modify triggering record fields BEFORE saving
- No DML operation needed (automatic)
- Fastest performance
- Use for: field calculations, validations, default values

**After-Save**
- Create/update related records AFTER saving
- Full DML operations available
- Use for: child records, notifications, callouts

### Common Patterns

**Pattern 1: Before-Save Field Update**
```
Trigger: Before Update on Opportunity
Entry Criteria: Stage = "Closed Won"
Assignment: Set CloseDate = TODAY(), WonBy__c = $User.Id
(No Update Records needed - automatic)
```

**Pattern 2: After-Save Related Record Creation**
```
Trigger: After Insert on Account
Entry Criteria: Type = "Customer"
Create Records: Default Opportunity for new customer
Send Email: Notify sales team
```

**Pattern 3: Cross-Object Update**
```
Trigger: After Update on Opportunity
Entry Criteria: Amount changed
Get Records: Related Account
Assignment: Recalculate Account.TotalOpportunityAmount__c
Update Records: Account with new total
```

### Best Practices
- ✅ Use Before-Save for simple field updates (performance)
- ✅ Filter with Entry Criteria (reduce unnecessary runs)
- ✅ Bulkify: handle up to 200 records per transaction
- ✅ Use recursion prevention ($Record__Prior for field comparisons)
- ✅ Test with bulk data (Data Loader, 200 records)

### Common Pitfalls
- ❌ DML in loops (governor limit error)
- ❌ No recursion prevention (infinite loop)
- ❌ Too broad entry criteria (runs unnecessarily)
- ❌ After-Save for simple field updates (use Before-Save)

---

## Schedule-Triggered Flow

### When to Use
- Periodic batch processing
- Cleanup old records
- Generate scheduled reports
- Time-based reminders or notifications

### Scheduling Options

**Daily**: Run every day at specific time
```xml
<frequency>Daily</frequency>
<startDate>2025-01-01</startDate>
<startTime>02:00:00</startTime>
```

**Weekly**: Run on specific days
```xml
<frequency>Weekly</frequency>
<daysOfWeek>Monday</daysOfWeek>
<daysOfWeek>Wednesday</daysOfWeek>
<startTime>03:00:00</startTime>
```

**Monthly**: Run on specific day of month
```xml
<frequency>Monthly</frequency>
<dayOfMonth>1</dayOfMonth>
<startTime>01:00:00</startTime>
```

### Common Patterns

**Pattern 1: Daily Cleanup**
```
Schedule: Daily at 2:00 AM
Get Records: Opportunities WHERE CloseDate < TODAY()-90 AND IsClosed=false
Loop: Each stale opportunity
  Assignment: Mark as Lost
Update Records: Batch update after loop
```

**Pattern 2: Weekly Report**
```
Schedule: Monday at 6:00 AM
Get Records: Cases created last week
Assignment: Build summary statistics
Send Email: Weekly report to managers
```

**Pattern 3: Monthly Reminder**
```
Schedule: 1st of month at 9:00 AM
Get Records: Contracts expiring next month
Loop: Each expiring contract
  Assignment: Add to notification collection
Send Email: Renewal reminders (bulk)
```

### Best Practices
- ✅ Run during off-peak hours (night/early morning)
- ✅ Limit records processed per run (use filters)
- ✅ Batch DML operations (collect in loop, update after)
- ✅ Monitor execution history regularly
- ✅ Set up email notifications for failures

### Common Pitfalls
- ❌ Processing too many records (timeout)
- ❌ Running during business hours (performance impact)
- ❌ No error handling (silent failures)
- ❌ DML in loop (governor limits with large batches)

---

## Autolaunched Flow

### When to Use
- Reusable logic called by multiple sources
- Invoked from Apex, other Flows, REST API
- Complex calculations or data transformations
- Subflows to modularize large Flows

### Invocation Methods

**From Apex**
```apex
Map<String, Object> params = new Map<String, Object>();
params.put('inputAccountId', accountId);
params.put('inputAmount', 1000.00);

Flow.Interview.Calculate_Discount flowInterview =
    new Flow.Interview.Calculate_Discount(params);
flowInterview.start();

Decimal discount = (Decimal) flowInterview.getVariableValue('outputDiscount');
```

**From Another Flow (Subflow)**
```
Subflow Element: Calculate_Discount
  Input: inputAccountId = {!varAccountId}
  Input: inputAmount = {!varTotalAmount}
  Output: {!varDiscount} = outputDiscount
```

**From REST API**
```bash
POST /services/data/v60.0/actions/custom/flow/Calculate_Discount
{
  "inputs": [
    {
      "inputAccountId": "001...",
      "inputAmount": 1000.00
    }
  ]
}
```

### Common Patterns

**Pattern 1: Calculation Subflow**
```
Input: inputAmount (Currency)
Input: inputTier (String)
Decision: Determine discount % based on tier
Assignment: outputDiscount = inputAmount * discountRate
Output: outputDiscount (Currency)
```

**Pattern 2: Data Validation**
```
Input: inputRecordId (String)
Get Records: Fetch record to validate
Decision: Check validation rules
Assignment: Set outputIsValid, outputErrorMessage
Output: outputIsValid (Boolean), outputErrorMessage (String)
```

**Pattern 3: Bulk Processing Helper**
```
Input: inputRecordCollection (SObject Collection)
Loop: Each record
  Assignment: Process/transform record
  Assignment: Add to output collection
Output: outputProcessedRecords (SObject Collection)
```

### Best Practices
- ✅ Define clear input/output variables
- ✅ Validate inputs (check for nulls)
- ✅ Return meaningful outputs (success flag, error messages)
- ✅ Keep focused on single responsibility
- ✅ Document expected inputs and outputs

### Common Pitfalls
- ❌ Missing input validation (null reference errors)
- ❌ No error outputs (caller can't handle failures)
- ❌ Too complex (split into multiple subflows)
- ❌ Modifying global variables (use inputs/outputs only)

---

## Comparison Summary

| Feature | Screen | Record-Triggered | Schedule-Triggered | Autolaunched |
|---------|--------|------------------|-------------------|--------------|
| **User interaction** | Yes | No | No | No |
| **Trigger** | Button/Action | Record change | Schedule | Code/API |
| **Runs as** | User | System | System | System |
| **Debugging** | Easy (live) | Moderate (logs) | Hard (async) | Moderate |
| **Performance** | N/A (user wait) | Critical | Batch | Depends on caller |
| **Test approach** | Manual UI | Data Loader bulk | Monitor history | Unit test calls |

---

## Migration Guide

### From Workflow Rules
→ **Use Record-Triggered Flow (Before-Save)**
- Field updates
- Email alerts
- Task creation

### From Process Builder
→ **Use Record-Triggered Flow (After-Save)**
- Related record creation
- Cross-object updates
- Approval submissions

### From Apex Triggers
→ **Use Record-Triggered Flow (Before/After-Save)**
- Simple field logic
- Standard CRUD operations
- No complex queries needed

**Keep Apex for:**
- Complex business logic
- External callouts with retry logic
- Performance-critical operations
- Security (with sharing enforcement)

---

**Last Updated:** 2025-01-09
**Version:** 1.0
