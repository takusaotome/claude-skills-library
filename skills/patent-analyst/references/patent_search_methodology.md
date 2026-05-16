# Patent Search Methodology Guide

This reference provides a structured methodology for conducting comprehensive patent searches.

## Search Process Overview

```
1. Define Scope → 2. Develop Strategy → 3. Execute Search → 4. Analyze Results → 5. Report
```

## 1. Scope Definition

### Information to Gather

| Category | Questions to Answer |
|----------|---------------------|
| Technical Field | What technology domain? What sub-fields? |
| Problem Solved | What problem does the invention address? |
| Key Features | What are the novel/inventive elements? |
| Prior Knowledge | Any known patents, publications, products? |
| Geographic Scope | Which markets/jurisdictions are relevant? |

### Concept Decomposition

Break the invention into searchable concepts:

1. **Core Concept**: Main technical idea
2. **Technical Elements**: Key components, materials, structures
3. **Application Domain**: Use cases, industries
4. **Functional Aspects**: What it does, how it performs

## 2. Search Strategy Development

### Keyword Expansion

For each concept, identify:
- **Synonyms**: Alternative terms with same meaning
- **Broader Terms**: More general concepts
- **Narrower Terms**: More specific concepts
- **Related Terms**: Associated concepts

**Example**:
```
Core Concept: "Image Segmentation"
├── Synonyms: pixel classification, image partition
├── Broader: image processing, computer vision
├── Narrower: semantic segmentation, instance segmentation
└── Related: object detection, edge detection
```

### Classification Codes

**CPC (Cooperative Patent Classification)** - Primary system for USPTO/EPO:

| Section | Description |
|---------|-------------|
| A | Human Necessities |
| B | Performing Operations; Transporting |
| C | Chemistry; Metallurgy |
| D | Textiles; Paper |
| E | Fixed Constructions |
| F | Mechanical Engineering |
| G | Physics (includes computing, imaging) |
| H | Electricity |

**Finding Relevant Codes**:
1. Search a few relevant patents → Check their CPC codes
2. Use USPTO/EPO classification search tools
3. Browse CPC hierarchy for related codes

### Boolean Query Construction

**Operators**:
- `AND`: Both terms required
- `OR`: Either term acceptable
- `NOT`: Exclude term
- `NEAR/n`: Terms within n words
- `*`: Wildcard (any characters)
- `?`: Single character wildcard
- `""`: Exact phrase

**Query Template**:
```
(concept1_term1 OR concept1_term2)
AND (concept2_term1 OR concept2_term2)
AND CPC/(classification_code)
NOT (exclusion_terms)
```

## 3. Search Execution

### Recommended Search Order

1. **Google Patents** - Broadest coverage, most accessible
2. **Espacenet** - Strong for EP patents, legal status
3. **USPTO PatFT** - Detailed US patent search
4. **J-PlatPat** - Japanese patents (English abstracts available)
5. **PatentScope** - PCT/WIPO applications
6. **Google Scholar** - Non-patent literature (NPL)

### Search Workflow

```
Phase 1: Broad Search (Cast wide net)
├── Use core keywords + classifications
├── Review 50-100 titles/abstracts
├── Identify 10-15 key patents
└── Note additional keywords discovered

Phase 2: Focused Search (Refine)
├── Analyze key patents in detail
├── Extract: new keywords, inventors, assignees
├── Citation search (forward + backward)
└── Identify 20-30 relevant references

Phase 3: Deep Dive (Critical review)
├── Full-text review of top 10-20 references
├── Compare claims to invention
└── Document differences (points of novelty)

Phase 4: NPL Search (Non-patent literature)
├── Academic publications (Google Scholar)
├── Conference papers (IEEE, ACM)
├── Product documentation, manuals
└── Standards, specifications
```

### Citation Analysis

**Forward Citations** (Who cites this patent?):
- Identifies follow-on innovations
- Shows technology evolution
- May reveal relevant newer art

**Backward Citations** (What does this patent cite?):
- Foundational prior art
- Key technical references
- Related technology areas

## 4. Results Analysis

### Relevance Assessment

| Level | Criteria |
|-------|----------|
| **HIGH** | Discloses multiple key features; same technical approach |
| **MEDIUM** | Discloses some features; different approach or application |
| **LOW** | Related field; different problem or solution |
| **NOT RELEVANT** | Unrelated despite keyword match |

### Feature Comparison Matrix

| Feature | Invention | Ref 1 | Ref 2 | Ref 3 |
|---------|-----------|-------|-------|-------|
| Feature A | Yes | Yes | No | Yes |
| Feature B | Yes | No | Yes | No |
| Feature C | Yes | No | No | No |
| **Relevance** | - | MEDIUM | MEDIUM | LOW |

### Gap Analysis

Identify what's NOT in prior art:
- Which features are not disclosed?
- Which combinations are not taught?
- What problems are not addressed?

These gaps indicate potential novelty.

## 5. Documentation and Reporting

### Search Log

Maintain detailed search log:

```markdown
## Search Log

### Search 1
- **Date/Time**: 2025-01-15 14:30
- **Database**: Google Patents
- **Query**: (neural network OR CNN) AND (image segmentation)
- **Filters**: Type=Patent, Status=Active
- **Results**: 1,250 patents
- **Reviewed**: Top 50 by relevance
- **Key Findings**: 5 high-relevance patents identified
```

### Reference Summary

For each key reference:

```markdown
## Reference: US10,123,456

### Basic Information
- **Title**: Deep Learning for Medical Image Segmentation
- **Assignee**: MedTech Corp
- **Priority Date**: 2018-03-15
- **Status**: Active (granted 2020-08-01)

### Technical Disclosure
[Summary of what the patent teaches]

### Key Claims
- Claim 1: [Summary of independent claim]

### Relevance to Invention
- **Level**: HIGH
- **Features Disclosed**: [List]
- **Features NOT Disclosed**: [List]
- **Differences**: [Key distinctions]
```

## Quality Checklist

Before finalizing search:

- [ ] Multiple databases searched (not just one)
- [ ] Both patent and non-patent literature checked
- [ ] Classification codes used (not just keywords)
- [ ] Citation analysis performed
- [ ] Search log documented
- [ ] All key references analyzed for claim coverage
- [ ] Feature comparison matrix completed
- [ ] Geographic scope addressed
