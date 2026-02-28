# Specification Writing Standards

## 1. Applicable Standards

### IEEE 830 — Recommended Practice for Software Requirements Specifications

IEEE 830 defines the structure and quality attributes for Software Requirements Specifications (SRS). Although superseded by ISO/IEC/IEEE 29148, its quality criteria remain the industry gold standard.

**Key Quality Attributes (IEEE 830 Section 4.3):**

| Attribute | Definition | Verification Method |
|-----------|-----------|-------------------|
| Correct | Each requirement accurately represents a real need | Stakeholder review |
| Unambiguous | Each requirement has exactly one interpretation | Peer review, no vague terms |
| Complete | All requirements and references are present | Traceability matrix check |
| Consistent | No requirement contradicts another | Cross-reference validation |
| Ranked for importance | Priority assigned to each requirement | MoSCoW or numeric priority |
| Verifiable | Each requirement can be objectively tested | Test case derivability |
| Modifiable | Structure allows changes without cascading effects | Modular organization with IDs |
| Traceable | Origin and downstream artifacts are linked | Bidirectional traceability matrix |

### ISO/IEC/IEEE 29148:2018 — Systems and Software Engineering — Life Cycle Processes — Requirements Engineering

This standard extends IEEE 830 and provides a complete framework for requirements engineering across the lifecycle. Key contributions:

- Defines requirements at system, software, and interface levels
- Specifies the relationship between ConOps, StRS, SyRS, SRS, and IRS documents
- Mandates traceability between requirement levels

**Document Hierarchy (ISO 29148):**

```
ConOps (Concept of Operations)
  └── StRS (Stakeholder Requirements Specification)
       └── SyRS (System Requirements Specification)
            ├── SRS (Software Requirements Specification)  ← This skill's primary output
            └── IRS (Interface Requirements Specification)
```

## 2. ID Numbering Conventions

### Standard Prefixes

| Prefix | Entity | Format | Example |
|--------|--------|--------|---------|
| REQ | Requirement | REQ-NNN | REQ-001 |
| SCR | Screen / Page | SCR-NNN | SCR-001 |
| API | API Endpoint | API-NNN | API-001 |
| TBL | Database Table | TBL-NNN | TBL-001 |
| SEQ | Sequence Diagram | SEQ-NNN | SEQ-001 |
| STS | State / State Machine | STS-NNN | STS-001 |
| ERR | Error Code | ERR-NNN | ERR-001 |
| IDX | Index | IDX-NNN | IDX-001 |

### Sub-element IDs

Sub-elements are namespaced under their parent:

| Sub-element | Format | Example | Description |
|------------|--------|---------|-------------|
| UI Element | SCR-NNN-ENNN | SCR-001-E01 | Element 01 on screen 001 |
| Screen Event | SCR-NNN-EVNNN | SCR-001-EV01 | Event 01 on screen 001 |
| API Parameter | API-NNN-PNNN | API-001-P01 | Parameter 01 of endpoint 001 |
| Table Column | TBL-NNN-CNNN | TBL-001-C01 | Column 01 of table 001 |
| Table Index | TBL-NNN-IXNNN | TBL-001-IX01 | Index 01 of table 001 |

### ID Assignment Rules

1. **Sequential numbering** — Assign IDs in order of creation; do not reuse deleted IDs
2. **Zero-padded** — Use three digits minimum (001, 002, ..., 999)
3. **Immutable** — Once assigned, an ID must not change; mark deprecated IDs as `[DEPRECATED]`
4. **Cross-document consistent** — The same entity must have the same ID across all documents

## 3. Traceability Matrix

### Purpose

A traceability matrix links requirements to their downstream implementation artifacts, ensuring:

- Every requirement is addressed (forward traceability)
- Every artifact traces back to a requirement (backward traceability)
- Impact analysis when requirements change

### Standard Format

| REQ ID | Description | SCR IDs | API IDs | TBL IDs | Test Case IDs | Status |
|--------|-----------|---------|---------|---------|--------------|--------|
| REQ-001 | User registration | SCR-001, SCR-002 | API-001, API-002 | TBL-001 | TC-001, TC-002 | Draft |
| REQ-002 | User login | SCR-003 | API-003 | TBL-001 | TC-003 | Draft |

### Traceability Rules

1. Every REQ must map to at least one SCR, API, or TBL
2. Every SCR, API, and TBL must trace back to at least one REQ
3. Orphaned artifacts (no REQ mapping) must be justified or removed
4. Matrix must be updated whenever any artifact changes

## 4. Version Control for Specifications

### Document Version Format

Use semantic versioning for specification documents:

```
Major.Minor (e.g., 1.0, 1.1, 2.0)
```

- **Major** — Structural changes, scope changes, or breaking changes
- **Minor** — Additions, corrections, or non-breaking modifications

### Change History Table

| Version | Date | Author | Section Changed | Description |
|---------|------|--------|----------------|-------------|
| 0.1 | YYYY-MM-DD | Author Name | All | Initial draft |
| 0.2 | YYYY-MM-DD | Author Name | Section 4 | Added API endpoints API-005 through API-008 |
| 1.0 | YYYY-MM-DD | Approver Name | All | Approved for development |

### Review and Approval States

```
Draft → Under Review → Approved → Superseded/Archived
```

- **Draft** — Work in progress, not yet reviewed
- **Under Review** — Submitted for stakeholder review
- **Approved** — Accepted; baseline for development
- **Superseded** — Replaced by a newer version (keep for audit trail)

## 5. Terminology Glossary Management

### Glossary Structure

Every specification must include a terminology glossary to eliminate ambiguity.

| Term | Definition | Context | Source |
|------|-----------|---------|--------|
| User | An individual with an active account in the system | Authentication domain | REQ-001 |
| Active | A user whose account status is 'enabled' and last login within 90 days | User management | Business rule BR-012 |

### Glossary Rules

1. **Define before use** — Every domain-specific term must appear in the glossary before first use
2. **Single definition** — Each term has exactly one definition within the document scope
3. **No synonyms** — Use one consistent term throughout; list synonyms in glossary as "see [preferred term]"
4. **Avoid jargon** — If jargon is necessary, define it explicitly
5. **Cross-reference** — Link glossary terms to the requirements or sections that define them

## 6. Document Sections and Ordering

### Full Functional Specification — Standard Section Order

1. **Document Information** — ID, version, dates, authors, approvers, change history
2. **Introduction** — Purpose, scope, definitions, references, overview
3. **System Overview** — Architecture diagram, technology stack, deployment topology
4. **Screen Design** — Screen list, individual screen specs, screen transitions
5. **API Design** — Endpoint list, individual endpoint specs, sequence diagrams
6. **Database Design** — Table list, individual table specs, ER diagram, indexes
7. **Sequence Diagrams** — Major workflow sequences
8. **State Transition Diagrams** — Entity lifecycle state machines
9. **Non-Functional Requirements** — Performance, security, availability, scalability
10. **Appendix** — Traceability matrix, open issues, assumptions, constraints

### Section-Level Quality Requirements

| Section | Must Include | Must Not Include |
|---------|------------|-----------------|
| Introduction | Purpose, scope, definitions | Implementation details |
| System Overview | Architecture diagram | Detailed code |
| Screen Design | UI element table, event table | Backend logic details |
| API Design | Request/response schemas | Database queries |
| Database Design | Column definitions, ER diagram | Application logic |

## 7. Quality Criteria for Specifications

### Language Quality Rules

**Prohibited vague phrases:**

| Prohibited | Replacement |
|-----------|-------------|
| "appropriate" | Specify the exact criteria |
| "etc." | List all items explicitly |
| "as needed" | Define the specific condition |
| "should" (ambiguous) | Use "shall" (mandatory) or "may" (optional) |
| "user-friendly" | Specify measurable usability criteria |
| "fast" / "quickly" | Specify response time in milliseconds |
| "large" / "small" | Specify exact quantity or range |
| "similar to" | Specify exact behavior |

**Required precision terms:**

| Term | Meaning | Usage |
|------|---------|-------|
| SHALL | Mandatory requirement | "The system SHALL validate email format" |
| SHOULD | Recommended but not mandatory | "The UI SHOULD display a loading indicator" |
| MAY | Optional capability | "The API MAY support bulk operations" |
| MUST NOT | Prohibited behavior | "The system MUST NOT store plaintext passwords" |

### Completeness Checklist

Before finalizing any specification document, verify:

- [ ] Every REQ has at least one downstream artifact (SCR/API/TBL)
- [ ] Every artifact has a unique ID following the numbering convention
- [ ] Every screen has a UI element table and event table
- [ ] Every API endpoint has request/response examples
- [ ] Every database table has column definitions and audit columns
- [ ] All Mermaid diagrams render without syntax errors
- [ ] The traceability matrix is complete and bidirectional
- [ ] The glossary defines all domain-specific terms
- [ ] No prohibited vague phrases remain in the document
- [ ] Version history is updated with the current revision

### Review Checklist

| # | Check Item | Pass/Fail |
|---|-----------|-----------|
| 1 | All IDs follow the standard naming convention | |
| 2 | Traceability matrix is complete (forward and backward) | |
| 3 | No orphaned artifacts (every SCR/API/TBL maps to a REQ) | |
| 4 | All Mermaid diagrams are syntactically valid | |
| 5 | Error codes are standardized and consistent | |
| 6 | Audit columns present in every table definition | |
| 7 | JSON examples are valid and realistic | |
| 8 | Screen events reference valid API endpoints or screen targets | |
| 9 | No prohibited vague language found | |
| 10 | Glossary is complete and consistent | |

## 8. Cross-Reference Validation Rules

### Validation Checks

1. **SCR → API**: Every screen event with an API action must reference a defined API-xxx endpoint
2. **SCR → SCR**: Every screen transition target must reference a defined SCR-xxx screen
3. **API → TBL**: Every API endpoint that performs CRUD must reference the affected TBL-xxx tables
4. **TBL → TBL**: Every foreign key must reference a defined TBL-xxx table
5. **REQ → ***: Every requirement must map to at least one implementation artifact
6. **ERR consistency**: Error codes used in API specs must match the error code registry

### Broken Reference Resolution

When a broken reference is detected:

1. If the target artifact exists but has a different ID → Fix the reference
2. If the target artifact does not exist → Create it or remove the reference
3. If the reference is intentionally to a future artifact → Mark as `[PLANNED]` with expected delivery date
