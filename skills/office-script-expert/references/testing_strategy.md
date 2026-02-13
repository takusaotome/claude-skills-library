# Testing Strategy for Office Scripts

## Architecture: lib/ Separation for Testability

Office Scripts cannot be directly unit-tested because:
- They require the `ExcelScript.Workbook` parameter (not mockable without framework)
- They run in a specialized Office Scripts runtime, not Node.js
- The `main(workbook)` function signature is fixed by the platform

**Solution**: Extract all pure logic into `lib/*.ts` modules with standard ES exports.
These modules are testable via Vitest in a regular Node.js environment.

```
lib/                          # Testable pure logic (no ExcelScript dependency)
  types.ts                   # Interface definitions (shared)
  rounding.ts                # roundHalfEven2, roundUp2, roundUp4, roundDown4
  prep-calculator.ts         # calculatePrepRequirements, getPrepLocation, etc.
  ingredient-calculator.ts   # convertToLb, allocateInventoryFefo, etc.
  order-calculator.ts        # calculateOrderLots
  csv-parser.ts              # parseCsvText, normalizeHeaders, detectRecipeDiff

__tests__/                    # Vitest test files
  rounding.test.ts
  prep-calculator.test.ts
  ingredient-calculator.test.ts
  order-calculator.test.ts
  csv-parser.test.ts
```

**What cannot be tested**: Excel API interaction code (reading sheets, writing ranges,
protection handling). These are verified through manual testing in the Office Scripts editor.

## Project Setup

### package.json

```json
{
  "name": "office-scripts",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "vitest": "^2.0.0"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "outDir": "./dist",
    "rootDir": ".",
    "types": []
  },
  "include": ["lib/**/*.ts", "__tests__/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

**Note**: `"types": []` prevents automatic inclusion of `@types/node` or other ambient
declarations that could conflict with Office Scripts types.

### vitest.config.ts

```typescript
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    include: ["__tests__/**/*.test.ts"],
  },
});
```

## Test Categories

### 1. Unit Tests (Pure Logic)

Test individual functions with known inputs/outputs:

```typescript
describe("roundHalfEven2", () => {
  it("rounds normal values to 2 decimal places", () => {
    expect(roundHalfEven2(1.234)).toBe(1.23);
    expect(roundHalfEven2(1.236)).toBe(1.24);
  });
});
```

### 2. Boundary Value Tests

Test edge cases and boundaries:

```typescript
it("handles exact 0.5 boundary (banker's rounding)", () => {
  expect(roundHalfEven2(2.125)).toBe(2.12);  // Even floor -> keep
  expect(roundHalfEven2(0.015)).toBe(0.02);   // Odd floor -> round up
});

it("handles zero", () => {
  expect(roundHalfEven2(0)).toBe(0);
});

it("handles negative values", () => {
  expect(roundHalfEven2(-1.234)).toBe(-1.23);
});
```

### 3. Business Scenario Tests

Test with realistic business data combinations:

```typescript
it("handles business case: prep qty = adjusted_sales * recipe_qty", () => {
  expect(roundUp2(120.0 * 0.35)).toBe(42.0);
  expect(roundUp2(108.0 * 0.35)).toBe(37.8);
});

it("handles CK transfer truncation to prevent over-allocation", () => {
  expect(roundDown4(10.12345)).toBe(10.1234);
});
```

### 4. Python Consistency Tests

Verify TypeScript results match Python calculation engine:

```typescript
it("matches Python round() for business cases", () => {
  // Python: round(100 * 1.2, 2) = 120.0
  expect(roundHalfEven2(100 * 1.2)).toBe(120.0);
  // Python: round(50 * 0.9, 2) = 45.0
  expect(roundHalfEven2(50 * 0.9)).toBe(45.0);
});
```

**Recommended**: Generate test vectors from Python and verify in TypeScript:

```python
# Generate test vectors in Python
import json, math
cases = [(100, 1.2), (50, 0.9), (120, 1.2), (75, 1.15)]
vectors = [{"a": a, "b": b, "result": round(a * b, 2)} for a, b in cases]
print(json.dumps(vectors))
```

```typescript
// Verify in TypeScript
const vectors = [
  { a: 100, b: 1.2, result: 120.0 },
  { a: 50, b: 0.9, result: 45.0 },
];
vectors.forEach(({ a, b, result }) => {
  expect(roundHalfEven2(a * b)).toBe(result);
});
```

## Running Tests

```bash
# From the office_scripts directory:
cd excel/office_scripts

# Install dependencies
npm install

# Run all tests
npm test

# Run in watch mode (re-runs on file change)
npm run test:watch

# Type-check only (no test execution)
npm run typecheck
```

## Test Coverage Gap: Excel API Code

The following code paths are NOT covered by Vitest and must be manually tested:

- Sheet reading (`loadStores`, `loadPrepItems`, etc.)
- Sheet writing (`writePrepList`, `writeIngredientList`)
- Sheet protection handling (`unprotect` / `protect`)
- CSV dual-mode detection (single cell vs cell grid)
- Dashboard KPI updates
- Excel date serial number conversion in context

**Manual test procedure**:
1. Open the workbook in Excel Online
2. Paste test data in the appropriate input sheets
3. Run the script from the Office Scripts editor
4. Verify output sheets match expected results
5. Check for errors in the editor's Output pane
