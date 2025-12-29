#!/usr/bin/env python3
"""
Perspective Combiner

観点組み合わせフレームワークを使用して
新しい検証観点を創出する。
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import itertools


class PerspectiveCategory(Enum):
    """観点カテゴリ"""
    TEMPORAL = ("T", "時間的", "時系列、ライフサイクル")
    RELATIONAL = ("R", "関係的", "親子、兄弟、ネットワーク")
    QUANTITATIVE = ("Q", "数量的", "件数、比率、分布")
    GEOGRAPHIC = ("G", "地理的", "地域、オフィス")
    ROLE = ("O", "役割的", "所有者、部門")
    SOURCE = ("S", "ソース的", "データ元システム")
    STATE = ("ST", "状態的", "ステータス、ステージ")
    SEMANTIC = ("SE", "意味的", "タイプ、カテゴリ")

    def __init__(self, code: str, japanese: str, description: str):
        self.code = code
        self.japanese = japanese
        self.description = description


class CombinationOperator(Enum):
    """組み合わせ演算子"""
    AND = ("AND", "両方の観点が一致する必要")
    XOR = ("XOR", "観点が異なるべき（不整合検出）")
    SEQUENCE = ("SEQ", "一方が他方に先行")
    REQUIRES = ("REQ", "依存関係")

    def __init__(self, symbol: str, description: str):
        self.symbol = symbol
        self.description = description


@dataclass
class CombinedPerspective:
    """組み合わせ観点"""
    perspective_a: PerspectiveCategory
    perspective_b: PerspectiveCategory
    operator: CombinationOperator
    name: str
    description: str
    validation_focus: str
    example_query: Optional[str] = None


# 既知の有効な組み合わせパターン
KNOWN_COMBINATIONS: List[CombinedPerspective] = [
    CombinedPerspective(
        perspective_a=PerspectiveCategory.SOURCE,
        perspective_b=PerspectiveCategory.RELATIONAL,
        operator=CombinationOperator.AND,
        name="クロスソース参照整合性",
        description="異なるソースからの参照が正しく解決されるか",
        validation_focus="Property参照、Account参照のソース横断検証",
        example_query="source_a.property_id IN (SELECT id FROM source_b.properties)"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.GEOGRAPHIC,
        perspective_b=PerspectiveCategory.ROLE,
        operator=CombinationOperator.XOR,
        name="地理-所有者整合性",
        description="地域と所有者の割当が矛盾していないか",
        validation_focus="CAの物件にNYマネージャーが割当されていないか",
        example_query="property.state != owner.office_location"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.TEMPORAL,
        perspective_b=PerspectiveCategory.STATE,
        operator=CombinationOperator.SEQUENCE,
        name="ライフサイクル状態遷移",
        description="ステータス変更が時系列で妥当か",
        validation_focus="Closed Wonに必要なフィールドが揃っているか",
        example_query="stage = 'Closed Won' AND close_date IS NULL"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.SOURCE,
        perspective_b=PerspectiveCategory.SEMANTIC,
        operator=CombinationOperator.AND,
        name="ソース-RecordType整合性",
        description="データソースとRecordTypeの組み合わせが妥当か",
        validation_focus="ExRentソースがExpat Housing以外になっていないか",
        example_query="source = 'ExRent' AND record_type != 'Expat Housing'"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.ROLE,
        perspective_b=PerspectiveCategory.SOURCE,
        operator=CombinationOperator.AND,
        name="部門-エンティティ整合性",
        description="フォールバック所有者が正しい部門か",
        validation_focus="Commercialの物件にResidentialマネージャーが割当されていないか",
        example_query="entity_type = 'Commercial' AND owner.department = 'Residential'"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.RELATIONAL,
        perspective_b=PerspectiveCategory.RELATIONAL,
        operator=CombinationOperator.REQUIRES,
        name="Renewal連鎖完全性",
        description="更新Opportunityが親に正しくリンクされているか",
        validation_focus="Renewal Opportunityの親Opportunity存在確認",
        example_query="is_renewal = TRUE AND parent_opportunity_id IS NULL"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.SEMANTIC,
        perspective_b=PerspectiveCategory.RELATIONAL,
        operator=CombinationOperator.XOR,
        name="Contact RecordType-Deal整合性",
        description="ContactタイプとOpportunityタイプの組み合わせが妥当か",
        validation_focus="ExpatがIVP取引を持っていないか",
        example_query="contact.record_type = 'Expat' AND opportunity.type = 'IVP'"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.QUANTITATIVE,
        perspective_b=PerspectiveCategory.SOURCE,
        operator=CombinationOperator.AND,
        name="クロスソース属性整合性",
        description="同一エンティティの属性がソース間で一致するか",
        validation_focus="同一物件の属性がソース間で一致するか",
        example_query="source_a.property_name != source_b.property_name WHERE id = id"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.QUANTITATIVE,
        perspective_b=PerspectiveCategory.STATE,
        operator=CombinationOperator.REQUIRES,
        name="金額-ステージ相関",
        description="ステージに応じた金額の妥当性",
        validation_focus="Closed Wonに金額が設定されているか",
        example_query="stage = 'Closed Won' AND (amount IS NULL OR amount = 0)"
    ),
    CombinedPerspective(
        perspective_a=PerspectiveCategory.RELATIONAL,
        perspective_b=PerspectiveCategory.RELATIONAL,
        operator=CombinationOperator.REQUIRES,
        name="カスケード参照整合性",
        description="多段階の参照が全て有効か",
        validation_focus="Opp→Account→Parent Accountが全て存在するか",
        example_query="opportunity.account_id EXISTS AND account.parent_id EXISTS"
    )
]


# CRM移行の落とし穴（ベストプラクティスナレッジベース）
CRM_MIGRATION_PITFALLS = [
    ("A1", "重複レコード", "ファジーマッチング失敗による重複"),
    ("A2", "孤児レコード", "参照先が存在しないレコード"),
    ("A3", "必須フィールド空白", "Salesforce必須フィールドの欠損"),
    ("A4", "データ型不一致", "型変換エラー"),
    ("A5", "Picklist値不一致", "メタデータ同期漏れ"),
    ("A6", "文字エンコーディング問題", "Unicode/特殊文字の破損"),
    ("A7", "日付フォーマット不整合", "タイムゾーン/形式差異"),
    ("B1", "External ID設定ミス", "一意性制約違反"),
    ("B2", "インポート順序違反", "依存関係の見落とし"),
    ("B3", "Lookup解決失敗", "大文字小文字/スペース差異"),
    ("B4", "循環参照", "自己参照や相互参照"),
    ("C1", "OwnerId割当エラー", "無効なUser ID"),
    ("C2", "RecordType誤割当", "ビジネスルール違反"),
    ("C3", "履歴データ破損", "変更履歴の欠損"),
    ("C4", "金額/収益不整合", "通貨換算/税計算エラー"),
    ("C5", "ステータスマッピングエラー", "ステージ/ステータスの誤変換"),
]


# 不動産業界固有の問題
REAL_ESTATE_PITFALLS = [
    ("D1", "住所標準化バリエーション", "同一住所の複数表記"),
    ("D2", "ユニット番号の曖昧さ", "Apt/Unit/#の混在"),
    ("D3", "物件名の不整合", "名称変更/略称の混在"),
    ("D4", "複数ユニット建物", "建物vsユニットレベルの混同"),
    ("D5", "住宅/商業の分類", "混合用途物件の扱い"),
    ("E1", "リース期間の断片化", "更新/延長の分離"),
    ("E2", "Renewal連鎖の切断", "更新履歴の欠損"),
    ("E3", "同一物件の複数取引タイプ", "Sale/Rent/Leaseの混在"),
    ("E4", "コミッション計算エラー", "分配率/計算ロジックの不整合"),
    ("F1", "テナント/オーナー/投資家の混同", "役割の誤分類"),
    ("F2", "エージェント/パートナーの混同", "内部/外部の区別"),
    ("F3", "親子会社の合併", "企業グループの扱い"),
]


def generate_new_perspective(
    exclude_categories: Optional[List[PerspectiveCategory]] = None
) -> CombinedPerspective:
    """
    ランダムに新しい観点の組み合わせを生成

    Args:
        exclude_categories: 除外するカテゴリ

    Returns:
        新しいCombinedPerspective
    """
    categories = list(PerspectiveCategory)
    if exclude_categories:
        categories = [c for c in categories if c not in exclude_categories]

    if len(categories) < 2:
        categories = list(PerspectiveCategory)

    perspective_a, perspective_b = random.sample(categories, 2)
    operator = random.choice(list(CombinationOperator))

    return CombinedPerspective(
        perspective_a=perspective_a,
        perspective_b=perspective_b,
        operator=operator,
        name=f"{perspective_a.japanese}×{perspective_b.japanese}",
        description=f"{perspective_a.description}と{perspective_b.description}の組み合わせ検証",
        validation_focus=f"要検討: {operator.description}の関係を持つケースを検証"
    )


def select_pitfall_combination() -> Tuple[Tuple, Tuple]:
    """
    CRM移行と不動産業界の落とし穴から組み合わせを選択

    Returns:
        (CRM pitfall, Real estate pitfall) のタプル
    """
    crm_pitfall = random.choice(CRM_MIGRATION_PITFALLS)
    real_estate_pitfall = random.choice(REAL_ESTATE_PITFALLS)
    return crm_pitfall, real_estate_pitfall


def generate_perspective_from_pitfalls(
    crm_pitfall: Tuple,
    real_estate_pitfall: Tuple
) -> Dict[str, str]:
    """
    落とし穴の組み合わせから新しい検証観点を生成

    Args:
        crm_pitfall: CRM移行の落とし穴
        real_estate_pitfall: 不動産業界の落とし穴

    Returns:
        新しい検証観点の辞書
    """
    return {
        "source_crm": f"{crm_pitfall[0]}: {crm_pitfall[1]}",
        "source_real_estate": f"{real_estate_pitfall[0]}: {real_estate_pitfall[1]}",
        "combined_perspective": f"{crm_pitfall[1]} + {real_estate_pitfall[1]}",
        "validation_approach": f"""
            CRMの「{crm_pitfall[2]}」問題が、
            不動産の「{real_estate_pitfall[2]}」と組み合わさった場合の検証
        """.strip(),
        "suggested_checks": [
            f"{crm_pitfall[1]}の観点から{real_estate_pitfall[1]}を検証",
            f"{real_estate_pitfall[1]}のデータで{crm_pitfall[1]}の問題を探す"
        ]
    }


def get_all_perspective_combinations() -> List[Tuple[PerspectiveCategory, PerspectiveCategory, CombinationOperator]]:
    """
    すべての可能な観点組み合わせを生成

    Returns:
        (観点A, 観点B, 演算子) のタプルリスト
    """
    combinations = []
    for a, b in itertools.combinations(PerspectiveCategory, 2):
        for op in CombinationOperator:
            combinations.append((a, b, op))
    return combinations


def print_perspective_catalog():
    """既知の観点組み合わせカタログを表示"""
    print("=" * 80)
    print("観点組み合わせカタログ")
    print("=" * 80)

    for i, combo in enumerate(KNOWN_COMBINATIONS, 1):
        print(f"\n[{i}] {combo.name}")
        print(f"    組み合わせ: {combo.perspective_a.japanese} {combo.operator.symbol} {combo.perspective_b.japanese}")
        print(f"    説明: {combo.description}")
        print(f"    検証対象: {combo.validation_focus}")
        if combo.example_query:
            print(f"    クエリ例: {combo.example_query}")


def print_pitfall_catalog():
    """落とし穴カタログを表示"""
    print("=" * 80)
    print("CRM移行の落とし穴")
    print("=" * 80)
    for code, name, desc in CRM_MIGRATION_PITFALLS:
        print(f"  {code}: {name} - {desc}")

    print("\n" + "=" * 80)
    print("不動産業界固有の問題")
    print("=" * 80)
    for code, name, desc in REAL_ESTATE_PITFALLS:
        print(f"  {code}: {name} - {desc}")


if __name__ == "__main__":
    print("Perspective Combiner - 観点組み合わせフレームワーク")
    print()

    # 既知の組み合わせカタログを表示
    print_perspective_catalog()

    print("\n" + "=" * 80)
    print("ランダム生成された新観点")
    print("=" * 80)

    # ランダムに新観点を生成
    for i in range(3):
        new_perspective = generate_new_perspective()
        print(f"\n[New {i+1}] {new_perspective.name}")
        print(f"    演算子: {new_perspective.operator.symbol}")
        print(f"    説明: {new_perspective.description}")

    print("\n" + "=" * 80)
    print("落とし穴組み合わせから生成された観点")
    print("=" * 80)

    # 落とし穴の組み合わせから観点を生成
    crm, re = select_pitfall_combination()
    new_viewpoint = generate_perspective_from_pitfalls(crm, re)

    print(f"\n  CRM元: {new_viewpoint['source_crm']}")
    print(f"  不動産元: {new_viewpoint['source_real_estate']}")
    print(f"  新観点: {new_viewpoint['combined_perspective']}")
    print(f"  検証アプローチ: {new_viewpoint['validation_approach']}")
