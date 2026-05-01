---
layout: default
title: "Web Server Security Reviewer"
grand_parent: English
parent: Meta & Quality
nav_order: 30
lang_peer: /ja/skills/meta/web-server-security-reviewer/
permalink: /en/skills/meta/web-server-security-reviewer/
---

# Web Server Security Reviewer
{: .no_toc }

Phase 1 web server (nginx / apache, Linux-centric) security configuration review. Validates the target with `target_profile.yaml`, verifies evidence integrity via `MANIFEST.txt` + `manifest_attestation.txt`, and performs read-only inspection across 9 axes either over SSH or against a pre-collected manifest. Windows / IIS hard-fails in v1.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/web-server-security-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/web-server-security-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

Performs a structured Phase 1 security configuration review of a Linux web server running nginx or apache. Two evidence-collection modes are supported:

1. **Direct SSH (read-only)** — connect with witness approval and run only commands explicitly allowed by the 6-tier guardrail catalog.
2. **Pre-collected manifest** — receive a `MANIFEST.txt` (SHA256-listed evidence) and a `manifest_attestation.txt` (truthfulness attestation) and verify integrity before review.

Findings are scored across three axes (Exploitability × Blast Radius × Service Criticality). Items that cannot be confirmed from the available evidence are not silently dropped — they are managed through `observation_status` so reviewers and stakeholders can see exactly what is verified vs. unverified. The skill enforces a self-review pass before finalization. Windows / IIS targets hard-fail in v1.

---

## 2. Prerequisites

- Python 3.9+ with PyYAML
- For SSH mode: bastion / jump-host approval, witness availability, read-only credentials
- For manifest mode: `MANIFEST.txt`, `manifest_attestation.txt`, and the referenced evidence files
- Target: Linux (RHEL family primary; nginx or apache). Windows / IIS is out of scope in v1.

---

## 3. Quick Start

```bash
# Install the skill locally
make install SKILL=web-server-security-reviewer

# Or fetch the .skill package
curl -L -o web-server-security-reviewer.skill \
  https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/web-server-security-reviewer.skill

# Internal verification (17 PASS expected)
cd skills/web-server-security-reviewer && python3 scripts/verify_skill.py
```

Then in Claude Code, describe the target (target profile, evidence mode) and the skill will guide you through the workflow.

---

## 4. How It Works

1. **Scope & target_profile** — fix the target via `assets/target_profile_template.yaml` (host role, OS family, web server, environment).
2. **Integrity gate** — for manifest mode, validate every file's SHA256 against `MANIFEST.txt`, and confirm `manifest_attestation.txt` truthfulness level.
3. **9-axis scan** — execute checks defined in `references/checklist_9axes.yaml`: OS / Resources / Logs / Network / Services / Authentication / Monitoring / Backup / Certificates.
4. **Guardrail enforcement** — every command is filtered through 6 tiers: `allowed`, `conditional`, `conditional_sensitive`, `ask-first`, `exceptional_sensitive_read`, `forbidden`. 21 forbidden commands are explicitly enumerated.
5. **Severity scoring** — each finding gets Exploitability + Blast Radius + Service Criticality; unverifiable items go to `observation_status`.
6. **Self-review** — mandatory pass using `assets/self_review_template.md` before report finalization.
7. **Output** — populated report, action plan, and finding table; raw evidence kept separate from the report directory.

---

## 5. Usage Examples

- Pre-go-live hardening review of a public-facing nginx server
- Periodic posture audit of internal apache servers without direct SSH access (manifest mode)
- Reviewing third-party-provided evidence dumps with integrity proof
- Documenting unverified items via `observation_status` for follow-up scope
- Generating an action plan ready for ops handoff

---

## 6. Understanding the Output

- **Report** (`assets/report_template.md`) — narrative review with findings, severity, and recommendations
- **Action plan** (`assets/action_plan_template.md`) — prioritized remediation work
- **Finding table** (`assets/finding_table_template.md`) — structured table for ticket import
- **Self-review** (`assets/self_review_template.md`) — completed before finalization
- **Evidence directory layout** (`assets/evidence_directory_layout.md`) — mandates separation of `evidence_dir/` and `raw_evidence_store/`

Each finding is one of: confirmed (verified from evidence), observed-pending (managed unverified state), or out-of-scope (e.g. Windows/IIS hard-fail).

---

## 7. Tips & Best Practices

- Do not run any command outside the `command_reference.yaml` catalog without escalation; the catalog is the contract with the witness.
- Treat `observation_status` as a feature, not a workaround — silent omission of unverifiable findings is a quality gap.
- Keep raw evidence (full configs, key material) in `raw_evidence_store/` and never embed it directly in the report.
- For manifest mode, refuse to proceed if attestation level is below the documented threshold (`references/secret_masking.md` and `verification_summary.md`).
- Re-run `scripts/verify_skill.py` whenever you change templates or command_reference.

---

## 8. Combining with Other Skills

- Pair with `incident-rca-specialist` when the review uncovers an active incident or recent compromise indicator.
- Hand findings to `compliance-advisor` for J-SOX / SOX mapping where applicable.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/meta/' | relative_url }}).
- See the full English skill catalog: [skill catalog]({{ '/en/skill-catalog/' | relative_url }}).

---

## 9. Troubleshooting

- **`python3 scripts/verify_skill.py` reports a failure** — the skill ships expecting all 17 checks to pass. Investigate before using the skill in a real engagement.
- **Manifest integrity fails** — do not proceed. Either re-collect evidence or escalate per `references/guardrails.md`.
- **Windows / IIS target detected** — the skill hard-fails by design in v1. Use a different process for those targets.
- **Find unresolved template / command IDs** — `verify_skill.py` will surface them; fix the cross-reference before running a real review.
- **Sensitive output appears in the report draft** — relocate to `raw_evidence_store/` and apply the masking rules from `references/secret_masking.md`.

---

## 10. Reference

**References:**

- `skills/web-server-security-reviewer/references/checklist_9axes.yaml`
- `skills/web-server-security-reviewer/references/command_reference.yaml`
- `skills/web-server-security-reviewer/references/finding_taxonomy.md`
- `skills/web-server-security-reviewer/references/guardrails.md`
- `skills/web-server-security-reviewer/references/input_contract.md`
- `skills/web-server-security-reviewer/references/observation_status.md`
- `skills/web-server-security-reviewer/references/schema_validation.md`
- `skills/web-server-security-reviewer/references/secret_masking.md`
- `skills/web-server-security-reviewer/references/severity_criteria.md`
- `skills/web-server-security-reviewer/references/unsupported_matrix.md`
- `skills/web-server-security-reviewer/references/verification_summary.md`
- `skills/web-server-security-reviewer/references/role_extensions/_schema.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_edge.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_internal.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_public_facing.yaml`

**Scripts:**

- `skills/web-server-security-reviewer/scripts/verify_skill.py`
- `skills/web-server-security-reviewer/scripts/verification_run.py`

**Assets:**

- `skills/web-server-security-reviewer/assets/target_profile_template.yaml`
- `skills/web-server-security-reviewer/assets/manifest_template.txt`
- `skills/web-server-security-reviewer/assets/manifest_attestation_template.txt`
- `skills/web-server-security-reviewer/assets/finding_table_template.md`
- `skills/web-server-security-reviewer/assets/report_template.md`
- `skills/web-server-security-reviewer/assets/action_plan_template.md`
- `skills/web-server-security-reviewer/assets/evidence_directory_layout.md`
- `skills/web-server-security-reviewer/assets/self_review_template.md`
