# Risk Assessment Framework

This framework provides a structured methodology for quantifying and prioritizing contract risks.

## 1. Risk Scoring Methodology

### 1.1 Two-Dimensional Scoring

Each finding is scored on two dimensions:
- **Likelihood (L)**: Probability the risk will materialize
- **Impact (I)**: Severity of consequences if risk materializes

**Risk Score = Likelihood × Impact** (Range: 1-25)

### 1.2 Likelihood Scale

| Score | Level | Description | Indicators |
|-------|-------|-------------|-----------|
| 1 | Rare | Highly unlikely to occur | Strong contractual protections exist; no history of occurrence |
| 2 | Unlikely | Could occur but not expected | Some protections exist; rare in industry |
| 3 | Possible | May occur | Standard industry terms; occasional occurrence |
| 4 | Likely | Expected to occur | Weak protections; common occurrence |
| 5 | Almost Certain | Will occur unless addressed | No protection; counterparty history of behavior |

**Likelihood Assessment Questions**:
- Has this risk materialized in similar contracts?
- What is the counterparty's track record?
- Are there contractual safeguards in place?
- What are industry norms?

### 1.3 Impact Scale

| Score | Level | Description | Financial Threshold | Operational Threshold |
|-------|-------|-------------|--------------------|-----------------------|
| 1 | Negligible | Minimal impact | <$10K or <1% contract value | No operational disruption |
| 2 | Minor | Limited impact, easily managed | $10K-$50K or 1-5% | Minor inconvenience |
| 3 | Moderate | Noticeable impact | $50K-$250K or 5-15% | Temporary disruption |
| 4 | Major | Significant impact | $250K-$1M or 15-50% | Significant disruption |
| 5 | Severe | Critical, potential deal-breaker | >$1M or >50% | Business continuity threat |

**Impact Assessment Questions**:
- What is the maximum financial exposure?
- Could this affect operations?
- Are there reputational consequences?
- Could this lead to regulatory issues?

---

## 2. Risk Matrix

### 2.1 Visual Matrix

```
                        IMPACT
           1        2        3        4        5
         Negl.    Minor    Mod.     Major   Severe
       +--------+--------+--------+--------+--------+
     5 |   M    |   H    |   H    |   C    |   C    |  Almost
       |  (5)   |  (10)  |  (15)  |  (20)  |  (25)  |  Certain
       +--------+--------+--------+--------+--------+
     4 |   M    |   M    |   H    |   H    |   C    |  Likely
L      |  (4)   |  (8)   |  (12)  |  (16)  |  (20)  |
I      +--------+--------+--------+--------+--------+
K    3 |   L    |   M    |   M    |   H    |   H    |  Possible
E      |  (3)   |  (6)   |  (9)   |  (12)  |  (15)  |
L      +--------+--------+--------+--------+--------+
I    2 |   L    |   L    |   M    |   M    |   H    |  Unlikely
H      |  (2)   |  (4)   |  (6)   |  (8)   |  (10)  |
O      +--------+--------+--------+--------+--------+
O    1 |   L    |   L    |   L    |   M    |   M    |  Rare
D      |  (1)   |  (2)   |  (3)   |  (4)   |  (5)   |
       +--------+--------+--------+--------+--------+
```

### 2.2 Risk Level Definitions

| Level | Score Range | Color | Action Required |
|-------|-------------|-------|-----------------|
| **Critical (C)** | 20-25 | Red | Must address before signing; potential deal-breaker |
| **High (H)** | 10-19 | Orange | Negotiate to reduce; escalate if unsuccessful |
| **Medium (M)** | 4-9 | Yellow | Address if possible; accept with monitoring |
| **Low (L)** | 1-3 | Green | Accept; document for awareness |

---

## 3. Risk Categories

### 3.1 Category Definitions

| Category | Description | Examples |
|----------|-------------|----------|
| **Financial** | Direct monetary exposure | Liability, indemnification, pricing, penalties |
| **Operational** | Impact on business operations | Termination, SLA, service continuity |
| **Legal** | Legal and regulatory exposure | Compliance, jurisdiction, IP disputes |
| **Strategic** | Long-term business implications | Exclusivity, IP ownership, competitive |
| **Reputational** | Brand and relationship impact | Data breach, service failure, disputes |

### 3.2 Category-Specific Thresholds

**Financial Risks**:
| Risk Type | Low | Medium | High | Critical |
|-----------|-----|--------|------|----------|
| Liability exposure | <1x annual fees | 1-3x annual fees | 3-10x annual fees | >10x or unlimited |
| Indemnification | Capped & mutual | Capped, one-sided | Uncapped one-sided | Broad & unlimited |
| Penalties | <5% contract value | 5-15% | 15-50% | >50% |

**Operational Risks**:
| Risk Type | Low | Medium | High | Critical |
|-----------|-----|--------|------|----------|
| Lock-in period | <1 year | 1-2 years | 2-3 years | >3 years |
| Termination notice | 30 days | 60-90 days | 90-120 days | >120 days |
| SLA commitment | 99.99% | 99.9% | 99.5% | <99.5% or none |

**Legal Risks**:
| Risk Type | Low | Medium | High | Critical |
|-----------|-----|--------|------|----------|
| Jurisdiction | Home country | Familiar foreign | Unfamiliar | Hostile/unknown |
| Data protection | Full compliance | Minor gaps | Significant gaps | No provisions |
| IP assignment | Clear boundaries | Some ambiguity | Broad grants | Full assignment |

---

## 4. Overall Contract Risk Score

### 4.1 Calculation Method

**Step 1: Score Individual Findings**
For each finding:
- Assign Likelihood (1-5)
- Assign Impact (1-5)
- Calculate Risk Score = L × I

**Step 2: Apply Severity Weights**

| Severity Level | Weight Factor |
|----------------|---------------|
| Critical | 3.0x |
| High | 2.0x |
| Medium | 1.0x |
| Low | 0.5x |

**Step 3: Calculate Weighted Sum**
```
Weighted Sum = Σ(Finding Score × Weight Factor)
```

**Step 4: Normalize to 0-100 Scale**
```
Overall Score = (Weighted Sum / Maximum Possible Score) × 100

Where Maximum Possible Score = (Number of Findings × 25 × 3)
```

### 4.2 Simplified Calculation

For quick assessment:
```
Overall Score = (Critical × 20) + (High × 10) + (Medium × 5) + (Low × 2)

Capped at 100
```

### 4.3 Score Interpretation

| Score Range | Risk Level | Interpretation | Recommended Action |
|-------------|------------|----------------|-------------------|
| 0-25 | Low | Acceptable risk profile | Minor negotiation; can approve |
| 26-50 | Moderate | Manageable risks present | Negotiate key terms; conditional approve |
| 51-75 | High | Significant risk exposure | Major negotiation required; escalate |
| 76-100 | Critical | Unacceptable risk profile | Do not sign; consider alternatives |

---

## 5. Risk Aggregation

### 5.1 By Category Summary

```markdown
| Category | Critical | High | Medium | Low | Category Score |
|----------|----------|------|--------|-----|---------------|
| Financial | | | | | |
| Operational | | | | | |
| Legal | | | | | |
| Strategic | | | | | |
| Reputational | | | | | |
| **Total** | | | | | |
```

### 5.2 Concentration Analysis

Check for risk concentration:
- Multiple Critical/High findings in one category = heightened concern
- Single category driving >50% of total score = systemic issue
- Findings that compound each other = multiplied risk

---

## 6. Risk Prioritization

### 6.1 Prioritization Matrix

Prioritize findings based on:

1. **Severity First**: Critical → High → Medium → Low
2. **Within Severity**: Higher L×I score first
3. **Negotiability**: More negotiable items higher

### 6.2 Top 10 Risks Table

```markdown
| Rank | ID | Title | L | I | Score | Category | Negotiable |
|------|-----|-------|---|---|-------|----------|------------|
| 1 | | | | | | | Y/N |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | |
```

---

## 7. Decision Framework

### 7.1 Go/No-Go Criteria

**Automatic No-Go**:
- Any Critical finding without acceptable mitigation
- Overall score > 75 without clear path to reduction
- Legal counsel recommends rejection

**Conditional Go**:
- Overall score 26-75
- Critical findings can be negotiated
- Risk mitigation plan in place

**Go**:
- Overall score ≤ 25
- No Critical findings
- Risks within tolerance

### 7.2 Risk Tolerance Guidelines

| Contract Type | Risk Tolerance | Score Threshold |
|---------------|---------------|-----------------|
| Strategic partnership | Higher | ≤ 60 acceptable |
| Standard vendor | Moderate | ≤ 50 acceptable |
| Commodity purchase | Lower | ≤ 35 acceptable |
| High-value/long-term | Lower | ≤ 40 acceptable |

### 7.3 Escalation Criteria

Escalate to legal/senior management when:
- Any Critical finding identified
- Overall score > 50
- Unusual or non-standard terms
- Contract value exceeds threshold
- Strategic or precedent-setting deal

---

## 8. Risk Monitoring

### 8.1 Post-Signature Monitoring

For approved contracts with elevated risk:

| Risk Level | Monitoring Frequency | Actions |
|------------|---------------------|---------|
| Critical (accepted) | Monthly | Active tracking, management reporting |
| High | Quarterly | Review triggers, verify controls |
| Medium | Semi-annually | Renewal review, trigger check |
| Low | Annually | Standard renewal review |

### 8.2 Risk Triggers

Monitor for:
- Vendor performance issues
- Market rate changes
- Regulatory changes
- Vendor financial health
- Usage pattern changes

### 8.3 Documentation Requirements

Maintain records of:
- Original risk assessment
- Negotiation outcomes
- Residual risks accepted
- Monitoring actions taken
- Risk materializations
