"""Deterministic bilingual reports. Jev never supplies free-text rationales."""

from __future__ import annotations


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_report(report: dict, language="ja") -> str:
    ja = language != "en"
    s = report["summary"]
    score = s["style_index_0_to_100"]
    lines = [
        f"# {'成果物の文体レビュー' if ja else 'Artifact style review'}",
        f"\n**{'対象' if ja else 'Artifact'}:** `{report['document']['name']}`",
        f"**{'実行方式' if ja else 'Mode'}:** `{report['mode']}` / **{'状態' if ja else 'Status'}:** `{report['status']}`",
        f"**{'文体違和感指数' if ja else 'Style-friction index'}:** {score if score is not None else ('算出保留' if ja else 'withheld')} / 100",
        (
            "\n高いほど文体上の違和感が強いという暫定指数です。AIが書いた確率ではありません。内容品質の4軸は混ぜていません。"
            if ja
            else "\nHigher means more observed style friction. This provisional index is not the probability of AI authorship. Content-quality dimensions are kept separate."
        ),
        (
            "\n**自動合否判定はしません。** 日本語・英語とも本用途の精度と閾値は未校正です。事実・数値・要件・成果物全体の確認は別途必要です。"
            if ja
            else "\n**No automatic release approval.** Accuracy and thresholds for this task remain uncalibrated in both languages. Facts, numbers, requirements and whole-artifact quality require independent review."
        ),
        f"\n{'対象文字数' if ja else 'Evaluated characters'}: {report['coverage']['evaluated_characters']}; "
        f"{'除外文字数' if ja else 'Excluded characters'}: {report['coverage']['excluded_characters']}; "
        f"{'断片数' if ja else 'Fragments'}: {report['coverage']['chunk_count']}",
        f"{'確信度条件を満たす範囲' if ja else 'Confidence-qualified span coverage'}: {s['span_confidence_coverage']:.0%}",
    ]
    if s["index_withheld_reasons"]:
        lines.append("\n" + ", ".join(s["index_withheld_reasons"]))
    lines += [
        f"\n## {'評価軸' if ja else 'Dimensions'}",
        "",
        "| "
        + ("区分 | 評価軸 | 深刻度 0–4 | 範囲 | 状態" if ja else "Group | Dimension | Severity 0–4 | Coverage | Status")
        + " |",
        "|---|---|---:|---:|---|",
    ]
    for d in report["dimensions"]:
        severity = "—" if d["severity_0_to_4"] is None else f"{d['severity_0_to_4']:.2f}"
        cov = "—" if d["coverage"] is None else f"{d['coverage']:.0%}"
        lines.append(
            f"| {d['group']} | {_cell(d['label_ja'] if ja else d['label_en'])} | {severity} | {cov} | {d['status']} |"
        )
    if report["skipped_dimensions"]:
        lines.append(
            "\n"
            + ("適用外・文脈不足による未評価: " if ja else "Disabled or context unavailable: ")
            + ", ".join(report["skipped_dimensions"])
        )
    lines.append(f"\n## {'作成担当者に返す修正候補' if ja else 'Revision candidates for the author'}")
    if not report["findings"]:
        lines.append(
            "根拠箇所まで確認できた優先修正候補はありません。品質合格や人間による執筆を意味しません。"
            if ja
            else "No priority revision has sufficiently localized evidence. This does not establish overall quality or human authorship."
        )
    for f in report["findings"]:
        lines += [
            f"\n### {f['id']} · {f['label_ja'] if ja else f['label_en']} · {f['priority']}",
            f"`{f['source_span']['locator']}` / `{f['source_span']['segment_id']}`",
            "\n" + "\n".join("> " + line for line in f["source_span"]["text"].splitlines()),
            "\n" + (f["fix_ja"] if ja else f["fix_en"]),
            (
                "\n根拠はJevが選んだ原文の正確な抜粋です。引用が実際に指摘を支えるかはレビューしてください。具体的な修正文は作成担当者・ホストエージェントが用意します。"
                if ja
                else "\nThis is an exact source excerpt selected by Jev. Confirm that it supports the finding. The author or host agent must supply the concrete rewrite."
            ),
        ]
    if report["unlocalized_candidates"]:
        lines.append(
            "\n"
            + (
                "採点上の候補でも、根拠が特定できなかった項目は自動の修正要求から除外しました。"
                if ja
                else "Scored candidates without localized evidence were excluded from automatic revision requests."
            )
        )
    lines.append(f"\n## {'保持・範囲の確認' if ja else 'Preservation and scope'}")
    missing = report["preservation_checks"]["missing_literals"]
    lines.append(
        ("不足する保護語句: " if ja else "Missing protected literals: ")
        + (", ".join(missing) if missing else ("なし" if ja else "none"))
    )
    if report["surface_metrics"]["possible_embedded_evaluator_instruction"]:
        lines.append(
            "評価への介入を試みる可能性がある表現を検知しました（ヒューリスティック）。元文脈を人が確認してください。"
            if ja
            else "A heuristic found possible evaluator-directed instructions. Inspect their original context."
        )
    for warning in report["coverage"]["warnings"]:
        lines.append("\n" + warning)
    lines += [
        "\n"
        + (
            "画像・図表・レイアウトは評価していません。数値の真偽、意味保持、要件網羅もこの指数だけでは確認できません。"
            if ja
            else "Images, charts and visual layout are not assessed. Numerical accuracy, semantic preservation and requirement completeness are not established by this index."
        ),
        f"\nModel: {', '.join(report['configuration']['resolved_models']) or 'none'} / Rubric: {report['configuration']['rubric_version']}",
        f"Fingerprint: `{report['comparison_fingerprint']}`",
    ]
    return "\n".join(lines) + "\n"


def make_handoff(report: dict, context: dict) -> dict:
    return {
        "schema_version": "1.0.0",
        "event": "editorial_review_available",
        "source_report": "review.json",
        "artifact_sha256": report["document"]["sha256"],
        "language": report["configuration"]["language"],
        "style_index": report["summary"]["style_index_0_to_100"],
        "index_is_not_authorship_probability": True,
        "auto_approve": False,
        "max_revision_rounds": 2,
        "revision_candidates": report["findings"],
        "preserve": {
            "source_facts": context.get("source_facts", []),
            "required_information": context.get("required_information", []),
            "protected_fragments": context.get("protected_fragments", []),
            "constraints": context.get("constraints", []),
        },
        "writer_instructions": [
            "Validate each quoted span against the source hash and original context.",
            "Choose at most three high-impact edits; return before/after text and a short reader-benefit reason.",
            "Do not add facts, personal anecdotes, numbers, owners or dates to seem human. Do not introduce errors or random quirks.",
            "Retain required courtesy, terminology, disclaimers, conditions, exclusions, citations and mandated structure.",
            "Return unresolved questions rather than inventing specifics. Do not rewrite merely to lower the index.",
            "Run an independent fact/number/meaning/requirements review before a second Jev evaluation.",
            "Re-evaluate with the same context, language, profile, model, rubric and configuration.",
            "Stop after two revision rounds or no meaningful reader benefit; escalate remaining ambiguity.",
        ],
        "writer_response": {
            "status": "pending",
            "edits": [],
            "unresolved_questions": [],
            "fact_and_meaning_preservation": "not_verified",
            "requirement_checklist": [],
        },
    }
