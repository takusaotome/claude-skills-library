---
name: internal-audit-assistant
description: |
  内部監査業務支援スキル。リスクベース監査計画策定、監査プログラム作成、監査調書作成、
  フォローアップ管理を提供。IIA（内部監査人協会）国際基準準拠。
  Use when planning internal audits, conducting risk assessments, creating audit programs,
  documenting audit findings, or managing corrective actions.
  Triggers: "internal audit", "監査計画", "audit program", "監査調書", "CAR", "COSO", "IIA Standards".
---

# Internal Audit Assistant（内部監査支援）

## Overview

This skill provides professional internal audit support aligned with IIA (Institute of Internal Auditors) International Standards for the Professional Practice of Internal Auditing. Supports risk-based audit planning, audit program development, workpaper documentation, and corrective action tracking.

**Primary language**: Japanese (default), English supported
**Framework**: IIA Standards, COSO Internal Control Framework, ISO 19011 (Audit Guidelines)
**Output format**: Audit plans, audit programs, audit workpapers, CAR (Corrective Action Request) tracking

Use this skill when:
- Planning annual internal audit programs
- Conducting risk-based audit planning
- Creating audit checklists and programs
- Documenting audit findings and workpapers
- Managing corrective action follow-up
- Preparing for external audits (ISO, SOX, regulatory)

---

## Core Framework: IIA International Standards

### Definition of Internal Auditing

> Internal auditing is an independent, objective assurance and consulting activity designed to add value and improve an organization's operations. It helps an organization accomplish its objectives by bringing a systematic, disciplined approach to evaluate and improve the effectiveness of risk management, control, and governance processes.

### IIA Standards Structure

**Attribute Standards (1000 series)**:
- 1000: Purpose, Authority, and Responsibility
- 1100: Independence and Objectivity
- 1200: Proficiency and Due Professional Care
- 1300: Quality Assurance and Improvement Program

**Performance Standards (2000 series)**:
- 2000: Managing the Internal Audit Activity
- 2100: Nature of Work
- 2200: Engagement Planning
- 2300: Performing the Engagement
- 2400: Communicating Results
- 2500: Monitoring Progress
- 2600: Communicating the Acceptance of Risks

---

## Core Workflows

### Workflow 1: Risk-Based Audit Planning

**Purpose**: Develop annual internal audit plan based on organizational risk assessment.

#### Step 1: Universe of Auditable Entities

Create comprehensive list of all auditable entities:

**Example Universe**:
```markdown
| Entity ID | Entity Name | Department | Type | Last Audit | Risk Score |
|-----------|-------------|------------|------|------------|------------|
| FIN-01 | Accounts Payable | Finance | Process | 2024-03 | High |
| FIN-02 | Treasury Management | Finance | Process | 2023-11 | High |
| IT-01 | Access Management | IT | System | 2024-01 | Critical |
| IT-02 | Backup & Recovery | IT | System | 2023-06 | High |
| HR-01 | Payroll Processing | HR | Process | 2024-05 | Medium |
| OPS-01 | Procurement | Operations | Process | 2023-09 | High |
| OPS-02 | Inventory Management | Operations | Process | Never | Medium |
| COMP-01 | GDPR Compliance | Legal | Compliance | 2024-02 | High |
```

**Entity Types**:
- **Process**: Business processes (procurement, payroll, etc.)
- **System**: IT systems and applications
- **Compliance**: Regulatory compliance areas
- **Project**: Major projects or initiatives
- **Strategic**: Strategic risks (M&A, market entry, etc.)

#### Step 2: Risk Assessment Matrix

Assess each entity using quantitative risk scoring:

**Risk Factors** (each scored 1-5):
1. **Inherent Risk**: Complexity, volume, sensitivity of activity
2. **Control Environment**: Strength of existing controls
3. **Financial Impact**: Potential monetary impact of failure
4. **Regulatory Impact**: Compliance and legal consequences
5. **Last Audit Date**: Time since last audit
6. **Management Concern**: Requests from senior management

**Risk Score Calculation**:
```
Risk Score = (Inherent Risk × 0.25) +
             (Control Environment × 0.20) +
             (Financial Impact × 0.20) +
             (Regulatory Impact × 0.20) +
             (Last Audit Date × 0.10) +
             (Management Concern × 0.05)

Risk Level:
- Critical: 4.0 - 5.0
- High: 3.0 - 3.9
- Medium: 2.0 - 2.9
- Low: 1.0 - 1.9
```

**Example Risk Assessment**:
```markdown
Entity: IT-01 Access Management

| Factor | Score | Weight | Weighted Score |
|--------|-------|--------|----------------|
| Inherent Risk | 5 (Critical data access) | 0.25 | 1.25 |
| Control Environment | 3 (Some controls) | 0.20 | 0.60 |
| Financial Impact | 4 (Data breach costs) | 0.20 | 0.80 |
| Regulatory Impact | 5 (GDPR, SOX) | 0.20 | 1.00 |
| Last Audit Date | 2 (1 year ago) | 0.10 | 0.20 |
| Management Concern | 4 (Recent incidents) | 0.05 | 0.20 |

**Total Risk Score: 4.05 (Critical)**
```

#### Step 3: Audit Plan Prioritization

**Prioritization Rules**:
1. **Critical risk entities**: MUST audit annually
2. **High risk entities**: Audit every 1-2 years
3. **Medium risk entities**: Audit every 2-3 years
4. **Low risk entities**: Audit every 3-5 years or cyclically

**Additional Considerations**:
- Regulatory requirements (SOX audits, ISO surveillance)
- Management requests
- External audit coordination
- Resource availability (audit hours available)

#### Step 4: Annual Audit Plan Output

**Example Annual Audit Plan**:
```markdown
# FY2025 Internal Audit Plan

## Executive Summary
- Total Auditable Entities: 45
- Planned Audits: 18
- Total Audit Hours: 2,400 hours
- Risk Coverage: 85% of Critical/High risk entities

## Audit Schedule

| Quarter | Audit Name | Type | Risk Level | Hours | Lead Auditor |
|---------|------------|------|------------|-------|--------------|
| Q1 | IT Access Management | System | Critical | 200 | A. Tanaka |
| Q1 | Accounts Payable | Process | High | 150 | B. Sato |
| Q1 | SOX IT Controls | Compliance | High | 120 | A. Tanaka |
| Q2 | Treasury Management | Process | High | 180 | C. Suzuki |
| Q2 | Procurement | Process | High | 160 | B. Sato |
| Q2 | GDPR Compliance | Compliance | High | 140 | D. Yamada |
| Q3 | Backup & Recovery | System | High | 120 | A. Tanaka |
| Q3 | Vendor Management | Process | Medium | 140 | C. Suzuki |
| Q3 | Physical Security | Operational | Medium | 100 | B. Sato |
| Q4 | Payroll Processing | Process | Medium | 130 | D. Yamada |
| Q4 | Contract Management | Process | Medium | 120 | C. Suzuki |
| Q4 | Follow-up Audits | Various | - | 240 | All |

## Risk Coverage Analysis
- Critical Risk Entities: 5 → Audited: 5 (100%)
- High Risk Entities: 12 → Audited: 8 (67%)
- Medium Risk Entities: 18 → Audited: 4 (22%)
- Low Risk Entities: 10 → Audited: 0 (0%)

## Resource Allocation
- Lead Auditor A. Tanaka (IT): 800 hours
- Lead Auditor B. Sato (Ops): 650 hours
- Lead Auditor C. Suzuki (Finance): 600 hours
- Lead Auditor D. Yamada (Compliance): 350 hours
- Total: 2,400 hours
```

---

### Workflow 2: Audit Program Development

**Purpose**: Create detailed audit program (procedures and test steps) for each audit.

#### Step 1: Define Audit Objectives

Audit objectives should align with:
- Risk factors identified in planning phase
- IIA Standards (evaluate risk management, control, governance)
- Regulatory requirements (if applicable)

**Example (Accounts Payable Audit)**:
```markdown
## Audit Objectives

1. **Completeness**: Ensure all valid invoices are recorded and paid
2. **Accuracy**: Verify accuracy of invoice amounts and payment calculations
3. **Authorization**: Confirm proper approval of invoices and payments
4. **Segregation of Duties**: Verify separation of key functions
5. **Compliance**: Ensure compliance with company policies and tax regulations
6. **Fraud Prevention**: Assess controls to prevent duplicate payments and fictitious vendors
```

#### Step 2: Identify Key Controls

For each objective, identify key controls to be tested:

**Example Control Matrix (Accounts Payable)**:
```markdown
| Objective | Control ID | Control Description | Control Type | Frequency |
|-----------|------------|---------------------|--------------|-----------|
| Authorization | AP-C01 | Three-way match (PO/Receipt/Invoice) | Preventive | Per transaction |
| Authorization | AP-C02 | Approval workflow (manager sign-off) | Preventive | Per invoice |
| Accuracy | AP-C03 | Automated GL posting validation | Detective | Daily |
| Segregation | AP-C04 | Different users for AP entry vs. payment approval | Preventive | Continuous |
| Fraud Prevention | AP-C05 | Duplicate invoice check (system control) | Preventive | Per invoice |
| Fraud Prevention | AP-C06 | Vendor master file review | Detective | Quarterly |
```

#### Step 3: Design Test Procedures

For each control, design specific test procedures:

**Test Procedure Template**:
```markdown
### Test Procedure: AP-C01 (Three-Way Match)

**Control Objective**: Ensure invoices are matched to purchase orders and receiving reports before payment.

**Test Steps**:
1. Obtain AP transaction listing for [audit period]
2. Select sample of [X] invoices using [sampling method]
3. For each sample item:
   a. Verify existence of approved purchase order
   b. Verify existence of receiving report (goods receipt)
   c. Verify invoice matches PO and receipt (quantities, prices)
   d. Verify discrepancies are investigated and resolved
   e. Document any exceptions
4. Calculate exception rate
5. Assess control effectiveness

**Sample Size**: 30 transactions (statistical sampling, 95% confidence)
**Sampling Method**: Random selection from population
**Expected Result**: 0-1 exceptions acceptable (95% compliance)
**Workpaper Reference**: AP-01-T1
```

#### Step 4: Complete Audit Program

**Audit Program Structure**:
```markdown
# Audit Program: Accounts Payable

## Audit Information
- Audit ID: FIN-AP-2025-Q1
- Audit Period: January 1 - March 31, 2025
- Auditee: Finance Department - Accounts Payable Team
- Lead Auditor: B. Sato
- Planned Hours: 150
- Fieldwork Dates: April 7-18, 2025

## Section 1: Planning and Risk Assessment
- [ ] Review prior audit findings and corrective actions
- [ ] Conduct entrance meeting with AP Manager
- [ ] Obtain and review AP policies and procedures
- [ ] Perform walkthrough of AP process
- [ ] Identify and document key controls
- [ ] Assess inherent and residual risk
- [ ] Finalize audit scope and objectives

## Section 2: Control Testing
- [ ] Test AP-C01: Three-way match (WP: AP-01-T1)
- [ ] Test AP-C02: Approval workflow (WP: AP-02-T2)
- [ ] Test AP-C03: GL posting validation (WP: AP-03-T3)
- [ ] Test AP-C04: Segregation of duties (WP: AP-04-T4)
- [ ] Test AP-C05: Duplicate invoice check (WP: AP-05-T5)
- [ ] Test AP-C06: Vendor master file review (WP: AP-06-T6)

## Section 3: Substantive Testing
- [ ] Analyze vendor concentration risk
- [ ] Review aged payables report
- [ ] Test completeness of accruals
- [ ] Verify tax withholding accuracy
- [ ] Test foreign currency invoice processing (if applicable)

## Section 4: Reporting
- [ ] Summarize test results and exceptions
- [ ] Draft audit findings
- [ ] Conduct exit meeting with auditee
- [ ] Prepare audit report
- [ ] Issue Corrective Action Requests (CARs)
- [ ] Obtain management responses
- [ ] Finalize and distribute audit report

## Audit Team
- Lead Auditor: B. Sato (80 hours)
- Staff Auditor: E. Kobayashi (50 hours)
- QA Reviewer: Chief Audit Executive (20 hours)
```

---

### Workflow 3: Audit Workpaper Documentation

**Purpose**: Create standardized, professional audit workpapers that document audit procedures, evidence, and conclusions.

#### Workpaper Best Practices

**IIA Standards Requirements (2330)**:
- Document sufficient, reliable, relevant, and useful information
- Support conclusions and engagement results
- Enable experienced auditor to understand work performed
- Retain in accordance with organizational policies and legal requirements

**Workpaper Indexing System**:
```
[Audit Code]-[Section]-[Sequence]

Examples:
AP-01-T1 = Accounts Payable, Section 01 (Three-way match), Test 1
AP-02-T2 = Accounts Payable, Section 02 (Approvals), Test 2
IT-ACC-01 = IT Access Mgmt, Section ACC (Access Controls), Workpaper 01
```

#### Workpaper Template

**Standard Workpaper Header**:
```markdown
# Audit Workpaper

**Audit Name**: Accounts Payable Process Audit
**Audit ID**: FIN-AP-2025-Q1
**Workpaper Ref**: AP-01-T1
**Prepared By**: E. Kobayashi
**Date**: 2025-04-10
**Reviewed By**: B. Sato
**Review Date**: 2025-04-15

---

## Objective
Test the effectiveness of three-way match control (AP-C01) to ensure invoices are properly validated before payment.

## Scope
Invoice transactions from January 1 - March 31, 2025

## Procedure
1. Obtained AP transaction listing (3,450 invoices totaling $12.5M)
2. Selected random sample of 30 invoices (see sampling workpaper AP-00-SMPL)
3. For each sample, verified:
   - Approved purchase order exists
   - Receiving report exists
   - Invoice matches PO and receipt
   - Discrepancies properly resolved
4. Documented exceptions
5. Calculated exception rate and assessed control effectiveness

## Population
- Total invoices: 3,450
- Total value: $12,500,000
- Sample size: 30 invoices
- Sample value: $145,000

## Test Results

| Sample # | Invoice # | Amount | PO Match | Receipt Match | Discrepancy Resolution | Exception? |
|----------|-----------|--------|----------|---------------|------------------------|------------|
| 1 | INV-00125 | $4,500 | ✓ | ✓ | N/A | No |
| 2 | INV-00230 | $12,300 | ✓ | ✓ | N/A | No |
| 3 | INV-00341 | $2,100 | ✓ | ✓ | N/A | No |
| ... | ... | ... | ... | ... | ... | ... |
| 18 | INV-02187 | $8,700 | ✗ | ✓ | No PO on file | **YES** |
| ... | ... | ... | ... | ... | ... | ... |
| 30 | INV-03412 | $5,200 | ✓ | ✓ | N/A | No |

**Summary**:
- Total samples tested: 30
- Exceptions found: 1
- Exception rate: 3.3%

## Exceptions Detail

**Exception 1 (Sample #18 - INV-02187)**:
- Invoice amount: $8,700
- Issue: No purchase order found in system
- Auditee explanation: "Emergency repair - verbal approval from CFO due to urgency"
- Supporting evidence: Email from CFO dated same day as invoice
- Auditor assessment: Control bypass justified but not properly documented per policy

## Conclusion

**Control Effectiveness**: PARTIALLY EFFECTIVE

**Rationale**:
- 96.7% of tested transactions had proper three-way match
- One exception identified (emergency bypass) was justified but lacked proper documentation
- Control operates effectively in normal circumstances
- Policy does not clearly address emergency approval process

**Recommendation**:
Define formal process for emergency purchases including required documentation and retroactive PO creation.

## Evidence Attached
- Appendix A: Sample selection (AP-00-SMPL)
- Appendix B: Exception - Invoice INV-02187 with email approval
- Appendix C: AP Policy excerpt (Section 4.2 - Three-way match requirement)

---

**QA Review Notes** (B. Sato, 2025-04-15):
- Workpaper adequately documents testing performed
- Conclusion supported by evidence
- Recommendation is reasonable and actionable
- Approved for inclusion in audit report
```

#### Common Workpaper Types

1. **Planning Workpapers**:
   - Risk assessment matrix
   - Audit planning memo
   - Sample size calculation

2. **Process Documentation**:
   - Process flowcharts
   - Walkthrough notes
   - Control identification matrix

3. **Test Workpapers**:
   - Control testing results (like example above)
   - Substantive test results
   - Data analytics output

4. **Finding Workpapers**:
   - Finding development (root cause analysis)
   - Management responses
   - Corrective action plans

5. **Administrative Workpapers**:
   - Time budget vs. actual
   - Entrance/exit meeting minutes
   - Document request logs

---

### Workflow 4: Audit Finding Development

**Purpose**: Document audit findings with proper structure, root cause analysis, and actionable recommendations.

#### Finding Structure

**Well-Developed Finding Includes**:
1. **Condition**: What is the current state? (What we found)
2. **Criteria**: What should be the state? (Standard/policy/best practice)
3. **Cause**: Why did the issue occur? (Root cause)
4. **Effect**: What is the impact/risk? (Consequence)
5. **Recommendation**: What should be done? (Action)
6. **Management Response**: Auditee's corrective action plan

#### Finding Severity Classification

**Critical**:
- Significant control deficiency
- Immediate action required
- High probability of material impact
- Regulatory non-compliance with legal consequences

**High**:
- Important control weakness
- Could result in significant loss/exposure
- Requires timely remediation (30-90 days)

**Medium**:
- Control improvement opportunity
- Moderate risk exposure
- Should be addressed in reasonable timeframe (90-180 days)

**Low**:
- Minor control gap or inefficiency
- Low risk impact
- Enhancement recommendation (180+ days acceptable)

#### Finding Template

```markdown
# Audit Finding: [Finding Title]

**Finding ID**: FIN-AP-2025-F01
**Audit**: Accounts Payable Process Audit (FIN-AP-2025-Q1)
**Date Identified**: 2025-04-15
**Severity**: MEDIUM
**Auditee**: Finance Department - Accounts Payable

---

## 1. Condition (What we found)

One invoice payment ($8,700) was processed without a purchase order on file. The invoice was approved verbally by the CFO due to an emergency equipment repair, and email confirmation was provided. However, this emergency approval process is not documented in the Accounts Payable policy, and no retroactive purchase order was created.

**Evidence**: Invoice INV-02187 dated 2025-02-15 (see workpaper AP-01-T1, Sample #18)

---

## 2. Criteria (What should be)

According to the Accounts Payable Policy (Section 4.2):
> "All invoices must be matched to an approved purchase order and receiving report (three-way match) before payment is authorized."

Additionally, best practice (COSO Internal Control Framework) requires formal authorization and documentation for all financial transactions, including exceptions.

---

## 3. Cause (Root cause analysis)

**Root Causes Identified**:

1. **Policy Gap**: The AP policy does not address emergency procurement situations that require expedited payment
2. **Process Gap**: No formal process exists for retroactive PO creation after emergency purchases
3. **Training Gap**: AP staff unclear on how to handle exceptions to standard three-way match requirement

**5 Whys Analysis**:
- Why was invoice paid without PO? → Emergency repair needed immediate payment
- Why was emergency process not followed? → No emergency process defined
- Why is no emergency process defined? → Policy was written for standard transactions only
- Why wasn't policy updated? → Emergency situations are rare, not prioritized
- Why weren't exceptions tracked? → No mechanism to identify policy gaps

---

## 4. Effect (Impact and risk)

**Actual Impact**:
- One transaction processed outside of standard controls
- Control effectiveness reduced (96.7% vs. 100% target)

**Potential Risk** (if not addressed):
- Increased risk of unauthorized payments
- Lack of accountability for emergency approvals
- Potential for fraud (claiming "emergency" to bypass controls)
- External audit finding (SOX control deficiency)
- Inconsistent application of controls

**Risk Rating**: MEDIUM
- Likelihood: Low (emergencies are rare)
- Impact: Moderate (could lead to unauthorized payments if abused)

---

## 5. Recommendation

**Recommended Actions**:

1. **Update AP Policy** (Priority: High, Due: 60 days)
   - Add Section 4.2.1: "Emergency Procurement Procedures"
   - Define what constitutes an "emergency"
   - Specify approval authority for emergency purchases (CFO or COO)
   - Require email/written confirmation before payment
   - Require retroactive PO creation within 5 business days

2. **Implement Monitoring Control** (Priority: Medium, Due: 90 days)
   - Create monthly report of invoices paid without PO
   - Review by AP Manager to ensure all exceptions are legitimate emergencies
   - Track emergency purchases separately for trend analysis

3. **Training** (Priority: Medium, Due: 90 days)
   - Train AP staff on updated policy
   - Provide examples of emergency vs. non-emergency situations
   - Clarify escalation process

---

## 6. Management Response

**Auditee**: Jane Smith, AP Manager
**Response Date**: 2025-04-20
**Status**: AGREED

**Response**:
"We agree with the finding and recommendations. The emergency repair situation highlighted a gap in our policy that we had not previously identified. We will implement all three recommendations.

**Action Plan**:

1. **Update AP Policy**
   - Responsible: Jane Smith (AP Manager) + Legal review
   - Target Completion: June 15, 2025
   - Status: Draft policy update in progress

2. **Implement Monitoring Control**
   - Responsible: John Tanaka (AP Supervisor)
   - Target Completion: July 15, 2025
   - Status: Report template being designed

3. **Training**
   - Responsible: Jane Smith (AP Manager)
   - Target Completion: July 30, 2025
   - Status: Scheduled for July team meeting

**Additional Actions**:
- We have already created retroactive PO (PO-2025-9999) for the emergency repair invoice
- We will circulate interim guidance to AP team this week while policy is being updated"

---

## Follow-Up Plan

**Follow-up Audit Date**: August 2025 (90 days after report issuance)

**Validation Procedures**:
1. Review updated AP Policy to confirm emergency procedures are documented
2. Test 3 months of "invoices without PO" report to verify monitoring control
3. Interview AP staff to confirm training completion and understanding
4. Review any emergency purchases that occurred post-implementation

**Closure Criteria**:
- Updated policy approved and published
- Monitoring report generated monthly with management review
- AP staff training completion >90%
- No unauthorized bypass of three-way match control

---

**Auditor**: B. Sato, Lead Auditor
**Date**: 2025-04-22
**Status**: OPEN
**Follow-up Scheduled**: 2025-08-15
```

---

### Workflow 5: Corrective Action Tracking

**Purpose**: Systematically track and verify implementation of corrective actions from audit findings.

#### CAR (Corrective Action Request) Lifecycle

**Lifecycle Stages**:
```
1. OPEN → Finding identified, CAR issued
2. IN PROGRESS → Auditee working on corrective action
3. PENDING VALIDATION → Auditee claims completion, awaiting audit validation
4. VALIDATED → Audit confirms corrective action is effective
5. CLOSED → CAR officially closed
6. OVERDUE → Past due date, escalation triggered
7. REOPENED → Validation failed, corrective action inadequate
```

#### CAR Tracking Database

**CAR Master List Structure**:
```markdown
| CAR ID | Audit | Finding | Severity | Auditee | Due Date | Status | Days Open | Owner |
|--------|-------|---------|----------|---------|----------|--------|-----------|-------|
| CAR-2025-001 | AP Audit | Emergency PO process | Medium | Finance | 2025-07-30 | In Progress | 45 | J. Smith |
| CAR-2025-002 | IT Access | Terminated user access | High | IT | 2025-06-15 | Overdue | 90 | K. Lee |
| CAR-2025-003 | Payroll | Overtime approval | Low | HR | 2025-09-30 | Open | 10 | M. Garcia |
| CAR-2024-087 | Procurement | Vendor vetting | High | Ops | 2025-01-31 | Pending Validation | 180 | T. Nguyen |
```

#### Follow-Up Validation Process

**Validation Approach by Finding Type**:

**Control Design Findings** (Policy/procedure updates):
1. Review updated documentation
2. Verify approval and publication
3. Confirm training/communication completed
4. Interview sample of staff to confirm awareness

**Control Operating Effectiveness Findings** (Control not working):
1. Re-test the control (sample transactions after implementation date)
2. Verify system/process changes implemented
3. Review evidence of ongoing monitoring
4. Interview control owners

**Compliance Findings** (Regulatory violations):
1. Review remediation plan execution
2. Test compliance on post-implementation transactions
3. Verify self-monitoring mechanism established
4. Confirm reporting to regulatory body (if required)

#### Escalation Protocol

**Escalation Triggers**:
```markdown
## Escalation Level 1: Management Reminder
**Trigger**: 7 days before due date
**Action**: Email reminder to CAR owner and direct supervisor

## Escalation Level 2: Supervisor Escalation
**Trigger**: CAR overdue by 1-7 days
**Action**: Email to CAR owner's director with CC to Chief Audit Executive

## Escalation Level 3: Executive Escalation
**Trigger**: CAR overdue by 8-30 days (High/Critical) or 31-90 days (Medium/Low)
**Action**: Report to Audit Committee with executive management response required

## Escalation Level 4: Audit Committee Formal Action
**Trigger**: CAR overdue by >30 days (Critical), >60 days (High), or >90 days (Medium)
**Action**:
- Formal presentation to Audit Committee
- Executive accountability discussion
- Potential performance management action
- External reporting consideration (if regulatory)
```

#### CAR Dashboard and Reporting

**Monthly CAR Status Report**:
```markdown
# Corrective Action Request (CAR) Status Report
**Report Date**: May 31, 2025
**Reporting Period**: May 1-31, 2025

## Executive Summary
- Total Open CARs: 24
- CARs Due This Month: 8
- CARs Closed This Month: 5
- Overdue CARs: 3 (1 Critical, 2 High)
- On-Time Closure Rate: 87% (target: >90%)

## CARs by Severity
| Severity | Open | In Progress | Overdue | Avg Days Open |
|----------|------|-------------|---------|---------------|
| Critical | 2 | 2 | 1 | 45 |
| High | 8 | 6 | 2 | 67 |
| Medium | 12 | 10 | 0 | 52 |
| Low | 2 | 2 | 0 | 38 |
| **Total** | **24** | **20** | **3** | **56** |

## CARs by Department
| Department | Open CARs | Overdue | Closure Rate |
|------------|-----------|---------|--------------|
| IT | 9 | 2 | 78% |
| Finance | 6 | 0 | 92% |
| Operations | 5 | 1 | 85% |
| HR | 3 | 0 | 100% |
| Legal | 1 | 0 | 100% |

## Overdue CARs Requiring Attention

### CAR-2024-098 (CRITICAL) - IT Access Management
- **Finding**: Terminated employees retain system access for >24 hours
- **Auditee**: IT Department (K. Lee)
- **Original Due Date**: March 31, 2025
- **Days Overdue**: 61 days
- **Status**: Awaiting system upgrade to automate deprovisioning
- **Escalation**: Escalated to CIO and Audit Committee on May 15
- **Action Required**: Executive management to approve budget for identity management system

### CAR-2025-015 (HIGH) - Vendor Onboarding
- **Finding**: Vendor background checks not performed consistently
- **Auditee**: Procurement (T. Nguyen)
- **Original Due Date**: May 15, 2025
- **Days Overdue**: 16 days
- **Status**: New vendor screening process implemented but not yet validated
- **Escalation**: Reminder sent to CPO on May 20
- **Action Required**: Schedule follow-up validation audit

[Additional overdue CARs...]

## Upcoming CARs Due (Next 30 Days)
- June 15: CAR-2025-022 (Payroll overtime approval process)
- June 20: CAR-2025-024 (Data backup testing)
- June 30: CAR-2025-027 (Travel expense policy compliance)
- July 5: CAR-2025-029 (Change management documentation)

## Recommendations
1. **IT Department**: Requires focused attention - 2 overdue CARs, lowest closure rate
2. **CAR-2024-098 (Critical)**: Escalate to CEO for budget approval decision
3. **Follow-up Audits**: Schedule validation audits for June to clear pending CARs

---

**Prepared By**: Internal Audit Department
**Next Report**: June 30, 2025
```

---

## Deliverable Templates

### 1. Internal Audit Report Template

```markdown
# Internal Audit Report: [Audit Name]

**Report Date**: [Date]
**Audit ID**: [ID]
**Audit Period**: [Period]
**Report Classification**: CONFIDENTIAL - INTERNAL USE ONLY

---

## Executive Summary

**Audit Objective**: [1-2 sentences]

**Scope**: [What was audited, time period, locations]

**Overall Opinion**: [SATISFACTORY / NEEDS IMPROVEMENT / UNSATISFACTORY]

**Key Findings Summary**:
- [Critical findings count] Critical findings
- [High findings count] High priority findings
- [Medium findings count] Medium priority findings
- [Low findings count] Low priority findings

**Management Action Required**: [Yes/No - brief description]

---

## Background

[Brief description of the audited area, its importance to the organization, prior audit history]

---

## Audit Scope and Methodology

**Scope**:
- Audit period: [Date range]
- Locations: [Locations audited]
- Processes covered: [List]
- Out of scope: [Exclusions]

**Methodology**:
- Risk assessment and audit planning
- Interviews with [X] personnel
- Review of [X] documents/policies
- Testing of [X] samples across [Y] controls
- Data analytics on [population size]

**Standards Applied**: IIA International Standards for the Professional Practice of Internal Auditing

---

## Audit Opinion

**[SATISFACTORY / NEEDS IMPROVEMENT / UNSATISFACTORY]**

**Opinion Criteria**:
- **Satisfactory**: Controls are adequately designed and operating effectively. No significant weaknesses identified.
- **Needs Improvement**: Some control weaknesses identified that require management attention. Risks are elevated but not critical.
- **Unsatisfactory**: Significant control deficiencies exist. High risk of material impact. Immediate action required.

**Rationale**: [2-3 sentences explaining the opinion]

---

## Detailed Findings

### Finding 1: [Finding Title]

**Severity**: [Critical/High/Medium/Low]

**Condition**: [What we found]

**Criteria**: [What should be]

**Cause**: [Why it happened]

**Effect**: [Impact/risk]

**Recommendation**: [What should be done]

**Management Response**:
- **Agreed/Disagreed**: [Status]
- **Action Plan**: [Management's corrective action plan]
- **Responsible Party**: [Name, title]
- **Target Completion**: [Date]

**CAR ID**: [CAR reference]

---

[Repeat for each finding]

---

## Positive Observations

[Optional section highlighting strengths and good practices observed during the audit]

---

## Conclusion

[Summary paragraph reinforcing opinion and emphasizing key actions required]

---

## Appendices

**Appendix A**: Audit Program
**Appendix B**: List of Personnel Interviewed
**Appendix C**: Documents Reviewed
**Appendix D**: Detailed Test Results (if applicable)

---

**Report Distribution**:
- [Auditee names and titles]
- Chief Audit Executive
- Audit Committee Chair
- [Other stakeholders]

**Prepared By**: [Lead Auditor name]
**Reviewed By**: [QA Reviewer name]
**Approved By**: [Chief Audit Executive name]

**Follow-Up Audit**: [Scheduled date for CAR validation]
```

---

## Audit Tools and Techniques

### 1. Sampling Methods

**Judgmental Sampling**:
- Auditor selects samples based on professional judgment
- Used for: High-risk transactions, unusual items, prior problem areas
- Limitation: Not statistically projectable

**Statistical Sampling**:
- Random selection with statistical validity
- Types:
  - **Attribute Sampling**: Test compliance (yes/no result) - used for control testing
  - **Variable Sampling**: Estimate monetary amounts - used for substantive testing
- Advantage: Results can be projected to population with confidence level

**Sample Size Calculation (Attribute Sampling)**:
```
Factors:
- Population size
- Confidence level (typically 90-95%)
- Tolerable error rate (typically 5-10%)
- Expected error rate (based on prior audits)

Example:
- Population: 3,450 invoices
- Confidence: 95%
- Tolerable error: 5%
- Expected error: 1%
→ Sample size: 93 invoices

(Use statistical sampling calculator or table)
```

### 2. Data Analytics Techniques

**Common Analytics for Internal Audit**:

**Benford's Law Analysis**:
- Detect anomalies in numeric data (fraud detection)
- First digit frequency should follow Benford's distribution
- Application: Invoice amounts, expense reports, payroll

**Duplicate Detection**:
- Identify duplicate invoices, payments, vendor records
- Exact match or fuzzy matching
- Application: Accounts payable, procurement

**Gap Analysis**:
- Find missing sequence numbers (invoice #, PO #, check #)
- Indicate missing or deleted records
- Application: Transaction completeness testing

**Outlier Analysis**:
- Identify transactions outside normal range (Z-score, IQR method)
- Application: Expense claims, pricing anomalies

**Trend Analysis**:
- Time series analysis to identify unusual patterns
- Application: Sales trends, overtime hours, inventory turnover

**Segregation of Duties (SoD) Analysis**:
- Matrix analysis of user permissions
- Identify SoD conflicts (e.g., same user can enter and approve invoices)
- Application: ERP systems, financial systems

### 3. Interview Techniques

**Effective Interviewing**:

**Before the Interview**:
- Review process documentation
- Prepare open-ended questions
- Understand interviewee's role

**During the Interview**:
- Start with easy, non-threatening questions
- Use open-ended questions: "Can you walk me through the process?"
- Listen actively, take notes
- Observe body language for concerns
- Ask follow-up questions based on responses

**Interview Question Examples**:
- "What happens when [exception situation]?"
- "Who else is involved in this process?"
- "What are the most common problems you encounter?"
- "How do you know if an error occurred?"
- "What happens if [control] fails?"

**After the Interview**:
- Document interview notes immediately
- Verify understanding with process walkthrough
- Follow up on unclear points

---

## Best Practices

### 1. Independence and Objectivity

Internal auditors must maintain independence:
- **Organizational Independence**: Report to Audit Committee, not management
- **Objectivity**: Avoid auditing areas where auditor previously worked (<1 year)
- **No Advisory Role**: Avoid consulting on processes you will audit

### 2. Professional Skepticism

Maintain questioning mindset:
- Don't accept explanations without evidence
- Consider "What if this control fails?"
- Look for compensating controls
- Question unusual transactions or patterns

### 3. Risk-Based Approach

Focus audit efforts on highest risks:
- Update risk assessments annually
- Adjust audit plan as new risks emerge
- Communicate risk insights to management and Audit Committee

### 4. Communication Throughout Audit

Don't wait until final report:
- Entrance meeting: Set expectations
- Weekly status updates during fieldwork
- Discuss findings as they are identified (no surprises)
- Exit meeting: Review findings before issuing report

### 5. Quality Assurance

All audit work should be reviewed:
- Peer review of workpapers
- Supervisory review before report issuance
- External QA assessment every 5 years (IIA requirement)

---

## Common Pitfalls

### ❌ Inadequate Planning

Jumping into testing without understanding the process and risks.
**Solution**: Spend adequate time on risk assessment and planning (20-30% of audit hours).

### ❌ Insufficient Documentation

Workpapers lack detail; another auditor cannot understand what was done.
**Solution**: Document as if someone else will review your work (they will).

### ❌ Weak Findings (Lack of Impact)

Finding describes a minor issue without explaining the risk.
**Solution**: Always articulate "Effect" (impact/risk) clearly. If impact is minor, it's not a finding.

### ❌ Recommendations Without Root Cause

Suggesting solutions without understanding why the problem occurred.
**Solution**: Perform root cause analysis (5 Whys, Fishbone) before recommending corrective actions.

### ❌ Delay in Reporting

Waiting weeks/months after fieldwork to issue report; findings are stale.
**Solution**: Issue draft report within 2 weeks of fieldwork completion.

### ❌ Poor Follow-Up

Assuming management will implement corrective actions without validation.
**Solution**: Systematically track and validate all CARs. Escalate overdue items.

---

このスキルの目的は、組織の内部監査業務をIIA国際基準に準拠した形で支援し、リスクベースの効果的な監査を実現することです。適切な計画、実施、報告、フォローアップを通じて、組織のガバナンス、リスク管理、内部統制の改善に貢献してください。
