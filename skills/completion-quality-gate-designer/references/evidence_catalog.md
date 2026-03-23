# Evidence Catalog

This document provides a comprehensive inventory of evidence types used in quality gates, organized by category. For each evidence type, it specifies the expected format, typical source, auto-collectability, and guidance on evaluating quality.

## 1. Test Result Evidence

Test results are the most common form of quality gate evidence. The key discipline is ensuring that test results specify scope, source, and completeness.

### 1.1 Unit Test Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | Individual functions/methods behave correctly in isolation |
| **Typical source** | `pytest`, `jest`, `JUnit`, `go test` |
| **Auto-collectible** | Yes -- CI pipeline standard output |
| **Required fields** | Total tests, passed, failed, skipped, error, execution time, coverage % |
| **Common pitfall** | Reporting "188 passed" without disclosing that 12 were skipped. Skipped tests must be reported and justified. |
| **Quality check** | Verify that test count has not decreased since last gate (regression detection). Verify that skipped tests are documented with reasons. |

### 1.2 Integration Test Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | Components interact correctly across boundaries (API calls, DB queries, message queues) |
| **Typical source** | `pytest -m integration`, `jest --testPathPattern=integration`, custom test suites |
| **Auto-collectible** | Yes -- CI pipeline, but may require special environment setup |
| **Required fields** | Total tests, passed, failed, skipped, execution time, environment description |
| **Common pitfall** | Running integration tests against a mock instead of a real service and reporting them as integration evidence. Specify the target environment explicitly. |
| **Quality check** | Verify that the environment description matches the intended test environment (staging vs mock). |

### 1.3 End-to-End (E2E) Test Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | User-facing workflows function correctly from start to finish |
| **Typical source** | Playwright, Cypress, Selenium, custom E2E frameworks |
| **Auto-collectible** | Yes -- but typically runs on a separate schedule or pipeline stage |
| **Required fields** | Total scenarios, passed, failed, skipped, screenshots/videos on failure, browser/device matrix |
| **Common pitfall** | E2E tests are often slow and flaky. Teams may exclude them from the standard command set and then forget to run them. If E2E is part of the gate criteria, it must be in the standard command set. |
| **Quality check** | Verify that E2E was actually executed (not just unit tests reported as "all tests"). Check CI job logs for the specific E2E stage. |

### 1.4 Performance/Load Test Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | System meets performance requirements under expected and peak load |
| **Typical source** | k6, JMeter, Locust, Artillery |
| **Auto-collectible** | Partially -- execution can be automated, but result interpretation often requires human review |
| **Required fields** | Scenarios tested, concurrent users, request rate, latency percentiles (P50/P95/P99), error rate, throughput, resource utilization |
| **Common pitfall** | Running a load test with unrealistic traffic patterns and claiming "performance verified." |
| **Quality check** | Verify that test scenarios match production traffic patterns. Verify that thresholds are defined before the test runs (not determined after seeing results). |

## 2. CI/CD Pipeline Evidence

### 2.1 CI Pipeline Output

| Attribute | Description |
|-----------|-------------|
| **What it proves** | The automated build and test pipeline completed with a specific result |
| **Typical source** | GitHub Actions, GitLab CI, Jenkins, CircleCI |
| **Auto-collectible** | Yes -- the pipeline itself is the source of truth |
| **Required fields** | Pipeline ID/URL, trigger (commit hash, branch, PR), start time, end time, overall status, per-stage status |
| **Common pitfall** | Referencing a pipeline run from a different commit than the one being evaluated. Always link evidence to the specific commit hash. |
| **Quality check** | Verify that the pipeline commit hash matches the release candidate commit. Verify that no stages were manually skipped or overridden. |

### 2.2 Required Status Checks

| Attribute | Description |
|-----------|-------------|
| **What it proves** | Branch protection rules enforced specific checks before merge |
| **Typical source** | GitHub branch protection settings, GitLab merge request approvals |
| **Auto-collectible** | Yes -- platform API or UI |
| **Required fields** | List of required checks, status of each check, merge commit hash, merge author, approval records |
| **Common pitfall** | Having required status checks configured but then using admin override to merge without them passing. Track admin overrides as exceptions. |
| **Quality check** | Audit merge history for admin overrides. Each override should correspond to an exception register entry. |

### 2.3 Artifact Registry Records

| Attribute | Description |
|-----------|-------------|
| **What it proves** | A specific build artifact was published to the artifact registry |
| **Typical source** | Docker Hub, AWS ECR, npm registry, PyPI, Maven Central |
| **Auto-collectible** | Yes -- registry API |
| **Required fields** | Artifact name, version/tag, digest/hash, publish timestamp, source commit hash |
| **Quality check** | Verify that the published artifact's source commit matches the verified commit. |

## 3. Static Analysis Evidence

### 3.1 Linter Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | Code conforms to style and basic quality rules |
| **Typical source** | ESLint, Pylint, Ruff, RuboCop, Checkstyle |
| **Auto-collectible** | Yes |
| **Required fields** | Tool name and version, rule set (config file reference), total issues by severity, zero-tolerance violations |
| **Quality check** | Verify that the rule set has not been weakened since the last gate (no rules silently disabled). |

### 3.2 Security Scanner Results

| Attribute | Description |
|-----------|-------------|
| **What it proves** | No known security vulnerabilities above the defined threshold |
| **Typical source** | Snyk, Trivy, Dependabot, CodeQL, SonarQube |
| **Auto-collectible** | Yes |
| **Required fields** | Tool name and version, scan scope (dependencies, code, containers), findings by severity (critical/high/medium/low), suppressed findings with justification |
| **Common pitfall** | Suppressing findings without documented justification. Every suppression must reference an exception register entry or a documented false-positive rationale. |
| **Quality check** | Verify that critical and high findings are either resolved or registered as exceptions. Verify that suppressions have justification. |

### 3.3 Code Coverage Report

| Attribute | Description |
|-----------|-------------|
| **What it proves** | What percentage of the codebase is exercised by tests |
| **Typical source** | coverage.py, Istanbul/nyc, JaCoCo, go tool cover |
| **Auto-collectible** | Yes |
| **Required fields** | Overall coverage %, line coverage %, branch coverage %, per-module breakdown, uncovered critical paths |
| **Common pitfall** | Achieving high coverage by testing trivial paths while leaving critical business logic uncovered. Coverage is a necessary but not sufficient quality indicator. |
| **Quality check** | Review uncovered lines in critical modules. Verify that coverage has not decreased since the last gate. |

## 4. Manual Verification Evidence

### 4.1 Peer Review Records

| Attribute | Description |
|-----------|-------------|
| **What it proves** | Another qualified person has reviewed the artifact and found it acceptable |
| **Typical source** | Pull request reviews, code review tools, design review minutes |
| **Auto-collectible** | Partially -- PR approval status is auto-collectible; review depth is not |
| **Required fields** | Reviewer name, review date, scope of review, approval status, comments/findings |
| **Quality check** | Verify that the reviewer is not the same person as the author. Verify that the review covers the intended scope (not just a rubber-stamp approval). |

### 4.2 User Acceptance Testing (UAT) Records

| Attribute | Description |
|-----------|-------------|
| **What it proves** | End users or their representatives have validated that the artifact meets business requirements |
| **Typical source** | UAT session notes, acceptance test case results, stakeholder sign-off forms |
| **Auto-collectible** | No -- inherently manual |
| **Required fields** | Tester name and role, test date, test cases executed, results per case, overall acceptance decision, conditions or reservations |
| **Quality check** | Verify that the UAT scope covers the acceptance criteria defined in the requirements. Verify that the tester has appropriate domain knowledge. |

### 4.3 Exploratory Testing Notes

| Attribute | Description |
|-----------|-------------|
| **What it proves** | A skilled tester has explored the system beyond scripted test cases and documented findings |
| **Typical source** | Session-based test management notes, bug reports, observation logs |
| **Auto-collectible** | No |
| **Required fields** | Tester name, session duration, areas explored, charter/focus, findings, new risks identified |
| **Quality check** | Verify that exploratory testing was time-boxed and focused (not ad-hoc). Verify that findings are actionable (filed as bugs or documented as known limitations). |

## 5. Exception and Approval Evidence

### 5.1 Exception Approval Records

| Attribute | Description |
|-----------|-------------|
| **What it proves** | A specific incomplete item was formally reviewed and approved for deferral |
| **Typical source** | Exception register, issue tracker, approval emails |
| **Auto-collectible** | No -- requires human judgment and sign-off |
| **Required fields** | Exception ID, what is deferred, why, risk assessment, temporary control, due date, owner, approver name and date |
| **Quality check** | Verify that the approver has appropriate authority for the risk level. Verify that the temporary control is actually in place (not just planned). |

### 5.2 Gate Sign-off Records

| Attribute | Description |
|-----------|-------------|
| **What it proves** | The designated authority has reviewed all gate evidence and approved progression |
| **Typical source** | Gate review meeting minutes, sign-off forms, approval workflow records |
| **Auto-collectible** | No |
| **Required fields** | Gate ID, approver name, approval date, evidence reviewed (list with links), conditions, next gate |
| **Quality check** | Verify that the approver reviewed the actual evidence (not just the summary). Verify that conditions from previous gates have been met. |

## 6. Evidence Quality Principles

### Traceability
Every piece of evidence must be traceable to a specific artifact version (commit hash, build number, document version). Evidence without version traceability is unreliable.

### Durability
Evidence must be stored in a location that persists beyond the build pipeline execution. Terminal output that is not captured is not evidence. CI logs that expire after 30 days must be archived if the gate record needs to persist longer.

### Immutability
Evidence should not be modifiable after the gate review. Use artifact digests, signed commits, or immutable storage to ensure that evidence cannot be retroactively altered.

### Completeness
Every gate criterion must have corresponding evidence. A gate record with missing evidence fields is incomplete and should not be accepted. "N/A" is only acceptable if the criterion is documented as not applicable for this specific project, with justification.
