# Failure Mode and Effects Analysis (FMEA)

## Document Information

| Field | Value |
|-------|-------|
| **FMEA Type** | [ ] Process (PFMEA)  [ ] Design (DFMEA) |
| **Process/Product Name** | [Enter name] |
| **Project** | [Project name/ID] |
| **Prepared By** | [Name] |
| **Date** | YYYY-MM-DD |
| **Revision** | [Version number] |

---

## Team Members

| Name | Role/Function |
|------|---------------|
| [Name] | [Role] |
| [Name] | [Role] |
| [Name] | [Role] |
| [Name] | [Role] |

---

## FMEA Worksheet

| # | Process Step / Component | Potential Failure Mode | Potential Effect(s) of Failure | S | Potential Cause(s) | O | Current Controls | D | RPN | Recommended Actions | Resp. | Target Date | Actions Taken | New S | New O | New D | New RPN |
|---|-------------------------|----------------------|------------------------------|---|-------------------|---|------------------|---|-----|---------------------|-------|-------------|---------------|-------|-------|-------|---------|
| 1 | [Step/Part] | [How it could fail] | [Impact of failure] | | [Why it would fail] | | [Prevention/Detection] | | | [Action to reduce risk] | [Name] | [Date] | [What was done] | | | | |
| 2 | | | | | | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | | | | | | |
| 5 | | | | | | | | | | | | | | | | | |

---

## Rating Scales

### Severity (S) - How Bad is the Effect?

| Rating | Criteria | Effect Description |
|--------|----------|-------------------|
| 10 | Hazardous without warning | Safety issue, regulatory non-compliance, no warning |
| 9 | Hazardous with warning | Safety issue with warning possible |
| 8 | Very High | Product/process inoperable, 100% affected |
| 7 | High | Product/process operable but degraded, most affected |
| 6 | Moderate | Product/process operable but some items not functional |
| 5 | Low | Product/process operable but comfort/convenience reduced |
| 4 | Very Low | Fit, finish, or appearance issue, noticed by most |
| 3 | Minor | Fit, finish, or appearance issue, noticed by some |
| 2 | Very Minor | Fit, finish, or appearance issue, noticed by few |
| 1 | None | No discernible effect |

---

### Occurrence (O) - How Likely is the Cause?

| Rating | Criteria | Probability | Cpk Equivalent |
|--------|----------|-------------|----------------|
| 10 | Very High | ≥ 100 per 1,000 | < 0.33 |
| 9 | | 50 per 1,000 | ≈ 0.33 |
| 8 | High | 20 per 1,000 | ≈ 0.51 |
| 7 | | 10 per 1,000 | ≈ 0.67 |
| 6 | Moderate | 5 per 1,000 | ≈ 0.83 |
| 5 | | 2 per 1,000 | ≈ 1.00 |
| 4 | | 1 per 1,000 | ≈ 1.17 |
| 3 | Low | 0.5 per 1,000 | ≈ 1.33 |
| 2 | | 0.1 per 1,000 | ≈ 1.50 |
| 1 | Remote | ≤ 0.01 per 1,000 | ≥ 1.67 |

---

### Detection (D) - How Likely to Detect Before Customer?

| Rating | Criteria | Detection Method |
|--------|----------|------------------|
| 10 | Almost impossible | No detection method available |
| 9 | Very remote | Detection method not reliable |
| 8 | Remote | Detection is difficult |
| 7 | Very low | Low capability detection |
| 6 | Low | May detect failure mode |
| 5 | Moderate | Moderate chance of detection |
| 4 | Moderately high | Good chance of detection |
| 3 | High | High probability of detection |
| 2 | Very high | Almost certain detection |
| 1 | Almost certain | Failure mode will be detected |

---

## RPN Calculation

**RPN = Severity × Occurrence × Detection**

- Minimum: 1 × 1 × 1 = 1
- Maximum: 10 × 10 × 10 = 1,000

### Action Priority Guidelines

| RPN Range | Priority Level | Action Required |
|-----------|---------------|-----------------|
| > 200 | Critical | Immediate action required |
| 100-200 | High | Action plan required |
| 50-100 | Medium | Consider action |
| < 50 | Low | Monitor, document |

**Note**: Also consider high Severity (≥ 8) items regardless of RPN.

---

## Detailed Failure Mode Analysis

### Item 1: [Process Step / Component Name]

**Failure Mode**: [How it could fail]

**Effects of Failure**:
- On next operation: [Effect]
- On end customer: [Effect]
- Severity Rating: [1-10]

**Potential Causes**:
| Cause | Occurrence Rating |
|-------|-------------------|
| [Cause 1] | [1-10] |
| [Cause 2] | [1-10] |

**Current Controls**:
| Control Type | Control Description | Detection Rating |
|--------------|---------------------|------------------|
| Prevention | [What prevents this?] | |
| Detection | [What detects this?] | [1-10] |

**RPN Calculation**:
- S = [value] × O = [value] × D = [value] = **RPN = [value]**

**Recommended Action**:
[Action to reduce S, O, or D]

---

## Summary of High-Risk Items

| Rank | Process Step | Failure Mode | RPN | Priority Action |
|------|--------------|--------------|-----|-----------------|
| 1 | [Step] | [Mode] | [RPN] | [Action] |
| 2 | [Step] | [Mode] | [RPN] | [Action] |
| 3 | [Step] | [Mode] | [RPN] | [Action] |
| 4 | [Step] | [Mode] | [RPN] | [Action] |
| 5 | [Step] | [Mode] | [RPN] | [Action] |

---

## Action Tracking

| Action # | Action Description | Owner | Due Date | Status | Completion Date |
|----------|-------------------|-------|----------|--------|-----------------|
| 1 | [Action] | [Name] | [Date] | [ ] Open [ ] Closed | [Date] |
| 2 | [Action] | [Name] | [Date] | [ ] Open [ ] Closed | [Date] |
| 3 | [Action] | [Name] | [Date] | [ ] Open [ ] Closed | [Date] |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial FMEA |
| | | | |

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| FMEA Lead | [Name] | _________ | _____ |
| Process Owner | [Name] | _________ | _____ |
| Quality | [Name] | _________ | _____ |
