# Meeting Minutes Review Criteria

This document defines the detailed scoring criteria for each review dimension.

## 1. Completeness (25% weight)

### Required Sections

| Section | Points | Criteria |
|---------|--------|----------|
| Meeting Header | 5 | Date, time, location/platform, attendees |
| Agenda | 3 | List of topics discussed |
| Discussion Summary | 5 | Key points from each agenda item |
| Decisions | 5 | All decisions made with context |
| Action Items | 5 | All follow-up tasks assigned |
| Next Steps | 2 | Follow-up meeting or milestones |

### Scoring Rules

- **90-100**: All sections present with substantive content
- **80-89**: All sections present, minor gaps in content
- **70-79**: 1 required section missing or significantly weak
- **60-69**: 2 required sections missing or weak
- **< 60**: Multiple critical sections missing

### Common Issues

1. Missing attendee list or incomplete attendance
2. Vague discussion summaries that don't capture key points
3. No clear separation between discussion and decisions
4. Missing meeting date or time

## 2. Action Items (25% weight)

### Required Components

Each action item MUST have:

| Component | Points | Criteria |
|-----------|--------|----------|
| Description | 3 | Clear, specific task description |
| Owner | 3 | Single named individual responsible |
| Deadline | 3 | Specific date (not "ASAP" or "soon") |
| Context | 1 | Link to discussion that generated it |

### Action Item Format Standards

**Good Example:**
```
- [ ] @John Smith: Complete API documentation for v2.0 endpoints
      Due: 2025-01-20
      Context: Discussion item #3
```

**Poor Example:**
```
- John to finish docs soon
```

### Scoring Rules

- **90-100**: All action items have owner, deadline, and clear description
- **80-89**: Minor issues (e.g., 1-2 items missing deadlines)
- **70-79**: Significant issues (multiple items missing components)
- **60-69**: Most items incomplete
- **< 60**: Action items unusable for tracking

### Common Issues

1. Team/group assigned instead of individual owner
2. Relative deadlines ("next week") instead of dates
3. Vague descriptions ("follow up on issue")
4. Missing action items for discussed decisions

## 3. Decisions (20% weight)

### Required Components

| Component | Points | Criteria |
|-----------|--------|----------|
| Decision Statement | 4 | Clear, unambiguous decision text |
| Context | 3 | Why decision was needed |
| Alternatives | 2 | Options considered (if applicable) |
| Rationale | 3 | Why this option was chosen |
| Impact | 2 | Who/what is affected |

### Decision Format Standards

**Good Example:**
```
### Decision: Use PostgreSQL for Production Database

**Context**: Need to select database for new microservice

**Alternatives Considered**:
1. PostgreSQL — Strong JSON support, team experience
2. MySQL — Lower cost, simpler setup
3. MongoDB — Document flexibility

**Rationale**: PostgreSQL chosen for JSON support needed by API
and team's existing expertise reduces ramp-up time.

**Impact**: DevOps team to provision by 2025-01-25
```

**Poor Example:**
```
Decided to use Postgres.
```

### Scoring Rules

- **90-100**: All decisions documented with context and rationale
- **80-89**: Most decisions well-documented, minor gaps
- **70-79**: Decisions present but lacking context/rationale
- **60-69**: Many decisions missing or poorly documented
- **< 60**: Critical decisions not captured

### Common Issues

1. Implicit decisions not explicitly stated
2. No rationale for why decision was made
3. Missing impact assessment
4. Decisions mixed into discussion without clear demarcation

## 4. Consistency (15% weight)

### Source Material Alignment

| Check | Points | Criteria |
|-------|--------|----------|
| Agenda Coverage | 4 | All agenda items addressed |
| Terminology | 3 | Consistent with project glossary |
| Attendee Match | 3 | Matches invitation/sign-in |
| Topic Accuracy | 3 | Discussion reflects actual conversation |
| Action Alignment | 2 | Actions match decisions |

### Consistency Checks

1. **Agenda Coverage**: Every agenda item has corresponding discussion
2. **Topic Drift**: Unplanned topics noted as "Added Items"
3. **Attendee Verification**: Matches meeting invitation or sign-in
4. **Terminology**: Uses project-standard terms consistently
5. **Cross-Reference**: Actions trace back to decisions

### Scoring Rules

- **90-100**: Full alignment with source materials
- **80-89**: Minor inconsistencies (terminology, 1 missing topic)
- **70-79**: Moderate inconsistencies affecting traceability
- **60-69**: Significant gaps between sources and minutes
- **< 60**: Major alignment issues or unverifiable content

### Common Issues

1. Agenda items skipped without explanation
2. Inconsistent terminology (using multiple names for same concept)
3. Discussion topics not in original agenda without notation
4. Attendee list doesn't match actual participants

## 5. Clarity (15% weight)

### Clarity Standards

| Criterion | Points | Description |
|-----------|--------|-------------|
| Specificity | 4 | Concrete details over vague statements |
| Unambiguous | 4 | Single clear interpretation |
| Professional | 3 | Appropriate tone and language |
| Scannable | 2 | Easy to find key information |
| Concise | 2 | No unnecessary verbosity |

### Language Quality Checks

**Avoid Vague Language:**
- ❌ "The team will look into this"
- ✅ "@Sarah will investigate API latency and report findings by Friday"

**Avoid Ambiguity:**
- ❌ "We agreed to improve performance"
- ✅ "Decided to reduce API response time to <200ms by Q2"

**Avoid Passive Voice (for action items):**
- ❌ "Documentation should be updated"
- ✅ "@Mike to update user documentation"

### Scoring Rules

- **90-100**: Clear, specific, professional throughout
- **80-89**: Mostly clear with occasional vague language
- **70-79**: Several instances of unclear or ambiguous text
- **60-69**: Frequent clarity issues affecting usability
- **< 60**: Minutes too vague to be useful

### Common Issues

1. Pronouns without clear antecedents ("they decided", "it should")
2. Relative terms without context ("soon", "later", "improved")
3. Technical jargon without definition for mixed audience
4. Run-on sentences making parsing difficult

## Overall Score Calculation

```
Overall = (Completeness × 0.25) + (ActionItems × 0.25) +
          (Decisions × 0.20) + (Consistency × 0.15) + (Clarity × 0.15)
```

## Score Interpretation

| Score | Rating | Action Required |
|-------|--------|-----------------|
| 90-100 | Excellent | Ready for distribution |
| 80-89 | Good | Minor revisions recommended |
| 70-79 | Acceptable | Revisions needed before distribution |
| 60-69 | Below Standard | Significant revisions required |
| < 60 | Unacceptable | Major rewrite needed |
