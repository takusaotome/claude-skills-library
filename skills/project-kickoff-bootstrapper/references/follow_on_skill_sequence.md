# Follow-On Skill Sequence

The bootstrap skill should end by recommending the next best skill, not by trying to do everything itself.

## 1. Recommended Sequence After Bootstrap

### If completion criteria are still weak
Recommend:
- `completion-quality-gate-designer`

Use when:
- `QUALITY_GATES.md` is still shallow
- exit criteria, evidence ownership, or waiver rules need rigor

### If reuse risk or shared utilities look dangerous
Recommend:
- `hidden-contract-investigator`

Use when:
- the repo relies on wrappers, shared services, legacy helpers, or poorly named abstractions
- mocks are hiding real runtime behavior

### If risky implementation patterns are likely
Recommend:
- `safe-by-default-architect`

Use when:
- auth, SQL, file I/O, external integrations, or security-sensitive design choices are involved
- the team wants safe defaults before coding expands

### If business rules span multiple flows or modules
Recommend:
- `cross-module-consistency-auditor`

Use when:
- the same rule appears in API, batch, admin, export, or reporting flows
- copy-paste or update-leak risk is visible

### If production-only failures are a concern
Recommend:
- `production-parity-test-designer`

Use when:
- staging differs from prod
- packaging, runtime dependencies, migrations, or DB dialect differences matter

## 2. Recommendation Rule

Do not recommend every skill every time.
Recommend only the 1–3 most relevant follow-on skills based on:
- detected repo risks
- missing rigor in the generated docs
- the user’s stated goals

## 3. Handoff Format

End with:
- `Recommended next skill`
- `Why it is the next bottleneck`
- `Which generated file it should deepen`
