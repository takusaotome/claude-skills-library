# Definition of Done Framework

This document defines the standard completion vocabulary, provides detailed definitions for each completion state, catalogs common misuse patterns, and maps terminology between Japanese and English.

## 1. The Five Completion States

The foundation of this framework is that "done" is not a single binary state. Work progresses through a series of states, each with distinct meaning and evidence requirements. Conflating these states is the root cause of most completion-related quality escapes.

### State 1: Implemented (実装完了)

**Definition**: The code (or artifact) has been written, committed to version control, and passes the author's local checks. No assertion is made about integration quality, acceptance, or production readiness.

**What it means**:
- Source code is committed to the feature branch
- The author believes the code meets the requirements
- Basic compilation or syntax checks pass
- The author has run local unit tests (but CI may not have run yet)

**What it does NOT mean**:
- Integration tests have passed
- The code has been peer-reviewed
- The artifact meets acceptance criteria
- The feature is ready for release

**Required evidence**: Commit hash, branch name, author self-assessment

**JP/EN mapping**:
| Japanese | English | Notes |
|----------|---------|-------|
| 実装完了 | Implemented | Strictly code-level completion |
| コーディング完了 | Coding complete | Synonym, acceptable |
| 開発完了 | Development complete | Ambiguous -- avoid unless scoped to coding only |

---

### State 2: Verified (検証完了)

**Definition**: All standard verification commands have been executed against the artifact, results are recorded, and all mandatory criteria are met (or exceptions are formally registered).

**What it means**:
- All CI-defined standard commands have been executed
- Test results are recorded in a durable location
- Coverage thresholds are met
- Static analysis findings are within acceptable limits
- Any failures that are not resolved are registered as exceptions

**What it does NOT mean**:
- A human has reviewed and approved the results
- The artifact is accepted by stakeholders
- The artifact is ready for production deployment
- All edge cases have been tested (unless the standard command set covers them)

**Required evidence**: CI pipeline output, test report (total/passed/failed/skipped/coverage), static analysis report, exception register (if any)

**JP/EN mapping**:
| Japanese | English | Notes |
|----------|---------|-------|
| 検証完了 | Verified | Machine-verified against standard commands |
| テスト完了 | Testing complete | Acceptable if scope is explicitly defined |
| 品質確認完了 | Quality verification complete | Acceptable; implies broader scope than just tests |
| 全テストOK | All tests OK | DANGEROUS -- only acceptable if no exceptions exist and scope is explicit |

---

### State 3: Accepted (受入完了)

**Definition**: A designated approver (who is not the producer) has reviewed the verification evidence and formally signed off that the artifact meets acceptance criteria.

**What it means**:
- A human approver has reviewed the test results, coverage data, and exception register
- The approver confirms that the evidence supports the quality claim
- The approver's identity and date are recorded
- Any conditions on acceptance are documented

**What it does NOT mean**:
- The artifact has been deployed to production
- All exceptions have been resolved (they may be accepted with conditions)
- Post-deployment verification has occurred

**Required evidence**: Approver name, approval date, conditions (if any), reference to the verification evidence reviewed

**JP/EN mapping**:
| Japanese | English | Notes |
|----------|---------|-------|
| 受入完了 | Accepted | Formal human sign-off |
| 承認済 | Approved | Synonym, acceptable |
| レビュー完了 | Review complete | Acceptable if the review is the acceptance activity |

---

### State 4: Released (リリース完了)

**Definition**: The artifact has been deployed to the target production environment, post-deployment verification has been performed, and the deployment is confirmed operational.

**What it means**:
- The artifact is live in the production environment
- Post-deployment smoke tests have passed
- Monitoring confirms no anomalies
- The release record is updated with deployment timestamp and verification results

**What it does NOT mean**:
- All known limitations have been resolved (they may be documented and accepted)
- The feature is being used by all users (feature flags may limit exposure)

**Required evidence**: Deployment timestamp, environment identifier, post-deployment test results, monitoring status (nominal/degraded)

**JP/EN mapping**:
| Japanese | English | Notes |
|----------|---------|-------|
| リリース完了 | Released | Deployed and confirmed operational |
| デプロイ完了 | Deploy complete | Acceptable if post-deployment verification is included |
| 本番反映済 | Production-deployed | Acceptable |
| 出荷完了 | Shipped | Common in product contexts |

---

### State 5: Exception-approved (例外承認済)

**Definition**: One or more items that would normally be required for gate passage have been formally waived, with documented risk, temporary controls, owner, approver, and expiration date.

**What it means**:
- Specific incomplete items are identified and documented
- The risk of each item is assessed
- Temporary mitigating controls are in place
- An approver with appropriate authority has signed off
- A due date for resolution is set

**What it does NOT mean**:
- The item is forgotten or deprioritized
- The exception is permanent
- The risk is accepted without mitigation

**Required evidence**: Exception register entry with all required fields populated

**JP/EN mapping**:
| Japanese | English | Notes |
|----------|---------|-------|
| 例外承認済 | Exception-approved | Formal waiver with conditions |
| 条件付き承認 | Conditionally approved | Synonym, acceptable |
| 仮承認 | Provisional approval | Acceptable if conditions and expiration are documented |

## 2. Common Misuse Patterns

These are real-world patterns where completion vocabulary is misused, leading to quality escapes.

### Pattern A: "Complete" Without Verification

**What happens**: A developer marks a task as "complete" after committing code. The project tracker shows 100% completion. But standard verification has not been run.

**Root cause**: The tracker does not distinguish between Implemented and Verified.

**Prevention**: Configure the tracker to require separate state transitions. "Implemented" is not a terminal state; it must transition to "Verified" or "Exception-approved" before the item can be considered for release.

### Pattern B: "All Tests Pass" With Scope Ambiguity

**What happens**: A test report states "188 tests passed, 0 failed." This is cited as evidence that quality is confirmed. However, the 188 tests are unit tests only; integration and E2E tests were not executed (or were executed separately and had failures).

**Root cause**: The test report does not specify which standard command(s) were executed and what scope they cover.

**Prevention**: Every test report must include the exact command(s) that were run, the scope of each command, and explicit acknowledgment of what was NOT tested.

### Pattern C: "全OK" With Known Limitations

**What happens**: A completion summary states "全項目OK" (all items OK). However, a separate document lists three known limitations. The reader of the summary has no indication that exceptions exist.

**Root cause**: The summary language does not reference the exception register.

**Prevention**: Prohibit "all OK" language when any exception is registered. Required format: "N items verified, M exceptions registered (see Exception Register)."

### Pattern D: Metrics Divergence

**What happens**: The test report says 188 tests. The completion summary says 192 tests. The CI dashboard says 185 tests. Three different numbers for the same metric.

**Root cause**: Each document was authored independently, possibly from different test runs or with different counting methodologies.

**Prevention**: Designate a single authoritative source for each metric (the CI pipeline output). All other documents must reference that source, not independently count.

### Pattern E: "Release Ready" Without Post-Deployment Plan

**What happens**: A release decision document recommends release, but there is no post-deployment verification plan, no rollback plan, and no monitoring criteria defined.

**Root cause**: The release gate criteria did not include operational readiness items.

**Prevention**: The release gate must explicitly require post-deployment verification plan, rollback procedure, and monitoring criteria as mandatory evidence.

## 3. State Transition Rules

States must transition in order. Skipping states is prohibited unless an exception is formally approved.

```
Implemented --> Verified --> Accepted --> Released
                    |
                    +--> Exception-approved --> (Accepted with conditions)
```

### Valid Transitions

| From | To | Condition |
|------|----|-----------|
| Implemented | Verified | All standard commands executed and results recorded |
| Verified | Accepted | Approver signs off on evidence |
| Accepted | Released | Deployment executed and post-deployment verification passes |
| Verified | Exception-approved | One or more criteria not met; exception formally registered |
| Exception-approved | Accepted | Approver accepts with documented conditions |

### Invalid Transitions (PROHIBITED)

| From | To | Why Prohibited |
|------|----|----------------|
| Implemented | Accepted | Cannot accept without verification evidence |
| Implemented | Released | Cannot release without verification or acceptance |
| Verified | Released | Cannot release without acceptance sign-off |
| Exception-approved | Released | Cannot release without acceptance (even conditional) |

## 4. Vocabulary Quick Reference Card

A summary card for posting in team workspaces or including in project documentation.

| State | JP | EN | Implies Quality? | Implies Approval? | Implies Production? |
|-------|-----|-----|-------------------|--------------------|--------------------|
| Implemented | 実装完了 | Implemented | No | No | No |
| Verified | 検証完了 | Verified | Yes (machine) | No | No |
| Accepted | 受入完了 | Accepted | Yes (human) | Yes | No |
| Released | リリース完了 | Released | Yes | Yes | Yes |
| Exception-approved | 例外承認済 | Exception-approved | Partial | Conditional | No |
