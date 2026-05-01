#!/usr/bin/env python3
"""
Bilingual Proposal Document Generator for AI-BPO Services

Generates professional proposal documents in Markdown format with
Japanese and English content side by side or selectable.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_json_file(file_path: str) -> dict[str, Any]:
    """Load JSON file and return contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string."""
    if currency == "USD":
        return f"${amount:,.0f}"
    elif currency == "JPY":
        return f"¥{amount:,.0f}"
    return f"{amount:,.0f} {currency}"


def generate_executive_summary(
    client_name: str,
    services: list[dict],
    roi_data: dict,
    roadmap_data: dict,
    language: str = "bilingual",
) -> str:
    """Generate executive summary section."""
    service_count = len(services)
    annual_savings = roi_data.get("financial_summary", {}).get("annual_savings_usd", 0)
    payback_months = roi_data.get("financial_summary", {}).get("payback_months", 0)
    roi_pct = roi_data.get("financial_summary", {}).get("three_year_roi_percentage", 0)
    duration_weeks = roadmap_data.get("total_duration_weeks", 20)

    if language == "english":
        return f"""## Executive Summary

This proposal outlines an AI-powered BPO solution designed specifically for {client_name}'s US operations. Our recommendation includes {service_count} integrated service modules that will:

- **Reduce operational costs** by {format_currency(annual_savings)} annually
- **Achieve ROI** of {roi_pct}% over 3 years
- **Recover investment** within {payback_months} months
- **Complete implementation** in {duration_weeks} weeks

Our solution combines proven automation technology with deep understanding of Japanese business practices, ensuring seamless integration with your existing operations and headquarters reporting requirements.
"""
    elif language == "japanese":
        return f"""## エグゼクティブサマリー

本提案書は、{client_name}様の米国事業向けに設計されたAI駆動型BPOソリューションをご提案いたします。{service_count}つの統合サービスモジュールにより、以下を実現します：

- **年間運用コスト削減**: {format_currency(annual_savings)}
- **3年間ROI**: {roi_pct}%
- **投資回収期間**: {payback_months}ヶ月
- **導入期間**: {duration_weeks}週間

当社のソリューションは、実績のある自動化技術と日本のビジネス慣行への深い理解を組み合わせ、既存のオペレーションや本社報告要件とのシームレスな統合を保証いたします。
"""
    else:  # bilingual
        return f"""## Executive Summary / エグゼクティブサマリー

This proposal outlines an AI-powered BPO solution designed specifically for {client_name}'s US operations.

本提案書は、{client_name}様の米国事業向けに設計されたAI駆動型BPOソリューションをご提案いたします。

| Metric / 指標 | Value / 値 |
|--------------|-----------|
| Service Modules / サービスモジュール数 | {service_count} |
| Annual Cost Savings / 年間コスト削減 | {format_currency(annual_savings)} |
| 3-Year ROI / 3年間ROI | {roi_pct}% |
| Payback Period / 投資回収期間 | {payback_months} months / ヶ月 |
| Implementation Duration / 導入期間 | {duration_weeks} weeks / 週間 |

Our solution combines proven automation technology with deep understanding of Japanese business practices.

当社のソリューションは、実績のある自動化技術と日本のビジネス慣行への深い理解を組み合わせています。
"""


def generate_services_section(
    services: list[dict],
    language: str = "bilingual",
) -> str:
    """Generate proposed services section."""
    lines = []

    if language == "bilingual":
        lines.append("## Proposed Services / ご提案サービス\n")
    elif language == "english":
        lines.append("## Proposed Services\n")
    else:
        lines.append("## ご提案サービス\n")

    for i, service in enumerate(services, 1):
        name = service.get("service_name", "Service")
        category = service.get("category", "").replace("_", " ").title()
        automation_rate = service.get("estimated_automation_rate", 0.8) * 100
        ai_components = service.get("ai_components", [])

        if language == "bilingual":
            lines.append(f"### {i}. {name}\n")
            lines.append(f"**Category / カテゴリ**: {category}\n")
            lines.append(f"**Expected Automation Rate / 期待自動化率**: {automation_rate:.0f}%\n")
            lines.append("**AI Components / AI構成要素**:")
            for comp in ai_components:
                lines.append(f"- {comp.replace('_', ' ').title()}")
            lines.append("")
        elif language == "english":
            lines.append(f"### {i}. {name}\n")
            lines.append(f"**Category**: {category}\n")
            lines.append(f"**Expected Automation Rate**: {automation_rate:.0f}%\n")
            lines.append("**AI Components**:")
            for comp in ai_components:
                lines.append(f"- {comp.replace('_', ' ').title()}")
            lines.append("")
        else:
            # Japanese version would need translated names
            lines.append(f"### {i}. {name}\n")
            lines.append(f"**カテゴリ**: {category}\n")
            lines.append(f"**期待自動化率**: {automation_rate:.0f}%\n")
            lines.append("**AI構成要素**:")
            for comp in ai_components:
                lines.append(f"- {comp.replace('_', ' ').title()}")
            lines.append("")

    return "\n".join(lines)


def generate_roi_section(
    roi_data: dict,
    language: str = "bilingual",
) -> str:
    """Generate ROI analysis section."""
    current = roi_data.get("current_state", {})
    future = roi_data.get("future_state", {})
    financial = roi_data.get("financial_summary", {})
    implementation = roi_data.get("implementation_costs", {})

    if language == "bilingual":
        return f"""## ROI Analysis / ROI分析

### Current State vs. Future State / 現状 vs. 将来状態

| Metric / 指標 | Current / 現状 | Future / 将来 | Change / 変化 |
|--------------|---------------|--------------|--------------|
| Annual Cost / 年間コスト | {format_currency(current.get("annual_cost_usd", 0))} | {format_currency(future.get("annual_cost_usd", 0))} | -{format_currency(financial.get("annual_savings_usd", 0))} |
| FTE Equivalent / FTE相当 | {current.get("fte_equivalent", 0):.1f} | {future.get("fte_equivalent", 0):.1f} | -{current.get("fte_equivalent", 0) - future.get("fte_equivalent", 0):.1f} |

### Investment Summary / 投資サマリー

| Item / 項目 | Amount / 金額 |
|------------|--------------|
| Implementation Cost / 導入コスト | {format_currency(financial.get("implementation_cost_usd", 0))} |
| Annual Savings / 年間削減額 | {format_currency(financial.get("annual_savings_usd", 0))} |
| Payback Period / 投資回収期間 | {financial.get("payback_months", 0)} months / ヶ月 |
| 3-Year NPV | {format_currency(financial.get("three_year_npv_usd", 0))} |
| 3-Year ROI | {financial.get("three_year_roi_percentage", 0)}% |

### Implementation Cost Breakdown / 導入コスト内訳

| Component / 構成 | Cost / コスト |
|-----------------|-------------|
| Setup & Configuration / セットアップ・設定 | {format_currency(implementation.get("setup_and_configuration_usd", 0))} |
| Integration Development / 連携開発 | {format_currency(implementation.get("integration_development_usd", 0))} |
| Training / 研修 | {format_currency(implementation.get("training_usd", 0))} |
| Change Management / 変更管理 | {format_currency(implementation.get("change_management_usd", 0))} |
| **Total / 合計** | **{format_currency(implementation.get("total_implementation_cost_usd", 0))}** |
"""
    elif language == "english":
        return f"""## ROI Analysis

### Current State vs. Future State

| Metric | Current | Future | Change |
|--------|---------|--------|--------|
| Annual Cost | {format_currency(current.get("annual_cost_usd", 0))} | {format_currency(future.get("annual_cost_usd", 0))} | -{format_currency(financial.get("annual_savings_usd", 0))} |
| FTE Equivalent | {current.get("fte_equivalent", 0):.1f} | {future.get("fte_equivalent", 0):.1f} | -{current.get("fte_equivalent", 0) - future.get("fte_equivalent", 0):.1f} |

### Investment Summary

| Item | Amount |
|------|--------|
| Implementation Cost | {format_currency(financial.get("implementation_cost_usd", 0))} |
| Annual Savings | {format_currency(financial.get("annual_savings_usd", 0))} |
| Payback Period | {financial.get("payback_months", 0)} months |
| 3-Year NPV | {format_currency(financial.get("three_year_npv_usd", 0))} |
| 3-Year ROI | {financial.get("three_year_roi_percentage", 0)}% |
"""
    else:  # japanese
        return f"""## ROI分析

### 現状 vs. 将来状態

| 指標 | 現状 | 将来 | 変化 |
|-----|-----|-----|-----|
| 年間コスト | {format_currency(current.get("annual_cost_usd", 0))} | {format_currency(future.get("annual_cost_usd", 0))} | -{format_currency(financial.get("annual_savings_usd", 0))} |
| FTE相当 | {current.get("fte_equivalent", 0):.1f} | {future.get("fte_equivalent", 0):.1f} | -{current.get("fte_equivalent", 0) - future.get("fte_equivalent", 0):.1f} |

### 投資サマリー

| 項目 | 金額 |
|-----|-----|
| 導入コスト | {format_currency(financial.get("implementation_cost_usd", 0))} |
| 年間削減額 | {format_currency(financial.get("annual_savings_usd", 0))} |
| 投資回収期間 | {financial.get("payback_months", 0)}ヶ月 |
| 3年NPV | {format_currency(financial.get("three_year_npv_usd", 0))} |
| 3年ROI | {financial.get("three_year_roi_percentage", 0)}% |
"""


def generate_roadmap_section(
    roadmap_data: dict,
    language: str = "bilingual",
) -> str:
    """Generate implementation roadmap section."""
    phases = roadmap_data.get("phases", [])
    milestones = roadmap_data.get("milestones", [])

    lines = []

    if language == "bilingual":
        lines.append("## Implementation Roadmap / 導入ロードマップ\n")
        lines.append("### Project Timeline / プロジェクトタイムライン\n")
        lines.append("| Phase / フェーズ | Duration / 期間 | Start / 開始 | End / 終了 |")
        lines.append("|----------------|----------------|-------------|-----------|")
    elif language == "english":
        lines.append("## Implementation Roadmap\n")
        lines.append("### Project Timeline\n")
        lines.append("| Phase | Duration | Start | End |")
        lines.append("|-------|----------|-------|-----|")
    else:
        lines.append("## 導入ロードマップ\n")
        lines.append("### プロジェクトタイムライン\n")
        lines.append("| フェーズ | 期間 | 開始 | 終了 |")
        lines.append("|---------|-----|-----|-----|")

    for phase in phases:
        if language == "bilingual":
            name = f"{phase['phase_name']} / {phase['phase_name_ja']}"
        elif language == "english":
            name = phase["phase_name"]
        else:
            name = phase["phase_name_ja"]

        duration = f"{phase['duration_weeks']} weeks" if language != "japanese" else f"{phase['duration_weeks']}週間"
        lines.append(f"| {name} | {duration} | {phase['start_date']} | {phase['end_date']} |")

    lines.append("")

    # Milestones
    if language == "bilingual":
        lines.append("### Key Milestones / 主要マイルストーン\n")
    elif language == "english":
        lines.append("### Key Milestones\n")
    else:
        lines.append("### 主要マイルストーン\n")

    for milestone in milestones:
        if language == "bilingual":
            lines.append(f"- **{milestone['date']}**: {milestone['name']} / {milestone['name_ja']}")
        elif language == "english":
            lines.append(f"- **{milestone['date']}**: {milestone['name']}")
        else:
            lines.append(f"- **{milestone['date']}**: {milestone['name_ja']}")

    return "\n".join(lines)


def generate_terms_section(language: str = "bilingual") -> str:
    """Generate terms and conditions section."""
    if language == "bilingual":
        return """## Terms & Conditions / 契約条件

### Payment Terms / 支払条件
- Implementation fees: 50% upon contract signing, 50% upon go-live
- 導入費用: 契約締結時に50%、稼働開始時に50%
- Monthly service fees: Invoiced monthly, net 30 days
- 月額サービス料: 月次請求、30日以内支払い

### Service Level Agreement / サービスレベル契約
- System availability: 99.5% (Standard), 99.9% (Premium)
- システム可用性: 99.5%（スタンダード）、99.9%（プレミアム）
- Response time: 4 hours (Standard), 1 hour (Premium)
- 応答時間: 4時間（スタンダード）、1時間（プレミアム）

### Data Security / データセキュリティ
- SOC 2 Type II certified
- SOC 2 Type II認証取得済み
- US data residency
- 米国データレジデンシー
- End-to-end encryption
- エンドツーエンド暗号化

### Contract Term / 契約期間
- Initial term: 12 months
- 初期契約期間: 12ヶ月
- Renewal: Auto-renewal with 90-day notice for cancellation
- 更新: 解約は90日前通知で自動更新
"""
    elif language == "english":
        return """## Terms & Conditions

### Payment Terms
- Implementation fees: 50% upon contract signing, 50% upon go-live
- Monthly service fees: Invoiced monthly, net 30 days

### Service Level Agreement
- System availability: 99.5% (Standard), 99.9% (Premium)
- Response time: 4 hours (Standard), 1 hour (Premium)

### Data Security
- SOC 2 Type II certified
- US data residency
- End-to-end encryption

### Contract Term
- Initial term: 12 months
- Renewal: Auto-renewal with 90-day notice for cancellation
"""
    else:
        return """## 契約条件

### 支払条件
- 導入費用: 契約締結時に50%、稼働開始時に50%
- 月額サービス料: 月次請求、30日以内支払い

### サービスレベル契約
- システム可用性: 99.5%（スタンダード）、99.9%（プレミアム）
- 応答時間: 4時間（スタンダード）、1時間（プレミアム）

### データセキュリティ
- SOC 2 Type II認証取得済み
- 米国データレジデンシー
- エンドツーエンド暗号化

### 契約期間
- 初期契約期間: 12ヶ月
- 更新: 解約は90日前通知で自動更新
"""


def generate_next_steps(language: str = "bilingual") -> str:
    """Generate next steps section."""
    if language == "bilingual":
        return """## Next Steps / 次のステップ

1. **Schedule Discovery Session / ディスカバリーセッションの設定**
   - 1-hour workshop to review requirements
   - 要件確認のための1時間ワークショップ

2. **Finalize Scope / スコープの最終化**
   - Confirm service selection and volumes
   - サービス選択と処理量の確認

3. **Contract Review / 契約レビュー**
   - Legal and procurement review
   - 法務・調達レビュー

4. **Project Kickoff / プロジェクトキックオフ**
   - Target: Within 2 weeks of contract signing
   - 目標: 契約締結後2週間以内

---

**Contact / お問い合わせ**

For questions about this proposal, please contact:
本提案に関するご質問は、以下までお問い合わせください：

*[Sales Representative Name / 営業担当者名]*
*[Email / メール]*
*[Phone / 電話]*
"""
    elif language == "english":
        return """## Next Steps

1. **Schedule Discovery Session**
   - 1-hour workshop to review requirements

2. **Finalize Scope**
   - Confirm service selection and volumes

3. **Contract Review**
   - Legal and procurement review

4. **Project Kickoff**
   - Target: Within 2 weeks of contract signing

---

**Contact**

For questions about this proposal, please contact:

*[Sales Representative Name]*
*[Email]*
*[Phone]*
"""
    else:
        return """## 次のステップ

1. **ディスカバリーセッションの設定**
   - 要件確認のための1時間ワークショップ

2. **スコープの最終化**
   - サービス選択と処理量の確認

3. **契約レビュー**
   - 法務・調達レビュー

4. **プロジェクトキックオフ**
   - 目標: 契約締結後2週間以内

---

**お問い合わせ**

本提案に関するご質問は、以下までお問い合わせください：

*[営業担当者名]*
*[メール]*
*[電話]*
"""


def generate_proposal(
    client_name: str,
    services_file: str | None = None,
    roi_file: str | None = None,
    roadmap_file: str | None = None,
    language: str = "bilingual",
    output_path: str | None = None,
) -> str:
    """
    Generate complete proposal document.

    Args:
        client_name: Client company name
        services_file: Path to services JSON
        roi_file: Path to ROI JSON
        roadmap_file: Path to roadmap JSON
        language: Output language ('english', 'japanese', 'bilingual')
        output_path: Output file path

    Returns:
        Generated proposal as markdown string
    """
    # Load data files
    services_data = load_json_file(services_file) if services_file else {"selected_services": []}
    roi_data = load_json_file(roi_file) if roi_file else {}
    roadmap_data = load_json_file(roadmap_file) if roadmap_file else {}

    services = services_data.get("selected_services", [])

    # Generate document
    today = datetime.now().strftime("%Y-%m-%d")

    if language == "bilingual":
        title = f"# AI-BPO Service Proposal / AI-BPOサービス提案書\n\n**Client / お客様**: {client_name}\n\n**Date / 日付**: {today}\n\n**Version / バージョン**: 1.0\n"
    elif language == "english":
        title = f"# AI-BPO Service Proposal\n\n**Client**: {client_name}\n\n**Date**: {today}\n\n**Version**: 1.0\n"
    else:
        title = f"# AI-BPOサービス提案書\n\n**お客様**: {client_name}\n\n**日付**: {today}\n\n**バージョン**: 1.0\n"

    sections = [
        title,
        "---\n",
        generate_executive_summary(client_name, services, roi_data, roadmap_data, language),
        generate_services_section(services, language),
        generate_roi_section(roi_data, language),
        generate_roadmap_section(roadmap_data, language),
        generate_terms_section(language),
        generate_next_steps(language),
    ]

    proposal = "\n".join(sections)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(proposal)
        print(f"Proposal saved to: {output_path}", file=sys.stderr)

    return proposal


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate bilingual AI-BPO proposal document")
    parser.add_argument(
        "--client-name",
        required=True,
        help="Client company name",
    )
    parser.add_argument(
        "--services",
        help="Path to services JSON file",
    )
    parser.add_argument(
        "--roi",
        help="Path to ROI JSON file",
    )
    parser.add_argument(
        "--roadmap",
        help="Path to roadmap JSON file",
    )
    parser.add_argument(
        "--language",
        choices=["english", "japanese", "bilingual"],
        default="bilingual",
        help="Output language (default: bilingual)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output markdown file path",
    )

    args = parser.parse_args()

    proposal = generate_proposal(
        client_name=args.client_name,
        services_file=args.services,
        roi_file=args.roi,
        roadmap_file=args.roadmap,
        language=args.language,
        output_path=args.output,
    )

    print(proposal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
