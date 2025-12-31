# Clause Analysis Guide

This guide provides detailed analysis criteria for each clause type across different contract categories.

## 1. Universal Clauses (All Contract Types)

### 1.1 Definitions (定義条項)

**Purpose**: Establish clear meaning for key terms used throughout the agreement.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Are all capitalized terms defined? | Medium | Undefined terms create ambiguity |
| Are definitions circular or self-referencing? | Medium | Can lead to interpretation disputes |
| Is "Affiliate" defined appropriately? | High | Overly broad can extend obligations |
| Is "Confidential Information" scoped correctly? | High | See NDA-specific section |
| Are date/time references clear? | Low | "Business Day" should be defined |

**Red Flags**:
- Definitions that expand scope unilaterally
- "Including but not limited to" without bounds
- Vague terms like "reasonable" without objective criteria

---

### 1.2 Term and Renewal (契約期間・更新)

**Purpose**: Define contract duration and renewal mechanisms.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Initial term clearly stated? | Low | |
| Auto-renewal clause present? | High | Check notice period |
| Notice period for non-renewal? | High | >60 days is concerning |
| Renewal pricing terms? | High | Watch for price escalation clauses |
| Early termination rights? | Medium | Should be mutual |

**Standard Market Terms**:
- Notice period: 30-60 days before renewal
- Auto-renewal periods: 1 year (standard), monthly (SaaS)
- Price increase cap: CPI or 3-5% annual

**Red Flags**:
- Auto-renewal with >90 day notice requirement
- Price increases at "sole discretion"
- Evergreen clauses without opt-out
- Minimum term commitments exceeding 3 years

---

### 1.3 Termination (解除・終了)

**Purpose**: Define conditions and consequences of contract termination.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Termination for convenience? | High | Should be mutual |
| Termination for cause/breach? | High | Cure period should exist |
| Cure period length? | Medium | 30 days standard |
| Termination for insolvency? | Medium | Check jurisdiction rules |
| Post-termination obligations? | High | Data return, transition assistance |
| Termination fees/penalties? | High | Should be reasonable |

**Standard Market Terms**:
- Termination for convenience: 30-90 days written notice
- Cure period for breach: 30 days (general), 10 days (payment)
- Transition assistance: 30-90 days at cost

**Red Flags**:
- One-sided termination rights (only vendor can terminate)
- No cure period for breach
- Excessive termination penalties (>remaining contract value)
- Loss of data access upon termination
- Forfeiture of prepaid fees

---

### 1.4 Limitation of Liability (責任制限)

**Purpose**: Cap potential damages and exclude certain damage types.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Is there a liability cap? | Critical | Absence = unlimited exposure |
| Cap amount relative to contract value? | High | 1-2x annual fees typical |
| Consequential damages excluded? | High | Standard market practice |
| Carve-outs for indemnification? | High | May negate the cap |
| Carve-outs for gross negligence/willful misconduct? | Medium | Standard and acceptable |
| IP infringement in carve-outs? | High | Can create significant exposure |

**Standard Market Terms**:
- Cap: 12-24 months of fees paid/payable
- Excluded: Indirect, consequential, special, punitive damages
- Carve-outs: Gross negligence, willful misconduct, confidentiality breach

**Red Flags**:
- No liability cap (unlimited liability)
- Cap applies only to one party
- Broad carve-outs that effectively negate the cap
- "Super cap" inadequate for risk level
- Exclusions for critical loss types (data loss, business interruption)

---

### 1.5 Indemnification (補償)

**Purpose**: Allocate responsibility for third-party claims.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Is indemnification mutual? | High | Should cover both parties |
| Scope of indemnified claims? | High | IP, personal injury, breach typical |
| Cap on indemnification? | Critical | Should be capped |
| Exclusive remedy specified? | Medium | Limits exposure |
| Procedure requirements? | Medium | Notice, cooperation, control |

**Standard Market Terms**:
- Mutual indemnification for respective breaches
- Vendor indemnifies for IP infringement
- Customer indemnifies for misuse, data provided
- Cap: Equal to or greater than general liability cap

**Red Flags**:
- One-sided indemnification (you indemnify, they don't)
- No cap on indemnification obligations
- "Indemnify and hold harmless" without limits
- Broad indemnification for "any and all claims"
- No control over defense/settlement

---

### 1.6 Confidentiality (秘密保持)

**Purpose**: Protect proprietary information disclosed during the relationship.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Definition of Confidential Information? | High | See NDA section for details |
| Exclusions clearly stated? | Medium | Publicly known, independently developed |
| Permitted disclosures? | Medium | Employees, contractors, legal requirement |
| Security obligations? | High | "Reasonable" should be defined |
| Duration of obligation? | High | 2-5 years typical, trade secrets perpetual |
| Return/destruction requirements? | Medium | Should be clear and feasible |

**Standard Market Terms**:
- Duration: 3-5 years (general info), perpetual (trade secrets)
- Standard exclusions: Public domain, prior knowledge, independent development, third-party disclosure
- Permitted: Need-to-know employees, contractors under similar obligations

**Red Flags**:
- Perpetual confidentiality for all information (not just trade secrets)
- One-sided protection (only your info protected, not theirs)
- Inadequate exclusions
- Requirement to return information that's embedded in systems

---

### 1.7 Intellectual Property Rights (知的財産権)

**Purpose**: Define ownership and rights to intellectual property.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Pre-existing IP protected? | Critical | Should remain with original owner |
| Work product ownership? | Critical | Customer should own custom deliverables |
| License grants scope? | High | Should be limited to purpose |
| Improvements/enhancements? | High | Who owns improvements to base IP? |
| Moral rights waiver? | Medium | May be required in some jurisdictions |
| Feedback/suggestions rights? | Medium | Watch for broad grants |

**Standard Market Terms**:
- Customer owns: Custom deliverables, customer data, customer-provided materials
- Vendor owns: Pre-existing IP, tools, methodologies, generic know-how
- License: Non-exclusive license to use vendor IP in deliverables

**Red Flags**:
- Vendor owns all work product (including custom development)
- Broad assignment of customer IP beyond project scope
- Unlimited license to customer feedback/suggestions
- No license-back for pre-existing customer IP used in deliverables
- IP assignment buried in general terms

---

### 1.8 Governing Law and Dispute Resolution (準拠法・紛争解決)

**Purpose**: Establish legal framework for interpreting and enforcing the contract.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Governing law specified? | High | Should be familiar jurisdiction |
| Venue/jurisdiction? | High | Should be accessible |
| Arbitration or litigation? | Medium | Consider cost and enforceability |
| Arbitration rules and seat? | High | AAA, JAMS, ICC typical |
| Jury waiver? | Medium | Common in US contracts |
| Class action waiver? | Medium | May not be enforceable |

**Jurisdiction Considerations**:
| Location | Considerations |
|----------|---------------|
| Delaware, NY (US) | Sophisticated commercial law |
| California (US) | Employee-friendly, consumer protection |
| England | Neutral for international deals |
| Singapore, Hong Kong | Good for APAC deals |
| Japan | Required for Japanese entities in some cases |

**Red Flags**:
- Governing law in unfamiliar or unfavorable jurisdiction
- Mandatory arbitration in distant location
- Waiver of right to jury trial without consideration
- Broad waiver of legal remedies

---

### 1.9 Force Majeure (不可抗力)

**Purpose**: Excuse non-performance due to events beyond control.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Events defined? | Medium | Should include relevant scenarios |
| Pandemic/epidemic included? | High | Post-COVID consideration |
| Notification requirements? | Medium | Should be reasonable |
| Mitigation obligations? | Medium | Should require reasonable efforts |
| Termination right after extended FM? | High | Should be mutual |

**Standard Market Terms**:
- Events: Acts of God, war, terrorism, government action, natural disasters
- Notification: Prompt written notice with details
- Duration cap: 60-180 days before termination right

**Red Flags**:
- Only one party gets FM protection
- Economic hardship or market changes included (not true FM)
- No termination right after extended FM period
- FM excuses payment obligations

---

### 1.10 Assignment and Subcontracting (譲渡・再委託)

**Purpose**: Control transfer of rights and obligations.

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Assignment requires consent? | Medium | Should for both parties |
| Exception for affiliates? | Medium | Common and acceptable |
| Exception for M&A? | High | May transfer to competitor |
| Subcontracting permitted? | Medium | Should require notice/approval |
| Subcontractor liability? | High | Prime contractor should remain liable |

**Standard Market Terms**:
- Assignment requires prior written consent (not unreasonably withheld)
- Exception for affiliates and M&A (with notice)
- Subcontracting permitted with vendor responsibility

**Red Flags**:
- One-sided (they can assign, you cannot)
- Free assignment to affiliates including competitors
- No restriction on subcontracting
- Subcontractor not bound by confidentiality

---

## 2. NDA-Specific Clauses

### 2.1 Scope of Confidential Information

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Marking requirements? | High | Should not require marking for oral disclosures |
| Oral disclosure handling? | High | Should be confirmed in writing within reasonable time |
| Residual knowledge clause? | Critical | Can negate protection entirely |
| Standard exclusions present? | Medium | Public domain, prior knowledge, etc. |

**Recommended Definition**:
```
"Confidential Information" means any non-public information disclosed by one
party to the other, whether orally, in writing, or by inspection, including
but not limited to technical data, trade secrets, know-how, research, product
plans, services, customers, markets, software, developments, inventions,
processes, formulas, technology, designs, drawings, engineering, hardware
configuration, marketing, finances, or other business information.
```

**Red Flags**:
- "Residual knowledge" exception allowing free use of information retained in memory
- No exclusions (everything is confidential forever)
- Marking requirement for ALL disclosures (impossible for oral)
- Overly short confirmation period for oral disclosures (<5 days)

### 2.2 Purpose Limitation

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Purpose clearly defined? | High | Should be specific |
| Scope appropriate? | High | Not broader than necessary |
| Changes require amendment? | Medium | Should require written consent |

**Red Flags**:
- Vague purpose ("evaluating potential business relationship")
- Purpose allows competitive use
- Purpose can be changed unilaterally

### 2.3 Return and Destruction

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Trigger clearly defined? | Medium | Upon termination or request |
| Destruction certification? | Medium | Should be required |
| Exceptions for legal holds? | Medium | Necessary for compliance |
| Exception for embedded systems? | Medium | Reasonable with continued confidentiality |

---

## 3. MSA-Specific Clauses

### 3.1 Relationship of Parties

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Independent contractor status? | High | Should be clearly stated |
| No agency relationship? | Medium | Neither party agent for other |
| Employment relationship disclaimed? | High | Important for liability |

### 3.2 Order of Precedence

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Hierarchy clearly stated? | High | MSA vs. SOW vs. schedules |
| Conflict resolution specified? | High | Which document prevails? |
| Amendment requirements? | Medium | Should require written agreement |

**Standard Order**:
1. Amendments (newest first)
2. SOW/Order Form
3. Schedules/Exhibits
4. MSA

---

## 4. SOW/Service Agreement-Specific Clauses

### 4.1 Scope of Work

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Deliverables clearly defined? | Critical | Should be specific and measurable |
| Acceptance criteria stated? | Critical | Should be objective |
| Exclusions stated? | High | What is NOT included |
| Change order process? | High | Should require mutual agreement |

**Red Flags**:
- Vague deliverable descriptions ("consulting services")
- No acceptance criteria
- "Deemed acceptance" after short period
- Unilateral scope changes allowed

### 4.2 Acceptance and Rejection

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Acceptance testing period? | High | Should be adequate (15-30 days) |
| Rejection notice requirements? | Medium | Should specify deficiencies |
| Cure period for rejected deliverables? | High | Should allow correction |
| Partial acceptance allowed? | Medium | Should be possible |
| Deemed acceptance period? | High | Should be reasonable |

**Standard Market Terms**:
- Testing period: 15-30 business days
- Rejection notice: Written with specific deficiencies
- Cure attempts: 2-3 attempts before termination right
- Deemed acceptance: Only after testing period expires without response

### 4.3 Milestones and Payment

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Milestone definitions clear? | High | Should be measurable |
| Payment tied to acceptance? | High | Should be after acceptance |
| Holdback/retainage? | Medium | 10-20% until final acceptance |
| Late payment terms? | Medium | Interest should be reasonable |

---

## 5. SLA-Specific Clauses

### 5.1 Service Levels

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Metrics clearly defined? | Critical | Uptime, response time, etc. |
| Measurement methodology? | Critical | How is it measured? |
| Measurement period? | High | Monthly typical |
| Exclusions from calculation? | High | Planned maintenance, FM, customer-caused |
| Reporting requirements? | Medium | Should be regular and transparent |

**Common SLA Metrics**:
| Metric | Typical Target | Notes |
|--------|---------------|-------|
| Uptime/Availability | 99.9% - 99.99% | Measured monthly |
| Response Time | <500ms | 95th percentile |
| Support Response | 1-4 hours | Based on severity |
| Resolution Time | 4-24 hours | Based on severity |

### 5.2 Service Credits

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Credit calculation method? | High | Should be clear and meaningful |
| Credit cap? | Medium | Often 10-30% of monthly fees |
| Exclusive remedy provision? | Critical | May limit other remedies |
| Credit claim process? | Medium | Should be straightforward |

**Red Flags**:
- Credits that are sole and exclusive remedy (no termination right)
- Credit cap too low (<10% monthly)
- Complex claim process that discourages claims
- Credits applicable only to future services (not refunds)

### 5.3 Support and Maintenance

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Support hours? | Medium | 24/7 vs. business hours |
| Support channels? | Low | Phone, email, chat |
| Severity definitions? | High | Should be objective |
| Escalation process? | Medium | Should be clear |

---

## 6. License Agreement-Specific Clauses

### 6.1 Grant of License

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| License type? | High | Perpetual vs. subscription |
| Scope (users, sites, etc.)? | High | Should match needs |
| Exclusivity? | Medium | Typically non-exclusive |
| Sublicense rights? | Medium | For affiliates, contractors |
| Territory restrictions? | Medium | Should cover operations |

### 6.2 Use Restrictions

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Prohibited uses reasonable? | High | Should not unduly limit business |
| Reverse engineering restriction? | Medium | Standard, may conflict with law |
| Modification restrictions? | Medium | May limit integration |
| Competitive use restriction? | High | Watch for anti-competitive terms |

**Red Flags**:
- Restrictions that prevent normal business use
- Overly broad competitive use restrictions
- Restrictions on discussing product publicly
- Restrictions on benchmarking without consent

### 6.3 Audit Rights

**Key Review Points**:
| Check Item | Risk Level | Notes |
|------------|------------|-------|
| Audit frequency? | Medium | Once per year typical |
| Notice period? | Medium | 30 days reasonable |
| Audit scope? | High | Should be limited to license compliance |
| Cost of audit? | High | Vendor pays unless >5% variance |
| Remediation period? | Medium | Should be reasonable |

---

## 7. Analysis Workflow

### Step 1: Clause Identification
Scan the contract and check off which clauses are present:
- [ ] Definitions
- [ ] Term and Renewal
- [ ] Termination
- [ ] Limitation of Liability
- [ ] Indemnification
- [ ] Confidentiality
- [ ] IP Rights
- [ ] Governing Law
- [ ] Force Majeure
- [ ] Assignment
- [ ] [Contract-type specific clauses]

### Step 2: Clause Evaluation
For each clause present, complete:
1. Read clause completely
2. Identify key terms and conditions
3. Check against this guide's review points
4. Flag any red flags or concerns
5. Rate risk level (Critical/High/Medium/Low)
6. Document findings in standard format

### Step 3: Missing Clause Analysis
For any standard clauses NOT present:
1. Note the absence
2. Assess risk of missing protection
3. Recommend adding if necessary
4. Draft proposed language if critical

### Step 4: Cross-Reference Check
Verify consistency across clauses:
- Definitions match usage throughout
- Liability caps consistent with indemnification
- Termination consequences match other obligations
- Dates and notice periods consistent
