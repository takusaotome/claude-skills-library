# Office Scripts Platform Limitations

## P1: No `import` / `export` Statements

Office Scripts run in an isolated sandbox. The `import` and `export` keywords are **not supported** in the runtime environment.

### Workaround: Inline with Markers

```typescript
// In CalculateRequirements.ts:
// ============================================================
// INLINED: lib/rounding.ts
// ============================================================

function roundHalfEven2(value: number): number {
  // ... (copy from lib/rounding.ts, remove `export` keyword)
}
```

**Workflow**:
1. Edit the canonical version in `lib/*.ts` (with `export`)
2. Run `vitest run` to verify
3. Copy the function body into the main script
4. Replace `export function` with `function`
5. Add `// INLINED: lib/<filename>.ts` marker comment

### Why Markers Matter

- They create a traceable link between the inline copy and the canonical source
- During code review, reviewers can verify the inline copy matches `lib/`
- Future updates can be found with `grep "INLINED"` across all scripts

## P2: No External Libraries

npm packages like `lodash`, `date-fns`, `decimal.js` cannot be imported.
All utility functions must be written from scratch.

### Impact
- CSV parsing: Hand-written state machine (`parseCsvText`)
- Date handling: Manual Excel serial number conversion (`excelDateToJsDate`)
- Rounding: Custom banker's rounding implementation (`roundHalfEven2`)

## P3: Map/Set `for..of` May Fail at Runtime

While TypeScript compiles `for (const [key, value] of map)` without errors,
the Office Scripts runtime may throw errors or produce unexpected behavior.

### Safe Patterns

```typescript
// UNSAFE in Office Scripts:
for (const [key, value] of myMap) { ... }  // May fail at runtime

// SAFE: Array.from + indexed loop
const entries = Array.from(myMap.entries());
for (let i = 0; i < entries.length; i++) {
  const key = entries[i][0];
  const value = entries[i][1];
  // ...
}

// SAFE: forEach (when you don't need break/continue)
myMap.forEach((value, key) => {
  // ...
});
```

### Real Example (from CalculateRequirements.ts)

```typescript
// CK transfer calculation:
const sortedEntries = Array.from(storeShortage.entries())
  .filter((e) => e[1] > 0)
  .sort((a, b) => b[1] - a[1]);

for (let _i = 0; _i < sortedEntries.length; _i++) {
  const key = sortedEntries[_i][0];
  const shortage = sortedEntries[_i][1];
  // ...
}
```

**Note**: Use `_i`, `_ri`, `_ci` etc. prefixes to avoid variable name collisions when nesting multiple indexed loops.

## P4: 120-Second Timeout

All Office Script executions must complete within **120 seconds**.
For large datasets (1000+ menu items x 10+ stores), optimize:

- Batch `setValues()` calls (write entire range at once, not cell-by-cell)
- Minimize `getValues()` calls (read sheet once, process in memory)
- Avoid redundant sheet reads (load all master data upfront, pass as parameters)

### Anti-pattern

```typescript
// SLOW: Cell-by-cell write
for (let i = 0; i < results.length; i++) {
  sheet.getRange(`A${i+2}`).setValue(results[i].name);
  sheet.getRange(`B${i+2}`).setValue(results[i].qty);
}

// FAST: Batch write
const values = results.map(r => [r.name, r.qty]);
sheet.getRangeByIndexes(1, 0, values.length, 2).setValues(values);
```

## P5: `console.log` Limitations

`console.log` output is visible in the Office Scripts editor "Output" pane but:
- Has limited buffer size
- Not available in Power Automate-triggered runs
- Cannot be programmatically captured

### Workaround for Debugging

Write debug info to a dedicated cell or sheet:

```typescript
// Debug output to a cell
dashboard.getRange("Z1").setValue(`Debug: ${prepResults.length} prep items`);
```

## P6: TypeScript Subset Constraints

Office Scripts use a TypeScript subset. Some features that may not work:

- Decorators
- Ambient type declarations
- Some advanced generic patterns
- Dynamic `import()`
- `eval()`
- DOM APIs (`document`, `window`)

### Safe TypeScript Features

- Interfaces and type aliases
- Generics (basic)
- Union types (`string | number`)
- Optional chaining (`obj?.prop`)
- Nullish coalescing (`value ?? default`)
- Array methods (`map`, `filter`, `reduce`, `sort`)
- Template literals
- Destructuring (basic)
- Spread operator
