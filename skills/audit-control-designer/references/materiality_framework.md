# Materiality Framework

This document defines the materiality framework used in control design, providing guidelines for setting thresholds at the overall and control-specific levels.

---

## 1. Materiality Hierarchy

Materiality operates at three levels, from broadest to most granular:

```
Overall Materiality
  └── Performance Materiality (50-75% of Overall)
        └── Clearly Trivial Threshold (3-5% of Overall)
```

### 1.1 Overall Materiality

**Definition**: The maximum amount of uncorrected misstatements that, individually or in aggregate, would be expected to influence the economic decisions of financial statement users.

**Determination**: Set by the external auditor based on a percentage of an appropriate benchmark.

| Benchmark | Typical Range | Common Application |
|---|---|---|
| Revenue | 0.5-1% | Revenue-driven businesses (retail, services) |
| Total Assets | 0.5-1% | Asset-heavy businesses (manufacturing, real estate) |
| Pre-tax Income | 5-10% | Profitable, stable businesses |
| COGS | 1-2% | Cost-driven businesses (F&B, manufacturing) |
| Equity | 1-2% | Regulated entities (financial institutions) |

**Note**: The formal Overall Materiality is set by the external auditor. For internal control design purposes, use a provisional estimate based on the most relevant benchmark, and note it as "(provisional — pending auditor confirmation)".

### 1.2 Performance Materiality

**Definition**: The amount set below Overall Materiality to reduce the probability that the aggregate of uncorrected and undetected misstatements exceeds Overall Materiality. Used for planning the nature, timing, and extent of audit procedures.

**Determination**:

```
Performance Materiality = Overall Materiality × (50-75%)
```

The percentage depends on:

| Factor | Lower End (50%) | Higher End (75%) |
|---|---|---|
| Prior year misstatements | Many/significant | Few/minor |
| Risk assessment | Higher risk | Lower risk |
| First-year audit | Yes | No |
| Management reliability | Lower confidence | Higher confidence |

**Application in Control Design**: Performance Materiality is the primary threshold used for:
- Determining control testing sample sizes
- Setting investigation thresholds for variances
- Deciding when to escalate findings

### 1.3 Clearly Trivial Threshold

**Definition**: The amount below which misstatements are obviously trivial and need not be accumulated or reported.

**Determination**:

```
Clearly Trivial = Overall Materiality × (3-5%)
```

**Application**: Items below this threshold do not need to be tracked as findings. This prevents over-investigation of immaterial items.

---

## 2. Control-Specific Thresholds

Each control should have a threshold that triggers investigation or escalation. Control thresholds must be set within the materiality framework.

### 2.1 Threshold Setting Principles

| Principle | Description |
|---|---|
| **Below Performance Materiality** | Control thresholds must be lower than Performance Materiality to provide early warning |
| **Actionable** | Thresholds should trigger a specific, defined action |
| **Measurable** | Must be expressed in quantifiable terms (dollars, percentages, counts) |
| **Consistent** | Related controls should use consistent threshold logic |

### 2.2 Threshold Types

| Type | Expression | Example |
|---|---|---|
| **Absolute amount** | Fixed dollar/currency threshold | "$100 per invoice" |
| **Percentage** | Percentage of a reference amount | "3% of invoice amount" |
| **Whichever-greater** | Higher of absolute or percentage | "$100 or 3% of invoice, whichever is greater" |
| **Aggregate** | Total across items in a period | "Total unresolved variances > 10% of Overall Materiality" |

### 2.3 Threshold Guidelines by Control Template

| Template | Suggested Threshold Basis | Typical Range |
|---|---|---|
| T-AP-01 | Item count: zero tolerance for unmatched items | 0 unmatched at day-end |
| T-AP-02 | Per-invoice variance | $100 or 3% of invoice amount, whichever is greater |
| T-INV-01 | Per-item count variance | ±5% (quantity basis) per item |
| T-INV-02 | Per-adjustment amount | 5% of Overall Materiality per adjustment entry |
| T-CO-01 | Aggregate unrecorded returns near period-end | 10% of Overall Materiality |
| T-VAL-01 | Time to update | 5 business days from receipt of revision notice |
| T-CALC-01 | Template integrity | Zero unauthorized formula changes |
| T-CALC-02 | Re-calculation approval | 100% approval rate; zero unapproved re-calculations |

---

## 3. Escalation Rules

### 3.1 Single-Item Escalation

When a single item exceeds its control threshold:

| Threshold Level | Action |
|---|---|
| Below Clearly Trivial | No action required |
| Between Clearly Trivial and Performance Materiality | Investigate and resolve at operational level |
| Between Performance Materiality and Overall Materiality | Escalate to accounting manager; document resolution |
| Above Overall Materiality | Escalate to senior management and external auditor |

### 3.2 Aggregate Escalation

When the aggregate of items in a period exceeds thresholds:

| Condition | Action |
|---|---|
| Aggregate findings < 10% of Overall Materiality | Monitor and resolve in normal course |
| Aggregate findings 10-50% of Overall Materiality | Accounting manager review; root cause analysis |
| Aggregate findings > 50% of Overall Materiality | Senior management notification; consider adjusting controls |
| Aggregate findings > Overall Materiality | External auditor notification required |

---

## 4. Materiality in Different Contexts

### 4.1 By Industry

| Industry | Primary Benchmark | Typical Overall Materiality | Special Considerations |
|---|---|---|---|
| **F&B** | COGS | 1-2% of monthly COGS | High perishability; shrinkage may be separately material |
| **Retail** | Revenue | 0.5-1% of revenue | High volume, low margin per transaction |
| **Manufacturing** | Revenue or COGS | 0.5-1% | WIP valuation, scrap, and rework may need separate thresholds |
| **Services** | Revenue or Pre-tax Income | 1-2% of revenue | Labor cost is primary; project-level materiality may apply |

### 4.2 By Regulatory Context

| Context | Impact on Materiality |
|---|---|
| **SEC/SOX (US)** | PCAOB standards; materiality for ICFR assessment may differ from financial statement materiality |
| **J-SOX (Japan)** | J-SOX materiality typically aligned with financial statement materiality |
| **Voluntary audit** | Management-defined materiality; more flexibility but less regulatory protection |
| **IPO preparation** | Often more conservative (lower) materiality to demonstrate control maturity |

---

## 5. Materiality Framework Template

Use this template to document the materiality framework for a specific engagement:

| Item | Value | Basis | Status |
|---|---|---|---|
| Overall Materiality | | % of [benchmark] | Provisional / Confirmed |
| Performance Materiality | | % of Overall Materiality | |
| Clearly Trivial | | % of Overall Materiality | |

### Control-Specific Thresholds

| Control ID | Threshold | Type | Escalation Level |
|---|---|---|---|
| | | Absolute / % / Aggregate | Manager / Senior Mgmt / Auditor |

### Notes

- Formal materiality is set by the external auditor; internal thresholds are provisional
- Review and adjust thresholds after the first period of measurement
- Document any deviations from the framework with justification
