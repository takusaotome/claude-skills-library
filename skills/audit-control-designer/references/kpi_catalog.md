# Audit Control KPI Catalog

This document defines Key Performance Indicators (KPIs) for measuring the effectiveness of internal controls. KPIs are generalized from real audit engagements and applicable across industries.

---

## KPI Index

| KPI ID | Name | Primary Assertion | Process Pattern |
|---|---|---|---|
| K01 | Transcription Error Rate | Accuracy | AP |
| K02 | Stocktake Variance Rate | Existence | Inventory |
| K03 | Invoice Variance Rate | Completeness | AP |
| K04 | Resubmission Rate | Accuracy | AP / Reporting |
| K05 | Re-calculation Rate | Accuracy | COGS Calculation |
| K06 | Exception Incidence Rate | Cut-off, Completeness | Returns/Credits |
| K07 | Settlement Variance Rate | Accuracy | Cash/Payment |
| K08 | Period Attribution Error Rate | Cut-off | Returns/Credits, AP |

---

## K01: Transcription Error Rate

### Definition

The ratio of transcription entries that required correction to total transcription entries, measuring the accuracy of manual data entry.

### Formula

```
K01 = (Corrected transcription entries / Total transcription entries) × 100%
```

### Applicable Controls

- T-AP-01 (Invoice Entry Completeness)
- T-AP-02 (Invoice Matching)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Daily |
| Aggregation level | Per location, then consolidated |
| Data source | Entry correction logs, matching variance reports |
| Assertion | Accuracy |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Industry average (manual entry) | 1-3% | Structural error rate in manual transcription |
| Initial baseline | TBD (measure first) | Establish current state before setting targets |
| Short-term target | < 2% | Achievable with standardized templates |
| Medium-term target | < 0.5% | Requires OCR/automation |

---

## K02: Stocktake Variance Rate

### Definition

The ratio of variance quantity to total counted quantity in physical inventory counts, measuring the accuracy of inventory records.

### Formula

```
K02 = (Σ |Book quantity - Counted quantity| / Σ Counted quantity) × 100%
```

Note: Use absolute values to capture both over- and under-counts.

### Applicable Controls

- T-INV-01 (Physical Inventory Count)
- T-INV-02 (Inventory Adjustment Approval)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Monthly (at stocktake) |
| Aggregation level | Per item category, per location, then consolidated |
| Data source | Count sheets vs. book records |
| Assertion | Existence |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Industry average (F&B) | 2-5% | High perishability and manual counting |
| Industry average (Retail) | 1-3% | Higher SKU accuracy with barcode scanning |
| Short-term target | < 5% | Achievable with standardized procedures |
| Medium-term target | < 2% | Requires electronic counting tools |

---

## K03: Invoice Variance Rate

### Definition

The ratio of invoices with unresolved variances to total invoices processed, measuring the completeness and accuracy of accounts payable processing.

### Formula

```
K03 = (Invoices with unresolved variances / Total invoices processed) × 100%
```

### Applicable Controls

- T-AP-02 (Invoice Matching)
- T-AP-01 (Invoice Entry Completeness)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Daily/Weekly |
| Aggregation level | Per vendor, per location, then consolidated |
| Data source | Matching log, variance reports |
| Assertion | Completeness |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Initial baseline | TBD (measure first) | Establish current state |
| Short-term target | < 5% | Variance rate with manual reconciliation |
| Medium-term target | < 2% | With semi-automated matching |

---

## K04: Resubmission Rate

### Definition

The ratio of data submissions (daily reports, invoice packages, etc.) that were rejected and required resubmission to total submissions.

### Formula

```
K04 = (Resubmitted items / Total submitted items) × 100%
```

### Applicable Controls

- T-AP-01 (indirectly — measures data quality at entry)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Daily |
| Aggregation level | Per location, then consolidated |
| Data source | Submission tracking log |
| Assertion | Accuracy |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Initial baseline | TBD | Measure resubmission frequency |
| Short-term target | < 10% | With standardized templates |
| Medium-term target | < 3% | With validation rules at submission |

---

## K05: Re-calculation Rate

### Definition

The frequency of COGS or financial re-calculations per period, measuring the stability and reliability of the calculation process.

### Formula

```
K05 = (Number of re-calculations / Number of period-end closes) × 100%
```

Note: A rate of 100% means one re-calculation per close. Target is to minimize re-calculations caused by process failures (as opposed to legitimate late inputs).

### Applicable Controls

- T-CALC-01 (Template Management)
- T-CALC-02 (Re-calculation Change Management)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Monthly |
| Aggregation level | Per entity |
| Data source | Re-calculation log, change reason documents |
| Assertion | Accuracy (Reproducibility) |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Current typical | 100-300% (1-3 re-runs per close) | Common in manual environments |
| Short-term target | Documented reasons for all re-runs | Not about reducing count, but managing it |
| Medium-term target | < 100% (re-runs are exceptions, not routine) | Requires upstream process improvements |

---

## K06: Exception Incidence Rate

### Definition

The ratio of exception cases (returns, disputes, escalations) to total transactions in the related process.

### Formula

```
K06 = (Exception cases / Total transactions) × 100%
```

### Applicable Controls

- T-CO-01 (Returns Cut-off Verification)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Monthly |
| Aggregation level | Per exception type, then consolidated |
| Data source | Exception management log |
| Assertion | Cut-off, Completeness |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Initial baseline | TBD | Measure exception frequency |
| Target | Monitoring trend, not absolute value | Focus on reducing recurring exceptions |

---

## K07: Settlement Variance Rate

### Definition

The ratio of payment settlement variances to total settlements, measuring the accuracy of payment processing and reconciliation.

### Formula

```
K07 = (Settlement variances / Total settlements) × 100%
```

### Applicable Controls

- (Custom controls for payment reconciliation)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Monthly |
| Aggregation level | Per payment method, per processor |
| Data source | Settlement reports, bank reconciliation |
| Assertion | Accuracy |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Initial baseline | TBD | Measure current variance rate |
| Target | < 1% | With automated reconciliation |

---

## K08: Period Attribution Error Rate

### Definition

The ratio of transactions near period-end that were attributed to the wrong accounting period, measuring cut-off accuracy.

### Formula

```
K08 = (Mis-attributed transactions / Total transactions in cut-off window) × 100%
```

Note: "Cut-off window" is typically ±5 business days around the period boundary.

### Applicable Controls

- T-CO-01 (Returns Cut-off Verification)

### Measurement Details

| Attribute | Value |
|---|---|
| Collection frequency | Monthly |
| Aggregation level | Per transaction type |
| Data source | Cut-off verification list |
| Assertion | Cut-off |

### Baseline and Target Guidelines

| Level | Value | Interpretation |
|---|---|---|
| Initial baseline | TBD | Measure attribution accuracy |
| Short-term target | < 5% | With defined base date rules |
| Medium-term target | < 1% | With automated period assignment |

---

## KPI Selection Guidelines

### For Control Design

1. Every control should have at least one associated KPI
2. High-risk controls should have dedicated KPIs
3. KPIs should be measurable with available data sources
4. Baseline measurement must precede target setting

### For Roadmap Initiatives

1. Each roadmap initiative should link to 1-2 KPIs as success criteria
2. Short-term initiatives: focus on "measurement starts" as the success criterion
3. Medium-term initiatives: set numerical targets based on baseline data
4. All KPI targets should be reviewed and adjusted after the first measurement cycle

### KPI Assignment Template

| Control ID | KPI | Current Baseline | Short-term Target | Medium-term Target | Data Source |
|---|---|---|---|---|---|
| | | TBD | | | |
