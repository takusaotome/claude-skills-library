# Action Recommendation Patterns

## Overview

This guide provides structured patterns for presenting recommendations and action requests to executives. Clear, well-structured recommendations accelerate decision-making and reduce back-and-forth.

## Recommendation Types

### Type 1: Single Recommendation

Use when there is one clear course of action.

**Structure**:
```
RECOMMENDATION: [Clear action statement]

Rationale:
• [Reason 1 with supporting data]
• [Reason 2 with supporting data]
• [Reason 3 with supporting data]

Risks Considered:
• [Risk 1]: Mitigated by [action]
• [Risk 2]: Acceptable because [reason]

Required:
• Decision by: [Date]
• Resources: [Specific resources]
• Approver: [Who needs to approve]
```

**Example**:
```
RECOMMENDATION: Approve vendor switch from Acme to Beta Corp

Rationale:
• 25% cost reduction ($120K annual savings)
• Better SLA (99.9% vs. current 99.5%)
• 3 reference customers in our industry

Risks Considered:
• Transition disruption: Mitigated by 60-day parallel run
• New relationship: Beta Corp assigned dedicated account team

Required:
• Decision by: November 15
• Resources: IT team (2 FTE) for 6-week transition
• Approver: CTO signature required
```

---

### Type 2: Options Comparison

Use when presenting multiple viable alternatives for executive decision.

**Structure**:
```
DECISION NEEDED: [What needs to be decided]

Options Summary:
┌──────────────┬─────────────┬─────────────┬─────────────┐
│ Criteria     │ Option A    │ Option B    │ Option C    │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ Cost         │ [value]     │ [value]     │ [value]     │
│ Timeline     │ [value]     │ [value]     │ [value]     │
│ Risk         │ [value]     │ [value]     │ [value]     │
│ Benefit      │ [value]     │ [value]     │ [value]     │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ RECOMMENDED  │             │     ✓       │             │
└──────────────┴─────────────┴─────────────┴─────────────┘

Why We Recommend Option B:
[2-3 sentence rationale]

Stakeholder Alignment:
• [Stakeholder 1]: Supports Option B
• [Stakeholder 2]: Prefers Option A, concern addressed by [X]
```

**Example**:
```
DECISION NEEDED: How to expand customer support capacity

Options Summary:
┌──────────────┬─────────────┬─────────────┬─────────────┐
│ Criteria     │ A: Hire     │ B: Outsource│ C: Automate │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ Cost/Year    │ $400K       │ $280K       │ $150K       │
│ Time to Live │ 4 months    │ 6 weeks     │ 6 months    │
│ Quality Risk │ Low         │ Medium      │ Medium      │
│ Scalability  │ Limited     │ High        │ Very High   │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ RECOMMENDED  │             │     ✓       │             │
└──────────────┴─────────────┴─────────────┴─────────────┘

Why We Recommend Outsourcing (Option B):
Fastest path to capacity increase before holiday peak. Lower risk
than automation for complex support cases. Can transition to
automation in Phase 2 with proven AI models.

Stakeholder Alignment:
• VP Customer Success: Supports outsourcing
• CFO: Prefers automation long-term, accepts phased approach
```

---

### Type 3: Go/No-Go Decision

Use for binary decisions requiring explicit approval.

**Structure**:
```
┌────────────────────────────────────────────────────────┐
│                    GO / NO-GO                          │
│             [Project or Initiative Name]               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  RECOMMENDATION:  ● GO    ○ NO-GO                     │
│                                                        │
├────────────────────────────────────────────────────────┤
│ GO Criteria Status:                                    │
│                                                        │
│  ✓ Budget approved                                     │
│  ✓ Resources allocated                                 │
│  ⚠ Technical risk medium (mitigation in place)        │
│  ✓ Stakeholder alignment confirmed                    │
│                                                        │
├────────────────────────────────────────────────────────┤
│ If GO:                      │ If NO-GO:               │
│ • Start: [Date]            │ • Impact: [Description]  │
│ • First milestone: [Date]   │ • Alternative: [Action]  │
│ • Investment: [Amount]      │ • Revisit: [Date]        │
├────────────────────────────────────────────────────────┤
│ APPROVERS:                                             │
│                                                        │
│ ___________________  ___________                       │
│ [Name, Title]        Date                             │
│                                                        │
│ ___________________  ___________                       │
│ [Name, Title]        Date                             │
└────────────────────────────────────────────────────────┘
```

---

### Type 4: Phased Implementation

Use for large initiatives requiring staged approval.

**Structure**:
```
RECOMMENDATION: Approve [Initiative] in Phases

Phase Overview:
┌─────────────┬───────────────────────────────────────────┐
│             │      Q1      │      Q2      │      Q3     │
├─────────────┼──────────────┼──────────────┼─────────────┤
│ Phase 1     │ ████████████ │              │             │
│ Pilot       │   $150K      │              │             │
├─────────────┼──────────────┼──────────────┼─────────────┤
│ Phase 2     │              │ ████████████ │             │
│ Rollout     │              │   $400K      │             │
├─────────────┼──────────────┼──────────────┼─────────────┤
│ Phase 3     │              │              │ ████████████│
│ Scale       │              │              │   $800K     │
└─────────────┴──────────────┴──────────────┴─────────────┘

Phase 1 Approval Request:
• Budget: $150K
• Duration: 12 weeks
• Success Criteria: [Specific metrics]
• Go/No-Go Gate: [Date]

Future Phase Commitments:
Phase 2 and 3 budgets are estimates only. Full approval
contingent on Phase 1 success criteria being met.
```

---

### Type 5: Resource Request

Use when requesting budget, headcount, or other resources.

**Structure**:
```
RESOURCE REQUEST

Request Summary:
┌────────────────────────────────────────────────────────┐
│ What:     [Specific resource requested]                │
│ Amount:   [Quantity/Cost]                              │
│ When:     [Timeline needed]                            │
│ Duration: [How long needed]                            │
└────────────────────────────────────────────────────────┘

Business Case:
• Problem: [Issue being addressed]
• Impact without: [Cost/risk of not approving]
• Expected return: [ROI or benefit]

Alternatives Considered:
┌────────────────┬─────────────┬──────────────────────────┐
│ Alternative    │ Cost        │ Why Not Recommended      │
├────────────────┼─────────────┼──────────────────────────┤
│ Do nothing     │ $0          │ [Impact of inaction]     │
│ Partial        │ [Cost]      │ [Limitation]             │
│ Alternative    │ [Cost]      │ [Issue]                  │
└────────────────┴─────────────┴──────────────────────────┘

Approval Chain:
□ Manager approval (< $50K)
□ Director approval ($50K - $250K)
☑ VP approval required ($250K+)
```

---

## Risk Presentation Patterns

### Risk Matrix

```
                    LIKELIHOOD
            Low         Medium        High
         ┌─────────┬─────────────┬───────────┐
    High │ Monitor │ Mitigate    │ CRITICAL  │
         │         │             │ ACTION    │
I        ├─────────┼─────────────┼───────────┤
M   Med  │ Accept  │ Monitor/    │ Mitigate  │
P        │         │ Mitigate    │           │
A        ├─────────┼─────────────┼───────────┤
C   Low  │ Accept  │ Accept      │ Monitor   │
T        │         │             │           │
         └─────────┴─────────────┴───────────┘
```

### Risk Table

```
┌──────────────────┬────────┬────────────┬───────────────────┐
│ Risk             │ Impact │ Likelihood │ Mitigation        │
├──────────────────┼────────┼────────────┼───────────────────┤
│ Vendor delay     │ High   │ Medium     │ Milestone-based   │
│                  │        │            │ payments          │
├──────────────────┼────────┼────────────┼───────────────────┤
│ Cost overrun     │ Medium │ Low        │ 15% contingency   │
│                  │        │            │ in budget         │
├──────────────────┼────────┼────────────┼───────────────────┤
│ Adoption         │ High   │ Medium     │ Change management │
│ resistance       │        │            │ program           │
└──────────────────┴────────┴────────────┴───────────────────┘
```

---

## Financial Justification Patterns

### ROI Calculation

```
FINANCIAL SUMMARY

Investment Required:
• Implementation costs:     $300K
• Ongoing annual costs:     $100K
• Total 3-year investment:  $600K

Expected Returns:
• Annual cost savings:      $250K
• Revenue enablement:       $150K
• Total 3-year benefit:     $1,200K

Key Metrics:
┌─────────────────┬───────────────┐
│ Metric          │ Value         │
├─────────────────┼───────────────┤
│ ROI             │ 100%          │
│ Payback Period  │ 18 months     │
│ NPV (10% disc.) │ $380K         │
│ IRR             │ 45%           │
└─────────────────┴───────────────┘
```

### Cost-Benefit Summary

```
                Year 1    Year 2    Year 3    Total
              ┌─────────┬─────────┬─────────┬─────────┐
Investment    │ ($400K) │  ($50K) │  ($50K) │ ($500K) │
              ├─────────┼─────────┼─────────┼─────────┤
Cost Savings  │  $100K  │  $200K  │  $200K  │  $500K  │
Revenue Gain  │   $50K  │  $150K  │  $200K  │  $400K  │
              ├─────────┼─────────┼─────────┼─────────┤
Net Benefit   │ ($250K) │  $300K  │  $350K  │  $400K  │
              └─────────┴─────────┴─────────┴─────────┘

Break-even: Month 18
```

---

## Timeline Presentation Patterns

### Milestone Timeline

```
IMPLEMENTATION TIMELINE

     Month 1      Month 2      Month 3      Month 4
    ──────────────────────────────────────────────────→
         │            │            │            │
         ▼            ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Phase 1 │  │ Phase 2 │  │ Phase 3 │  │ Go-Live │
    │ Design  │  │ Build   │  │ Test    │  │         │
    └─────────┘  └─────────┘  └─────────┘  └─────────┘
         ↓            ↓            ↓            ↓
    Milestone:   Milestone:   Milestone:   Milestone:
    Design       Dev          UAT          Launch
    signoff      complete     signoff      complete
```

### Gantt-Style View

```
PROJECT TIMELINE

                    Nov     Dec     Jan     Feb     Mar
                  ├───────┼───────┼───────┼───────┼───────┤
Requirements      ████████│       │       │       │       │
Design            │  █████████    │       │       │       │
Development       │       │ ███████████████       │       │
Testing           │       │       │       ██████████      │
Deployment        │       │       │       │       │ ██████│
                  └───────┴───────┴───────┴───────┴───────┘
                                          ▲
                              Key Decision Point
                              Budget reconfirmation
```

---

## Approval Request Patterns

### Standard Approval Block

```
┌────────────────────────────────────────────────────────┐
│                 APPROVAL REQUESTED                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│ Request:    Approve $500K budget for Project Alpha     │
│                                                        │
│ Deadline:   Decision needed by November 15             │
│                                                        │
│ Authority:  VP Engineering (budget > $250K)            │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│ □ APPROVED    □ APPROVED WITH CONDITIONS    □ DENIED  │
│                                                        │
│ Conditions/Comments:                                   │
│ _________________________________________________     │
│ _________________________________________________     │
│                                                        │
│ Signature: _________________  Date: ______________    │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Escalation Request

```
ESCALATION TO [EXECUTIVE NAME]

Issue: [One-line description]

Background:
[2-3 sentences of essential context]

Current Status:
• Attempted: [What has been tried]
• Blocked by: [What's preventing resolution]

Impact if Not Resolved:
• [Quantified consequence]
• Deadline: [When impact occurs]

Options:
1. [Option A]: [Brief description]
2. [Option B]: [Brief description]

Recommendation: Option [X] because [reason]

Ask: [Specific action needed from escalation recipient]
Decision needed by: [Date/Time]
```

---

## FYI/Informational Patterns

### Status Update (No Action Required)

```
┌────────────────────────────────────────────────────────┐
│  FYI: NO ACTION REQUIRED                               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Subject: [Brief topic]                                │
│                                                        │
│  Key Updates:                                          │
│  • [Update 1]                                          │
│  • [Update 2]                                          │
│  • [Update 3]                                          │
│                                                        │
│  Next Update: [Date]                                   │
│  Questions: Contact [Name] at [email]                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Awareness Alert

```
AWARENESS ALERT

Issue: [One-line description]

What's Happening:
[2-3 sentences describing the situation]

Current Status:
• Impact: [Description of who/what is affected]
• Status: [Under control / Being monitored / Escalated]
• Timeline: [Expected resolution]

Your Role:
□ No action needed - awareness only
□ May receive inquiries - talking points below
□ Downstream impact possible - monitor for [X]

Updates: Will be provided [frequency/channel]
```

---

## Checklist: Before Sending Any Recommendation

**Structure**:
- [ ] Recommendation is clear in first paragraph
- [ ] Options are presented consistently (if applicable)
- [ ] Risks are acknowledged with mitigations
- [ ] Timeline is specific

**Financial**:
- [ ] Costs are quantified
- [ ] Benefits are quantified
- [ ] ROI or business case is clear
- [ ] Budget source identified (if applicable)

**Action**:
- [ ] Specific ask is stated
- [ ] Decision deadline is included
- [ ] Approver has authority to decide
- [ ] Next steps are clear

**Stakeholder**:
- [ ] Key stakeholders consulted
- [ ] Objections addressed
- [ ] Alignment documented
