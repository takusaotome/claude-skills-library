#!/usr/bin/env python3
"""
verification_run.py — 分析検証 A / B 用のヘルパースクリプト

verify_skill.py が自動検証可能な範囲（E/F/G/D-γ/cross-references）を扱うのに対し、
本スクリプトは既存レポート 3 本（公開・本部・店舗）を入力として:
  - A: HQ Critical/High recall
  - B: 124 件→83 件マッピング率

を計算する。9 観点 keyword 辞書を使うため keyword 拡充に応じて結果が変わる。
完全自動化ではなく、辞書品質に依存する分析検証である点に注意。

使い方:
  python3 scripts/verification_run.py [path_to_reports_dir]
  デフォルトのレポートパスは引数なしで利用可能。
"""

import os
import re
import sys

DEFAULT_REPORTS_DIR = "/Users/takueisaotome/PycharmProjects/round1-projects/docs/server_review_2026Q2"

AXIS_KW_FULL = {
    "A1": [
        "Rocky Linux",
        "Ubuntu",
        "カーネル",
        "EOL",
        "稼働",
        "uptime",
        "再起動",
        "OS 世代",
        "435 日",
        "271 日",
        "312 日",
        "CentOS",
    ],
    "A2": [
        "ディスク",
        "メモリ",
        "/var/log",
        "/home/log",
        "/log/",
        "GB",
        "使用率",
        "EBS",
        "content/",
        "signedPDF",
        "PII",
        "蓄積",
        "capture",
        "qr_code",
    ],
    "A3": [
        "log4js",
        "ログ",
        "rotation",
        "logrotate",
        "remove_log",
        "numBackups",
        "compress",
        "journald",
        "access.log",
        "system.log",
        "tar.gz",
        "access_log",
    ],
    "A4": [
        "nginx",
        "firewall",
        "TLS",
        "SSL",
        "0.0.0.0",
        "バインド",
        "rpcbind",
        "VPN",
        ".git",
        "tun",
        "WAF",
        "rate limit",
        "セキュリティヘッダ",
        "worker_processes",
        "Cookie",
        "ssl_protocols",
        "ssl_ciphers",
        "limit_req",
        "HSTS",
        "CSP",
        "TLSv1",
        "mod_security",
        "X-Frame",
        "fail2ban",
        "同居",
        "port",
        "ssl.conf",
        "sameSite",
        "httpOnly",
        "静的経路",
        "経路",
        "404",
        "5xx",
        "エラーページ",
    ],
    "A5": [
        "Node.js",
        "forever",
        "プロセス",
        "systemd",
        "/usr/share",
        "バージョン",
        "アプリ配置",
        "npm",
        "jsonwebtoken",
        "express",
        "依存",
        "package.json",
        "openconnect",
        "再接続スクリプト",
        "/usr/bin/node",
        "pm2",
        "forever.service",
        "curl -k",
        "バッチ",
        "crontab",
        "cron",
        "git コマンド",
        "インストール",
    ],
    "A6": [
        "SSH",
        "sudoers",
        "NOPASSWD",
        "PermitRoot",
        "X11Forwarding",
        "AllowUsers",
        "SELinux",
        "AppArmor",
        "shadow",
        "パーミッション",
        "644",
        "755",
        "session-config",
        "db-config",
        ".env",
        "authorized_keys",
        "sshd_config",
        "権限",
        "秘密ファイル",
        "auth",
        "bash_history",
        "HISTTIMEFORMAT",
        "sql",
        "dump",
        "dbdump",
        "放置",
        "配下",
    ],
    "A7": ["監視", "CloudWatch", "Zabbix", "Datadog", "監視エージェント", "agent", "newrelic"],
    "A8": ["バックアップ", "スナップショット", "リストア", "Backup"],
    "A9": [
        "証明書",
        "期限",
        "chronyd",
        "NTP",
        "タイムゾーン",
        "TZ",
        "cert",
        "DigiCert",
        "2029-11-08",
        "hwclock",
        "時刻",
    ],
}
META_PATTERNS = ["F1' に統合", "計画書", "F56g に統合", "F56 系へ吸収"]


def classify(text):
    matched = set()
    for axis, kws in AXIS_KW_FULL.items():
        for kw in kws:
            if kw in text:
                matched.add(axis)
                break
    return matched


def is_meta(desc):
    return any(p in desc for p in META_PATTERNS)


def extract_findings(reports_dir):
    """3 レポートから Finding (id, desc) を抽出"""
    reports = ["01_public_server.md", "02_hq_server.md", "03_store_servers.md"]
    all_findings = []
    for r in reports:
        path = os.path.join(reports_dir, r)
        if not os.path.exists(path):
            print(f"  WARN: {path} not found, skipping")
            continue
        content = open(path).read()
        rows = re.findall(r"\| (F\d+[a-z\']?|\bH-F\d+|\bS-F\d+) \| ([^|]+) \|", content)
        for fid, desc in rows:
            all_findings.append({"report": r, "id": fid.strip(), "desc": desc.strip()})
    return all_findings


def verification_a(reports_dir):
    """A: HQ Critical/High recall"""
    print("\n=== A: HQ Critical/High recall ===")
    hq_path = os.path.join(reports_dir, "02_hq_server.md")
    if not os.path.exists(hq_path):
        print(f"  SKIP: {hq_path} not found")
        return None
    hq = open(hq_path).read()
    crit_section = hq[hq.find("### 3.1") : hq.find("### 3.2 High")] if "### 3.2 High" in hq else ""
    high_section = hq[hq.find("### 3.2 High") : hq.find("### 3.3 Medium")] if "### 3.3 Medium" in hq else ""
    crit_ids = set(re.findall(r"\*\*(H-F\d+)\b", crit_section))
    high_ids = set(re.findall(r"\| (H-F\d+) \|", high_section))

    desc_map = {}
    for fid in crit_ids | high_ids:
        idx = hq.find(fid)
        if idx > 0:
            desc_map[fid] = hq[idx : idx + 500]

    ch = crit_ids | high_ids
    mapped = [fid for fid in ch if fid in desc_map and classify(desc_map[fid])]
    recall = len(mapped) / len(ch) * 100 if ch else 0

    print(f"  Critical: {sorted(crit_ids)}")
    print(f"  High:     {sorted(high_ids)}")
    print(f"  Mapped:   {sorted(mapped)} ({len(mapped)}/{len(ch)})")
    print(f"  Recall:   {recall:.1f}%")
    print(f"  [{'PASS' if recall == 100 else 'FAIL'}] A.1 HQ recall 100%")
    return recall == 100


def verification_b(reports_dir):
    """B: 124→83 マッピング率"""
    print("\n=== B: 既存 Finding 観点マッピング ===")
    all_findings = extract_findings(reports_dir)
    real = [f for f in all_findings if not is_meta(f["desc"])]
    mapped = sum(1 for f in real if classify(f["desc"]))
    rate = mapped / len(real) * 100 if real else 0

    print(f"  Extracted:        {len(all_findings)}")
    print(f"  After meta excl:  {len(real)}")
    print(f"  Mapped:           {mapped}")
    print(f"  Rate:             {rate:.1f}%")
    print(f"  [{'PASS' if rate >= 90 else 'FAIL'}] B.1 マッピング率 ≥ 90%")
    return rate >= 90


def main():
    reports_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REPORTS_DIR
    print("# Verification run (analytical)")
    print(f"# Reports dir: {reports_dir}")

    if not os.path.isdir(reports_dir):
        print(f"\n  FAIL: reports directory not found: {reports_dir}")
        print(f"  使い方: python3 {sys.argv[0]} [path_to_reports_dir]")
        sys.exit(1)

    a = verification_a(reports_dir)
    b = verification_b(reports_dir)

    print("\n=== SUMMARY (analytical) ===")
    results = [("A.1", a), ("B.1", b)]
    passed = sum(1 for _, ok in results if ok)
    print(f"Total: {passed}/{len(results)} PASS")
    if passed < len(results):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
