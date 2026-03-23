# Exception Governance

This document defines the rules for when quality gate exceptions are permissible, when they are not, how they are escalated, and how they expire. The goal is to ensure that exceptions are controlled, temporary, and transparent -- never a backdoor for bypassing quality.

## 1. Core Principles

### Exceptions Are Not Failures -- They Are Controlled Decisions

An exception means: "We acknowledge this item is incomplete. We have assessed the risk, put temporary controls in place, assigned an owner, set a deadline, and obtained appropriate approval." This is fundamentally different from ignoring an incomplete item or pretending it does not exist.

### Every Exception Must Be More Expensive Than Compliance

The exception process should require more effort than simply meeting the original criterion. If filing an exception is easier than doing the work, the exception process is broken and will be abused.

### No Permanent Exceptions

Every exception must have an expiration date. If an item is permanently deferred, it should be removed from the gate criteria entirely (with a formal change request), not carried as an eternal exception.

## 2. Exception Eligibility Rules

### 2.1 Exception-Eligible Items

The following types of items MAY be eligible for exception, subject to risk assessment and approval:

| Category | Example | Typical Condition |
|----------|---------|-------------------|
| Non-critical test coverage gaps | Edge case scenario not covered by automated tests | Manual verification performed and documented; automated test added to backlog with due date |
| Minor documentation gaps | API documentation for internal-only endpoints | Core user-facing documentation is complete; internal docs added to backlog |
| Performance optimization | Response time at P99 is 520ms against 500ms target | Degradation is minor; optimization ticket created with priority |
| Non-blocking static analysis findings | Medium-severity linter warnings in legacy code | Findings are isolated to non-critical paths; remediation scheduled |
| Feature completeness for non-MVP features | Advanced filtering option not implemented | Core workflow is complete; feature is flagged as known limitation in release notes |
| Cross-browser compatibility | Minor rendering difference in one browser version | Primary browsers function correctly; fix scheduled for next sprint |

### 2.2 Exception-Ineligible Items (MUST Block)

The following items MUST NOT be granted exceptions under any circumstances. These are non-negotiable gate blockers:

| Category | Example | Why It Must Block |
|----------|---------|-------------------|
| Critical security vulnerabilities | SQL injection, authentication bypass, remote code execution | Direct risk of data breach or unauthorized access |
| Data loss or corruption risks | Unhandled write path that could delete user data | Irreversible damage to users |
| Regulatory compliance failures | GDPR data handling violation, PCI DSS non-compliance | Legal liability |
| Critical functional failures | Core workflow does not complete successfully | Product is fundamentally broken |
| Missing rollback capability | No way to revert the deployment if problems occur | Deployment risk without recovery |
| Authentication/authorization bypass | Users can access resources they should not | Security boundary violation |
| Build reproducibility failure | Cannot reproduce the build from source | Cannot verify what is being deployed |

### 2.3 Gray Zone Items (Require Escalation)

Some items fall between eligible and ineligible. These require escalation to a higher authority:

| Category | Example | Escalation Authority |
|----------|---------|---------------------|
| High-severity security findings (not critical) | Cross-site scripting in admin panel with IP restriction | Security team lead + project sponsor |
| Significant performance degradation | 2x latency increase under normal load | Architecture lead + product owner |
| Incomplete data migration | 5% of records require manual correction | Data owner + project sponsor |
| Third-party dependency vulnerability | Upstream library has known CVE with no fix available | Security team + architecture lead |

## 3. Exception Record Requirements

Every exception MUST include all of the following fields. An exception record with any field missing is not valid and must not be accepted.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Exception ID** | Unique identifier | EX-2026-001 |
| **Gate ID** | Which gate this exception applies to | G3 (Verification Complete) |
| **Item Description** | What is incomplete or non-compliant | E2E tests for payment flow on Safari not executed |
| **Reason** | Why the item cannot be completed by the gate deadline | Safari test environment unavailable due to infrastructure migration |
| **Risk Assessment** | What could go wrong if this item remains incomplete | Payment flow may fail on Safari; estimated 8% of user base affected |
| **Risk Level** | Severity classification | Medium |
| **Temporary Control** | What mitigation is in place until the item is resolved | Manual QA verification performed on Safari; monitoring alert configured for payment errors by browser |
| **Due Date** | When the item must be resolved | 2026-04-15 |
| **Owner** | Who is responsible for resolving the item | QA Lead (name) |
| **Approver** | Who approved the exception (must differ from owner) | Project Manager (name) |
| **Approval Date** | When the exception was approved | 2026-03-20 |
| **Closure Evidence** | What evidence will confirm the item is resolved | CI pipeline showing Safari E2E tests passing; test report attached |

## 4. Escalation Paths

### Severity-Based Escalation

| Risk Level | Approver Authority | Escalation If Disputed |
|------------|-------------------|----------------------|
| Low | Team lead or gate owner | Project manager |
| Medium | Project manager | Project sponsor or steering committee |
| High | Project sponsor | Steering committee or executive sponsor |
| Critical | Not eligible for exception | Must block the gate |

### Escalation Process

1. **Requestor** prepares the exception record with all required fields
2. **Gate owner** performs initial assessment: Is the item eligible for exception?
3. If eligible, gate owner routes to the appropriate approver based on risk level
4. **Approver** reviews the exception record, focusing on:
   - Is the risk assessment accurate?
   - Is the temporary control adequate?
   - Is the due date realistic?
   - Is the closure evidence clearly defined?
5. Approver either approves, requests modifications, or rejects
6. If rejected, the item must be resolved before the gate can pass
7. If the requestor disagrees with rejection, they may escalate to the next level

### Escalation Time Limits

- Low risk: Decision within 1 business day
- Medium risk: Decision within 2 business days
- High risk: Decision within 3 business days, with interim status updates daily

If the escalation authority does not respond within the time limit, the gate defaults to blocking (conservative approach).

## 5. Expiration and Renewal Rules

### Maximum Exception Duration

| Risk Level | Maximum Duration | Renewal Allowed |
|------------|-----------------|-----------------|
| Low | 90 calendar days | Yes, once, with re-assessment |
| Medium | 60 calendar days | Yes, once, with escalated approval |
| High | 30 calendar days | No -- must be resolved or escalated further |

### Expiration Process

1. **14 days before expiration**: Automated reminder to the owner
2. **7 days before expiration**: Automated reminder to the owner and approver
3. **On expiration date**: If not resolved or renewed, the exception status changes to "Expired"
4. **Expired exceptions**: Must be treated as open gate blockers. The gate is retroactively considered non-compliant until the item is resolved or a new exception is approved.

### Renewal Process

1. Owner submits a renewal request with:
   - Updated risk assessment (has the risk changed?)
   - Progress report (what has been done so far?)
   - New due date (must be shorter than original duration)
   - Updated temporary control (has the mitigation changed?)
2. Renewal approval requires the same or higher authority as the original exception
3. A renewed exception retains the original Exception ID with a suffix (e.g., EX-2026-001-R1)

## 6. Exception Closure

### Closure Process

1. Owner completes the remediation work
2. Owner produces the closure evidence specified in the exception record
3. Owner updates the exception status to "Resolution Pending"
4. Gate owner or approver verifies the closure evidence
5. If verified, status changes to "Closed"
6. If not verified, status changes to "Reopened" with a new due date

### Closure Evidence Standards

Closure evidence must meet the same standards as original gate evidence:
- Traceable to a specific artifact version
- Stored in a durable, addressable location
- Immutable after verification
- Reviewed by someone other than the owner

## 7. Monitoring and Reporting

### Exception Dashboard Metrics

Track the following metrics to assess exception governance health:

| Metric | Healthy Range | Warning Sign |
|--------|--------------|--------------|
| Open exceptions per project | 0-3 | More than 5 suggests gate criteria are unrealistic |
| Average time to close | Under 30 days | Over 45 days suggests exceptions are being used to avoid work |
| Renewal rate | Under 10% | Over 25% suggests due dates are set unrealistically |
| Expired exceptions | 0 | Any expired exception indicates governance failure |
| Exception-to-gate ratio | Under 0.5 per gate | Over 1.0 per gate suggests systemic quality issues |

### Periodic Review

At each project retrospective, review the exception register:
- Were exceptions justified?
- Were temporary controls effective?
- Were due dates met?
- Should any gate criteria be adjusted based on exception patterns?
- Are there systemic issues that generate repeated exceptions?
