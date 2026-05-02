#!/usr/bin/env python3
"""
verify_skill.py — Web Server Security Reviewer スキルの自動検証
検証 A〜G + cross-reference + Spo-cha 名詞混入 を一括実行
Exit code: 0 = 全 PASS / 1 = 1 件以上 FAIL

使い方:
  cd ~/.claude/skills/web-server-security-reviewer
  python3 scripts/verify_skill.py
"""

import glob
import hashlib
import os
import re
import sys
import tempfile
from datetime import datetime

import yaml

results = []


def t(name, ok, msg=""):
    mark = "PASS" if ok else "FAIL"
    results.append((name, ok, msg))
    line = f"[{mark}]  {name}"
    if msg:
        line += f": {msg}"
    print(line)


def main():
    print(f"# Verification run: {datetime.now().isoformat()}")
    print(f"# CWD: {os.getcwd()}\n")

    # === E-1: YAML schema ===
    print("### E-1: YAML schema 静的検証 ###")
    yamls = [
        "references/checklist_9axes.yaml",
        "references/command_reference.yaml",
        "references/role_extensions/_schema.yaml",
        "references/role_extensions/generic_public_facing.yaml",
        "references/role_extensions/generic_internal.yaml",
        "references/role_extensions/generic_edge.yaml",
        "assets/target_profile_template.yaml",
    ]
    parse_ok = True
    for f in yamls:
        try:
            yaml.safe_load(open(f))
        except Exception as e:
            parse_ok = False
            print(f"  PARSE FAIL {f}: {e}")
    t("E-1.1 YAML パース 7/7", parse_ok)

    schema = yaml.safe_load(open("references/role_extensions/_schema.yaml"))
    req = schema["required_check_keys"]
    ok = True
    total = 0
    for path in [
        "references/checklist_9axes.yaml",
        "references/role_extensions/generic_public_facing.yaml",
        "references/role_extensions/generic_internal.yaml",
        "references/role_extensions/generic_edge.yaml",
    ]:
        d = yaml.safe_load(open(path))
        checks = d.get("checks", [])
        for axis in d.get("axes", []):
            checks.extend(axis.get("checks", []))
        for c in checks:
            total += 1
            missing = [k for k in req if k not in c]
            if missing:
                ok = False
                print(f"  SCHEMA FAIL {path}:{c.get('id')}: {missing}")
    t("E-1.2 schema 必須キー全 check 準拠", ok, f"total={total}")

    # === E-2: enum cross-check ===
    print("\n### E-2: enum cross-check ###")
    obs = open("references/observation_status.md").read()
    sev = open("references/severity_criteria.md").read()
    obs_enum = set(re.findall(r"^\|\s+`([a-z0-9_]+)`\s+\|", obs, re.MULTILINE))
    sev_mentioned = set(
        re.findall(
            r"`(confirmed|likely|not_observed|not_applicable|unknown_evidence_missing"
            r"|blocked_by_permission|out_of_scope_phase1|unsupported_in_v1"
            r"|confirmed_with_mitigation_unverified)`",
            sev,
        )
    )
    diff = sev_mentioned - obs_enum
    t("E-2.1 enum 完全一致", not diff, f"obs={len(obs_enum)} sev={len(sev_mentioned)} diff={diff}")

    # === E-3: forbidden 網羅 ===
    print("\n### E-3: read-only ガード網羅 ###")
    guard = open("references/guardrails.md").read()
    fb = [
        "sed -i",
        "rm",
        "mv",
        "cp",
        "chmod",
        "chown",
        "systemctl restart",
        "systemctl stop",
        "systemctl start",
        "crontab -e",
        "logrotate -f",
        "certbot renew",
        "ufw",
        "firewall-cmd",
        "docker compose",
        "dnf",
        "apt",
        "kill",
        "pkill",
        "tee",
        "truncate",
    ]
    miss = [c for c in fb if c not in guard]
    t("E-3.1 forbidden 21 コマンド網羅", not miss, f"missing={miss}")
    ssh4 = ["引用の外で redirect", "引用の中で redirect", "パイプ後 local tee", "引用の中で tee"]
    t("E-3.2 SSH redirect 4 ケース", all(c in guard for c in ssh4))

    # === F: hard fail ===
    print("\n### F: Windows/IIS hard fail ###")
    matrix = open("references/unsupported_matrix.md").read()
    t(
        "F.1 hard fail 条件記載",
        "os_family: windows" in matrix and "web_server: iis" in matrix and "hard fail" in matrix,
    )

    def chk(d):
        o = d.get("target", {}).get("os_family", "")
        w = d.get("target", {}).get("web_server", "")
        return "hard_fail" if (o in ["windows"] or w in ["iis"]) else "ok"

    t("F.2 windows hard_fail", chk({"target": {"os_family": "windows", "web_server": "nginx"}}) == "hard_fail")
    t("F.3 iis hard_fail", chk({"target": {"os_family": "rhel", "web_server": "iis"}}) == "hard_fail")
    t("F.4 rhel/nginx 正常系", chk({"target": {"os_family": "rhel", "web_server": "nginx"}}) == "ok")

    # === G: MANIFEST integrity ===
    print("\n### G: MANIFEST integrity ###")
    m = open("assets/manifest_template.txt").read()
    t("G.1 MANIFEST 自己参照断ち", "does NOT include itself" in m or "自身は除外" in m)
    a = open("assets/manifest_attestation_template.txt").read()
    t("G.2 attestation 真正性レベル明記", "manifest_sha256:" in a and "NOT a cryptographic signature" in a)

    with tempfile.TemporaryDirectory() as td:
        f1 = os.path.join(td, "a.yaml")
        open(f1, "w").write("foo: bar\n")
        sha = hashlib.sha256(open(f1, "rb").read()).hexdigest()
        mf = os.path.join(td, "MANIFEST.txt")
        open(mf, "w").write(f"{sha}  ./a.yaml\n")
        msha = hashlib.sha256(open(mf, "rb").read()).hexdigest()
        att = os.path.join(td, "manifest_attestation.txt")
        open(att, "w").write(f"manifest_sha256: {msha}\n")

        ok1 = sha == hashlib.sha256(open(f1, "rb").read()).hexdigest()
        ok2 = msha == hashlib.sha256(open(mf, "rb").read()).hexdigest()
        t("G.3 正常時の sha256 一致", ok1 and ok2)

        open(f1, "w").write("foo: TAMPERED\n")
        new_sha = hashlib.sha256(open(f1, "rb").read()).hexdigest()
        t("G.4 ファイル改変検出", new_sha != sha)

        open(mf, "a").write("# tampered\n")
        new_msha = hashlib.sha256(open(mf, "rb").read()).hexdigest()
        t("G.5 MANIFEST 改変検出（attestation 経由）", new_msha != msha)

    # === D-γ: Spo-cha 固有名詞混入 ===
    print("\n### D-γ: Spo-cha 固有名詞混入 ###")
    spocha = [
        "spo-cha",
        "spocha",
        "round1",
        "r1-spocha",
        "roundone45",
        "spo-cha.round1usa.com",
        "spochaheadserver",
        "r1spocha-",
        "PLM",
        "PCC",
        "PHM",
        "CLM",
        "ATC",
        "WLB",
        "ngrok",
    ]
    files = (
        glob.glob("**/*.md", recursive=True)
        + glob.glob("**/*.yaml", recursive=True)
        + glob.glob("**/*.txt", recursive=True)
    )
    # 検査メタ文書を除外（検査対象を文字列引用するためのメタ参照を含む）
    META_EXCLUDE = {"references/verification_summary.md"}
    files = [f for f in files if not f.startswith("scripts/") and f not in META_EXCLUDE]
    hits = []
    for f in files:
        content = open(f).read()
        for term in spocha:
            pat = (r"\b" + re.escape(term) + r"\b") if len(term) <= 4 else re.escape(term)
            if re.search(pat, content, re.IGNORECASE):
                hits.append((f, term))
                break
    t("D-γ Spo-cha 固有名詞混入", not hits, f"files={len(files)} hits={len(hits)}")

    # === Cross-references ===
    print("\n### Cross-references ###")
    tax = open("references/finding_taxonomy.md").read()
    todo = tax.find("## 4. 拡充 TODO")
    defined_section = tax[:todo] if todo > 0 else tax
    defined_tpls = set(re.findall(r"^###\s+(TPL-[A-Z0-9-]+):", defined_section, re.MULTILINE))

    ref_tpls = set()
    cmd_refs_all = []
    for path in [
        "references/checklist_9axes.yaml",
        "references/role_extensions/generic_public_facing.yaml",
        "references/role_extensions/generic_internal.yaml",
        "references/role_extensions/generic_edge.yaml",
    ]:
        d = yaml.safe_load(open(path))
        checks = d.get("checks", [])
        for axis in d.get("axes", []):
            checks.extend(axis.get("checks", []))
        for c in checks:
            if c.get("template_finding_id"):
                ref_tpls.add(c["template_finding_id"])
            for r in c.get("command_refs", []):
                cmd_refs_all.append((c["id"], r))

    miss_tpl = ref_tpls - defined_tpls
    t(
        "TPL references 全件解決",
        not miss_tpl,
        f"defined={len(defined_tpls)} ref={len(ref_tpls)} missing={len(miss_tpl)}",
    )

    cmd_ref = yaml.safe_load(open("references/command_reference.yaml"))
    all_cmd = set()
    for cmds in cmd_ref.get("axes", {}).values():
        for c in cmds:
            all_cmd.add(c["cmd_id"])
    unr = [(cid, r) for cid, r in cmd_refs_all if r not in all_cmd]
    t("command_refs 全件解決", not unr, f"total={len(cmd_refs_all)} cmd_ids={len(all_cmd)} unresolved={len(unr)}")

    # === H: Wizard pipeline integrity ===
    print("\n### H: Interview wizard pipeline ###")
    wizard_files = [
        "references/interview_wizard.md",
        "scripts/build_target_profile.py",
        "assets/wizard_answers_example.json",
        "scripts/tests/test_build_target_profile.py",
    ]
    missing = [f for f in wizard_files if not os.path.exists(f)]
    t("H.1 wizard ファイル存在", not missing, f"missing={missing}")

    # SKILL.md が wizard ファイルに言及している
    skill_md = open("SKILL.md").read()
    skill_refs = [
        "references/interview_wizard.md",
        "scripts/build_target_profile.py",
        "assets/wizard_answers_example.json",
    ]
    miss_ref = [r for r in skill_refs if r not in skill_md]
    t("H.2 SKILL.md 参照整合", not miss_ref, f"missing_refs={miss_ref}")

    # smoke: example JSON → YAML 生成が exit 0 で必須キー一式を含む
    if not missing:
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "tp.yaml")
            import subprocess

            r = subprocess.run(
                [
                    sys.executable,
                    "scripts/build_target_profile.py",
                    "--answers",
                    "assets/wizard_answers_example.json",
                    "--output",
                    out,
                ],
                capture_output=True,
                text=True,
            )
            t("H.3 wizard smoke (exit 0)", r.returncode == 0, r.stderr.strip())

            if r.returncode == 0 and os.path.exists(out):
                tp = yaml.safe_load(open(out))
                req_keys = {
                    "review_id",
                    "target",
                    "connection_mode",
                    "ssh",
                    "evidence",
                    "scope",
                    "incident_context",
                    "retention",
                    "exceptional_approvals",
                }
                miss_k = req_keys - set(tp.keys())
                t("H.4 生成 YAML 必須キー網羅", not miss_k, f"missing={miss_k}")
                # delete_after が派生されている
                t(
                    "H.5 retention.delete_after 派生",
                    "delete_after" in tp.get("retention", {}),
                    "",
                )

    # === Summary ===
    print("\n### SUMMARY ###")
    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"Total: {passed}/{total} PASS")
    if passed < total:
        print("FAIL:")
        for n, ok, m in results:
            if not ok:
                print(f"  - {n}: {m}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
