#!/usr/bin/env python3
"""build_target_profile.py — wizard answers → target_profile.yaml.

Reads a JSON answers blob (collected via the interview wizard described in
references/interview_wizard.md), validates inputs, fills defaults, derives
values (delete_after, source_confidence), and emits target_profile.yaml
conforming to references/input_contract.md.

Usage:
    python3 scripts/build_target_profile.py --answers wizard_answers.json \\
        --output target_profile.yaml

    # Or positional form:
    python3 scripts/build_target_profile.py wizard_answers.json \\
        --output target_profile.yaml
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HARD_FAIL_OS = {"windows"}
HARD_FAIL_WEB = {"iis"}

VALID_OS_FAMILY = {"rhel", "debian", "windows"}
VALID_WEB_SERVER = {"nginx", "apache", "iis", "none"}
VALID_CONNECTION_MODE = {"ssh_direct", "offline_evidence"}
VALID_AUTHENTICITY = {"attestation_only", "external_channel", "gpg_signed", "ssh_signed"}
VALID_SOURCE_CONFIDENCE = {"high", "medium", "low"}
PRESET_ROLE_EXTENSIONS = {
    "public_facing": ["generic_public_facing"],
    "internal": ["generic_internal"],
    "edge": ["generic_edge"],
}

ALL_AXES = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]
DEFAULT_EARLY_DELETION_CONDITIONS = [
    "シークレットローテーション完了 かつ レビュー成果物確定後",
]

SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
REVIEW_ID_RE = re.compile(r"^[A-Z][A-Z0-9_]*-REVIEW-\d{4}-\d{4}-\d{2}$")

# Strings the wizard accepts as "no value" (case-insensitive).
NULL_EQUIVALENTS = {"", "none", "null", "なし", "n/a"}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class WizardError(ValueError):
    """Validation error in wizard answers (recoverable — re-prompt user)."""


class HardFailError(RuntimeError):
    """Unsupported configuration that aborts the entire review."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def normalize_csv(value: Any) -> list[str]:
    """Normalize free-text comma-separated input into a clean list."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [s.strip() for s in str(value).split(",") if s.strip()]


def normalize_optional_null(value: Any) -> str | None:
    """Treat empty / "none" / "null" / "なし" / "n/a" (any case) as None.

    Used for optional fields where the wizard hint allows the user to type
    a sentinel string instead of leaving the answer blank.
    """
    if value is None:
        return None
    raw = str(value).strip()
    if raw.lower() in NULL_EQUIVALENTS:
        return None
    return raw


def validate_machine_id_sha256(value: Any) -> str:
    """Reject raw /etc/machine-id; only accept lowercase hex SHA256 (64 chars)."""
    if not isinstance(value, str):
        raise WizardError("machine_id_sha256 must be a string")
    v = value.strip()
    if not SHA256_RE.match(v):
        raise WizardError(
            f"machine_id_sha256 must be lowercase hex 64 chars (got {len(v)} chars). "
            "Provide SHA256 of /etc/machine-id, NOT the raw machine-id."
        )
    return v


def _parse_iso8601(value: str, field: str) -> datetime:
    """Parse ISO8601, accepting trailing Z for UTC."""
    if not isinstance(value, str) or not value.strip():
        raise WizardError(f"{field} must be a non-empty ISO8601 string")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise WizardError(f"{field} must be ISO8601 (e.g. 2026-05-01T03:00:00-07:00); got {value!r}") from exc


def derive_delete_after(collection_completed_at: str, raw_retention_days: int) -> str:
    """delete_after = collection_completed_at + raw_retention_days (preserves tz offset)."""
    dt = _parse_iso8601(collection_completed_at, "collection_completed_at")
    if not isinstance(raw_retention_days, int) or raw_retention_days < 1:
        raise WizardError("raw_retention_days must be a positive integer")
    return (dt + timedelta(days=raw_retention_days)).isoformat()


def infer_role_extensions(role: str) -> list[str]:
    """Map preset role → bundled extension list. Custom roles return []."""
    return list(PRESET_ROLE_EXTENSIONS.get(role, []))


def derive_source_confidence(
    *,
    connection_mode: str,
    authenticity_level: str,
    collected_by: str,
    approved_by: str,
) -> tuple[str, str]:
    """Derive (source_confidence, reason) using §2.3 of SKILL.md.

    high:   ssh_direct + manifest verified + collected_by == approved_by (self-review)
    medium: ssh_direct (other-collected) OR offline with external_channel/signed
    low:    offline + attestation_only (or unknown auth)
    """
    same_actor = bool(collected_by) and bool(approved_by) and collected_by.strip() == approved_by.strip()

    if connection_mode == "ssh_direct" and same_actor:
        return (
            "high",
            "SSH 直接接続 + 立会者承認 + manifest 検証済 + 採取者本人がレビュー実施",
        )
    if connection_mode == "ssh_direct":
        return (
            "medium",
            "SSH 直接接続だが採取者と立会者が異なる",
        )
    if authenticity_level in {"external_channel", "gpg_signed", "ssh_signed"}:
        return (
            "medium",
            f"offline_evidence + {authenticity_level} による認証性確認",
        )
    return (
        "low",
        "offline_evidence + attestation_only（自己申告のみ）",
    )


# ---------------------------------------------------------------------------
# Build pipeline
# ---------------------------------------------------------------------------


def _check_hard_fail(target: dict) -> None:
    os_family = str(target.get("os_family", "")).lower()
    web_server = str(target.get("web_server", "")).lower()
    if os_family in HARD_FAIL_OS:
        raise HardFailError(
            f"os_family={os_family} は v1 で未対応 (hard fail)。 v2 計画に含めるか、別の対象に切り替えてください。"
        )
    if web_server in HARD_FAIL_WEB:
        raise HardFailError(
            f"web_server={web_server} は v1 で未対応 (hard fail)。"
            " v2 計画に含めるか、別の Web サーバ対象に切り替えてください。"
        )


def _validate_review_id(value: str) -> str:
    if not isinstance(value, str) or not REVIEW_ID_RE.match(value):
        raise WizardError(
            f"review_id must match <PROJECT>-REVIEW-YYYY-MMDD-NN (e.g. ACME-REVIEW-2026-0501-01); got {value!r}"
        )
    return value


def _build_target(answers_target: dict) -> dict:
    os_family = str(answers_target.get("os_family", "")).lower()
    if os_family not in VALID_OS_FAMILY:
        raise WizardError(f"target.os_family must be one of {sorted(VALID_OS_FAMILY)}; got {os_family!r}")
    web_server = str(answers_target.get("web_server", "")).lower()
    if web_server not in VALID_WEB_SERVER:
        raise WizardError(f"target.web_server must be one of {sorted(VALID_WEB_SERVER)}; got {web_server!r}")

    fp_in = answers_target.get("host_fingerprint", {}) or {}
    machine_id = validate_machine_id_sha256(fp_in.get("machine_id_sha256", ""))

    primary_ipv4 = str(fp_in.get("primary_ipv4", "")).strip()
    ssh_host_key = str(fp_in.get("ssh_host_key_sha256", "")).strip()
    timezone = str(fp_in.get("timezone", "")).strip()
    for name, val in (
        ("primary_ipv4", primary_ipv4),
        ("ssh_host_key_sha256", ssh_host_key),
        ("timezone", timezone),
    ):
        if not val:
            raise WizardError(f"target.host_fingerprint.{name} is required")

    hostname = str(answers_target.get("hostname", "")).strip()
    if not hostname:
        raise WizardError("target.hostname is required")
    os_version = str(answers_target.get("os_version", "")).strip()
    if not os_version:
        raise WizardError("target.os_version is required")

    role = str(answers_target.get("role", "")).strip()
    if not role:
        raise WizardError("target.role is required")

    # Stage 1 may return the placeholder "custom"; the actual role string
    # then arrives in target.custom_role. Substitute and validate.
    if role.lower() == "custom":
        custom_role = str(answers_target.get("custom_role", "") or "").strip()
        if not custom_role:
            raise WizardError(
                "target.custom_role is required when target.role='custom' "
                "(provide the actual role string, e.g. 'api_gateway')"
            )
        if custom_role.lower() == "custom":
            raise WizardError("target.custom_role cannot itself be 'custom'; provide the actual role string")
        role = custom_role

    return {
        "hostname": hostname,
        "fqdn": str(answers_target.get("fqdn", "") or ""),
        "role": role,
        "os_family": os_family,
        "os_version": os_version,
        "web_server": web_server,
        "app_runtime": str(answers_target.get("app_runtime", "") or "none"),
        "host_fingerprint": {
            "machine_id": machine_id,
            "primary_ipv4": primary_ipv4,
            "ssh_host_key_sha256": ssh_host_key,
            "timezone": timezone,
        },
    }


def _build_ssh(connection_mode: str, ssh_in: dict | None) -> dict | None:
    if connection_mode != "ssh_direct":
        return None
    if not ssh_in:
        raise WizardError("ssh block is required when connection_mode=ssh_direct")
    required = ("user", "approved_by", "approved_at")
    for key in required:
        if not ssh_in.get(key):
            raise WizardError(f"ssh.{key} is required when connection_mode=ssh_direct")
    _parse_iso8601(ssh_in["approved_at"], "ssh.approved_at")
    return {
        "bastion": normalize_optional_null(ssh_in.get("bastion")),
        "user": str(ssh_in["user"]).strip(),
        "approved_by": str(ssh_in["approved_by"]).strip(),
        "approved_at": str(ssh_in["approved_at"]).strip(),
    }


def _build_evidence(evidence_in: dict, connection_mode: str) -> dict:
    completed_at = evidence_in.get("collection_completed_at")
    if not completed_at:
        raise WizardError("evidence.collection_completed_at is required")
    _parse_iso8601(completed_at, "evidence.collection_completed_at")

    started_at = evidence_in.get("collection_started_at") or completed_at
    _parse_iso8601(started_at, "evidence.collection_started_at")

    authenticity = str(evidence_in.get("authenticity_level", "")).strip()
    if authenticity not in VALID_AUTHENTICITY:
        raise WizardError(
            f"evidence.authenticity_level must be one of {sorted(VALID_AUTHENTICITY)}; got {authenticity!r}"
        )

    collected_by = str(evidence_in.get("collected_by", "")).strip()
    if not collected_by:
        raise WizardError("evidence.collected_by is required")

    explicit_conf = evidence_in.get("source_confidence")
    if explicit_conf:
        if explicit_conf not in VALID_SOURCE_CONFIDENCE:
            raise WizardError(f"evidence.source_confidence must be one of {sorted(VALID_SOURCE_CONFIDENCE)}")
        confidence = explicit_conf
        reason = str(evidence_in.get("source_confidence_reason", "")).strip() or "manual override (no derivation)"
    else:
        confidence, reason = derive_source_confidence(
            connection_mode=connection_mode,
            authenticity_level=authenticity,
            collected_by=collected_by,
            approved_by=evidence_in.get("approved_by", "") or "",
        )

    masking = evidence_in.get("masking_at_collection")
    if masking is None:
        masking = True

    evidence_dir = str(evidence_in.get("evidence_dir", "")).strip()
    raw_store = str(evidence_in.get("raw_evidence_store", "")).strip()
    if not evidence_dir:
        raise WizardError("evidence.evidence_dir is required")
    if not raw_store:
        raise WizardError("evidence.raw_evidence_store is required")

    return {
        "collected_by": collected_by,
        "collection_started_at": started_at,
        "collection_completed_at": completed_at,
        "evidence_dir": evidence_dir,
        "raw_evidence_store": raw_store,
        "authenticity_level": authenticity,
        "source_confidence": confidence,
        "source_confidence_reason": reason,
        "masking_at_collection": bool(masking),
    }


def _build_scope(scope_in: dict, role: str) -> dict:
    axes = scope_in.get("axes_in_scope") or list(ALL_AXES)
    if isinstance(axes, str):
        axes = normalize_csv(axes)
    invalid = [a for a in axes if a not in ALL_AXES]
    if invalid:
        raise WizardError(f"scope.axes_in_scope contains invalid axes: {invalid}")

    explicit_exts = scope_in.get("role_extensions")
    if explicit_exts:
        role_extensions = explicit_exts if isinstance(explicit_exts, list) else normalize_csv(explicit_exts)
    else:
        role_extensions = infer_role_extensions(role)

    return {
        "axes_in_scope": list(axes),
        "role_extensions": list(role_extensions),
        "out_of_scope": normalize_csv(scope_in.get("out_of_scope")),
    }


def _build_incident(incident_in: dict) -> dict:
    active = bool(incident_in.get("active_incident", False))
    incident_id = str(incident_in.get("incident_id", "") or "").strip()
    summary = str(incident_in.get("incident_summary", "") or "").strip()
    if active and not incident_id:
        raise WizardError("incident_context.incident_id is required when active_incident=true")
    if active and not summary:
        raise WizardError("incident_context.incident_summary is required when active_incident=true")
    return {
        "active_incident": active,
        "incident_id": incident_id,
        "incident_summary": summary,
    }


def _build_retention(retention_in: dict, completed_at: str) -> dict:
    days = retention_in.get("raw_retention_days", 90)
    if not isinstance(days, int):
        try:
            days = int(days)
        except (TypeError, ValueError) as exc:
            raise WizardError("retention.raw_retention_days must be an integer") from exc
    if days < 1:
        raise WizardError("retention.raw_retention_days must be a positive integer")

    owner = str(retention_in.get("owner", "")).strip()
    if not owner:
        raise WizardError("retention.owner is required")

    approvers = normalize_csv(retention_in.get("access_approvers"))
    if not approvers:
        raise WizardError("retention.access_approvers must contain at least one entry")

    rotation = normalize_csv(retention_in.get("rotation_dependencies"))

    early = retention_in.get("early_deletion_conditions")
    early_list = normalize_csv(early) if early else list(DEFAULT_EARLY_DELETION_CONDITIONS)

    return {
        "raw_retention_days": days,
        "owner": owner,
        "delete_after": derive_delete_after(completed_at, days),
        "access_approvers": approvers,
        "rotation_dependencies": rotation,
        "early_deletion_conditions": early_list,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_profile(answers: dict) -> dict:
    """Build a target_profile dict from wizard answers.

    Order matters: hard-fail gates fire BEFORE any other validation so that
    unsupported configurations abort early without partial work.
    """
    target_in = answers.get("target", {}) or {}
    _check_hard_fail(target_in)

    review_id = _validate_review_id(answers.get("review_id", ""))

    connection_mode = str(answers.get("connection_mode", "")).strip()
    if connection_mode not in VALID_CONNECTION_MODE:
        raise WizardError(f"connection_mode must be one of {sorted(VALID_CONNECTION_MODE)}; got {connection_mode!r}")

    target = _build_target(target_in)
    ssh = _build_ssh(connection_mode, answers.get("ssh"))
    evidence_in = dict(answers.get("evidence") or {})
    if ssh and "approved_by" not in evidence_in:
        evidence_in["approved_by"] = ssh["approved_by"]
    evidence = _build_evidence(evidence_in, connection_mode)
    scope = _build_scope(answers.get("scope") or {}, target["role"])
    incident = _build_incident(answers.get("incident_context") or {})
    retention = _build_retention(
        answers.get("retention") or {},
        evidence["collection_completed_at"],
    )

    profile: dict = {
        "review_id": review_id,
        "target": target,
        "connection_mode": connection_mode,
        "ssh": ssh,
        "evidence": evidence,
        "scope": scope,
        "incident_context": incident,
        "retention": retention,
        "exceptional_approvals": list(answers.get("exceptional_approvals") or []),
    }
    return profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build target_profile.yaml from wizard answers JSON.")
    parser.add_argument(
        "answers_positional",
        nargs="?",
        help="Path to wizard_answers.json (positional, optional alias for --answers).",
    )
    parser.add_argument(
        "--answers",
        "-a",
        dest="answers_path",
        help="Path to wizard_answers.json.",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output path for target_profile.yaml.",
    )
    args = parser.parse_args(argv)

    answers_path = args.answers_path or args.answers_positional
    if not answers_path:
        parser.error("either --answers/-a or a positional answers path is required")

    try:
        answers = json.loads(Path(answers_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: failed to read answers JSON: {exc}", file=sys.stderr)
        return 2

    try:
        profile = build_profile(answers)
    except HardFailError as exc:
        print(f"HARD FAIL: {exc}", file=sys.stderr)
        return 3
    except WizardError as exc:
        print(f"VALIDATION ERROR: {exc}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        yaml.safe_dump(profile, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
    print(f"Wrote {out_path} (review_id={profile['review_id']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
