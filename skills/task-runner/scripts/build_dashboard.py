#!/usr/bin/env python3
"""task-runner の tasks/ フォルダを読み、看板ボード形式のダッシュボード HTML を生成する。

使い方:
    python3 build_dashboard.py [tasksフォルダのパス] [--out 出力先] [--done-days 日数]

- 既定の tasks フォルダ: ./tasks
- 既定の出力先: <tasks>/dashboard.html
- 読み取り専用。タスクファイルには一切書き込まない。
- 外部ライブラリ・外部CDN不要（標準ライブラリのみ、HTMLは単一ファイルで完結）。
- タスクに `## 計画カード` があれば、カードを押したときに図解つきの計画カードを表示する。
"""

import argparse
import html
import os
import re
import sys
from datetime import datetime, timedelta

COLUMNS = [
    ("todo", "未着手", "todo"),
    ("doing", "実行中", "doing"),
    ("blocked", "要確認", "blocked"),
    ("done", "完了", "done"),
]
STALE_MINUTES = 60
FIELD_RE = re.compile(r"^\s*[-*]\s*([^:：]+)[:：]\s*(.*)$")
ITEM_RE = re.compile(r"^\s*[-*]\s*(?:\[([^\]]*)\]\s*)?(.*)$")
NAME_RE = re.compile(r"^(\d{8})?_?(\d+)?_?(.*)$")
PLAN_WAIT_PREFIX = "計画の確認待ち"
# `- 確認してほしいこと: なし` を「確認点1件」と数えないための語
NONE_WORDS = {"なし", "特になし", "ありません", "特にありません", "-", "ー", "—"}

# 計画カードの「進め方」タグ → 図の種類
STEP_KINDS = {
    "読む": "read",
    "作る": "make",
    "確かめる": "check",
    "確認": "check",
    "外部": "ext",
    "外に触れる": "ext",
    "止まる": "stop",
}
STEP_LABELS = {"read": "読む", "make": "作る", "check": "確かめる", "ext": "外に触れる", "stop": "止まる"}
# 計画カードの「外に触れること」タグ → 記号
EXT_KINDS = {"する": "y", "しない": "n", "保存": "a"}
EXT_MARKS = {"y": "!", "n": "×", "a": "✓"}

ICONS = {
    "read": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "make": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "check": '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    "ext": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14L21 3"/>',
    "stop": '<rect x="6" y="6" width="12" height="12" rx="2"/>',
}


def parse_dt(value):
    value = (value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def parse_name_date(date_str):
    # 存在しない日付（13月、2月30日など）は日付なしとして扱い、ボード全体を落とさない
    try:
        return datetime.strptime(date_str, "%Y%m%d") if date_str else None
    except ValueError:
        return None


def strip_comment(value):
    # "不可   # メール送信..." のようなインラインコメントを除く
    return re.split(r"\s+#", value, maxsplit=1)[0].strip()


def parse_plan(lines):
    """`## 計画カード` の本文を dict にする。書式が崩れていても落ちずに読める範囲だけ返す。

    トップレベルは `- 見出し: 値`、その下の字下げした `- [タグ] 本文` を項目として読む。
    """
    raw = {}
    key = None
    for line in lines:
        if not line.strip():
            continue
        if not line[:1].isspace():
            fm = FIELD_RE.match(line)
            if not fm:
                key = None
                continue
            key = fm.group(1).strip()
            value = fm.group(2).strip()
            raw[key] = value if value else []
        elif key is not None:
            im = ITEM_RE.match(line)
            if not im or not im.group(2).strip():
                continue
            if not isinstance(raw.get(key), list):
                raw[key] = []
            raw[key].append(((im.group(1) or "").strip(), im.group(2).strip()))
    if not raw:
        return None

    def items(name):
        # `- 確認してほしいこと: 〇〇` のように1行で書かれても、1項目として拾う（黙って消さない）
        value = raw.get(name)
        if isinstance(value, list):
            return [item for item in value if item[1] not in NONE_WORDS]
        if value and value not in NONE_WORDS:
            im = ITEM_RE.match("- " + value)
            return [((im.group(1) or "").strip(), im.group(2).strip())] if im and im.group(2).strip() else []
        return []

    goal = raw.get("やること")
    return {
        "goal": goal if isinstance(goal, str) else "",
        "steps": [(STEP_KINDS.get(tag, "make"), text) for tag, text in items("進め方")],
        "ext": [(EXT_KINDS.get(tag, "a"), text) for tag, text in items("外に触れること")],
        "assume": [text for _, text in items("前提")],
        "review": [text for _, text in items("確認してほしいこと")],
        "done": [(tag.lower() == "x", text) for tag, text in items("終わりの条件")],
    }


def parse_task(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        text = ""

    base = os.path.basename(path)[:-3]
    m = NAME_RE.match(base)
    date_str, prio, rest = (m.group(1), m.group(2), m.group(3)) if m else (None, None, base)

    title = None
    fields = {}
    sections = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
            continue
        if title is None and line.startswith("# "):
            title = line[2:].strip()
            continue
        fm = FIELD_RE.match(line)
        if fm:
            fields[fm.group(1).strip()] = strip_comment(fm.group(2))

    result_lines = [l.strip() for l in sections.get("結果", []) if l.strip()]
    log_lines = [l.strip().lstrip("-* ").strip() for l in sections.get("実行ログ", []) if l.strip()]

    return {
        "file": base + ".md",
        "title": title or rest or base,
        "date": parse_name_date(date_str),
        "prio": int(prio) if prio else None,
        "purpose": fields.get("目的", ""),
        "external": fields.get("外部操作", ""),
        "output": fields.get("出力先", ""),
        "started": parse_dt(fields.get("開始")),
        "finished": parse_dt(fields.get("完了")),
        "result": result_lines,
        "last_log": log_lines[-1] if log_lines else "",
        "plan": parse_plan(sections.get("計画カード", [])),
        "mtime": datetime.fromtimestamp(os.path.getmtime(path)),
    }


def list_md(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(os.path.join(folder, n) for n in os.listdir(folder) if n.endswith(".md") and not n.startswith("_"))


def collect(tasks_dir, now, done_days):
    data = {key: [] for key, _, _ in COLUMNS}
    for key in ("todo", "doing", "blocked"):
        data[key] = [parse_task(p) for p in list_md(os.path.join(tasks_dir, key))]

    done_all = []
    done_root = os.path.join(tasks_dir, "done")
    if os.path.isdir(done_root):
        for month in sorted(os.listdir(done_root)):
            sub = os.path.join(done_root, month)
            if os.path.isdir(sub):
                done_all += [parse_task(p) for p in list_md(sub)]
    cutoff = now - timedelta(days=done_days)
    for t in done_all:
        t["_when"] = t["finished"] or t["mtime"]
    done_all.sort(key=lambda t: t["_when"], reverse=True)
    data["done"] = [t for t in done_all if t["_when"] >= cutoff]

    # todo は実行順（ファイル名昇順）。未来日付は「予定」扱い
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    for t in data["todo"]:
        t["future"] = bool(t["date"] and t["date"] > today)
    for t in data["doing"]:
        t["stale"] = bool(t["started"] and now - t["started"] > timedelta(minutes=STALE_MINUTES))
    for t in data["blocked"]:
        t["plan_wait"] = bool(t["result"] and t["result"][0].lstrip("-* ").startswith(PLAN_WAIT_PREFIX))

    done_this_month = sum(1 for t in done_all if t["_when"].strftime("%Y-%m") == now.strftime("%Y-%m"))
    return data, len(done_all), done_this_month


def read_config_mode(tasks_dir):
    path = os.path.join(tasks_dir, "_config.md")
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\s*mode\s*:\s*(\S+)", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return "dry-run"


def read_log(tasks_dir, n=8):
    path = os.path.join(tasks_dir, "log.md")
    try:
        with open(path, encoding="utf-8") as f:
            lines = [l.strip()[2:].strip() for l in f if l.strip().startswith("- ")]
    except OSError:
        return []
    return lines[-n:][::-1]


def esc(s):
    return html.escape(str(s or ""))


def short(s, n=90):
    s = str(s or "")
    return s if len(s) <= n else s[: n - 1] + "…"


def fmt_dt(d, with_time=True):
    if not d:
        return ""
    return d.strftime("%m/%d %H:%M" if with_time else "%m/%d")


def open_review_count(t, col):
    """人が判断すべき点の数。完了したタスクでは数えない。"""
    if col == "done" or not t.get("plan"):
        return 0
    return len(t["plan"]["review"])


def render_flow(steps):
    parts = []
    for i, (kind, text) in enumerate(steps):
        arrow = '<span class="arrow" aria-hidden="true">→</span>' if i < len(steps) - 1 else ""
        parts.append(
            f'<div class="step"><div class="node {kind}" title="{STEP_LABELS[kind]}">'
            f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[kind]}</svg>'
            f"<span>{esc(text)}</span></div>{arrow}</div>"
        )
    used = [k for k in STEP_LABELS if any(s[0] == k for s in steps)]
    legend = "".join(f'<span><i class="sw {k}"></i>{STEP_LABELS[k]}</span>' for k in used)
    return f'<div class="flow">{"".join(parts)}</div><div class="legend">{legend}</div>'


def render_detail(t, col, col_label, idx):
    """カードを押したときに開く計画カード。<template> に入れておき、JS が表示する。"""
    plan = t.get("plan")
    blocks = []

    if col == "blocked" and t["result"]:
        kind = "wait" if t.get("plan_wait") else "stop"
        rest = "".join(f"<p>{esc(l.lstrip('-* '))}</p>" for l in t["result"][1:4])
        blocks.append(f'<div class="banner {kind}"><b>{esc(t["result"][0].lstrip("-* "))}</b>{rest}</div>')
    elif col == "done":
        first = esc(t["result"][0].lstrip("-* ")) if t["result"] else "完了しました"
        blocks.append(f'<div class="banner done"><b>完了しました</b><p>{first}</p></div>')
    elif col == "todo" and t.get("future"):
        blocks.append(
            f'<div class="banner wait"><b>{fmt_dt(t["date"], False)} から実行対象になります</b>'
            "<p>それまでは選ばれません。</p></div>"
        )
    elif col == "doing" and t.get("stale"):
        blocks.append(
            '<div class="banner stop"><b>停止の疑いがあります</b>'
            f"<p>開始 {fmt_dt(t['started'])} から{STALE_MINUTES}分以上たっています。</p></div>"
        )

    goal = (plan and plan["goal"]) or t["purpose"]
    if goal:
        blocks.append(f'<p class="goal"><small>このタスクでやること</small>{esc(goal)}</p>')

    if plan:
        review = plan["review"] if col != "done" else []
        if review:
            items = "".join(f"<li>{esc(r)}</li>" for r in review)
            how = (
                f"問題なければ、アプリで「{esc(t['title'])} OK」と伝えてください。"
                "答えがあれば一緒に書いてください（例: 「社内メールも含めて OK」）。"
                if t.get("plan_wait")
                else "気になる点があれば、タスクに書き足してください。"
            )
            blocks.append(
                f'<section class="review"><h4>あなたに確認してほしいこと（{len(review)}点）</h4>'
                f'<ol>{items}</ol><p class="how">{how}</p></section>'
            )
        if plan["steps"]:
            blocks.append(f'<section class="sec"><h4>進め方</h4>{render_flow(plan["steps"])}</section>')
        ext = (
            "".join(f'<li><span class="mk {k}">{EXT_MARKS[k]}</span><span>{esc(x)}</span></li>' for k, x in plan["ext"])
            or '<li class="empty-li">書かれていません</li>'
        )
        assume = (
            "".join(f'<li><span class="mk q">?</span><span>{esc(a)}</span></li>' for a in plan["assume"])
            or '<li class="empty-li">なし</li>'
        )
        blocks.append(
            f'<div class="two"><section class="box"><h4>外に触れること</h4><ul>{ext}</ul></section>'
            f'<section class="box"><h4>AI が決めた前提</h4><ul>{assume}</ul></section></div>'
        )
        if plan["done"]:
            checks = "".join(
                f'<li class="{"on" if ok else ""}"><span class="cb">{"✓" if ok else ""}</span>{esc(x)}</li>'
                for ok, x in plan["done"]
            )
            blocks.append(f'<section class="box checks"><h4>終わりの条件</h4><ul>{checks}</ul></section>')
    else:
        blocks.append(
            '<p class="noplan">計画カードはまだありません。「このタスクどう進めるの？」と頼むと作ります。</p>'
        )

    info = []
    if t["output"]:
        info.append(f"<dt>出力先</dt><dd>{esc(t['output'])}</dd>")
    if t["external"]:
        info.append(f"<dt>外部操作</dt><dd>{esc(t['external'])}</dd>")
    if col in ("done", "blocked") and len(t["result"]) > 4:
        body = "<br>".join(esc(l) for l in t["result"][:12])
        info.append(f"<dt>結果</dt><dd>{body}</dd>")
    if t["last_log"]:
        info.append(f"<dt>最新ログ</dt><dd>{esc(t['last_log'])}</dd>")
    info.append(f"<dt>ファイル</dt><dd class='mono'>{esc(t['file'])}</dd>")
    blocks.append(f'<dl class="info">{"".join(info)}</dl>')

    eyebrow = col_label + (f" ・ 優先 {t['prio']}" if t.get("prio") is not None else "")
    return f"""
      <template id="detail-{idx}">
        <div class="sheet-top">
          <div><div class="eyebrow">{esc(eyebrow)}</div><h2 id="sheet-title">{esc(t["title"])}</h2></div>
          <button class="close" type="button" data-close>閉じる</button>
        </div>
        {"".join(blocks)}
      </template>"""


def render_card(t, col, idx):
    badges = []
    if t.get("prio") is not None:
        badges.append(f'<span class="badge prio p{min(t["prio"], 3)}">P{t["prio"]}</span>')
    if t.get("date"):
        badges.append(f'<span class="badge">{fmt_dt(t["date"], False)}</span>')
    if col == "todo" and t.get("future"):
        badges.append('<span class="badge future">予定</span>')
    if col == "doing" and t.get("stale"):
        badges.append('<span class="badge warn">停止の疑い</span>')
    if col == "blocked" and t.get("plan_wait"):
        badges.append('<span class="badge plan">計画の確認待ち</span>')
    if t.get("external") == "許可":
        badges.append('<span class="badge ext">外部操作あり</span>')
    n_review = open_review_count(t, col)
    if n_review:
        badges.append(f'<span class="badge rv">要確認 {n_review}</span>')

    meta = ""
    if col == "doing" and t.get("started"):
        meta = f"開始 {fmt_dt(t['started'])}"
    elif col == "done":
        meta = f"完了 {fmt_dt(t.get('finished') or t.get('_when'))}"
    elif col == "blocked" and t.get("last_log"):
        meta = short(t["last_log"], 60)

    headline = ""
    if col == "blocked" and t["result"]:
        headline = f'<p class="reason">{esc(short(t["result"][0].lstrip("-* "), 110))}</p>'
    elif col == "done" and t["result"]:
        headline = f'<p class="sub">{esc(short(t["result"][0].lstrip("-* "), 90))}</p>'
    elif t["purpose"]:
        headline = f'<p class="sub">{esc(short(t["purpose"], 90))}</p>'

    search = esc(" ".join([t["title"], t["file"], t["purpose"], " ".join(t["result"])]).lower())
    return f"""
      <button type="button" class="card {col}{" stale" if t.get("stale") else ""}" data-i="{idx}"
        data-search="{search}" aria-haspopup="dialog">
        <span class="badges">{"".join(badges)}</span>
        <h3>{esc(t["title"])}</h3>
        {headline}
        {f'<p class="meta">{esc(meta)}</p>' if meta else ""}
      </button>"""


def render(tasks_dir, now, done_days):
    data, done_total, done_month = collect(tasks_dir, now, done_days)
    mode = read_config_mode(tasks_dir)
    logs = read_log(tasks_dir)
    stale = sum(1 for t in data["doing"] if t.get("stale"))
    ready = sum(1 for t in data["todo"] if not t.get("future"))
    to_judge = sum(open_review_count(t, "blocked") for t in data["blocked"])

    blocked_sub = "なし"
    if data["blocked"]:
        blocked_sub = f"あなたが判断する点 {to_judge}" if to_judge else "人の対応待ち"
    kpis = [
        ("未着手", len(data["todo"]), f"うち実行対象 {ready}", "todo"),
        ("実行中", len(data["doing"]), "停止の疑い %d" % stale if stale else "正常", "doing"),
        ("要確認", len(data["blocked"]), blocked_sub, "blocked"),
        ("今月の完了", done_month, f"累計 {done_total}", "done"),
    ]
    kpi_html = "".join(
        f'<div class="kpi {cls}"><span class="k-label">{label}</span>'
        f'<span class="k-num">{num}</span><span class="k-sub">{esc(sub)}</span></div>'
        for label, num, sub, cls in kpis
    )

    cols_html = ""
    templates = ""
    idx = 0
    for key, label, cls in COLUMNS:
        cards = ""
        for t in data[key]:
            cards += render_card(t, key, idx)
            templates += render_detail(t, key, label, idx)
            idx += 1
        note = f"直近{done_days}日" if key == "done" else ""
        if not cards:
            cards = '<p class="empty">なし</p>'
        cols_html += f"""
    <section class="col {cls}">
      <header><span class="dot"></span><h2>{label}</h2><span class="count">{len(data[key])}</span>
        {f'<span class="note">{note}</span>' if note else ""}</header>
      <div class="cards">{cards}</div>
    </section>"""

    log_html = "".join(f"<li class='mono'>{esc(l)}</li>" for l in logs) or "<li>ログはまだありません</li>"
    mode_cls = "live" if mode == "live" else "dry"
    project = os.path.basename(os.path.dirname(os.path.abspath(tasks_dir))) or "tasks"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>タスクボード | {esc(project)}</title>
<style>
:root {{
  --bg:#f5f6f8; --panel:#ffffff; --col:#eceef2; --text:#1c2230; --muted:#667085; --line:#dde1e8;
  --todo:#5b7cfa; --doing:#e0a100; --blocked:#e5484d; --done:#2f9e6b; --ext:#8e4ec6;
  --shadow:0 1px 2px rgba(16,24,40,.06);
  --read:#e4e8ee; --read-ink:#5f6b7c; --make:#d5ece9; --make-ink:#0e6b64;
  --check:#f6ebd3; --check-ink:#9a6210; --ext-bg:#f8ddd7; --ext-ink:#c2412d;
  --review-bg:#fdf3dc; --review-ink:#8a5a0b;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#12151b; --panel:#1b1f27; --col:#171a21; --text:#e6e9ef; --muted:#98a2b3; --line:#2a2f3a;
    --shadow:none;
    --read:#262f3b; --read-ink:#a3adbb; --make:#163b39; --make-ink:#3cc4b5;
    --check:#3f3320; --check-ink:#e2b25a; --ext-bg:#43231e; --ext-ink:#f07a63;
    --review-bg:#3a2f1a; --review-ink:#f0c46e; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Yu Gothic UI","Segoe UI",sans-serif;
  font-size:14px; line-height:1.5; }}
.wrap {{ max-width:1400px; margin:0 auto; padding:20px 16px 40px; }}
.top {{ display:flex; flex-wrap:wrap; align-items:center; gap:12px; justify-content:space-between; }}
h1 {{ font-size:20px; margin:0; }}
.stamp {{ color:var(--muted); font-size:12px; }}
.mode {{ font-size:12px; font-weight:600; padding:2px 10px; border-radius:999px; }}
.mode.dry {{ background:color-mix(in srgb,var(--doing) 18%,transparent); color:var(--doing); }}
.mode.live {{ background:color-mix(in srgb,var(--done) 18%,transparent); color:var(--done); }}
input[type=search] {{ padding:7px 12px; border:1px solid var(--line); border-radius:8px; background:var(--panel);
  color:var(--text); width:220px; max-width:100%; font-size:13px; }}
.kpis {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:16px 0; }}
.kpi {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 14px;
  display:flex; flex-direction:column; border-top:3px solid var(--c); box-shadow:var(--shadow); }}
.kpi.todo{{--c:var(--todo)}} .kpi.doing{{--c:var(--doing)}} .kpi.blocked{{--c:var(--blocked)}} .kpi.done{{--c:var(--done)}}
.k-label {{ color:var(--muted); font-size:12px; }}
.k-num {{ font-size:26px; font-weight:700; line-height:1.2; font-variant-numeric:tabular-nums; }}
.k-sub {{ color:var(--muted); font-size:12px; }}
.board {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; align-items:start; }}
.col {{ background:var(--col); border-radius:12px; padding:10px; min-height:120px; }}
.col.todo{{--c:var(--todo)}} .col.doing{{--c:var(--doing)}} .col.blocked{{--c:var(--blocked)}} .col.done{{--c:var(--done)}}
.col header {{ display:flex; align-items:center; gap:8px; padding:2px 4px 10px; }}
.col h2 {{ font-size:14px; margin:0; }}
.dot {{ width:9px; height:9px; border-radius:50%; background:var(--c); }}
.count {{ font-size:12px; color:var(--muted); background:var(--panel); border-radius:999px; padding:0 8px; }}
.note {{ margin-left:auto; font-size:11px; color:var(--muted); }}
.cards {{ display:flex; flex-direction:column; gap:8px; }}
.card {{ display:block; width:100%; text-align:left; font:inherit; color:inherit; cursor:pointer;
  background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--c);
  border-radius:8px; box-shadow:var(--shadow); padding:10px 12px; }}
.card:hover {{ border-color:var(--c); }}
.card:focus-visible {{ outline:3px solid var(--todo); outline-offset:2px; }}
.card.stale {{ outline:2px solid var(--blocked); }}
.card h3 {{ font-size:14px; margin:4px 0 2px; word-break:break-word; }}
.sub, .reason, .meta {{ margin:2px 0 0; font-size:12px; }}
.sub {{ color:var(--muted); }}
.reason {{ color:var(--blocked); }}
.meta {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
.badges {{ display:flex; flex-wrap:wrap; gap:4px; }}
.badge {{ font-size:11px; padding:0 6px; border-radius:4px; background:var(--col); color:var(--muted); }}
.badge.prio.p1 {{ background:color-mix(in srgb,var(--blocked) 16%,transparent); color:var(--blocked); font-weight:600; }}
.badge.prio.p2 {{ background:color-mix(in srgb,var(--doing) 16%,transparent); color:var(--doing); font-weight:600; }}
.badge.future {{ background:color-mix(in srgb,var(--todo) 14%,transparent); color:var(--todo); }}
.badge.warn {{ background:var(--blocked); color:#fff; }}
.badge.ext {{ background:color-mix(in srgb,var(--ext) 16%,transparent); color:var(--ext); }}
.badge.plan, .badge.rv {{ background:var(--review-bg); color:var(--review-ink); font-weight:600; }}
.mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:12px; }}
.empty {{ color:var(--muted); font-size:12px; text-align:center; margin:12px 0; }}
.log {{ margin-top:20px; background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 16px; }}
.log h2 {{ font-size:14px; margin:0 0 6px; }}
.log ul {{ margin:0; padding-left:18px; color:var(--muted); }}
.hidden {{ display:none; }}
[hidden] {{ display:none !important; }}

/* 計画カード（右から開くシート） */
.scrim {{ position:fixed; inset:0; background:rgba(10,14,20,.45); z-index:10; }}
.sheet {{ position:fixed; top:0; right:0; bottom:0; width:min(720px,100%); background:var(--bg); z-index:11;
  overflow-y:auto; box-shadow:-8px 0 30px rgba(0,0,0,.18); }}
.sheet-in {{ padding:18px 20px 40px; display:flex; flex-direction:column; gap:16px; }}
.sheet-top {{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; }}
.eyebrow {{ font-size:12px; color:var(--muted); letter-spacing:.04em; }}
.sheet h2 {{ font-size:20px; line-height:1.35; margin:2px 0 0; }}
.sheet h4 {{ font-size:14px; margin:0 0 10px; }}
.close {{ font:inherit; font-size:13px; cursor:pointer; padding:6px 12px; border:1px solid var(--line);
  border-radius:8px; background:var(--panel); color:var(--text); white-space:nowrap; }}
.close:focus-visible {{ outline:3px solid var(--todo); }}
.banner {{ border-radius:10px; padding:12px 14px; }}
.banner b {{ display:block; }}
.banner p {{ margin:4px 0 0; font-size:13px; }}
.banner.stop {{ background:var(--ext-bg); }} .banner.stop b {{ color:var(--ext-ink); }}
.banner.wait {{ background:var(--review-bg); }} .banner.wait b {{ color:var(--review-ink); }}
.banner.done {{ background:var(--make); }} .banner.done b {{ color:var(--make-ink); }}
.goal {{ margin:0; padding:14px 16px; background:var(--panel); border:1px solid var(--line); border-radius:10px;
  font-size:18px; font-weight:700; line-height:1.5; }}
.goal small {{ display:block; font-size:11px; font-weight:400; color:var(--muted); margin-bottom:2px; }}
.review {{ background:var(--review-bg); border:2px solid var(--review-ink); border-radius:10px; padding:14px 16px; }}
.review h4 {{ color:var(--review-ink); }}
.review ol {{ margin:0; padding-left:1.4em; display:flex; flex-direction:column; gap:6px; font-weight:600; }}
.review .how {{ margin:10px 0 0; font-size:13px; }}
.flow {{ display:flex; flex-wrap:wrap; row-gap:8px; }}
.step {{ display:flex; align-items:center; }}
.node {{ width:112px; min-height:92px; border-radius:10px; padding:8px; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:6px; text-align:center; font-size:12px; line-height:1.4;
  border:2px solid transparent; }}
.node svg {{ width:24px; height:24px; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; flex:none; }}
.node.read {{ background:var(--read); }} .node.read svg {{ stroke:var(--read-ink); }}
.node.make {{ background:var(--make); }} .node.make svg {{ stroke:var(--make-ink); }}
.node.check {{ background:var(--check); }} .node.check svg {{ stroke:var(--check-ink); }}
.node.ext {{ background:var(--ext-bg); border-color:var(--ext-ink); }} .node.ext svg {{ stroke:var(--ext-ink); }}
.node.stop {{ background:var(--text); color:var(--bg); }} .node.stop svg {{ stroke:var(--bg); }}
.arrow {{ width:20px; text-align:center; color:var(--muted); }}
.legend {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:8px; font-size:12px; color:var(--muted); }}
.sw {{ display:inline-block; width:11px; height:11px; border-radius:3px; margin-right:4px; vertical-align:-1px; }}
.sw.read {{ background:var(--read); }} .sw.make {{ background:var(--make); }} .sw.check {{ background:var(--check); }}
.sw.ext {{ background:var(--ext-bg); border:1px solid var(--ext-ink); }} .sw.stop {{ background:var(--text); }}
.two {{ display:grid; grid-template-columns:1fr 1fr; gap:12px; }}
.box {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }}
.box ul {{ margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:6px; font-size:13px; }}
.box li {{ display:flex; gap:8px; align-items:flex-start; }}
.mk {{ flex:none; width:19px; height:19px; border-radius:50%; display:inline-flex; align-items:center;
  justify-content:center; font-size:11px; font-weight:700; margin-top:1px; }}
.mk.y {{ background:var(--ext-ink); color:var(--panel); }}
.mk.n {{ background:var(--read); color:var(--read-ink); }}
.mk.a {{ background:var(--make); color:var(--make-ink); }}
.mk.q {{ background:color-mix(in srgb,var(--todo) 16%,transparent); color:var(--todo); }}
.empty-li {{ color:var(--muted); }}
.cb {{ flex:none; width:16px; height:16px; border:2px solid var(--muted); border-radius:4px; margin-top:2px;
  display:inline-flex; align-items:center; justify-content:center; font-size:11px; }}
.checks li.on .cb {{ background:var(--done); border-color:var(--done); color:#fff; }}
.noplan {{ margin:0; padding:12px 14px; border:1px dashed var(--line); border-radius:10px; color:var(--muted); font-size:13px; }}
.info {{ margin:0; display:grid; grid-template-columns:auto 1fr; gap:4px 12px; font-size:12px;
  border-top:1px dashed var(--line); padding-top:10px; }}
.info dt {{ color:var(--muted); white-space:nowrap; }}
.info dd {{ margin:0; word-break:break-word; }}

@media (max-width:980px) {{ .board {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:600px) {{
  .board, .kpis {{ grid-template-columns:1fr 1fr; }} .board {{ grid-template-columns:1fr; }}
  .two {{ grid-template-columns:1fr; }}
  .flow {{ flex-direction:column; }}
  .step {{ flex-direction:column; align-items:stretch; }}
  .node {{ width:100%; min-height:0; flex-direction:row; justify-content:flex-start; text-align:left; padding:8px 12px; }}
  .arrow {{ width:auto; height:16px; line-height:16px; transform:rotate(90deg); }}
}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div>
      <h1>タスクボード <span class="mode {mode_cls}">{esc(mode)}</span></h1>
      <div class="stamp">{esc(project)} ・ 更新 {now.strftime("%Y-%m-%d %H:%M")}</div>
    </div>
    <input type="search" id="q" placeholder="件名・内容で絞り込み">
  </div>
  <div class="kpis">{kpi_html}</div>
  <main class="board">{cols_html}
  </main>
  <section class="log"><h2>最近の実行ログ</h2><ul>{log_html}</ul></section>
</div>
<div class="scrim" id="scrim" hidden></div>
<aside class="sheet" id="sheet" hidden role="dialog" aria-modal="true" aria-labelledby="sheet-title">
  <div class="sheet-in" id="sheet-in"></div>
</aside>
{templates}
<script>
document.getElementById('q').addEventListener('input', function(e) {{
  var q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('.card').forEach(function(c) {{
    c.classList.toggle('hidden', q && c.dataset.search.indexOf(q) < 0);
  }});
}});
var sheet = document.getElementById('sheet'), scrim = document.getElementById('scrim'), lastFocus = null;
function openSheet(i) {{
  var tpl = document.getElementById('detail-' + i);
  if (!tpl) return;
  var body = document.getElementById('sheet-in');
  body.innerHTML = '';
  body.appendChild(tpl.content.cloneNode(true));
  lastFocus = document.activeElement;
  scrim.hidden = false; sheet.hidden = false; sheet.scrollTop = 0;
  var c = body.querySelector('[data-close]');
  c.addEventListener('click', closeSheet);
  c.focus();
}}
function closeSheet() {{
  sheet.hidden = true; scrim.hidden = true;
  if (lastFocus) lastFocus.focus();
}}
document.querySelectorAll('.card').forEach(function(c) {{
  c.addEventListener('click', function() {{ openSheet(c.dataset.i); }});
}});
scrim.addEventListener('click', closeSheet);
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape' && !sheet.hidden) closeSheet();
}});
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="task-runner のカンバン型ダッシュボードを生成")
    ap.add_argument("tasks_dir", nargs="?", default="tasks")
    ap.add_argument("--out", help="出力先（既定: <tasks_dir>/dashboard.html）")
    ap.add_argument("--done-days", type=int, default=14, help="完了列に表示する日数（既定14）")
    ap.add_argument("--now", help="現在日時の上書き（YYYY-MM-DD HH:MM、テスト用）")
    args = ap.parse_args()

    if not os.path.isdir(args.tasks_dir):
        sys.exit(f"tasks フォルダが見つかりません: {args.tasks_dir}")
    now = parse_dt(args.now) if args.now else datetime.now()
    if now is None:
        sys.exit(f"--now の形式が不正です（YYYY-MM-DD HH:MM）: {args.now}")
    out = args.out or os.path.join(args.tasks_dir, "dashboard.html")
    page = render(args.tasks_dir, now, args.done_days)
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(page)
    os.replace(tmp, out)  # 途中で止まっても壊れたHTMLを残さない
    print(out)


if __name__ == "__main__":
    main()
