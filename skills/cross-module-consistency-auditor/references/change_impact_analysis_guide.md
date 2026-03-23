# Change Impact Analysis Guide

## Purpose

This reference provides systematic techniques for identifying the full blast radius of a change. The goal is to ensure that no affected module, output, test, or document is missed when a change propagates across a system.

## Finding the Source of Truth

### Definition

The **source of truth** is the single authoritative location where a piece of logic, data definition, or business rule is canonically implemented. All other occurrences are either references to this location or copies of it.

### Identification Techniques

1. **Follow the Write Path**: Trace where the data or behavior is first created. The module that performs the initial calculation, validation, or transformation is typically the source of truth.

2. **Check for Shared Libraries**: Look for utility functions, shared services, or common modules that encapsulate the logic. If such a module exists, it is likely the source of truth.

3. **Search for Constants and Configuration**: Business rules often originate from configuration tables, constants files, or environment variables. These are upstream sources of truth.

4. **Examine Database Constraints**: CHECK constraints, triggers, and stored procedures that enforce a rule at the persistence layer may serve as the authoritative definition.

5. **Review API Contracts**: For inter-service communication, the API contract (OpenAPI spec, protobuf schema, GraphQL schema) often serves as the source of truth for data shape and validation rules.

### Common Pitfalls

- **Assuming the UI is the source of truth**: UI validation is typically a convenience copy. The backend service or database constraint is usually authoritative.
- **Confusing the first implementation with the source of truth**: The first code written is not necessarily the canonical version. The one that is tested, documented, and referenced by others is the source of truth.
- **Missing configuration-level sources**: Some logic is driven by database rows (feature flags, rule tables, configuration entries) rather than code.

## Tracing Propagation Paths

### Upstream Analysis

Upstream modules are those that produce or define the data that the change kernel consumes. Changes to upstream modules can invalidate assumptions made by the change kernel.

**Upstream Trace Procedure:**

1. Identify all inputs to the change kernel (function parameters, database reads, API calls, configuration lookups)
2. For each input, trace backward to its origin:
   - Which module writes this data?
   - Which API provides this data?
   - Which configuration defines this value?
3. Assess whether the upstream module needs modification:
   - Does the upstream data format need to change?
   - Does the upstream validation need to accommodate new values?
   - Does the upstream module need to produce additional data?

### Downstream Analysis

Downstream modules are those that consume the output of the change kernel. They may break or produce incorrect results if the change kernel's output changes.

**Downstream Trace Procedure:**

1. Identify all outputs of the change kernel (return values, database writes, API responses, events published, files generated)
2. For each output, trace forward to all consumers:
   - Which modules read this data from the database?
   - Which services subscribe to events published by this module?
   - Which reports query this data?
   - Which batch jobs process this data?
   - Which external systems receive this data via integration?
3. Assess the impact on each downstream consumer:
   - Can the downstream module handle the new data format?
   - Does the downstream aggregation include or exclude the new data correctly?
   - Does the downstream display render the new data appropriately?

### Lateral Analysis

Lateral modules are those that implement the same or similar logic independently. They are not in the data flow path but must maintain consistency with the change.

**Lateral Trace Procedure:**

1. Search for code duplication: functions with similar names, similar structure, or similar comments
2. Search for copy-paste indicators: identical variable names, identical comment blocks, similar error messages
3. Search for parallel implementations: the same business operation implemented for different entity types, different channels, or different regions
4. Check for similar configuration: parallel feature flags, parallel rule tables, parallel constant definitions

## Including Documentation and Tests in Impact Analysis

### Documentation Impact

Changes frequently invalidate existing documentation. Include these in the impact map:

- **Technical specifications**: Architecture documents, design documents, data flow diagrams
- **API documentation**: OpenAPI specs, Swagger docs, Postman collections, integration guides
- **User guides**: End-user documentation, training materials, help center articles
- **Runbooks**: Operational procedures, troubleshooting guides, deployment checklists
- **Release notes**: Feature descriptions, known limitations, migration instructions

### Test Impact

Changes create test obligations at multiple levels:

- **Unit tests**: Tests for the source-of-truth module and each copy
- **Integration tests**: Tests for interactions between affected modules
- **E2E tests**: Tests for complete user flows that traverse affected modules
- **Performance tests**: If the change affects calculation paths that are performance-sensitive
- **Regression tests**: Tests that verify previously working functionality remains correct

### Identifying Missing Test Coverage

For each affected module, check:

1. Does a test file exist for this module?
2. Does the test file cover the specific behavior being changed?
3. Are there integration tests that exercise the interaction between this module and its upstream/downstream modules?
4. Are there E2E tests that exercise the complete flow?

Modules with no test coverage for the affected behavior should be flagged as high-risk in the impact map.

## Practical Checklist

Use this checklist to verify that the impact analysis is complete:

- [ ] Source of truth identified and documented
- [ ] All upstream dependencies traced
- [ ] All downstream consumers traced
- [ ] All lateral (copy-paste) implementations found
- [ ] All 8 impact lenses applied (input, persistence, aggregation, display, API, reverse, permission, downstream jobs)
- [ ] Documentation impact assessed (specs, API docs, user guides, runbooks)
- [ ] Test impact assessed (unit, integration, E2E, performance, regression)
- [ ] Missing test coverage flagged
- [ ] Uncertain modules marked with [NEEDS CONFIRMATION]
- [ ] Module count tallied per lens category
- [ ] Copy count vs shared-reference count documented
