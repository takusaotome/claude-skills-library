"""Two-pass review: independent ordinal judgments, then bounded evidence selection."""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from .common import ReviewError, digest
from .extract import make_chunks
from .metrics import protected_checks, surface_metrics
from .questions import active_dimensions, check_request_budget, evidence_questions, questions_for, state_for

PIPELINE_VERSION = "1.0.0"


def build_plan(
    document: dict,
    context: dict,
    rubric: dict,
    *,
    profile="email",
    language="ja",
    model="jev-1.13.0",
    chunk_chars=2600,
    max_chunks=128,
    top_k=5,
    max_requests=150,
    workers=2,
) -> dict:
    if profile not in rubric["profiles"]:
        raise ReviewError("Unknown document profile.")
    if language not in {"ja", "en", "mixed"}:
        raise ReviewError("Language must be ja, en or mixed.")
    if not 500 <= chunk_chars <= 5000:
        raise ReviewError("--chunk-chars must be between 500 and 5000.")
    if not 1 <= top_k <= 8:
        raise ReviewError("--top-k must be 1 through 8.")
    if not 1 <= workers <= 4:
        raise ReviewError("--workers must be 1 through 4.")
    chunks = make_chunks(document, chunk_chars, max_chunks)
    dimensions, skipped = active_dimensions(rubric, profile, context)
    q = questions_for(dimensions, rubric)
    payloads = []
    for chunk in chunks:
        payload = {
            "model": model,
            "state": state_for(chunk, len(chunks), context, language, profile, rubric),
            "questions": q,
        }
        check_request_budget(payload)
        payloads.append(payload)
    upper_bound = len(chunks) + min(top_k, len(chunks))
    if upper_bound > max_requests:
        raise ReviewError(
            f"Planned upper bound is {upper_bound} logical API calls, above --max-requests {max_requests}. Nothing sent."
        )
    configuration = {
        "profile": profile,
        "language": language,
        "requested_model": model,
        "chunk_chars": chunk_chars,
        "top_k": top_k,
        "rubric_version": rubric["version"],
        "rubric_sha256": digest(rubric),
        "context_sha256": digest(context),
        "extractor_version": document["extractor_version"],
        "pipeline_version": PIPELINE_VERSION,
        "thresholds": rubric["thresholds"],
        "extraction_scope": document["scope"],
    }
    return {
        "chunks": chunks,
        "dimensions": dimensions,
        "skipped_dimensions": skipped,
        "payloads": payloads,
        "configuration": configuration,
        "workers": workers,
        "planned_calls_upper_bound": upper_bound,
        "max_http_attempts_upper_bound": 3 * upper_bound,
        "evaluated_characters": sum(c["chars"] for c in chunks),
    }


def _aggregate(document: dict, plan: dict, responses: list[dict], rubric: dict) -> tuple[list[dict], dict, list[dict]]:
    t = rubric["thresholds"]
    dimrows = []
    candidates = []
    for dim in plan["dimensions"]:
        rows = []
        for chunk, response in zip(plan["chunks"], responses):
            app = response["answers"]["app__" + dim["id"]]
            sev = response["answers"]["sev__" + dim["id"]]
            confident_app = app["confidence"] >= t["applicability_confidence"]
            if confident_app and app["choice"] == "not_applicable":
                status = "not_applicable"
            elif confident_app and app["choice"] == "assessable" and sev["confidence"] >= t["score_confidence"]:
                status = "assessed"
            else:
                status = "uncertain"
            rows.append(
                {
                    "chunk_id": chunk["id"],
                    "characters": chunk["chars"],
                    "status": status,
                    "applicability": app,
                    "severity": sev["score"],
                    "confidence": sev["confidence"],
                    "probability_mass_severity_3_or_4": sum(v for k, v in sev["probabilities"].items() if int(k) >= 3),
                }
            )
        denominator = sum(r["characters"] for r in rows if r["status"] != "not_applicable")
        valid = [r for r in rows if r["status"] == "assessed"]
        validchars = sum(r["characters"] for r in valid)
        coverage = validchars / denominator if denominator else None
        severity = sum(r["severity"] * r["characters"] for r in valid) / validchars if validchars else None
        avgconf = sum(r["confidence"] * r["characters"] for r in valid) / validchars if validchars else None
        item = {
            "id": dim["id"],
            "group": dim["group"],
            "label_ja": dim["label_ja"],
            "label_en": dim["label_en"],
            "effective_weight": dim["effective_weight"],
            "severity_0_to_4": round(severity, 4) if severity is not None else None,
            "coverage": round(coverage, 4) if coverage is not None else None,
            "mean_model_confidence": round(avgconf, 4) if avgconf is not None else None,
            "status": "not_applicable"
            if denominator == 0
            else ("assessed" if coverage >= t["min_coverage"] else "insufficient_coverage"),
            "chunks": rows,
        }
        dimrows.append(item)
        if valid:
            hotspot = max(valid, key=lambda r: r["severity"])
            if hotspot["severity"] >= t["finding_score"]:
                candidates.append({"dimension": dim, "row": hotspot})
    style = [d for d in dimrows if d["group"] == "style" and d["status"] != "not_applicable"]
    trusted = [d for d in style if d["status"] == "assessed" and d["severity_0_to_4"] is not None]
    totalweight = sum(d["effective_weight"] for d in style)
    trustedweight = sum(d["effective_weight"] for d in trusted)
    wcoverage = trustedweight / totalweight if totalweight else 0
    span_coverage = sum((d["coverage"] or 0) * d["effective_weight"] for d in style) / totalweight if totalweight else 0
    text = "".join(s["text"] for c in plan["chunks"] for s in c["segments"])
    # Conservative operational floor only, not a validated psychometric threshold.
    import re

    short = (
        len(re.findall(r"\S", text)) < 80
        if plan["configuration"]["language"] != "en"
        else len(re.findall(r"\b\w+\b", text)) < 35
    )
    index = None
    reasons = []
    if short:
        reasons.append("short_text_overall_index_withheld")
    if len(trusted) < t["minimum_style_dimensions"]:
        reasons.append("too_few_assessable_style_dimensions")
    if wcoverage < t["min_coverage"] or span_coverage < t["min_coverage"]:
        reasons.append("insufficient_confident_coverage")
    if any("no usable text layer" in w for w in document["warnings"]):
        reasons.append("incomplete_pdf_text_coverage")
    if not reasons and trustedweight:
        index = round(sum(d["severity_0_to_4"] * d["effective_weight"] for d in trusted) / trustedweight * 25, 1)
    summary = {
        "style_index_0_to_100": index,
        "higher_means": "more_observable_style_friction",
        "is_ai_authorship_probability": False,
        "calibration_status": rubric["calibration_status"],
        "dimension_weight_coverage": round(wcoverage, 4),
        "span_confidence_coverage": round(span_coverage, 4),
        "index_withheld_reasons": reasons,
        "quality_dimensions_excluded_from_style_index": True,
        "global_structure_scope": "chunk-level aggregation; cross-fragment coherence requires a separate review",
    }
    candidates.sort(key=lambda c: (c["row"]["severity"], c["dimension"]["group"] == "quality"), reverse=True)
    return dimrows, summary, candidates[: plan["configuration"]["top_k"]]


def execute(document: dict, context: dict, rubric: dict, plan: dict, client) -> dict:
    # Executor.map retains order so weights, source chunks and responses remain aligned.
    with ThreadPoolExecutor(max_workers=plan["workers"]) as pool:
        responses = list(pool.map(client.evaluate, plan["payloads"]))
    dims, summary, candidates = _aggregate(document, plan, responses, rubric)
    grouped = defaultdict(list)
    for candidate in candidates:
        grouped[candidate["row"]["chunk_id"]].append(candidate)
    chunks = {c["id"]: c for c in plan["chunks"]}
    evidence_records = []
    findings = []
    evidence_gaps = []
    for cid, items in grouped.items():
        chunk = chunks[cid]
        payload = {
            "model": plan["configuration"]["requested_model"],
            "state": state_for(
                chunk, len(chunks), context, plan["configuration"]["language"], plan["configuration"]["profile"], rubric
            ),
            "questions": evidence_questions([item["dimension"] for item in items], chunk),
        }
        check_request_budget(payload)
        response = client.evaluate(payload)
        evidence_records.append({"request_sha256": digest(payload), "response": response})
        by_id = {s["id"]: s for s in chunk["segments"]}
        for item in items:
            d = item["dimension"]
            row = item["row"]
            a = response["answers"]["evidence__" + d["id"]]
            if a["choice"] == "none" or a["confidence"] < rubric["thresholds"]["evidence_confidence"]:
                evidence_gaps.append(
                    {
                        "dimension": d["id"],
                        "chunk_id": cid,
                        "reason": "No sufficiently confident localized evidence; do not demand a rewrite on this score alone.",
                    }
                )
                continue
            seg = by_id.get(a["choice"])
            if seg is None or document["text"][seg["start"] : seg["end"]] != seg["text"]:
                raise ReviewError("Evidence/source mismatch. No writer handoff was approved.")
            findings.append(
                {
                    "id": f"F{len(findings) + 1:02}",
                    "dimension": d["id"],
                    "group": d["group"],
                    "label_ja": d["label_ja"],
                    "label_en": d["label_en"],
                    "severity_0_to_4": round(row["severity"], 2),
                    "priority": "high" if row["severity"] >= 3 else "medium",
                    "chunk_id": cid,
                    "source_span": {
                        "segment_id": seg["id"],
                        "locator": seg["locator"],
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"],
                        "source_sha256": document["sha256"],
                    },
                    "score_model_confidence": row["confidence"],
                    "evidence_model_confidence": a["confidence"],
                    "evidence_selection_probability": a["probabilities"][a["choice"]],
                    "fix_ja": d["fix_ja"],
                    "fix_en": d["fix_en"],
                    "evidence_status": "exact_source_quote_selected_by_jev; semantic appropriateness_needs_reviewer",
                    "suggested_rewrite": None,
                    "rewrite_author": "pending_host_agent_or_writer",
                }
            )
    all_responses = responses + [record["response"] for record in evidence_records]
    models = sorted(set(r["model"] for r in all_responses))
    requested = plan["configuration"]["requested_model"]
    if len(models) > 1:
        raise ReviewError("Resolved model changed during review. Re-run with one pinned model version.")
    if models and requested not in {"jev-latest", "jev-preview"} and models[0] != requested:
        raise ReviewError("Provider resolved a different model than the pinned model requested.")
    metrics = surface_metrics(document["text"])
    checks = protected_checks(document["text"], context)
    state = "needs_editorial_review" if findings or evidence_gaps else "no_priority_findings"
    if summary["style_index_0_to_100"] is None:
        state = "insufficient_evidence"
    if checks["missing_literals"] or metrics["possible_embedded_evaluator_instruction"]:
        state = "needs_editorial_review"
    configuration = dict(plan["configuration"])
    configuration["resolved_models"] = models
    return {
        "schema_version": "1.0.0",
        "mode": getattr(client, "mode", "jev_live"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "document": {k: document[k] for k in ["name", "sha256", "scope", "detected_language", "extractor_version"]},
        "configuration": configuration,
        "comparison_fingerprint": digest(configuration),
        "status": state,
        "release_approval": False,
        "summary": summary,
        "dimensions": dims,
        "skipped_dimensions": plan["skipped_dimensions"],
        "findings": findings,
        "unlocalized_candidates": evidence_gaps,
        "coverage": {
            "evaluated_characters": plan["evaluated_characters"],
            "excluded_characters": sum(len(s["text"]) for s in document["segments"] if s["excluded"]),
            "chunk_count": len(plan["chunks"]),
            "sampling": False,
            "visual_assessment": False,
            "warnings": document["warnings"],
        },
        "surface_metrics": metrics,
        "preservation_checks": checks,
        "usage": {
            "successful_logical_calls": len(all_responses),
            "input_tokens": sum(r["usage"]["input_tokens"] for r in all_responses),
            "output_tokens": sum(r["usage"]["output_tokens"] for r in all_responses),
            "http_attempts": getattr(client, "attempts", None),
            "note": "Returned usage only; failed attempts may incur provider usage not reflected here.",
        },
        "audit": {
            "scoring": [{"request_sha256": digest(p), "response": r} for p, r in zip(plan["payloads"], responses)],
            "evidence": evidence_records,
        },
        "interpretation": "Editorial feedback, not AI detection or proof of authorship. Thresholds and Japanese/English task accuracy are unvalidated.",
    }
