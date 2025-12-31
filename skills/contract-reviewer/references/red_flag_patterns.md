# Red Flag Patterns

This guide catalogs high-risk contract language patterns. When these patterns appear, they warrant careful scrutiny and typically negotiation.

## Quick Reference: Critical Red Flags

| # | Pattern | Risk Category | Severity |
|---|---------|--------------|----------|
| 1 | Unlimited liability | Financial | Critical |
| 2 | One-sided indemnification | Financial | Critical |
| 3 | Automatic renewal with difficult opt-out | Operational | High |
| 4 | Unilateral amendment rights | Legal | Critical |
| 5 | Problematic governing law | Legal | High |
| 6 | Broad IP assignment | IP/Strategic | Critical |
| 7 | No consequential damages exclusion | Financial | High |
| 8 | Excessive termination penalties | Financial | High |
| 9 | Non-compete/exclusivity | Operational | High |
| 10 | Inadequate data protection | Compliance | High |

---

## 1. Financial Risk Patterns

### 1.1 Unlimited Liability

**Pattern**: Missing liability cap or explicit unlimited liability.

**Dangerous Language**:
```
"Party shall be liable for all damages arising from..."

"Party shall indemnify and hold harmless for any and all claims..."

"Notwithstanding any other provision, there shall be no limit on
liability for..."
```

**Why It's Dangerous**:
- Unlimited exposure to damages
- Single claim could exceed company resources
- Insurance may not cover unlimited exposure

**Recommended Response**:
- Negotiate liability cap (12-24 months fees typical)
- Ensure cap applies to all claims
- Define limited carve-outs (gross negligence, willful misconduct)

---

### 1.2 One-Sided Indemnification

**Pattern**: Only one party provides indemnification.

**Dangerous Language**:
```
"Customer shall indemnify, defend, and hold harmless Provider from
any and all claims..."

[No corresponding vendor indemnification]
```

**Why It's Dangerous**:
- Absorbing risk that belongs with the vendor
- No protection for vendor's breaches/negligence
- Unbalanced risk allocation

**Recommended Response**:
- Request mutual indemnification
- At minimum: Vendor indemnifies for IP infringement, data breach, gross negligence
- Cap indemnification obligations

---

### 1.3 Unlimited Price Increases

**Pattern**: Vendor can increase prices without limit.

**Dangerous Language**:
```
"Provider may adjust pricing at any time upon 30 days' notice."

"Renewal pricing shall be determined at Provider's sole discretion."

"Prices subject to change without notice."
```

**Why It's Dangerous**:
- Budget uncertainty
- Lock-in with escalating costs
- No negotiating leverage at renewal

**Recommended Response**:
- Cap annual increases (CPI + 2%, or fixed 3-5%)
- Lock rates for initial term and first renewal
- Right to terminate without penalty if increase exceeds cap

---

### 1.4 Hidden Fees and Charges

**Pattern**: Vague additional charges not specified.

**Dangerous Language**:
```
"Plus applicable fees for additional services."

"Customer responsible for travel, expenses, and incidentals."

"Standard professional services rates apply."
```

**Why It's Dangerous**:
- Unpredictable costs
- Disputes over scope of included services
- Budget overruns

**Recommended Response**:
- Require fee schedule as exhibit
- Cap expenses or include in fixed fee
- Define "included" services explicitly

---

## 2. Operational Risk Patterns

### 2.1 Automatic Renewal with Difficult Opt-Out

**Pattern**: Auto-renewal with long notice period or complex cancellation.

**Dangerous Language**:
```
"This Agreement shall automatically renew for successive one-year
periods unless either party provides written notice of non-renewal
at least 120 days prior to the end of the then-current term."

"Cancellation requests must be submitted via registered mail to
the address specified in Exhibit A."
```

**Why It's Dangerous**:
- Easy to miss notice deadline
- Locked in for another term unintentionally
- Difficult to compare alternatives before commitment

**Recommended Response**:
- Reduce notice period to 30-60 days
- Accept email or electronic notice
- Require reminder notification 30 days before deadline
- Add right to terminate at convenience with reasonable notice

---

### 2.2 Service Level Exclusions

**Pattern**: Broad exceptions that undermine SLA protections.

**Dangerous Language**:
```
"SLA credits shall not apply to outages caused by factors outside
Provider's reasonable control, including but not limited to network
issues, third-party services, scheduled maintenance, or peak usage
periods."

"Customer must submit claims within 5 business days of the incident."
```

**Why It's Dangerous**:
- SLA effectively meaningless
- Most outages could be excluded
- Onerous claim process discourages claims

**Recommended Response**:
- Limit exclusions to true force majeure
- Require scheduled maintenance during defined windows
- Extend claim period to 30 days
- Automatic credit application (no claim needed)

---

### 2.3 Termination Restrictions

**Pattern**: No termination for convenience or excessive penalties.

**Dangerous Language**:
```
"Customer may not terminate this Agreement prior to the end of
the Term except for Provider's material breach."

"Early termination fee equal to 100% of remaining fees under the Term."

"Upon termination, Customer forfeits all prepaid fees."
```

**Why It's Dangerous**:
- Locked in if service unsatisfactory
- Excessive cost to exit
- No flexibility for business changes

**Recommended Response**:
- Add termination for convenience with notice (90 days)
- Cap early termination fee (remaining fees on declining basis)
- Pro-rata refund of prepaid fees
- Specify data portability rights

---

### 2.4 Non-Compete or Exclusivity

**Pattern**: Restrictions on using competitors or offering competing services.

**Dangerous Language**:
```
"Customer shall not use any products or services competitive with
the Services during the Term and for 12 months thereafter."

"Provider shall be Customer's exclusive provider of..."

"Customer agrees not to solicit or hire any Provider personnel..."
```

**Why It's Dangerous**:
- Limits business flexibility
- May prevent using better solutions
- Restraint of trade concerns

**Recommended Response**:
- Remove exclusivity unless significant discount
- Limit non-compete to direct competitive products
- Limit non-solicitation to active engagement + short tail period

---

## 3. Legal Risk Patterns

### 3.1 Unilateral Amendment Rights

**Pattern**: One party can change terms without consent.

**Dangerous Language**:
```
"Provider may modify these terms at any time by posting updated
terms on its website."

"Provider reserves the right to change pricing, features, or terms
upon 30 days' notice."

"Continued use after modification constitutes acceptance."
```

**Why It's Dangerous**:
- Terms can change unfavorably
- No negotiating power
- May not notice changes

**Recommended Response**:
- Require mutual written consent for changes
- At minimum: Material changes require acceptance
- Right to terminate without penalty if terms change unfavorably
- Lock terms for committed term

---

### 3.2 Problematic Governing Law

**Pattern**: Unfavorable or inconvenient jurisdiction.

**Dangerous Language**:
```
"This Agreement shall be governed by the laws of [foreign country]."

"Any disputes shall be resolved in courts located in [distant city]."

"All disputes shall be resolved through binding arbitration in
[inconvenient location] under [unfamiliar rules]."
```

**Why It's Dangerous**:
- Unfamiliar legal system
- Expensive to litigate
- Unpredictable outcomes

**Recommended Response**:
- Negotiate neutral or home jurisdiction
- For international deals: consider England, New York, Singapore
- If arbitration: negotiate location, rules, language
- Preserve right to seek injunctive relief in any court

---

### 3.3 Waiver of Legal Rights

**Pattern**: Broad waivers of rights or remedies.

**Dangerous Language**:
```
"Customer waives any right to trial by jury."

"Customer waives any right to participate in class action lawsuits."

"The remedies set forth herein shall be Customer's sole and
exclusive remedies."
```

**Why It's Dangerous**:
- Limited legal recourse
- May not be enforceable (but still creates friction)
- May waive important protections

**Recommended Response**:
- Remove if not necessary
- Ensure exclusive remedy provisions carve out termination right
- Preserve equitable remedies (injunctive relief)

---

### 3.4 Unlimited Audit Rights

**Pattern**: Overly broad or frequent audit rights.

**Dangerous Language**:
```
"Provider may audit Customer's use of the Services at any time
without prior notice."

"Customer shall bear all costs associated with any audit."

"If audit reveals any underpayment, Customer shall pay 150% of
the shortfall."
```

**Why It's Dangerous**:
- Disruptive to operations
- Fishing expeditions
- Punitive true-up penalties

**Recommended Response**:
- Limit to once per 12 months
- Require 30 days advance notice
- Audits during business hours only
- Vendor pays unless >5% variance
- True-up at standard rates (not penalty rates)

---

## 4. Intellectual Property Risk Patterns

### 4.1 Broad IP Assignment

**Pattern**: Assignment of IP beyond project deliverables.

**Dangerous Language**:
```
"All work product, inventions, and intellectual property created
in connection with the Services shall be owned exclusively by Provider."

"Customer assigns to Provider all right, title, and interest in
any feedback, suggestions, or improvements related to the Services."

"Customer grants Provider a perpetual, irrevocable, royalty-free
license to use Customer Data in any manner."
```

**Why It's Dangerous**:
- Losing ownership of valuable IP
- Paying to create assets for vendor
- Customer data used for vendor's benefit

**Recommended Response**:
- Customer owns: Custom deliverables, customer data, customer's pre-existing IP
- Limit feedback license to product improvement
- Restrict use of customer data to service delivery

---

### 4.2 Residual Knowledge Exception

**Pattern**: Exception allowing use of retained knowledge.

**Dangerous Language**:
```
"Nothing in this Agreement shall restrict either party from using
ideas, concepts, know-how, or techniques retained in the unaided
memory of its personnel."
```

**Why It's Dangerous**:
- Can completely undermine confidentiality
- Difficult to prove what was "retained"
- Trade secrets may be freely used

**Recommended Response**:
- Remove entirely if possible
- Limit to general skills and experience
- Exclude trade secrets and specifically identified confidential information

---

### 4.3 Insufficient IP Indemnification

**Pattern**: Weak or absent IP infringement indemnification.

**Dangerous Language**:
```
"Provider makes no representation that the Services do not infringe
any third-party intellectual property rights."

"Provider's sole obligation for IP infringement shall be to modify
or replace the infringing component."
```

**Why It's Dangerous**:
- Customer bears IP risk for vendor's product
- No defense or indemnification
- Could face injunction and damages

**Recommended Response**:
- Full IP indemnification from vendor
- Defense AND indemnification (not just payment)
- Remedy options: modify, replace, refund
- No cap on IP indemnification

---

## 5. Compliance and Data Risk Patterns

### 5.1 Inadequate Data Protection

**Pattern**: Weak or missing data protection obligations.

**Dangerous Language**:
```
"Provider shall implement reasonable security measures."

"Customer is solely responsible for compliance with data protection laws."

[No data processing agreement / DPA]
```

**Why It's Dangerous**:
- GDPR / privacy law violations
- Inadequate security
- Regulatory liability

**Recommended Response**:
- Require specific security measures (SOC 2, ISO 27001)
- Include comprehensive DPA for GDPR compliance
- Breach notification within 24-72 hours
- Sub-processor restrictions

---

### 5.2 Weak Breach Notification

**Pattern**: Delayed or limited breach notification.

**Dangerous Language**:
```
"Provider shall notify Customer of any confirmed security breach
within 30 days of discovery."

"Notification shall be to Provider's general contact, not to specific
security contacts."
```

**Why It's Dangerous**:
- Delayed response to incidents
- Regulatory notification deadlines missed
- Inadequate incident response

**Recommended Response**:
- Notification within 24-48 hours (suspected breach)
- Notification within 24 hours (confirmed breach)
- Named security contacts
- Cooperation on investigation

---

### 5.3 Data Retention After Termination

**Pattern**: Vendor retains customer data after contract ends.

**Dangerous Language**:
```
"Provider shall retain Customer Data for 90 days following termination."

"Provider may retain aggregated or anonymized data indefinitely."

"Customer acknowledges that backup copies may exist and cannot be deleted."
```

**Why It's Dangerous**:
- Ongoing data exposure
- Compliance issues (right to deletion)
- Competitive concerns

**Recommended Response**:
- Customer data export before termination
- Deletion within 30 days of termination
- Certification of destruction
- Define "anonymized" strictly

---

## 6. Pattern Detection Checklist

### Critical Patterns (Always Flag)
- [ ] No liability cap or unlimited liability
- [ ] One-sided indemnification
- [ ] Unilateral amendment rights
- [ ] Broad IP assignment beyond deliverables
- [ ] Residual knowledge clause
- [ ] No data protection provisions

### High Priority Patterns (Usually Flag)
- [ ] Auto-renewal with >60 day notice
- [ ] No termination for convenience
- [ ] Termination penalties > 50% remaining fees
- [ ] No consequential damages exclusion
- [ ] Unfavorable governing law
- [ ] Excessive audit rights
- [ ] Weak breach notification

### Medium Priority Patterns (Evaluate Context)
- [ ] Price increase without cap
- [ ] Broad SLA exclusions
- [ ] Jury waiver / class action waiver
- [ ] Non-solicitation of employees
- [ ] Limitation on benchmarking
- [ ] Assignment restrictions (excluding affiliates)

---

## 7. Language Fixes for Common Patterns

### Liability Cap Addition
```
Before: [No liability cap]

After: "EXCEPT FOR [PARTY]'S INDEMNIFICATION OBLIGATIONS, GROSS
NEGLIGENCE, OR WILLFUL MISCONDUCT, IN NO EVENT SHALL EITHER PARTY'S
AGGREGATE LIABILITY UNDER THIS AGREEMENT EXCEED THE GREATER OF (A)
THE FEES PAID OR PAYABLE BY CUSTOMER DURING THE TWELVE (12) MONTHS
IMMEDIATELY PRECEDING THE EVENT GIVING RISE TO THE CLAIM, OR (B)
$[AMOUNT]."
```

### Mutual Indemnification
```
Before: [One-sided customer indemnification]

After: "Each party shall indemnify, defend, and hold harmless the
other party from and against any third-party claims arising from:
(a) the indemnifying party's breach of this Agreement; (b) the
indemnifying party's gross negligence or willful misconduct; and
(c) the indemnifying party's violation of applicable law. Additionally,
Provider shall indemnify Customer against claims that the Services
infringe any third-party intellectual property rights."
```

### Reasonable Amendment Clause
```
Before: "Provider may modify terms by posting to website."

After: "No amendment to this Agreement shall be effective unless
set forth in writing and signed by both parties. Notwithstanding
the foregoing, Provider may update its security practices and
technical documentation without Customer consent, provided such
updates do not materially diminish the Services."
```

### Termination for Convenience
```
Before: [No termination for convenience]

After: "Either party may terminate this Agreement for convenience
upon ninety (90) days' prior written notice to the other party.
Upon such termination, Customer shall pay for all Services rendered
through the effective date of termination, and any prepaid fees for
periods following termination shall be refunded on a pro-rata basis."
```
