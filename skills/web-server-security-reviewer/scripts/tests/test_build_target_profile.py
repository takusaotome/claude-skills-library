"""Tests for build_target_profile.py.

Validates the wizard-answers → target_profile.yaml pipeline:
- hard-fail gates (windows / iis)
- machine_id_sha256 raw-value rejection
- collection_completed_at required + collection_started_at default
- delete_after derivation
- enum validation
- defaults: axes_in_scope, role_extensions inference, masking_at_collection
- conditional required: ssh block when ssh_direct, incident fields when active
- CSV normalization for array fields
- source_confidence derivation
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from build_target_profile import (  # noqa: E402
    HardFailError,
    WizardError,
    build_profile,
    derive_delete_after,
    derive_source_confidence,
    infer_role_extensions,
    main,
    normalize_csv,
    validate_machine_id_sha256,
)

# ---------- Minimal valid wizard answers fixture ----------

MINIMAL_ANSWERS: dict = {
    "review_id": "ACME-REVIEW-2026-0501-01",
    "target": {
        "hostname": "web01",
        "fqdn": "web01.example.com",
        "role": "public_facing",
        "os_family": "rhel",
        "os_version": "Rocky Linux 9.5",
        "web_server": "nginx",
        "app_runtime": "nodejs-v20.10.0",
        "host_fingerprint": {
            "machine_id_sha256": "a" * 64,
            "primary_ipv4": "10.0.0.10",
            "ssh_host_key_sha256": "SHA256:abc123",
            "timezone": "America/Los_Angeles",
        },
    },
    "connection_mode": "ssh_direct",
    "ssh": {
        "bastion": "bastion01.example.com",
        "user": "ro_auditor",
        "approved_by": "Alice Witness",
        "approved_at": "2026-04-30T21:00:00-07:00",
    },
    "evidence": {
        "collected_by": "Alice Witness",
        "collection_completed_at": "2026-05-01T03:00:00-07:00",
        "evidence_dir": "./review_acme/evidence/",
        "raw_evidence_store": "s3://acme-security/raw/acme-review-2026-0501-01/",
        "authenticity_level": "external_channel",
    },
    "scope": {
        "out_of_scope": "Phase 2 コードレビュー, ペネトレーションテスト",
    },
    "incident_context": {
        "active_incident": False,
    },
    "retention": {
        "raw_retention_days": 90,
        "owner": "Bob Owner",
        "access_approvers": "Alice Witness, Carol SecretOwner",
        "rotation_dependencies": "VPN 認証情報ローテーション完了確認, DB 認証情報ローテーション完了確認",
    },
}


def _answers(**overrides) -> dict:
    """Deep-merge overrides onto MINIMAL_ANSWERS."""
    import copy

    base = copy.deepcopy(MINIMAL_ANSWERS)

    def merge(dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                merge(dst[k], v)
            else:
                dst[k] = v

    merge(base, overrides)
    return base


# ---------- Hard-fail gates ----------


class TestHardFail:
    def test_windows_hard_fails(self):
        with pytest.raises(HardFailError, match="windows"):
            build_profile(_answers(target={"os_family": "windows"}))

    def test_iis_hard_fails(self):
        with pytest.raises(HardFailError, match="iis"):
            build_profile(_answers(target={"web_server": "iis"}))

    def test_rhel_nginx_passes(self):
        profile = build_profile(_answers())
        assert profile["target"]["os_family"] == "rhel"
        assert profile["target"]["web_server"] == "nginx"

    def test_debian_apache_passes(self):
        profile = build_profile(_answers(target={"os_family": "debian", "web_server": "apache"}))
        assert profile["target"]["os_family"] == "debian"


# ---------- machine_id validation ----------


class TestMachineId:
    def test_rejects_raw_machine_id(self):
        # raw machine-id is typically 32 hex chars (no SHA256 prefix), or contains uppercase
        with pytest.raises(WizardError, match="64 chars"):
            validate_machine_id_sha256("abcd1234abcd1234abcd1234abcd1234")  # 32 chars

    def test_rejects_uppercase(self):
        with pytest.raises(WizardError, match="lowercase hex"):
            validate_machine_id_sha256("A" * 64)

    def test_rejects_non_hex(self):
        with pytest.raises(WizardError, match="lowercase hex"):
            validate_machine_id_sha256("z" * 64)

    def test_accepts_valid_sha256(self):
        valid = "a1b2c3d4e5f6" + "0" * 52
        assert validate_machine_id_sha256(valid) == valid

    def test_normalizes_whitespace(self):
        valid = "f" * 64
        assert validate_machine_id_sha256(f"  {valid}  ") == valid

    def test_build_profile_propagates_machine_id_error(self):
        with pytest.raises(WizardError):
            build_profile(_answers(target={"host_fingerprint": {"machine_id_sha256": "tooshort"}}))


# ---------- collection_*_at handling ----------


class TestCollectionTimestamps:
    def test_completed_at_required(self):
        bad = _answers()
        del bad["evidence"]["collection_completed_at"]
        with pytest.raises(WizardError, match="collection_completed_at"):
            build_profile(bad)

    def test_started_at_defaults_to_completed_at(self):
        profile = build_profile(_answers())
        assert profile["evidence"]["collection_started_at"] == profile["evidence"]["collection_completed_at"]

    def test_started_at_explicit_preserved(self):
        profile = build_profile(
            _answers(
                evidence={
                    "collection_started_at": "2026-05-01T02:00:00-07:00",
                    "collection_completed_at": "2026-05-01T03:00:00-07:00",
                }
            )
        )
        assert profile["evidence"]["collection_started_at"] == "2026-05-01T02:00:00-07:00"
        assert profile["evidence"]["collection_completed_at"] == "2026-05-01T03:00:00-07:00"

    def test_invalid_iso8601_rejected(self):
        with pytest.raises(WizardError, match="ISO8601"):
            build_profile(_answers(evidence={"collection_completed_at": "yesterday"}))


# ---------- delete_after derivation ----------


class TestDeleteAfter:
    def test_delete_after_basic(self):
        # 2026-05-01T03:00:00-07:00 + 90 days = 2026-07-30T03:00:00-07:00
        result = derive_delete_after("2026-05-01T03:00:00-07:00", 90)
        assert result == "2026-07-30T03:00:00-07:00"

    def test_delete_after_30_days(self):
        result = derive_delete_after("2026-05-01T03:00:00-07:00", 30)
        assert result == "2026-05-31T03:00:00-07:00"

    def test_delete_after_zulu_time(self):
        result = derive_delete_after("2026-05-01T10:00:00Z", 7)
        assert result == "2026-05-08T10:00:00+00:00"

    def test_delete_after_in_profile(self):
        profile = build_profile(_answers())
        assert profile["retention"]["delete_after"] == "2026-07-30T03:00:00-07:00"


# ---------- Defaults ----------


class TestDefaults:
    def test_axes_default_full(self):
        profile = build_profile(_answers())
        assert profile["scope"]["axes_in_scope"] == ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]

    def test_axes_explicit_preserved(self):
        profile = build_profile(_answers(scope={"axes_in_scope": ["A1", "A4"]}))
        assert profile["scope"]["axes_in_scope"] == ["A1", "A4"]

    def test_masking_at_collection_defaults_true(self):
        profile = build_profile(_answers())
        assert profile["evidence"]["masking_at_collection"] is True

    def test_exceptional_approvals_defaults_empty_list(self):
        profile = build_profile(_answers())
        assert profile["exceptional_approvals"] == []

    def test_early_deletion_conditions_default_provided(self):
        profile = build_profile(_answers())
        assert isinstance(profile["retention"]["early_deletion_conditions"], list)
        assert len(profile["retention"]["early_deletion_conditions"]) >= 1

    def test_app_runtime_defaults_to_none(self):
        ans = _answers()
        del ans["target"]["app_runtime"]
        profile = build_profile(ans)
        assert profile["target"]["app_runtime"] == "none"


# ---------- bastion normalization ----------


class TestBastionNormalization:
    @pytest.mark.parametrize("null_equiv", ["", "none", "None", "NONE", "null", "なし", "n/a", "N/A"])
    def test_null_equivalents_become_none(self, null_equiv):
        profile = build_profile(_answers(ssh={"bastion": null_equiv}))
        assert profile["ssh"]["bastion"] is None

    def test_real_bastion_preserved(self):
        profile = build_profile(_answers(ssh={"bastion": "bastion01.example.com"}))
        assert profile["ssh"]["bastion"] == "bastion01.example.com"

    def test_bastion_strips_whitespace(self):
        profile = build_profile(_answers(ssh={"bastion": "  bastion01  "}))
        assert profile["ssh"]["bastion"] == "bastion01"

    def test_explicit_python_none(self):
        profile = build_profile(_answers(ssh={"bastion": None}))
        assert profile["ssh"]["bastion"] is None


# ---------- custom role handling ----------


class TestCustomRole:
    def test_custom_role_requires_custom_role_string(self):
        # role="custom" alone is a placeholder, not a real role name
        with pytest.raises(WizardError, match="custom_role"):
            build_profile(_answers(target={"role": "custom"}))

    def test_custom_role_substituted_when_provided(self):
        profile = build_profile(_answers(target={"role": "custom", "custom_role": "api_gateway"}))
        assert profile["target"]["role"] == "api_gateway"

    def test_custom_role_extensions_inference_returns_empty(self):
        # api_gateway is not a preset → role_extensions empty unless explicitly given
        profile = build_profile(_answers(target={"role": "custom", "custom_role": "api_gateway"}))
        assert profile["scope"]["role_extensions"] == []

    def test_custom_role_with_explicit_extensions(self):
        profile = build_profile(
            _answers(
                target={"role": "custom", "custom_role": "api_gateway"},
                scope={"role_extensions": ["custom_api_gw"]},
            )
        )
        assert profile["scope"]["role_extensions"] == ["custom_api_gw"]

    def test_custom_role_empty_string_rejected(self):
        with pytest.raises(WizardError, match="custom_role"):
            build_profile(_answers(target={"role": "custom", "custom_role": "  "}))


# ---------- role_extensions inference ----------


class TestRoleExtensions:
    def test_public_facing_inferred(self):
        assert infer_role_extensions("public_facing") == ["generic_public_facing"]

    def test_internal_inferred(self):
        assert infer_role_extensions("internal") == ["generic_internal"]

    def test_edge_inferred(self):
        assert infer_role_extensions("edge") == ["generic_edge"]

    def test_custom_role_no_inference(self):
        # custom roles must be explicit; inference returns empty
        assert infer_role_extensions("api_gw") == []

    def test_explicit_extensions_preserved(self):
        profile = build_profile(_answers(scope={"role_extensions": ["custom_my_ext"]}))
        assert profile["scope"]["role_extensions"] == ["custom_my_ext"]

    def test_inferred_when_missing(self):
        profile = build_profile(_answers())
        assert profile["scope"]["role_extensions"] == ["generic_public_facing"]


# ---------- source_confidence derivation ----------


class TestSourceConfidence:
    def test_ssh_direct_self_collected_high(self):
        # ssh_direct + same person collected & approved + external_channel
        conf, reason = derive_source_confidence(
            connection_mode="ssh_direct",
            authenticity_level="external_channel",
            collected_by="Alice",
            approved_by="Alice",
        )
        assert conf == "high"
        assert "ssh" in reason.lower() or "SSH" in reason

    def test_ssh_direct_other_collected_medium(self):
        conf, _ = derive_source_confidence(
            connection_mode="ssh_direct",
            authenticity_level="external_channel",
            collected_by="Bob",
            approved_by="Alice",
        )
        assert conf == "medium"

    def test_offline_attestation_only_low(self):
        conf, _ = derive_source_confidence(
            connection_mode="offline_evidence",
            authenticity_level="attestation_only",
            collected_by="Bob",
            approved_by="",
        )
        assert conf == "low"

    def test_offline_external_channel_medium(self):
        conf, _ = derive_source_confidence(
            connection_mode="offline_evidence",
            authenticity_level="external_channel",
            collected_by="Bob",
            approved_by="Alice",
        )
        assert conf == "medium"

    def test_explicit_overrides_derivation(self):
        profile = build_profile(
            _answers(evidence={"source_confidence": "low", "source_confidence_reason": "manual override"})
        )
        assert profile["evidence"]["source_confidence"] == "low"
        assert profile["evidence"]["source_confidence_reason"] == "manual override"


# ---------- SSH conditional requirements ----------


class TestSshConditional:
    def test_ssh_required_when_ssh_direct(self):
        ans = _answers()
        del ans["ssh"]
        with pytest.raises(WizardError, match="ssh"):
            build_profile(ans)

    def test_ssh_approval_fields_required(self):
        ans = _answers()
        del ans["ssh"]["approved_by"]
        with pytest.raises(WizardError, match="approved_by"):
            build_profile(ans)

    def test_ssh_omitted_when_offline(self):
        ans = _answers(connection_mode="offline_evidence")
        del ans["ssh"]
        profile = build_profile(ans)
        assert profile["connection_mode"] == "offline_evidence"
        # ssh block may be absent or null in offline mode
        assert profile.get("ssh") in (None, {})


# ---------- Incident conditional requirements ----------


class TestIncidentConditional:
    def test_incident_id_required_when_active(self):
        ans = _answers(incident_context={"active_incident": True})
        with pytest.raises(WizardError, match="incident_id"):
            build_profile(ans)

    def test_incident_summary_required_when_active(self):
        ans = _answers(incident_context={"active_incident": True, "incident_id": "INC-123"})
        with pytest.raises(WizardError, match="incident_summary"):
            build_profile(ans)

    def test_inactive_incident_passes_with_empty(self):
        profile = build_profile(_answers())
        assert profile["incident_context"]["active_incident"] is False
        assert profile["incident_context"]["incident_id"] == ""
        assert profile["incident_context"]["incident_summary"] == ""


# ---------- CSV / array normalization ----------


class TestCsvNormalization:
    def test_normalize_simple_csv(self):
        assert normalize_csv("alice, bob, carol") == ["alice", "bob", "carol"]

    def test_normalize_handles_extra_whitespace(self):
        assert normalize_csv("  alice  ,  bob  ") == ["alice", "bob"]

    def test_normalize_strips_empty_segments(self):
        assert normalize_csv("alice,, ,bob,") == ["alice", "bob"]

    def test_normalize_empty_returns_empty(self):
        assert normalize_csv("") == []
        assert normalize_csv(None) == []

    def test_normalize_passthrough_list(self):
        assert normalize_csv(["x", "y"]) == ["x", "y"]

    def test_access_approvers_normalized(self):
        profile = build_profile(_answers())
        assert profile["retention"]["access_approvers"] == ["Alice Witness", "Carol SecretOwner"]

    def test_out_of_scope_normalized(self):
        profile = build_profile(_answers())
        assert "Phase 2 コードレビュー" in profile["scope"]["out_of_scope"]
        assert "ペネトレーションテスト" in profile["scope"]["out_of_scope"]

    def test_rotation_dependencies_normalized(self):
        profile = build_profile(_answers())
        assert len(profile["retention"]["rotation_dependencies"]) == 2


# ---------- Enum validation ----------


class TestEnumValidation:
    def test_invalid_role_allowed_as_custom_string(self):
        # custom role strings allowed
        profile = build_profile(_answers(target={"role": "api_gw"}))
        assert profile["target"]["role"] == "api_gw"

    def test_invalid_os_family_rejected(self):
        with pytest.raises(WizardError, match="os_family"):
            build_profile(_answers(target={"os_family": "alpine"}))

    def test_invalid_web_server_rejected(self):
        with pytest.raises(WizardError, match="web_server"):
            build_profile(_answers(target={"web_server": "caddy"}))

    def test_invalid_connection_mode_rejected(self):
        with pytest.raises(WizardError, match="connection_mode"):
            build_profile(_answers(connection_mode="rsync"))

    def test_invalid_authenticity_level_rejected(self):
        with pytest.raises(WizardError, match="authenticity_level"):
            build_profile(_answers(evidence={"authenticity_level": "trust_me"}))


# ---------- review_id format validation ----------


class TestReviewId:
    def test_invalid_review_id_format_rejected(self):
        with pytest.raises(WizardError, match="review_id"):
            build_profile(_answers(review_id="not-a-valid-id"))

    def test_valid_review_id_accepted(self):
        profile = build_profile(_answers(review_id="PROJX-REVIEW-2026-0501-03"))
        assert profile["review_id"] == "PROJX-REVIEW-2026-0501-03"


# ---------- Output structure matches input_contract ----------


class TestOutputStructure:
    def test_top_level_keys_present(self):
        profile = build_profile(_answers())
        for key in (
            "review_id",
            "target",
            "connection_mode",
            "ssh",
            "evidence",
            "scope",
            "incident_context",
            "retention",
            "exceptional_approvals",
        ):
            assert key in profile, f"missing top-level key: {key}"

    def test_yaml_serializable(self):
        profile = build_profile(_answers())
        text = yaml.safe_dump(profile, allow_unicode=True, sort_keys=False)
        roundtrip = yaml.safe_load(text)
        assert roundtrip["review_id"] == profile["review_id"]


# ---------- main() CLI ----------


class TestMainCli:
    def test_main_writes_yaml(self, tmp_path):
        answers_path = tmp_path / "answers.json"
        out_path = tmp_path / "target_profile.yaml"
        answers_path.write_text(json.dumps(MINIMAL_ANSWERS), encoding="utf-8")

        rc = main(["--answers", str(answers_path), "--output", str(out_path)])
        assert rc == 0
        assert out_path.exists()
        loaded = yaml.safe_load(out_path.read_text(encoding="utf-8"))
        assert loaded["review_id"] == "ACME-REVIEW-2026-0501-01"

    def test_main_hard_fail_returns_nonzero(self, tmp_path):
        answers_path = tmp_path / "answers.json"
        out_path = tmp_path / "target_profile.yaml"
        bad = _answers(target={"os_family": "windows"})
        answers_path.write_text(json.dumps(bad), encoding="utf-8")

        rc = main(["--answers", str(answers_path), "--output", str(out_path)])
        assert rc != 0
        assert not out_path.exists()

    def test_main_wizard_error_returns_nonzero(self, tmp_path):
        answers_path = tmp_path / "answers.json"
        out_path = tmp_path / "target_profile.yaml"
        bad = _answers()
        del bad["evidence"]["collection_completed_at"]
        answers_path.write_text(json.dumps(bad), encoding="utf-8")

        rc = main(["--answers", str(answers_path), "--output", str(out_path)])
        assert rc != 0

    def test_main_positional_answers_path(self, tmp_path):
        """Support `build_target_profile.py wizard_answers.json --output ...` form."""
        answers_path = tmp_path / "answers.json"
        out_path = tmp_path / "target_profile.yaml"
        answers_path.write_text(json.dumps(MINIMAL_ANSWERS), encoding="utf-8")

        rc = main([str(answers_path), "--output", str(out_path)])
        assert rc == 0
        assert out_path.exists()
