#!/usr/bin/env python3
"""Generate a PMBOK-compliant Project Charter Markdown skeleton.

Usage:
    python3 scripts/generate_project_charter.py \\
        --project "ECサイト構築" \\
        --sponsor "山田太郎" \\
        --pm "鈴木花子" \\
        --start-date 2026-04-01 \\
        --end-date 2026-11-30 \\
        --budget 100000000 \\
        --language ja \\
        --output /tmp/charter.md
"""

import argparse
from datetime import datetime
from pathlib import Path


def render_charter(
    project: str,
    sponsor: str,
    pm: str,
    start_date: str,
    end_date: str,
    budget: int,
    language: str = "ja",
) -> str:
    """Render a project charter Markdown skeleton with 12 sections."""
    today = datetime.now().strftime("%Y-%m-%d")
    budget_formatted = f"{budget:,}"

    if language == "ja":
        return _render_ja(project, sponsor, pm, start_date, end_date, budget_formatted, today)
    return _render_en(project, sponsor, pm, start_date, end_date, budget_formatted, today)


def _render_ja(
    project: str,
    sponsor: str,
    pm: str,
    start_date: str,
    end_date: str,
    budget: str,
    today: str,
) -> str:
    return f"""# プロジェクト憲章（Project Charter）

## 1. プロジェクト基本情報

| 項目 | 内容 |
|------|------|
| プロジェクト名 | {project} |
| プロジェクトコード | PRJ-XXXX-001 |
| プロジェクトマネージャー | {pm} |
| エグゼクティブスポンサー | {sponsor} |
| 発行日 | {today} |
| バージョン | 1.0 |

## 2. エグゼクティブサマリー

<!-- プロジェクトの要点を1-2段落で要約 -->

[TODO: プロジェクトの背景・目的・価値提案を記載]

## 3. プロジェクトの背景と目的

### 背景

<!-- 現在の課題と問題点、なぜこのプロジェクトが必要か -->

[TODO: 現状の課題を記載]

### 目的

1. **業務効率化**: [TODO: 具体的な効率化指標]
2. **品質向上**: [TODO: 品質指標の改善目標]
3. **顧客満足度向上**: [TODO: サービスレベルの改善]
4. **コスト削減**: [TODO: 具体的な削減額と根拠]

## 4. スコープ概要

### 含まれる内容（In Scope）

- [TODO: スコープ項目1]
- [TODO: スコープ項目2]
- [TODO: スコープ項目3]

### 含まれない内容（Out of Scope）

- [TODO: 除外項目1]
- [TODO: 除外項目2]

## 5. 主要な成果物

| 成果物 | 説明 | 納期 |
|--------|------|------|
| [TODO: 成果物1] | [説明] | [納期] |
| [TODO: 成果物2] | [説明] | [納期] |
| [TODO: 成果物3] | [説明] | [納期] |

## 6. マイルストーン

| マイルストーン | 予定日 | 説明 |
|--------------|--------|------|
| M1: プロジェクト開始 | {start_date} | キックオフ |
| M2: [TODO] | [YYYY-MM-DD] | [説明] |
| M3: [TODO] | [YYYY-MM-DD] | [説明] |
| M4: プロジェクト完了 | {end_date} | 最終納品 |

## 7. 概算予算

| カテゴリ | 概算金額（円） | 内訳 |
|---------|--------------|------|
| 開発費用 | [TODO] | [内訳] |
| インフラ費用 | [TODO] | [内訳] |
| 間接費用 | [TODO] | [内訳] |
| **合計** | **{budget}** | |

## 8. ステークホルダー

| 役割 | 氏名/部署 | 期待値・関心事 |
|------|----------|--------------|
| Executive Sponsor | {sponsor} | [TODO: 期待値] |
| Project Manager | {pm} | スケジュール・予算管理 |
| [TODO: 役割] | [氏名] | [期待値] |

## 9. 前提条件と制約条件

### 前提条件

- [TODO: 前提条件1]
- [TODO: 前提条件2]

### 制約条件

- 予算上限: {budget}円
- スケジュール: {start_date} ～ {end_date}
- [TODO: その他の制約]

## 10. 主要なリスク

| リスク | 影響 | 確率 | 対策 |
|--------|------|------|------|
| [TODO: リスク1] | 高/中/低 | 高/中/低 | [対策] |
| [TODO: リスク2] | 高/中/低 | 高/中/低 | [対策] |

## 11. 成功基準

1. **スコープ**: [TODO: スコープに関する成功基準]
2. **スケジュール**: {end_date}までにプロジェクト完了
3. **予算**: 予算{budget}円以内（±10%）
4. **品質**: [TODO: 品質に関する成功基準]

## 12. 承認

| 役割 | 氏名 | 署名 | 日付 |
|------|------|------|------|
| Executive Sponsor | {sponsor} | __________ | ____/____/____ |
| Project Manager | {pm} | __________ | ____/____/____ |
| [TODO: 承認者] | [氏名] | __________ | ____/____/____ |

---

*本文書は `project-plan-creator` スキルにより生成されました。*
*参照: `references/project_charter_guide.md`*
"""


def _render_en(
    project: str,
    sponsor: str,
    pm: str,
    start_date: str,
    end_date: str,
    budget: str,
    today: str,
) -> str:
    return f"""# Project Charter

## 1. Project Information

| Item | Details |
|------|---------|
| Project Name | {project} |
| Project Code | PRJ-XXXX-001 |
| Project Manager | {pm} |
| Executive Sponsor | {sponsor} |
| Issue Date | {today} |
| Version | 1.0 |

## 2. Executive Summary

<!-- Summarize the project in 1-2 paragraphs -->

[TODO: Describe background, purpose, and value proposition]

## 3. Background and Objectives

### Background

<!-- Current challenges and why this project is needed -->

[TODO: Describe current challenges]

### Objectives

1. **Operational Efficiency**: [TODO: Specific efficiency metrics]
2. **Quality Improvement**: [TODO: Quality improvement targets]
3. **Customer Satisfaction**: [TODO: Service level improvements]
4. **Cost Reduction**: [TODO: Specific reduction amounts and rationale]

## 4. Scope Overview

### In Scope

- [TODO: Scope item 1]
- [TODO: Scope item 2]
- [TODO: Scope item 3]

### Out of Scope

- [TODO: Exclusion item 1]
- [TODO: Exclusion item 2]

## 5. Key Deliverables

| Deliverable | Description | Due Date |
|------------|-------------|----------|
| [TODO: Deliverable 1] | [Description] | [Date] |
| [TODO: Deliverable 2] | [Description] | [Date] |
| [TODO: Deliverable 3] | [Description] | [Date] |

## 6. Milestones

| Milestone | Target Date | Description |
|-----------|------------|-------------|
| M1: Project Start | {start_date} | Kickoff |
| M2: [TODO] | [YYYY-MM-DD] | [Description] |
| M3: [TODO] | [YYYY-MM-DD] | [Description] |
| M4: Project Completion | {end_date} | Final delivery |

## 7. Budget Estimate

| Category | Estimated Cost | Breakdown |
|----------|---------------|-----------|
| Development | [TODO] | [Breakdown] |
| Infrastructure | [TODO] | [Breakdown] |
| Indirect Costs | [TODO] | [Breakdown] |
| **Total** | **{budget}** | |

## 8. Stakeholders

| Role | Name/Department | Expectations |
|------|----------------|--------------|
| Executive Sponsor | {sponsor} | [TODO: Expectations] |
| Project Manager | {pm} | Schedule & budget management |
| [TODO: Role] | [Name] | [Expectations] |

## 9. Assumptions and Constraints

### Assumptions

- [TODO: Assumption 1]
- [TODO: Assumption 2]

### Constraints

- Budget ceiling: {budget}
- Schedule: {start_date} to {end_date}
- [TODO: Other constraints]

## 10. Key Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [TODO: Risk 1] | High/Med/Low | High/Med/Low | [Mitigation] |
| [TODO: Risk 2] | High/Med/Low | High/Med/Low | [Mitigation] |

## 11. Success Criteria

1. **Scope**: [TODO: Scope-related success criteria]
2. **Schedule**: Project completion by {end_date}
3. **Budget**: Within {budget} (+/-10%)
4. **Quality**: [TODO: Quality-related success criteria]

## 12. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Executive Sponsor | {sponsor} | __________ | ____/____/____ |
| Project Manager | {pm} | __________ | ____/____/____ |
| [TODO: Approver] | [Name] | __________ | ____/____/____ |

---

*Generated by `project-plan-creator` skill.*
*Reference: `references/project_charter_guide.md`*
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a PMBOK-compliant Project Charter Markdown skeleton")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--sponsor", default="[TBD]", help="Executive sponsor name")
    parser.add_argument("--pm", required=True, help="Project manager name")
    parser.add_argument("--start-date", required=True, help="Project start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", required=True, help="Project end date (YYYY-MM-DD)")
    parser.add_argument("--budget", required=True, type=int, help="Total budget (integer, in JPY or USD)")
    parser.add_argument("--language", default="ja", choices=["ja", "en"], help="Output language (default: ja)")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    args = parser.parse_args()

    content = render_charter(
        project=args.project,
        sponsor=args.sponsor,
        pm=args.pm,
        start_date=args.start_date,
        end_date=args.end_date,
        budget=args.budget,
        language=args.language,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"Project charter generated: {output_path}")


if __name__ == "__main__":
    main()
