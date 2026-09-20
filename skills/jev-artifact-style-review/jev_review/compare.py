"""Conservative comparison: a lower style index never independently approves a rewrite."""

from __future__ import annotations

from .common import ReviewError, digest


def compare_reports(before: dict, after: dict) -> dict:
    for r in [before, after]:
        if r.get("schema_version") != "1.0.0" or "summary" not in r or "configuration" not in r:
            raise ReviewError("Unsupported or incomplete review report.")
    reasons = []
    if any(r.get("comparison_fingerprint") != digest(r["configuration"]) for r in [before, after]):
        reasons.append("stored_configuration_fingerprint_mismatch")
    if before.get("mode") != "jev_live" or after.get("mode") != "jev_live":
        reasons.append("non_live_or_fixture_results")
    if before.get("comparison_fingerprint") != after.get("comparison_fingerprint"):
        reasons.append("model_context_profile_language_rubric_or_extraction_configuration_changed")
    b = before["summary"]["style_index_0_to_100"]
    a = after["summary"]["style_index_0_to_100"]
    if a is None or b is None:
        reasons.append("one_or_both_indices_withheld")
    for key in ["span_confidence_coverage", "dimension_weight_coverage"]:
        if abs(before["summary"][key] - after["summary"][key]) > 0.10:
            reasons.append(key + "_changed_materially")
    bset = {d["id"] for d in before["dimensions"] if d["group"] == "style" and d["status"] == "assessed"}
    aset = {d["id"] for d in after["dimensions"] if d["group"] == "style" and d["status"] == "assessed"}
    if bset != aset:
        reasons.append("assessed_style_dimension_set_changed")
    threshold = after["configuration"]["thresholds"]["meaningful_delta"]
    delta = round(a - b, 1) if not reasons else None
    direction = (
        "not_comparable"
        if reasons
        else (
            "lower_style_friction"
            if delta <= -threshold
            else ("higher_style_friction" if delta >= threshold else "no_meaningful_change")
        )
    )
    warnings = []
    for field in ["numeric_tokens", "urls"]:
        if before["surface_metrics"][field] != after["surface_metrics"][field]:
            warnings.append(field + "_changed; verify against source, not automatically an error")
    if after["preservation_checks"]["missing_literals"]:
        warnings.append("required_protected_literal_missing")
    if after["surface_metrics"]["possible_embedded_evaluator_instruction"]:
        warnings.append("possible_prompt_injection")
    bd = {d["id"]: d for d in before["dimensions"]}
    quality_regressions = []
    for d in after["dimensions"]:
        previous = bd.get(d["id"])
        if d["group"] == "quality" and previous and d["status"] == previous["status"] == "assessed":
            bv = previous["severity_0_to_4"]
            av = d["severity_0_to_4"]
            if av is not None and bv is not None and av - bv >= 0.5:
                quality_regressions.append(d["id"])
    if quality_regressions:
        warnings.append("content_quality_regression_candidates")
    return {
        "schema_version": "1.0.0",
        "direction": direction,
        "before_index": b,
        "after_index": a,
        "delta_after_minus_before": delta,
        "comparability_reasons": reasons,
        "preservation_warnings": warnings,
        "quality_regression_candidates": quality_regressions,
        "source_hash_before": before["document"]["sha256"],
        "source_hash_after": after["document"]["sha256"],
        "release_approval": False,
        "semantic_preservation_verified": False,
        "decision": "Independent fact, meaning and requirements review required, even when style friction is lower.",
        "threshold_status": "provisional, not empirically calibrated",
    }
