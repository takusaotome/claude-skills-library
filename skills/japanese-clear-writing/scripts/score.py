#!/usr/bin/env python3
"""ルーブリックの合計点と判定を計算する。

使い方:
    python3 score.py 4 3 3 5 4 4        # 6項目を表の順に指定（各0〜5）
    python3 score.py 4 3 - 5 4 4        # 判定材料不足の項目は - にする

項目の順序:
    目的・構成(20) / 文の明瞭さ(20) / 曖昧さ・正確さ(20)
    用語の一貫性(15) / 読み手適合性(15) / 表記・視認性(10)

- 各項目は 項目点 / 5 * 配点 で換算する。
- "-" の項目は除外し、残りの配点で100点満点に換算する。
- 結果は小数第1位で四捨五入して表示する。
"""

import sys

ITEMS = [
    ("目的・構成", 20),
    ("文の明瞭さ", 20),
    ("曖昧さ・正確さ", 20),
    ("用語の一貫性", 15),
    ("読み手適合性", 15),
    ("表記・視認性", 10),
]


def verdict(score: float) -> str:
    if score >= 90:
        return "そのまま使いやすい"
    if score >= 75:
        return "概ね明瞭"
    if score >= 60:
        return "要改善"
    return "大幅な再構成を推奨"


def main(argv):
    if len(argv) != len(ITEMS):
        print(f"6項目を指定してください（0〜5、または -）。受け取った数: {len(argv)}", file=sys.stderr)
        return 2

    rows = []
    for (name, weight), raw in zip(ITEMS, argv):
        if raw == "-":
            rows.append((name, weight, None))
            continue
        try:
            value = float(raw)
        except ValueError:
            print(f"数値ではありません: {raw!r}（{name}）", file=sys.stderr)
            return 2
        if not 0 <= value <= 5:
            print(f"0〜5の範囲で指定してください: {raw}（{name}）", file=sys.stderr)
            return 2
        rows.append((name, weight, value))

    scored = [(n, w, v) for n, w, v in rows if v is not None]
    if not scored:
        print("採点できる項目がありません。", file=sys.stderr)
        return 2

    used_weight = sum(w for _, w, _ in scored)
    raw_total = sum(v / 5 * w for _, w, v in scored)
    total = raw_total / used_weight * 100

    for name, weight, value in rows:
        if value is None:
            print(f"- {name}：判定材料不足 / {weight}")
        else:
            print(f"- {name}：{value / 5 * weight:.1f} / {weight}（{value:g}/5）")

    print()
    print(f"合計：{total:.1f} / 100")
    if used_weight != 100:
        print(f"（{len(scored)}項目で換算。配点 {used_weight} 点分を100点に換算）")
    print(f"判定：{verdict(total)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
