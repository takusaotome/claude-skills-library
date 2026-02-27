# Check Rules — 12 Audit Document Quality Categories

This document defines the 12 check categories used by the audit-doc-checker skill. Each category includes its purpose, specific check items, severity criteria, and generalized examples.

---

## Category 1: Terminology Consistency (10 pts)

### Purpose

Verify that the same concept is referred to with consistent terminology throughout the document. Inconsistent terms create ambiguity and undermine auditability.

### Check Items

- Identify all domain-specific terms and verify each concept uses a single term consistently
- Check for synonyms used interchangeably (e.g., "external auditor" vs "audit firm" vs "CPA firm")
- Verify abbreviations are defined at first use and used consistently thereafter
- Check that role titles are consistent (e.g., not mixing "accounting manager" and "finance lead" for the same role)
- Verify process names match their IDs throughout the document

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | A term inconsistency creates ambiguity about which entity, role, or concept is being referenced, potentially affecting audit scope or control assignment |
| **Medium** | Terms are inconsistent but the intended meaning is clear from context |
| **Low** | Minor variations (e.g., abbreviation vs full name) where no ambiguity exists |

### Generalized Examples

- Using "IPO audit" and "financial statement audit" interchangeably when they have different scopes
- Mixing "store manager" and "location supervisor" for the same role in control assignments
- Using "invoice" and "bill" for the same document type without definition

---

## Category 2: Currency/Unit Consistency (10 pts)

### Purpose

Ensure all monetary amounts, measurement units, and quantitative references use a consistent system throughout the document. Mixed currencies or units invalidate threshold comparisons.

### Check Items

- Verify a base currency is explicitly stated (e.g., "All amounts in USD unless otherwise noted")
- Check that all monetary values use the same currency symbol/format
- Verify measurement units are consistent (e.g., not mixing kg and lbs, or hours and minutes for the same metric)
- Check that percentage bases are clearly defined (percentage of what?)
- Verify threshold values are stated with proper units

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | Mixed currencies without conversion basis (e.g., JPY thresholds in a USD-denominated document), making materiality judgments unreliable |
| **Medium** | Units are mixed but can be resolved with reasonable inference (e.g., "hours" vs "minutes" for effort estimates) |
| **Low** | Minor formatting inconsistencies (e.g., "$100" vs "USD 100") |

### Generalized Examples

- Document states "USD basis" but contains thresholds in JPY (e.g., "¥10,000")
- Mixing percentage bases: "5% of COGS" in one section, "5% of revenue" in another for the same threshold
- Effort estimates in minutes in one table and hours in another

---

## Category 3: Accounting Standards Alignment (15 pts)

### Purpose

Verify that all accounting treatment references, valuation methods, and regulatory citations are consistent with the stated accounting standard (US GAAP, IFRS, or J-GAAP).

### Check Items

- Verify the applicable accounting standard is explicitly stated
- Check that inventory valuation method references are valid under the stated standard
- Verify revenue recognition references cite the correct standard (ASC 606 / IFRS 15 / J-GAAP)
- Check that materiality concepts align with the relevant auditing standards (PCAOB / ISA / J-GAAS)
- Verify regulatory references match the jurisdiction (SEC, FSA, etc.)
- Check for LIFO usage under IFRS (prohibited) or J-GAAP (restricted)
- Verify lower-of-cost-or-market vs lower-of-cost-or-NRV treatment matches the standard

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | Direct contradiction with the stated accounting standard (e.g., citing J-GAAP inventory rules while claiming US GAAP compliance), or wrong regulatory body referenced |
| **Medium** | Reference to a valid but outdated or superseded standard, or missing standard citation for a material accounting treatment |
| **Low** | Minor citation format issues or references to generally accepted principles without specific ASC/IFRS paragraph numbers |

### Generalized Examples

- Stating "US GAAP" but citing "棚卸資産の評価に関する会計基準" (J-GAAP standard) for inventory valuation
- Referencing LIFO as the valuation method while claiming IFRS compliance
- Missing ASC 330 reference for inventory lower-of-cost-or-NRV treatment under US GAAP

---

## Category 4: Section Numbering/Cross-References (5 pts)

### Purpose

Verify that section/chapter numbers are sequential and that all internal cross-references point to existing sections with correct numbers.

### Check Items

- Verify section numbers are sequential without gaps or duplicates
- Check that all "see Section X.Y" references point to sections that exist
- Verify table/figure numbering is sequential
- Check that appendix references match actual appendix content
- Verify that change log references (e.g., "added in v3, section 8.1") match the actual document structure

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | A cross-reference points to a non-existent section that contains critical audit information (e.g., "SoD analysis in Section 8.1" when SoD is actually in 8.3) |
| **Medium** | Numbering gaps that cause confusion but referenced content exists elsewhere |
| **Low** | Minor numbering inconsistencies that don't affect navigation |

### Generalized Examples

- Change log says "added SoD analysis to Section 8.1" but it's actually Section 8.3
- Section 6 references "see Section 10.3 for expected outcomes" but Section 10 only goes to 10.2
- Appendix B is referenced but only Appendix A exists

---

## Category 5: Control Logic Consistency (15 pts)

### Purpose

Verify that control procedures, remediation actions, and expected outcomes form a logically consistent framework without internal contradictions.

### Check Items

- Check that each control's "procedure" logically achieves its stated "objective"
- Verify that "remediation" actions are actionable when the control detects a failure
- Check that control dependencies are acknowledged (e.g., C05 depends on a TBD decision, so its effectiveness is conditional)
- Verify that frequency and timing of controls are feasible (e.g., a daily control can't depend on monthly data)
- Check for contradictions between control descriptions and expected outcomes
- Verify that control type (preventive/detective) matches the procedure description
- Check that controls referencing "TBD" items are flagged as not fully implementable

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | A control procedure contradicts its remediation (e.g., cut-off rule is "TBD" but expected outcome says "fully implemented"), or a preventive control is described with detective characteristics |
| **Medium** | Control logic is sound but missing edge cases or exception handling |
| **Low** | Minor wording inconsistencies that don't affect the control's logical validity |

### Generalized Examples

- Control C05 references a "TBD accounting base date" but the roadmap says "framework established"
- A detective control lists "prevent errors" as its objective
- A monthly control claims to provide "daily monitoring" capability

---

## Category 6: Materiality Criteria Application (10 pts)

### Purpose

Verify that materiality thresholds are properly defined, internally consistent, and applied correctly throughout the document.

### Check Items

- Check that Overall Materiality is defined with a clear basis (e.g., "1-2% of COGS")
- Verify Performance Materiality is defined (typically 50-75% of Overall)
- Check that Clearly Trivial threshold is defined (typically 3-5% of Overall)
- Verify control-specific thresholds are consistent with the overall framework
- Check that threshold values are used consistently in control procedures and remediation actions
- Verify that qualitative materiality factors are considered where appropriate

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | Performance Materiality is missing entirely, or control thresholds exceed Overall Materiality (logically impossible) |
| **Medium** | Materiality is defined but not consistently applied in control thresholds, or the relationship between overall and performance materiality is unclear |
| **Low** | Materiality framework exists but lacks specific numerical thresholds (marked as TBD with clear resolution plan) |

### Generalized Examples

- Only Overall Materiality defined; no Performance Materiality or Clearly Trivial threshold
- Control threshold set at "5% of COGS" but Overall Materiality is "1-2% of COGS" (threshold exceeds materiality)
- Different controls use different materiality bases without explanation

---

## Category 7: Assertion Coverage (10 pts)

### Purpose

Verify that the five primary audit assertions (C/A/V/CO/E) are adequately covered by the designed controls, with no material gaps.

### Check Items

- Map each control to its covered assertions
- Check that all five assertions have at least one control
- Verify that high-risk assertions have multiple controls (defense in depth)
- Check for assertions that are mentioned in risk analysis but not addressed by any control
- Verify that the assertion mapping is consistent between the control table and the assertion mapping section
- Check for KPIs that directly measure each assertion's coverage

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | One or more assertions have zero control coverage, especially if identified as a risk in the analysis |
| **Medium** | All assertions are covered but some have only indirect or weak coverage (e.g., Cut-off covered only by a control with a TBD base date) |
| **Low** | Coverage exists but the assertion mapping table is incomplete or inconsistent with control descriptions |

### Generalized Examples

- Cut-off assertion identified as a risk but no KPI directly measures period attribution errors
- Existence assertion covered only by a stocktake control without double-count verification
- Completeness and Accuracy both claimed by one control with no differentiation in procedure

---

## Category 8: SoD Analysis Presence (5 pts)

### Purpose

Verify that segregation of duties risks are explicitly analyzed, with compensating controls identified for cases where full separation is not feasible.

### Check Items

- Check that SoD analysis section exists in the document
- Verify that key duty pairs are identified (entry/approval, ordering/receiving, recording/custody, counting/booking, calculation/verification)
- Check that each pair has a risk rating (High/Medium/Low)
- Verify that compensating controls are specified for pairs that cannot be fully separated
- Check that SoD recommendations are reflected in control procedures (e.g., "two persons required" in stocktake control)

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | No SoD analysis exists in a document that includes control design |
| **Medium** | SoD analysis exists but is incomplete (missing key pairs) or lacks compensating controls for identified risks |
| **Low** | SoD analysis is complete but not cross-referenced to control procedures |

### Generalized Examples

- Control design document with 8 controls but no SoD section
- SoD analysis identifies "entry and approval" separation but doesn't specify who should be separated
- High-risk SoD pair identified but no compensating control for small organizations

---

## Category 9: Open Items Management (10 pts)

### Purpose

Verify that all unresolved decisions, TBD items, and assumptions are explicitly tracked with clear ownership, options, and resolution timelines.

### Check Items

- Search for "TBD", "to be confirmed", "undecided", "pending", "open question" markers
- Check that each TBD item has: description, options, recommendation, owner, and timeline
- Verify that the document acknowledges the impact of unresolved items on related controls
- Check that status labels ("hypothesis", "estimate", "provisional") are used where appropriate
- Verify no implicit assumptions that should be explicit (e.g., assuming an accounting policy without stating it)

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | TBD items exist in critical control procedures without explicit tracking, or the document presents assumptions as facts without qualification |
| **Medium** | TBD items are tracked but missing resolution timeline or owner |
| **Low** | TBD items are well-managed but could benefit from more structured tracking format |

### Generalized Examples

- GRNI accrual policy referenced as "to be confirmed" in a control procedure but not listed in Open Questions
- Estimated values presented without "(estimate)" or "(provisional)" markers
- Cut-off base date marked TBD but the expected outcome section says "framework established"

---

## Category 10: Preventive/Detective Classification (5 pts)

### Purpose

Verify that each control is classified as preventive or detective, and that the classification matches the control's actual mechanism. Identify over-reliance on one type.

### Check Items

- Check that each control has a type classification (Preventive or Detective)
- Verify the classification matches the control description:
  - Preventive: Stops errors before they occur (e.g., system validation, approval before posting)
  - Detective: Identifies errors after they occur (e.g., reconciliation, variance analysis)
- Calculate the preventive/detective ratio
- Flag if all controls are detective (common in paper+Excel environments) with a note about migration path to preventive controls

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | No classification column exists in the control table |
| **Medium** | Classification exists but is incorrect for multiple controls, or all controls are one type without acknowledgment |
| **Low** | Minor misclassification for one control, or the document acknowledges the type imbalance |

### Generalized Examples

- Control table has no "Type" column
- A reconciliation control (detective) is labeled as "preventive"
- All 8 controls are detective but no note about moving toward preventive controls in the roadmap

---

## Category 11: Success Criteria Definition (5 pts)

### Purpose

Verify that roadmap initiatives and improvement plans have measurable success criteria (KPIs, targets, or completion definitions).

### Check Items

- Check that each roadmap initiative has at least one success criterion
- Verify success criteria are measurable (not just "improve" or "optimize")
- Check that KPI targets are linked to specific controls or initiatives
- Verify that baseline measurement plans exist for KPIs without current baselines
- Check that milestone dates use a consistent format (e.g., M+N notation)

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | Multiple initiatives have no success criteria and no KPI linkage |
| **Medium** | Success criteria exist but are vague or not measurable |
| **Low** | Success criteria are defined but missing baseline measurement plans |

### Generalized Examples

- Roadmap says "Standardize stocktake procedure" with no success metric
- Success criterion is "improve accuracy" without specifying target rate
- KPI targets specified but no plan for measuring the baseline

---

## Category 12: Metadata Freshness (5 pts)

### Purpose

Verify that document metadata (version number, last updated date, status, author) is consistent with the actual content.

### Check Items

- Check that version number in metadata matches the change log
- Verify the "last updated" date is plausible given the content
- Check that the status label (e.g., "draft", "pre-interview hypothesis") matches the document's maturity
- Verify author/owner information is present
- Check that the change log accurately reflects the differences between versions

### Severity Criteria

| Severity | Condition |
|---|---|
| **High** | Version number and change log are contradictory (e.g., metadata says "v4" but content includes v5 changes) |
| **Medium** | Metadata is present but partially outdated |
| **Low** | Minor metadata inconsistencies (e.g., missing author field) |

### Generalized Examples

- Metadata says "v4" but the change log includes a "v5" entry
- Status says "final" but document contains multiple TBD items
- Last updated date is 3 months old but the change log shows recent additions
