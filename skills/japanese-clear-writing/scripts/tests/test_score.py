"""Tests for score.py: rubric totals, rescaling, verdicts, and input errors."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import score  # noqa: E402


def run(capsys, *args):
    code = score.main(list(args))
    out, err = capsys.readouterr()
    return code, out, err


@pytest.mark.parametrize(
    "value, expected",
    [
        (100, "そのまま使いやすい"),
        (90, "そのまま使いやすい"),
        (89.9, "概ね明瞭"),
        (75, "概ね明瞭"),
        (74.9, "要改善"),
        (60, "要改善"),
        (59.9, "大幅な再構成を推奨"),
        (0, "大幅な再構成を推奨"),
    ],
)
def test_verdict_boundaries(value, expected):
    assert score.verdict(value) == expected


def test_weights_total_100():
    assert sum(w for _, w in score.ITEMS) == 100


def test_full_score(capsys):
    code, out, _ = run(capsys, "5", "5", "5", "5", "5", "5")
    assert code == 0
    assert "合計：100.0 / 100" in out
    assert "判定：そのまま使いやすい" in out
    assert "換算" not in out


def test_mixed_score(capsys):
    # 16 + 12 + 12 + 15 + 12 + 8 = 75
    code, out, _ = run(capsys, "4", "3", "3", "5", "4", "4")
    assert code == 0
    assert "合計：75.0 / 100" in out
    assert "判定：概ね明瞭" in out


def test_unrated_item_rescales_remaining_weight(capsys):
    # 16 + 12 + 15 + 12 + 8 = 63 over 80 points -> 78.75
    code, out, _ = run(capsys, "4", "3", "-", "5", "4", "4")
    assert code == 0
    assert "曖昧さ・正確さ：判定材料不足 / 20" in out
    assert "合計：78.8 / 100" in out
    assert "5項目で換算。配点 80 点分を100点に換算" in out


def test_decimal_points_are_accepted(capsys):
    code, out, _ = run(capsys, "4.5", "5", "5", "5", "5", "5")
    assert code == 0
    assert "（4.5/5）" in out


@pytest.mark.parametrize(
    "args",
    [
        ("4", "3", "3", "5", "4"),
        ("4", "3", "3", "5", "4", "4", "4"),
        ("4", "3", "x", "5", "4", "4"),
        ("4", "3", "6", "5", "4", "4"),
        ("4", "3", "-1", "5", "4", "4"),
        ("nan", "3", "3", "5", "4", "4"),
        ("-", "-", "-", "-", "-", "-"),
    ],
)
def test_invalid_input_returns_2(capsys, args):
    code, out, err = run(capsys, *args)
    assert code == 2
    assert err
    assert "合計" not in out
