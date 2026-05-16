# Patent Claim Analysis Guide

This reference provides guidance for interpreting patent claims and conducting claim mapping analysis.

## Understanding Patent Claims

### Claim Structure

Patent claims follow a specific structure:

```
[Preamble] comprising/including:
  [Element A];
  [Element B];
  [Element C]; and
  wherein [Limitation/Relationship].
```

**Example**:
```
A portable medical imaging device (preamble) comprising:
  a handheld ultrasound transducer (Element A);
  a processor configured to perform real-time image processing (Element B);
  a wireless communication module (Element C); and
  wherein the processor executes a CNN-based segmentation algorithm (Limitation).
```

### Claim Types

| Type | Description | Scope |
|------|-------------|-------|
| **Independent** | Stands alone; defines complete invention | Broadest |
| **Dependent** | References another claim; adds limitations | Narrower |
| **Method/Process** | Steps to perform an action | Action-focused |
| **Apparatus/Device** | Physical structure or system | Structure-focused |
| **System** | Combination of components | Integration-focused |
| **Composition** | Material or substance | Material-focused |

### Claim Language Interpretation

**Key Transitional Phrases**:

| Phrase | Meaning |
|--------|---------|
| `comprising` | Open-ended (additional elements allowed) |
| `consisting of` | Closed (only listed elements) |
| `consisting essentially of` | Semi-closed (only related elements) |

**Functional Language**:
- `configured to` - Must be capable of performing function
- `adapted to` - Designed/suited for function
- `for [function]` - Intended use (may not limit scope)

**Relational Terms**:
- `coupled to` - Connected (direct or indirect)
- `connected to` - Direct physical connection
- `in communication with` - Data/signal connection

## Claim Mapping Process

### Step 1: Parse Claim Elements

Break claim into discrete elements:

```markdown
## Claim 1 Analysis

**Original Claim**:
"A portable medical imaging device comprising:
a handheld ultrasound transducer;
a processor configured to perform real-time image processing using a CNN; and
a battery power source."

**Parsed Elements**:
1. Portable medical imaging device (preamble - apparatus)
2. Handheld ultrasound transducer
3. Processor configured to perform real-time image processing
4. Real-time processing uses CNN
5. Battery power source
```

### Step 2: Map Elements to Product/Prior Art

For each element, determine presence in product or prior art:

| Element | Present? | Evidence | Notes |
|---------|----------|----------|-------|
| Handheld transducer | YES | Product spec p.3 | 450g handheld unit |
| Processor for real-time | YES | NVIDIA Jetson specs | <100ms latency |
| CNN-based processing | YES | Software architecture doc | ResNet-50 backbone |
| Battery power | YES | Product spec p.4 | 4-hour LiPo battery |

### Step 3: Assess Match Quality

**Match Categories**:

| Category | Definition | Implication |
|----------|------------|-------------|
| **Literal Match** | Element exactly as claimed | Direct reading |
| **Equivalent** | Different form, same function | Doctrine of equivalents |
| **Absent** | Element not present | Non-infringement |
| **Uncertain** | Claim interpretation unclear | Further analysis needed |

### Step 4: Document Differences

For prior art analysis (patentability):
```markdown
**Claim Element**: Processor configured to perform real-time image processing

**Prior Art (US10,123,456)**:
- Discloses: "Processor for image processing"
- Does NOT teach: "Real-time" requirement (claims 50ms latency threshold)
- Difference: Prior art processes in batch mode (offline), not real-time

**Conclusion**: Element NOT disclosed in prior art
```

For FTO analysis (infringement):
```markdown
**Claim Element**: Battery power source

**Our Product**:
- Has: LiPo battery (4-hour runtime)
- Match: YES (literal)

**Potential Design-Around**:
- Use AC power only (plug-in device)
- But: Eliminates portability advantage (not practical)
```

## Claim Construction Principles

### Broadest Reasonable Interpretation (BRI)

During patent examination (USPTO), claims are given BRI:
- Terms interpreted as broadly as reasonable
- Based on specification and ordinary skill in art
- Favors finding prior art (higher bar for applicant)

### Phillips Standard (Litigation)

In litigation (courts, PTAB), claims construed per:
1. Claim language itself
2. Specification (patent document)
3. Prosecution history (file wrapper)
4. Extrinsic evidence (dictionaries, expert testimony)

### Common Claim Construction Issues

| Issue | Example | Resolution |
|-------|---------|------------|
| Indefiniteness | "Substantially real-time" | Check specification for definition |
| Means-plus-function | "Means for processing" | Limited to disclosed structure + equivalents |
| Antecedent basis | "The processor" (not previously introduced) | Check claim chain for introduction |

## Infringement Analysis Framework

### Literal Infringement

All claim elements must be present in accused product:

```
Element 1: Present? [YES/NO]
Element 2: Present? [YES/NO]
Element 3: Present? [YES/NO]
...
All YES → Literal Infringement
Any NO → No Literal Infringement (check DOE)
```

### Doctrine of Equivalents (DOE)

If not literal infringement, check if accused product has equivalent elements:

**Function-Way-Result Test**:
- Does equivalent perform **same function**?
- In **substantially same way**?
- To achieve **substantially same result**?

**Insubstantial Differences Test**:
- Is the difference between claim element and accused element insubstantial?

### Prosecution History Estoppel

Patentee may have surrendered claim scope during prosecution:
- Check file wrapper (USPTO PAIR)
- Look for claim amendments narrowing scope
- Arguments distinguishing prior art

If patentee disclaimed certain embodiments, cannot recapture via DOE.

## FTO vs. Invalidity Analysis

### FTO (Can we practice this technology?)

**Focus**: Our product vs. Their claims
**Question**: Do we infringe?
**Outcome**: Risk assessment + mitigation options

### Invalidity (Is their patent valid?)

**Focus**: Prior art vs. Their claims
**Question**: Does prior art anticipate or render obvious?
**Outcome**: Potential to invalidate patent

### Combined Strategy

```
If FTO analysis shows HIGH risk:
├── Option 1: Design-around (modify product)
├── Option 2: License (negotiate with patentee)
├── Option 3: Invalidity search (find prior art to invalidate)
└── Option 4: Accept risk (proceed with litigation budget)
```

## Claim Mapping Template

```markdown
## Claim Mapping: [Patent Number]

### Patent Information
- **Patent**: US10,XXX,XXX
- **Title**: [Title]
- **Assignee**: [Company]
- **Status**: Active (expires [date])

### Claim 1 (Independent)

**Claim Text**:
"[Full claim text]"

**Element-by-Element Analysis**:

| # | Claim Element | Present in [Product/Prior Art] | Evidence | Match Type |
|---|---------------|--------------------------------|----------|------------|
| 1 | [Element 1] | [YES/NO/UNCERTAIN] | [Reference] | [LITERAL/EQUIVALENT/ABSENT] |
| 2 | [Element 2] | [YES/NO/UNCERTAIN] | [Reference] | [LITERAL/EQUIVALENT/ABSENT] |
| 3 | [Element 3] | [YES/NO/UNCERTAIN] | [Reference] | [LITERAL/EQUIVALENT/ABSENT] |

**Conclusion**:
- [ ] All elements present → [INFRINGEMENT / ANTICIPATED]
- [ ] Missing elements → [NON-INFRINGEMENT / NOVEL]
- [ ] Uncertain elements → [FURTHER ANALYSIS NEEDED]

### Dependent Claims

**Claim 2** (depends on Claim 1, adds: "[additional limitation]")
- Additional element present? [YES/NO]
- If Claim 1 not infringed → Claim 2 not infringed
- If Claim 1 infringed → Check additional limitation

### Risk Assessment

**Overall Risk Level**: [HIGH/MEDIUM/LOW]

**Rationale**: [Explanation]

**Recommended Action**: [License/Design-Around/Proceed/Invalidate]
```
