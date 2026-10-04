"""Tests for build_dashboard: ticket parsing, column collection, and the CLI."""

import os
import subprocess
import sys
from datetime import datetime

import pytest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, SCRIPTS_DIR)

import build_dashboard as bd  # noqa: E402

SCRIPT = os.path.join(SCRIPTS_DIR, "build_dashboard.py")
NOW = datetime(2026, 10, 4, 12, 0)


def write(path, text=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return str(path)


def make_tasks(tmp_path):
    root = tmp_path / "tasks"
    for sub in ("todo", "doing", "blocked", "done"):
        (root / sub).mkdir(parents=True)
    return root


# --- parse_task -------------------------------------------------------------


def test_parse_task_reads_name_fields_and_sections(tmp_path):
    path = write(
        tmp_path / "20261001_2_売上集計.md",
        "# 売上を集計する\n\n- 目的: 月次報告\n- 外部操作: 不可   # comment\n- 開始: 2026-10-01 09:00\n\n## 結果\n完了しました\n\n## 実行ログ\n- 2026-10-01 09:05 done / ok\n",
    )
    t = bd.parse_task(path)
    assert t["title"] == "売上を集計する"
    assert t["date"] == datetime(2026, 10, 1)
    assert t["prio"] == 2
    assert t["purpose"] == "月次報告"
    assert t["external"] == "不可"
    assert t["result"] == ["完了しました"]


def test_parse_task_falls_back_to_file_name_for_title(tmp_path):
    t = bd.parse_task(write(tmp_path / "20261001_1_件名だけ.md"))
    assert t["title"] == "件名だけ"


def test_parse_task_without_date_prefix(tmp_path):
    t = bd.parse_task(write(tmp_path / "日付なし.md", "# x\n"))
    assert t["date"] is None


@pytest.mark.parametrize("name", ["20261399_1_bad.md", "20260230_1_feb30.md", "00000000_1_zero.md"])
def test_parse_task_treats_invalid_date_prefix_as_no_date(tmp_path, name):
    t = bd.parse_task(write(tmp_path / name, "# 不正な日付\n"))
    assert t["date"] is None
    assert t["title"] == "不正な日付"


# --- parse_dt ---------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2026-10-04 09:30", datetime(2026, 10, 4, 9, 30)),
        ("2026-10-04 09:30:15", datetime(2026, 10, 4, 9, 30, 15)),
        ("2026-10-04", datetime(2026, 10, 4)),
        ("", None),
        (None, None),
        ("not a date", None),
    ],
)
def test_parse_dt(value, expected):
    assert bd.parse_dt(value) == expected


# --- collect ----------------------------------------------------------------


def test_collect_marks_future_stale_and_plan_wait(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "20261010_1_future.md", "# future\n")
    write(root / "todo" / "20261001_1_due.md", "# due\n")
    write(root / "doing" / "20261001_1_stuck.md", "# stuck\n- 開始: 2026-10-04 10:00\n")
    write(root / "blocked" / "20261001_1_wait.md", "# wait\n\n## 結果\n計画の確認待ち: 外部操作あり\n")

    data, _, _ = bd.collect(str(root), NOW, 14)

    future = {t["title"]: t["future"] for t in data["todo"]}
    assert future == {"future": True, "due": False}
    assert data["doing"][0]["stale"] is True
    assert data["blocked"][0]["plan_wait"] is True


def test_collect_ignores_underscore_files(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "_template.md", "# template\n")
    data, _, _ = bd.collect(str(root), NOW, 14)
    assert data["todo"] == []


def test_collect_survives_invalid_date_ticket(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "20261399_1_bad.md", "# bad\n")
    data, _, _ = bd.collect(str(root), NOW, 14)
    assert [t["title"] for t in data["todo"]] == ["bad"]
    assert data["todo"][0]["future"] is False


# --- render / CLI -----------------------------------------------------------


def test_render_escapes_html_in_titles(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "20261001_1_x.md", "# <script>alert(1)</script>\n")
    page = bd.render(str(root), NOW, 14)
    assert "<script>alert(1)</script>" not in page
    assert "&lt;script&gt;" in page


def run_cli(*args):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)


def test_cli_writes_dashboard(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "20261001_1_x.md", "# x\n")
    res = run_cli(str(root), "--now", "2026-10-04 12:00")
    assert res.returncode == 0, res.stderr
    assert (root / "dashboard.html").is_file()


def test_cli_dashboard_survives_invalid_date_ticket(tmp_path):
    root = make_tasks(tmp_path)
    write(root / "todo" / "20261399_1_bad.md", "# bad\n")
    res = run_cli(str(root), "--now", "2026-10-04 12:00")
    assert res.returncode == 0, res.stderr
    assert "bad" in (root / "dashboard.html").read_text(encoding="utf-8")


def test_cli_rejects_invalid_now_with_clear_error(tmp_path):
    root = make_tasks(tmp_path)
    res = run_cli(str(root), "--now", "yesterday")
    assert res.returncode != 0
    assert "Traceback" not in res.stderr
    assert "--now" in res.stderr


def test_cli_missing_tasks_dir(tmp_path):
    res = run_cli(str(tmp_path / "nope"))
    assert res.returncode != 0
    assert "Traceback" not in res.stderr
