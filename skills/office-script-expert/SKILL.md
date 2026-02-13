---
name: office-script-expert
description: >
  Office Scripts (Excel Online / Microsoft 365) development expert skill.
  Covers platform limitations, ExcelScript API patterns, testing strategy (lib + Vitest),
  and 13 real-world bug patterns discovered during production development.
  Trigger words: Office Scripts, ExcelScript, Excel Online, Office Script development,
  TypeScript Excel, Excel automation, CalculateRequirements, ImportCsvData
---

# Office Scripts Expert Skill

## Overview

Office Scripts are TypeScript-based automation scripts for Excel on the web (Microsoft 365).
They are fundamentally different from VBA and Power Automate:

| Aspect | Office Scripts | VBA | Power Automate |
|--------|---------------|-----|----------------|
| Language | TypeScript (subset) | VBA | Low-code / expressions |
| Runtime | Server-side (Excel Online) | Client-side (Desktop) | Cloud service |
| Module system | **None** (no import/export) | Modules | Connectors |
| External libs | **Not available** | COM references | Connectors |
| Timeout | **120 seconds** | None | 30 min (premium) |
| Testing | Indirect (lib extraction) | Manual | Manual |

## Architecture Pattern: lib/ Extraction + Inline

Because Office Scripts cannot use `import`, the project uses a dual-file approach:

```
office_scripts/
  lib/                      # Canonical, testable source (ES modules)
    types.ts                # Interface definitions
    rounding.ts             # Rounding functions (export)
    prep-calculator.ts      # Prep calculation logic (export)
    ingredient-calculator.ts # Ingredient calculation logic (export)
    order-calculator.ts     # Order lot calculation (export)
    csv-parser.ts           # CSV parsing and header normalization (export)
  __tests__/                # Vitest unit tests
    rounding.test.ts
    prep-calculator.test.ts
    ingredient-calculator.test.ts
    order-calculator.test.ts
    csv-parser.test.ts
  CalculateRequirements.ts  # Main script (lib/* functions INLINED)
  ImportCsvData.ts          # Import script (lib/* functions INLINED)
```

**Key rule**: Edit `lib/*.ts` first, run tests, then copy the updated functions into the main scripts with `// INLINED: lib/*.ts` markers.

## 6 Critical Platform Constraints (P1-P6)

| ID | Constraint | Impact | Workaround |
|----|-----------|--------|------------|
| P1 | No `import`/`export` | Cannot share code between scripts | Inline with markers |
| P2 | No external libraries | No lodash, date-fns, etc. | Write from scratch |
| P3 | Map/Set `for..of` may fail | Runtime errors on iteration | `Array.from().forEach` or indexed loop |
| P4 | 120-second timeout | Large datasets may fail | Batch processing, minimize API calls |
| P5 | `console.log` limited | No persistent logging | Use cell writes for debug output |
| P6 | TypeScript subset | Some TS features unavailable | Test in Office Scripts editor |

See: [references/platform_limitations.md](references/platform_limitations.md)

## Reference Guide

Load these files based on your current task:

| Situation | Reference to Load |
|-----------|-------------------|
| Writing ExcelScript API code (read/write cells, sheets) | [excel_api_patterns.md](references/excel_api_patterns.md) |
| Debugging or reviewing existing code | [common_bug_patterns.md](references/common_bug_patterns.md) |
| Setting up or running tests | [testing_strategy.md](references/testing_strategy.md) |
| Understanding runtime constraints | [platform_limitations.md](references/platform_limitations.md) |
| Before deploying / code review | [implementation_checklist.md](assets/implementation_checklist.md) |

## Quick Reference Table

| Task | Pattern | Reference |
|------|---------|-----------|
| Read sheet data | `getUsedRange().getValues()` + header index lookup | excel_api_patterns.md #1 |
| Write results to sheet | `getRangeByIndexes().setValues()` | excel_api_patterns.md #2 |
| Protect/unprotect sheet | `unprotect() -> write -> protect()` | excel_api_patterns.md #3 |
| Parse CSV input | Dual-mode: single-cell text vs cell grid | excel_api_patterns.md #7 |
| Section-based sheet parsing | `currentSection` + `currentHeaders` state machine | excel_api_patterns.md #6 |
| Clear data without destroying headers | Pre-locate section positions, clear data rows only | excel_api_patterns.md #8 |
| Convert Excel dates | `excelDateToJsDate(serial)` | excel_api_patterns.md #4 |
| Sheet name with spaces in formulas | Quote: `'Sheet Name'!A1` | excel_api_patterns.md #5 |
| Iterate Map/Set | `Array.from(map.entries())` + indexed for loop | platform_limitations.md P3 |
| Rounding to match Python | `roundHalfEven2` / `roundUp2` / `roundUp4` / `roundDown4` | excel_api_patterns.md #9 |
| Test pure logic | `lib/*.ts` with Vitest | testing_strategy.md |
| Pre-deploy review | Implementation checklist | implementation_checklist.md |
