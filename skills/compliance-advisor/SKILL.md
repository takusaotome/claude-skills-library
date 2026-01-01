---
name: compliance-advisor
description: |
  コンプライアンス・内部統制支援の専門スキル。J-SOX/SOX対応、リスクコントロールマトリクス（RCM）作成、
  内部監査計画策定をサポート。内部統制の整備・運用評価から監査対応まで一貫した支援を提供。
  日英両言語のテンプレートを提供し、グローバル企業にも対応。COSO内部統制フレームワーク（2013年版）に準拠。

  Use when: creating J-SOX/SOX compliance documentation, building risk control matrices,
  planning internal audits, or assessing internal control effectiveness.

  Triggers: "J-SOX", "SOX", "内部統制", "コンプライアンス", "RCM", "リスクコントロールマトリクス",
  "内部監査", "compliance", "internal control", "internal audit", "risk assessment", "COSO"
---

# Compliance Advisor

## Overview

This skill provides comprehensive support for compliance, internal controls, and audit activities. It covers J-SOX (Japan) and SOX (US) compliance, Risk Control Matrix (RCM) development, and internal audit planning based on the COSO Internal Control Framework (2013).

### Key Capabilities

| Capability | Description |
|------------|-------------|
| J-SOX/SOX Compliance | Evaluate and document internal controls over financial reporting |
| RCM Development | Build Risk Control Matrices mapping risks to controls |
| Internal Audit | Plan and execute risk-based internal audits |
| Regulatory Response | Assess gaps and create remediation plans |

### Supported Frameworks

- **COSO Internal Control Framework (2013)** - 5 components, 17 principles
- **J-SOX** (金融商品取引法) - Japanese internal control requirements
- **SOX Section 404** - US Sarbanes-Oxley compliance
- **IIA Standards** - Internal audit professional standards

### Supported Languages

- **Japanese (日本語)**: Templates for domestic compliance
- **English**: Templates for global/US compliance

## When to Use This Skill

### Trigger Scenarios

1. **J-SOX/SOX Compliance**
   - "J-SOX対応の評価範囲を決定したい"
   - "Create SOX Section 404 documentation"

2. **RCM Development**
   - "リスクコントロールマトリクスを作成してください"
   - "Build an RCM for the procure-to-pay process"

3. **Internal Audit Planning**
   - "年間監査計画を策定したい"
   - "Develop a risk-based audit plan"

4. **Regulatory Response**
   - "規制対応のギャップ分析を行いたい"
   - "Assess compliance gaps and create remediation plan"

## Core Frameworks

### COSO Internal Control Framework (2013)

The skill is built on the COSO framework's 5 components:

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL ENVIRONMENT                       │
│  Integrity, Ethical Values, Oversight, Structure, Authority │
├─────────────────────────────────────────────────────────────┤
│                     RISK ASSESSMENT                          │
│  Objectives, Risk Identification, Fraud Risk, Change Impact │
├─────────────────────────────────────────────────────────────┤
│                   CONTROL ACTIVITIES                         │
│  Selection, Technology Controls, Policies & Procedures       │
├─────────────────────────────────────────────────────────────┤
│               INFORMATION & COMMUNICATION                    │
│  Quality Information, Internal Communication, External       │
├─────────────────────────────────────────────────────────────┤
│                 MONITORING ACTIVITIES                        │
│  Ongoing Evaluation, Deficiency Communication               │
└─────────────────────────────────────────────────────────────┘
```

### Financial Reporting Assertions

| Assertion | Description |
|-----------|-------------|
| **Existence/Occurrence** | Transactions and balances exist |
| **Completeness** | All transactions are recorded |
| **Rights & Obligations** | Assets are rights; liabilities are obligations |
| **Valuation/Allocation** | Recorded at appropriate amounts |
| **Presentation/Disclosure** | Properly classified and disclosed |

---

## Workflow 1: J-SOX/SOX Compliance

Use this workflow when establishing or evaluating internal controls over financial reporting.

### Step 1: Determine Evaluation Scope

Identify the scope of internal control evaluation:

**Scoping Criteria:**

| Criterion | Description | Threshold |
|-----------|-------------|-----------|
| Quantitative | Financial significance | > 5% of consolidated revenue/assets |
| Qualitative | Fraud risk, complexity | High inherent risk areas |
| Locations | Significant subsidiaries | Coverage of 70%+ of key metrics |

**Scope Documentation:**

```markdown
## Evaluation Scope

### Significant Accounts
| Account | Amount | % of Total | In Scope |
|---------|--------|------------|----------|
| Revenue | $XXX | XX% | Yes |
| Inventory | $XXX | XX% | Yes |

### Significant Processes
- Order-to-Cash
- Procure-to-Pay
- Inventory Management
- Financial Close
```

### Step 2: Identify Significant Accounts and Disclosures

Map accounts to processes and assertions:

| Account | Process | Key Assertions |
|---------|---------|----------------|
| Revenue | Order-to-Cash | Occurrence, Completeness, Cutoff |
| Accounts Receivable | Order-to-Cash | Existence, Valuation |
| Inventory | Inventory Mgmt | Existence, Valuation |
| Accounts Payable | Procure-to-Pay | Completeness, Accuracy |

### Step 3: Document Business Processes

Create process documentation:

1. **Process Narrative (業務記述書)**
   - Process objectives
   - Key activities and transactions
   - Systems and applications used
   - Roles and responsibilities

2. **Process Flowchart**
   ```mermaid
   flowchart TD
       A[Customer Order] --> B{Credit Check}
       B -->|Approved| C[Enter Order in System]
       B -->|Rejected| D[Notify Customer]
       C --> E[Pick & Ship]
       E --> F[Invoice Customer]
       F --> G[Record Revenue]
   ```

3. **Risk and Control Matrix (RCM)**
   - See Workflow 2 for detailed RCM development

### Step 4: Evaluate Design Effectiveness

Assess whether controls are properly designed:

**Design Evaluation Criteria:**

| Criterion | Question |
|-----------|----------|
| Precision | Is the control specific enough to address the risk? |
| Competence | Does the person performing have adequate skills? |
| Authority | Does the person have proper authorization? |
| Timeliness | Is the control performed at the right time? |
| Evidence | Is there documentation of control performance? |

### Step 5: Test Operating Effectiveness

Test whether controls are operating as designed:

**Testing Approach:**

| Control Frequency | Minimum Sample Size |
|-------------------|---------------------|
| Annual | 1 |
| Quarterly | 2 |
| Monthly | 2-5 |
| Weekly | 5-15 |
| Daily | 20-40 |

**Testing Methods:**

1. **Inquiry** - Ask control owners about procedures
2. **Observation** - Watch control being performed
3. **Inspection** - Review documentation/evidence
4. **Re-performance** - Execute the control independently

### Step 6: Evaluate and Report Deficiencies

Classify identified deficiencies:

| Classification | J-SOX Term | SOX Term | Definition |
|----------------|------------|----------|------------|
| Deficiency | 不備 | Control Deficiency | Design or operating gap |
| Significant Deficiency | 開示すべき重要な不備 | Significant Deficiency | Less severe than material weakness |
| Material Weakness | 重要な欠陥 | Material Weakness | Reasonable possibility of material misstatement |

Use template: `assets/jsox_sox_checklist_ja.md` or `assets/jsox_sox_checklist_en.md`

---

## Workflow 2: Risk Control Matrix (RCM) Development

Use this workflow when building or updating Risk Control Matrices.

### Step 1: Identify Process Objectives

Define what the process should achieve:

**Example - Order-to-Cash:**

| Objective | Description |
|-----------|-------------|
| Revenue Recognition | Revenue is recognized in the correct period |
| Accuracy | Invoices reflect actual goods/services delivered |
| Collectability | Receivables are collectible |

### Step 2: Identify Risks

For each objective, identify what could go wrong:

**Risk Identification Matrix:**

| Risk ID | Risk Description | Assertion | Inherent Risk |
|---------|-----------------|-----------|---------------|
| R-OTC-01 | Revenue recognized in wrong period | Cutoff | High |
| R-OTC-02 | Fictitious sales recorded | Occurrence | Medium |
| R-OTC-03 | Credit extended to non-creditworthy customers | Valuation | High |

**Inherent Risk Assessment:**

| Factor | Description | Rating Scale |
|--------|-------------|--------------|
| Likelihood | Probability of occurrence | 1 (Rare) - 5 (Almost Certain) |
| Impact | Financial/reputational impact | 1 (Negligible) - 5 (Catastrophic) |
| **Inherent Risk** | Likelihood × Impact | 1-25 |

### Step 3: Map Controls to Risks

Identify controls that mitigate each risk:

| Risk ID | Control ID | Control Description | Type | Frequency |
|---------|------------|---------------------|------|-----------|
| R-OTC-01 | C-OTC-01 | Revenue cutoff review at month-end | Detective | Monthly |
| R-OTC-02 | C-OTC-02 | System-enforced credit limit check | Preventive | Per transaction |
| R-OTC-02 | C-OTC-03 | Segregation of duties: Sales vs. Billing | Preventive | Continuous |

**Control Types:**

| Type | Description | Example |
|------|-------------|---------|
| **Preventive** | Prevents errors from occurring | System validation, authorization |
| **Detective** | Identifies errors after occurrence | Reconciliation, review |
| **Corrective** | Corrects identified errors | Exception handling, adjustments |

### Step 4: Identify Key Controls

Determine which controls are "key" for SOX/J-SOX purposes:

**Key Control Criteria:**

| Criterion | Yes | No |
|-----------|-----|-----|
| Addresses significant risk? | Key | Non-key |
| No compensating controls exist? | Key | Consider non-key |
| Only line of defense? | Key | Consider non-key |
| Required by regulation? | Key | Evaluate |

### Step 5: Assess Control Effectiveness

Evaluate whether controls adequately mitigate risks:

| Control Rating | Definition |
|----------------|------------|
| Effective | Properly designed and operating |
| Needs Improvement | Minor gaps identified |
| Ineffective | Significant gaps or not operating |

### Step 6: Calculate Residual Risk

**Residual Risk = Inherent Risk - Control Effectiveness**

| Inherent Risk | Control Rating | Residual Risk |
|---------------|----------------|---------------|
| High (15-25) | Effective | Low-Medium |
| High (15-25) | Ineffective | High (Escalate) |
| Medium (8-14) | Effective | Low |
| Low (1-7) | Any | Low |

Use template: `assets/risk_control_matrix_ja.md` or `assets/risk_control_matrix_en.md`

---

## Workflow 3: Internal Audit Planning

Use this workflow when developing internal audit plans.

### Step 1: Define the Audit Universe

Create a comprehensive list of auditable areas:

**Audit Universe Categories:**

| Category | Examples |
|----------|----------|
| Business Processes | Procurement, Sales, HR, IT |
| Functions | Finance, Operations, Compliance |
| Locations | Regional offices, plants, subsidiaries |
| Projects | Major initiatives, system implementations |
| Regulations | SOX, GDPR, industry-specific |

### Step 2: Assess Risks for Prioritization

Rate each auditable unit:

**Risk Assessment Factors:**

| Factor | Weight | Description |
|--------|--------|-------------|
| Financial Impact | 25% | Revenue, costs, assets at risk |
| Strategic Importance | 20% | Alignment with business objectives |
| Regulatory/Compliance | 20% | Legal and regulatory exposure |
| Prior Audit Results | 15% | Historical issues and findings |
| Change/Complexity | 10% | Recent changes, process complexity |
| Time Since Last Audit | 10% | Audit coverage freshness |

**Risk Scoring Matrix:**

| Rating | Score | Definition |
|--------|-------|------------|
| High | 4-5 | Significant risk exposure |
| Medium | 2-3 | Moderate risk exposure |
| Low | 1 | Minimal risk exposure |

### Step 3: Develop Annual Audit Plan

Create a risk-based audit schedule:

```markdown
## Annual Audit Plan FY20XX

| Audit # | Audit Area | Risk Rating | Q1 | Q2 | Q3 | Q4 | Hours |
|---------|------------|-------------|----|----|----|----|-------|
| IA-001 | Procurement | High | ██ | | | | 200 |
| IA-002 | Revenue Cycle | High | | ██ | | | 240 |
| IA-003 | IT General Controls | Medium | | | ██ | | 160 |
| IA-004 | Inventory Management | Medium | | | | ██ | 180 |
```

### Step 4: Design Audit Programs

Create detailed audit procedures:

**Audit Program Structure:**

1. **Audit Objectives**
   - What are we trying to verify?
   - What risks are we addressing?

2. **Scope and Approach**
   - Time period covered
   - Locations included
   - Sampling methodology

3. **Detailed Procedures**
   | Step | Procedure | Evidence | WP Ref |
   |------|-----------|----------|--------|
   | 1 | Interview process owner | Meeting notes | A-1 |
   | 2 | Walkthrough transaction flow | Flowchart | A-2 |
   | 3 | Select sample of transactions | Sample log | A-3 |
   | 4 | Test control operation | Test results | A-4 |

### Step 5: Execute and Document

**Working Paper Standards:**

| Element | Requirement |
|---------|-------------|
| Objective | Clear statement of what was tested |
| Procedure | Description of work performed |
| Evidence | Documentation obtained |
| Conclusion | Finding based on evidence |
| Preparer/Reviewer | Sign-off and date |

### Step 6: Report and Follow-Up

**Audit Report Structure:**

1. **Executive Summary**
   - Overall assessment
   - Key findings summary
   - Management action required

2. **Detailed Findings**
   | Finding | Risk | Recommendation | Management Response | Due Date |
   |---------|------|----------------|---------------------|----------|

3. **Appendices**
   - Scope and methodology
   - Testing details

Use template: `assets/internal_audit_plan_ja.md` or `assets/internal_audit_plan_en.md`

---

## Workflow 4: Regulatory Response Planning

Use this workflow when responding to new regulations or compliance gaps.

### Step 1: Understand Regulatory Requirements

Document the regulation's requirements:

| Element | Description |
|---------|-------------|
| Regulation Name | [Official name and citation] |
| Effective Date | [Compliance deadline] |
| Scope | [Who must comply] |
| Key Requirements | [Summary of obligations] |
| Penalties | [Non-compliance consequences] |

### Step 2: Conduct Gap Analysis

Compare current state to requirements:

**Gap Analysis Template:**

| Requirement | Current State | Gap | Priority | Effort |
|-------------|---------------|-----|----------|--------|
| [Req 1] | [Current] | [Gap description] | H/M/L | H/M/L |

**Gap Severity Classification:**

| Severity | Definition | Timeline |
|----------|------------|----------|
| Critical | Non-compliance exposure | Immediate action |
| High | Significant gap | < 30 days |
| Medium | Moderate gap | < 90 days |
| Low | Minor improvement | < 180 days |

### Step 3: Develop Remediation Plan

Create action plan to close gaps:

**Remediation Plan Structure:**

| Gap ID | Action Item | Owner | Start Date | Due Date | Status |
|--------|-------------|-------|------------|----------|--------|
| G-001 | Implement control X | [Name] | [Date] | [Date] | [Status] |

### Step 4: Implement Changes

Track implementation progress:

**Implementation Tracking:**

| Phase | Activities | Duration |
|-------|------------|----------|
| Design | Document new controls | 2-4 weeks |
| Develop | Build/configure systems | 4-8 weeks |
| Test | Validate effectiveness | 2-4 weeks |
| Deploy | Roll out changes | 1-2 weeks |
| Monitor | Post-implementation review | Ongoing |

### Step 5: Establish Ongoing Monitoring

Create sustainable compliance:

**Monitoring Framework:**

| Element | Frequency | Owner | Method |
|---------|-----------|-------|--------|
| Control Self-Assessment | Quarterly | Control Owners | Checklist |
| Management Review | Monthly | Compliance | Dashboard |
| Internal Audit | Annual | Internal Audit | Testing |
| External Audit | Annual | External | Independent |

---

## Quick Reference

### J-SOX/SOX Compliance Checklist

- [ ] Scoping completed and documented
- [ ] Significant accounts identified
- [ ] Significant processes mapped
- [ ] RCMs created for in-scope processes
- [ ] Entity-level controls evaluated
- [ ] IT general controls assessed
- [ ] Design effectiveness tested
- [ ] Operating effectiveness tested
- [ ] Deficiencies evaluated and classified
- [ ] Management's report prepared

### RCM Development Checklist

- [ ] Process objectives defined
- [ ] Risks identified for each objective
- [ ] Inherent risk assessed
- [ ] Controls mapped to risks
- [ ] Key controls identified
- [ ] Control effectiveness assessed
- [ ] Residual risk calculated
- [ ] Gaps and improvements documented

### Internal Audit Checklist

- [ ] Audit universe defined
- [ ] Risk assessment completed
- [ ] Annual plan approved by Audit Committee
- [ ] Audit programs developed
- [ ] Fieldwork completed
- [ ] Working papers reviewed
- [ ] Draft report issued
- [ ] Management responses obtained
- [ ] Final report distributed
- [ ] Follow-up scheduled

---

## Resources

### Templates (assets/)

| Template | Language | Use For |
|----------|----------|---------|
| `jsox_sox_checklist_ja.md` | Japanese | J-SOX compliance evaluation |
| `jsox_sox_checklist_en.md` | English | SOX compliance evaluation |
| `risk_control_matrix_ja.md` | Japanese | RCM development (domestic) |
| `risk_control_matrix_en.md` | English | RCM development (global) |
| `internal_audit_plan_ja.md` | Japanese | Audit planning (domestic) |
| `internal_audit_plan_en.md` | English | Audit planning (global) |

### Reference Guides (references/)

| Guide | Content |
|-------|---------|
| `jsox_sox_framework.md` | J-SOX and SOX requirements comparison |
| `internal_control_methodology.md` | COSO framework, 3 Lines of Defense |
| `risk_assessment_guide.md` | Risk evaluation methodology |

---

## Best Practices Summary

### Internal Control Design

1. **Preventive over Detective** - Prefer controls that prevent errors
2. **Automated over Manual** - Automated controls are more reliable
3. **Segregation of Duties** - Separate authorization, custody, recording
4. **Document Everything** - No documentation = no control
5. **Regular Review** - Controls decay without maintenance

### Risk Assessment

1. **Top-Down Approach** - Start with financial statement level
2. **Quantitative + Qualitative** - Consider both perspectives
3. **Fraud Risk** - Explicitly consider fraud scenarios
4. **Change Impact** - Assess how changes affect controls

### Internal Audit

1. **Independence** - Report to Audit Committee
2. **Risk-Based** - Focus on highest risk areas
3. **Value-Added** - Provide actionable recommendations
4. **Follow-Through** - Verify remediation completion

---

## Troubleshooting

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Too many key controls | Over-scoping | Re-evaluate significance criteria |
| Control testing delays | Resource constraints | Prioritize high-risk areas |
| Repeat deficiencies | Root cause not addressed | Conduct root cause analysis |
| Management pushback | Unclear value | Communicate business benefits |
| Documentation gaps | Process changes | Establish change management |

---

## Examples

### Example 1: J-SOX Initial Implementation

**Context**: Japanese public company implementing J-SOX for first time

**How This Skill Helps:**

1. **Workflow 1 (J-SOX)**: Determined evaluation scope using 5% threshold
2. **Workflow 2 (RCM)**: Created RCMs for 8 significant processes
3. **Result**: Achieved unqualified internal control report

### Example 2: SOX Remediation Project

**Context**: US subsidiary identified material weakness

**How This Skill Helps:**

1. **Workflow 4 (Regulatory)**: Conducted gap analysis
2. **Workflow 2 (RCM)**: Redesigned controls
3. **Workflow 1 (SOX)**: Re-tested operating effectiveness
4. **Result**: Remediated material weakness in 6 months

### Example 3: Risk-Based Audit Transformation

**Context**: Internal audit team shifting from cyclical to risk-based approach

**How This Skill Helps:**

1. **Workflow 3 (Audit)**: Created risk-scored audit universe
2. **Workflow 2 (RCM)**: Leveraged control testing results
3. **Result**: Increased audit coverage efficiency by 40%
