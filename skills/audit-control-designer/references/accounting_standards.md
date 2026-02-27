# Accounting Standards Reference — Control Design Impact

This document summarizes the differences between US GAAP, IFRS, and J-GAAP that affect internal control design. Only items with direct impact on control procedures are included.

---

## 1. Inventory Valuation

### Cost Flow Methods

| Method | US GAAP (ASC 330) | IFRS (IAS 2) | J-GAAP |
|---|---|---|---|
| **FIFO** | Permitted | Permitted | Permitted |
| **Weighted Average** | Permitted | Permitted | Permitted |
| **LIFO** | Permitted | **Prohibited** | Permitted (limited use) |
| **Specific Identification** | Required for unique items | Required for unique items | Permitted |

**Control Design Impact**:
- If IFRS applies: controls must enforce FIFO or weighted average only. Any LIFO usage is a compliance violation.
- If US GAAP applies with LIFO: additional LIFO reserve disclosure controls are needed. Consider FIFO for IFRS compatibility if dual reporting is anticipated.
- Cost method must be consistent across periods (accounting policy continuity).

### Lower-of-Cost-or-Market / Net Realizable Value

| Aspect | US GAAP (ASC 330-10-35) | IFRS (IAS 2.28-33) | J-GAAP |
|---|---|---|---|
| **Measurement** | Lower of cost or NRV (post ASU 2015-11 for non-LIFO) | Lower of cost or NRV | Lower of cost or NRV |
| **LIFO exception** | Lower of cost or market (floor/ceiling) for LIFO users | N/A (LIFO prohibited) | Lower of cost or market |
| **Reversal of write-down** | **Prohibited** | Permitted (up to original cost) | Permitted (up to original cost) |

**Control Design Impact**:
- US GAAP: Once inventory is written down, it cannot be written back up. Controls must prevent reversal entries.
- IFRS/J-GAAP: Write-down reversals are permitted but must be documented with evidence that conditions have changed.
- All standards: Period-end inventory valuation controls must include NRV assessment for perishable, obsolete, or slow-moving items.

---

## 2. Revenue Recognition

### Framework Comparison

| Aspect | US GAAP (ASC 606) | IFRS (IFRS 15) | J-GAAP |
|---|---|---|---|
| **Framework** | 5-step model | 5-step model (substantially converged) | Realization principle (converging toward IFRS) |
| **Contract identification** | Written, oral, or implied | Written, oral, or implied | Generally written |
| **Variable consideration** | Constrained estimate | Constrained estimate | Conservative recognition |
| **License revenue** | Point-in-time or over-time | Point-in-time or over-time | Varies |

**Control Design Impact**:
- ASC 606 / IFRS 15: Controls must verify proper identification of performance obligations and appropriate timing of recognition.
- For F&B/Retail with simple point-of-sale transactions: revenue recognition is straightforward, but gift cards, loyalty programs, and bundle pricing may require 5-step analysis.
- J-GAAP: May have different timing for certain transactions; controls should document the recognition criteria.

---

## 3. Lease Accounting

### Framework Comparison

| Aspect | US GAAP (ASC 842) | IFRS (IFRS 16) | J-GAAP |
|---|---|---|---|
| **Lessee classification** | Finance lease / Operating lease | Single model (all on balance sheet) | Finance lease / Operating lease |
| **Operating lease treatment** | Right-of-use asset + Lease liability (on balance sheet) | Right-of-use asset + Lease liability (on balance sheet) | Off-balance sheet (operating) |
| **Short-term exemption** | ≤ 12 months | ≤ 12 months | N/A |
| **Low-value exemption** | None | < ~$5,000 | N/A |

**Control Design Impact**:
- US GAAP / IFRS: Controls must ensure all leases (including operating) are properly capitalized with right-of-use assets and lease liabilities.
- J-GAAP: Operating leases remain off-balance sheet, but controls should ensure proper disclosure.
- All standards: Lease modification controls must capture changes and recompute lease liabilities.

---

## 4. Goodwill and Intangible Assets

### Impairment Testing

| Aspect | US GAAP (ASC 350) | IFRS (IAS 36) | J-GAAP |
|---|---|---|---|
| **Amortization** | Not amortized (indefinite-lived) | Not amortized (indefinite-lived) | Amortized (≤ 20 years) |
| **Impairment test** | Annual + trigger-based | Annual + trigger-based | Trigger-based only |
| **Impairment model** | Optional qualitative + quantitative | Single-step (recoverable amount) | Undiscounted cash flow first |
| **Reversal** | **Prohibited** | **Prohibited** | **Prohibited** |

**Control Design Impact**:
- US GAAP / IFRS: Annual impairment testing controls are required regardless of indicators.
- J-GAAP: Amortization controls needed; impairment testing only when indicators exist.
- All standards: Goodwill impairment reversals are prohibited across all three standards.

---

## 5. Provisions and Contingencies

| Aspect | US GAAP (ASC 450) | IFRS (IAS 37) | J-GAAP |
|---|---|---|---|
| **Recognition threshold** | "Probable" (>70-75% likely) | "Probable" (>50% likely) | "Probable" (similar to IFRS) |
| **Measurement** | Lower end of range (if no best estimate) | Best estimate (midpoint) | Best estimate |
| **Discounting** | Generally not required | Required if time value is material | Generally not required |

**Control Design Impact**:
- The "probable" threshold differs significantly between US GAAP and IFRS. A contingency at 60% likelihood would be recognized under IFRS but not US GAAP.
- Controls must apply the correct probability threshold for the applicable standard.
- Disclosure requirements differ: US GAAP requires disclosure of "reasonably possible" contingencies.

---

## 6. Summary: Key Control Design Decision Points

When designing controls, the accounting standard affects:

| Decision Point | What to Check |
|---|---|
| **Inventory cost method** | Is the chosen method permitted under the applicable standard? |
| **Inventory write-down reversal** | US GAAP prohibits reversal; IFRS/J-GAAP permit it |
| **Lease capitalization** | US GAAP/IFRS: all leases on balance sheet; J-GAAP: operating leases off-balance sheet |
| **Goodwill treatment** | J-GAAP: amortized; US GAAP/IFRS: impairment-tested |
| **Revenue recognition model** | ASC 606/IFRS 15: 5-step model; J-GAAP: realization principle |
| **Provision threshold** | US GAAP: >70-75%; IFRS/J-GAAP: >50% |
| **Regulatory body** | US GAAP: SEC/PCAOB; IFRS: local regulator + IAASB; J-GAAP: FSA/JICPA |

### Standard Selection Checklist for Control Design

Before starting control design, confirm:

- [ ] Applicable accounting standard is identified (US GAAP / IFRS / J-GAAP)
- [ ] Auditing standards are identified (PCAOB / ISA / J-GAAS)
- [ ] Inventory valuation method is confirmed and permitted under the standard
- [ ] Revenue recognition model requirements are understood
- [ ] Lease accounting treatment is determined
- [ ] Relevant ASC/IAS/IFRS paragraph references are documented
- [ ] Any areas of standard divergence that affect the engagement are flagged
