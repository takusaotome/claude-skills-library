#!/usr/bin/env python3
"""
Implementation Roadmap Generator for AI-BPO Proposals

Generates phased implementation plans with milestones and dependencies.
Outputs timeline in JSON format suitable for Gantt chart generation.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Any

# Phase templates with duration and activities
PHASE_TEMPLATES = {
    "discovery": {
        "phase_name": "Discovery & Assessment",
        "phase_name_ja": "ディスカバリー・アセスメント",
        "duration_weeks": 3,
        "activities": [
            {
                "name": "Kickoff Meeting",
                "name_ja": "キックオフミーティング",
                "duration_days": 1,
                "dependencies": [],
            },
            {
                "name": "Current State Process Mapping",
                "name_ja": "現状プロセスマッピング",
                "duration_days": 5,
                "dependencies": ["Kickoff Meeting"],
            },
            {
                "name": "Data Audit & Quality Assessment",
                "name_ja": "データ監査・品質評価",
                "duration_days": 5,
                "dependencies": ["Current State Process Mapping"],
            },
            {
                "name": "Integration Requirements Analysis",
                "name_ja": "連携要件分析",
                "duration_days": 5,
                "dependencies": ["Current State Process Mapping"],
            },
            {
                "name": "Future State Design Workshop",
                "name_ja": "将来状態設計ワークショップ",
                "duration_days": 2,
                "dependencies": ["Data Audit & Quality Assessment"],
            },
            {
                "name": "Implementation Plan Finalization",
                "name_ja": "実装計画最終化",
                "duration_days": 3,
                "dependencies": ["Future State Design Workshop"],
            },
        ],
        "deliverables": [
            "Process documentation",
            "Data quality report",
            "Integration specifications",
            "Detailed implementation plan",
        ],
        "deliverables_ja": [
            "プロセス文書",
            "データ品質レポート",
            "連携仕様書",
            "詳細実装計画",
        ],
    },
    "pilot": {
        "phase_name": "Pilot Implementation",
        "phase_name_ja": "パイロット実装",
        "duration_weeks": 5,
        "activities": [
            {
                "name": "Environment Setup",
                "name_ja": "環境構築",
                "duration_days": 5,
                "dependencies": [],
            },
            {
                "name": "Data Migration (Pilot Scope)",
                "name_ja": "データ移行（パイロット範囲）",
                "duration_days": 5,
                "dependencies": ["Environment Setup"],
            },
            {
                "name": "Integration Development",
                "name_ja": "連携開発",
                "duration_days": 10,
                "dependencies": ["Environment Setup"],
            },
            {
                "name": "AI Model Configuration",
                "name_ja": "AIモデル設定",
                "duration_days": 7,
                "dependencies": ["Data Migration (Pilot Scope)"],
            },
            {
                "name": "User Acceptance Testing",
                "name_ja": "受入テスト",
                "duration_days": 5,
                "dependencies": ["AI Model Configuration", "Integration Development"],
            },
            {
                "name": "Pilot Go-Live",
                "name_ja": "パイロット稼働開始",
                "duration_days": 1,
                "dependencies": ["User Acceptance Testing"],
            },
            {
                "name": "Pilot Monitoring & Adjustment",
                "name_ja": "パイロット監視・調整",
                "duration_days": 10,
                "dependencies": ["Pilot Go-Live"],
            },
        ],
        "deliverables": [
            "Configured environment",
            "Working pilot system",
            "UAT sign-off",
            "Pilot results report",
        ],
        "deliverables_ja": [
            "構築済み環境",
            "稼働中パイロットシステム",
            "UAT承認",
            "パイロット結果レポート",
        ],
    },
    "rollout": {
        "phase_name": "Phased Rollout",
        "phase_name_ja": "段階的展開",
        "duration_weeks": 8,
        "activities": [
            {
                "name": "Full Data Migration",
                "name_ja": "全データ移行",
                "duration_days": 10,
                "dependencies": [],
            },
            {
                "name": "End User Training",
                "name_ja": "エンドユーザー研修",
                "duration_days": 5,
                "dependencies": [],
            },
            {
                "name": "Wave 1 Go-Live",
                "name_ja": "Wave 1 稼働開始",
                "duration_days": 1,
                "dependencies": ["Full Data Migration", "End User Training"],
            },
            {
                "name": "Wave 1 Stabilization",
                "name_ja": "Wave 1 安定化",
                "duration_days": 10,
                "dependencies": ["Wave 1 Go-Live"],
            },
            {
                "name": "Wave 2 Go-Live",
                "name_ja": "Wave 2 稼働開始",
                "duration_days": 1,
                "dependencies": ["Wave 1 Stabilization"],
            },
            {
                "name": "Wave 2 Stabilization",
                "name_ja": "Wave 2 安定化",
                "duration_days": 10,
                "dependencies": ["Wave 2 Go-Live"],
            },
            {
                "name": "Full Production Go-Live",
                "name_ja": "本番稼働開始",
                "duration_days": 1,
                "dependencies": ["Wave 2 Stabilization"],
            },
            {
                "name": "Hypercare Support",
                "name_ja": "ハイパーケアサポート",
                "duration_days": 14,
                "dependencies": ["Full Production Go-Live"],
            },
        ],
        "deliverables": [
            "Trained users",
            "Full production system",
            "Operations documentation",
            "Hypercare report",
        ],
        "deliverables_ja": [
            "研修済みユーザー",
            "本番システム",
            "運用ドキュメント",
            "ハイパーケアレポート",
        ],
    },
    "optimization": {
        "phase_name": "Optimization",
        "phase_name_ja": "最適化",
        "duration_weeks": 4,
        "activities": [
            {
                "name": "Performance Analysis",
                "name_ja": "パフォーマンス分析",
                "duration_days": 5,
                "dependencies": [],
            },
            {
                "name": "Model Tuning",
                "name_ja": "モデルチューニング",
                "duration_days": 10,
                "dependencies": ["Performance Analysis"],
            },
            {
                "name": "Process Refinement",
                "name_ja": "プロセス改善",
                "duration_days": 5,
                "dependencies": ["Performance Analysis"],
            },
            {
                "name": "Lessons Learned Workshop",
                "name_ja": "振り返りワークショップ",
                "duration_days": 1,
                "dependencies": ["Model Tuning", "Process Refinement"],
            },
            {
                "name": "Transition to BAU",
                "name_ja": "通常運用への移行",
                "duration_days": 5,
                "dependencies": ["Lessons Learned Workshop"],
            },
        ],
        "deliverables": [
            "Optimization report",
            "Updated playbooks",
            "BAU operations handover",
            "Project closure document",
        ],
        "deliverables_ja": [
            "最適化レポート",
            "更新済みプレイブック",
            "通常運用引継ぎ",
            "プロジェクト完了文書",
        ],
    },
}

# Service complexity affects timeline
SERVICE_COMPLEXITY = {
    "fin-001": "medium",
    "fin-002": "low",
    "fin-003": "medium",
    "fin-004": "medium",
    "hr-001": "high",
    "hr-002": "low",
    "hr-004": "high",
    "cs-001": "low",
    "cs-002": "medium",
    "dp-001": "low",
    "dp-002": "low",
    "pr-001": "medium",
    "pr-002": "medium",
    "pr-003": "medium",
}


def calculate_complexity_factor(services: list[dict[str, Any]]) -> float:
    """
    Calculate timeline complexity factor based on selected services.

    Args:
        services: List of selected service dictionaries

    Returns:
        Complexity factor (1.0 = normal, >1.0 = longer timeline)
    """
    complexity_scores = {"low": 1, "medium": 2, "high": 3}
    total_score = 0

    for service in services:
        service_id = service.get("service_id", "")
        complexity = SERVICE_COMPLEXITY.get(service_id, "medium")
        total_score += complexity_scores[complexity]

    # Normalize: 1-3 services low impact, 4-6 medium, 7+ high
    service_count = len(services)
    count_factor = 1.0 + (max(0, service_count - 3) * 0.1)

    avg_complexity = total_score / max(service_count, 1)
    complexity_factor = 0.8 + (avg_complexity * 0.2)

    return round(complexity_factor * count_factor, 2)


def generate_timeline(
    start_date: str,
    phases: list[str],
    complexity_factor: float = 1.0,
) -> list[dict[str, Any]]:
    """
    Generate timeline with calculated dates.

    Args:
        start_date: Project start date (YYYY-MM-DD)
        phases: List of phase names to include
        complexity_factor: Factor to adjust durations

    Returns:
        List of phase dictionaries with dates
    """
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    timeline = []

    for phase_key in phases:
        if phase_key not in PHASE_TEMPLATES:
            continue

        phase = PHASE_TEMPLATES[phase_key].copy()
        adjusted_weeks = int(phase["duration_weeks"] * complexity_factor)

        phase_start = current_date
        phase_end = phase_start + timedelta(weeks=adjusted_weeks)

        # Calculate activity dates
        activities_with_dates = []
        activity_date = phase_start

        for activity in phase["activities"]:
            adjusted_days = max(1, int(activity["duration_days"] * complexity_factor))
            activity_end = activity_date + timedelta(days=adjusted_days)

            activities_with_dates.append(
                {
                    "name": activity["name"],
                    "name_ja": activity["name_ja"],
                    "start_date": activity_date.strftime("%Y-%m-%d"),
                    "end_date": activity_end.strftime("%Y-%m-%d"),
                    "duration_days": adjusted_days,
                    "dependencies": activity["dependencies"],
                }
            )

            # Simplified: sequential activities (real implementation would use dependencies)
            activity_date = activity_end

        timeline.append(
            {
                "phase_key": phase_key,
                "phase_name": phase["phase_name"],
                "phase_name_ja": phase["phase_name_ja"],
                "start_date": phase_start.strftime("%Y-%m-%d"),
                "end_date": phase_end.strftime("%Y-%m-%d"),
                "duration_weeks": adjusted_weeks,
                "activities": activities_with_dates,
                "deliverables": phase["deliverables"],
                "deliverables_ja": phase["deliverables_ja"],
            }
        )

        current_date = phase_end

    return timeline


def generate_milestones(timeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Generate key milestones from timeline.

    Args:
        timeline: List of phase dictionaries

    Returns:
        List of milestone dictionaries
    """
    milestones = []

    milestone_mapping = {
        "discovery": ("Discovery Complete", "ディスカバリー完了"),
        "pilot": ("Pilot Go-Live", "パイロット稼働開始"),
        "rollout": ("Production Go-Live", "本番稼働開始"),
        "optimization": ("Project Closure", "プロジェクト完了"),
    }

    for phase in timeline:
        phase_key = phase["phase_key"]
        if phase_key in milestone_mapping:
            names = milestone_mapping[phase_key]
            milestones.append(
                {
                    "name": names[0],
                    "name_ja": names[1],
                    "date": phase["end_date"],
                    "phase": phase["phase_name"],
                }
            )

    return milestones


def generate_roadmap(
    services_file: str | None = None,
    services_data: dict[str, Any] | None = None,
    start_date: str | None = None,
    output_path: str | None = None,
) -> dict[str, Any]:
    """
    Generate implementation roadmap.

    Args:
        services_file: Path to services JSON file
        services_data: Services data dictionary (alternative to file)
        start_date: Project start date (YYYY-MM-DD)
        output_path: Optional output file path

    Returns:
        Roadmap dictionary
    """
    # Load services
    if services_file:
        with open(services_file, "r", encoding="utf-8") as f:
            services_data = json.load(f)
    elif not services_data:
        services_data = {"selected_services": []}

    selected_services = services_data.get("selected_services", [])

    # Default start date
    if not start_date:
        start_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Calculate complexity
    complexity_factor = calculate_complexity_factor(selected_services)

    # Standard phases
    phases = ["discovery", "pilot", "rollout", "optimization"]

    # Generate timeline
    timeline = generate_timeline(start_date, phases, complexity_factor)
    milestones = generate_milestones(timeline)

    # Calculate totals
    total_weeks = sum(p["duration_weeks"] for p in timeline)
    project_end = timeline[-1]["end_date"] if timeline else start_date

    roadmap = {
        "schema_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "project_start": start_date,
        "project_end": project_end,
        "total_duration_weeks": total_weeks,
        "complexity_factor": complexity_factor,
        "services_included": [s["service_id"] for s in selected_services],
        "phases": timeline,
        "milestones": milestones,
        "assumptions": [
            "Client resources available as planned",
            "No major scope changes during implementation",
            "System access and credentials provided on schedule",
            "Training attendance per agreed schedule",
        ],
        "assumptions_ja": [
            "クライアントリソースが計画通り確保される",
            "実装中の大きなスコープ変更がない",
            "システムアクセスと資格情報がスケジュール通り提供される",
            "合意されたスケジュールで研修に参加する",
        ],
    }

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(roadmap, f, indent=2, ensure_ascii=False)
        print(f"Roadmap saved to: {output_path}", file=sys.stderr)

    return roadmap


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate implementation roadmap for AI-BPO services")
    parser.add_argument(
        "--services",
        help="Path to services JSON file from select_services.py",
    )
    parser.add_argument(
        "--start-date",
        help="Project start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file path",
    )

    args = parser.parse_args()

    roadmap = generate_roadmap(
        services_file=args.services,
        start_date=args.start_date,
        output_path=args.output,
    )

    print(json.dumps(roadmap, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
