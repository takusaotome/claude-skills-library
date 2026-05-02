---
layout: default
title: "Web Server Security Reviewer"
grand_parent: 日本語
parent: メタ・品質
nav_order: 30
lang_peer: /en/skills/meta/web-server-security-reviewer/
permalink: /ja/skills/meta/web-server-security-reviewer/
---

# Web Server Security Reviewer
{: .no_toc }

Web サーバ（nginx / apache、Linux 中心）の Phase 1 設定セキュリティレビュースキル。`target_profile.yaml` で対象を確定し、`MANIFEST.txt` ＋ `manifest_attestation.txt` で証跡 integrity を検証、SSH 直接 or 証跡受領モードで 9 観点を read-only 走査します。Windows / IIS は v1 hard fail。
{: .fs-6 .fw-300 }

<span class="badge badge-free">API不要</span>

[スキルパッケージをダウンロード (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/web-server-security-reviewer.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHubでソースを見る](https://github.com/takusaotome/claude-skills-library/tree/main/skills/web-server-security-reviewer){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>目次</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. 概要

nginx / apache が動作する Linux Web サーバ向けの Phase 1 設定セキュリティレビューを構造化された手順で実施します。証跡収集モードは2つ：

1. **SSH 直接（read-only）** — 立会者承認のもと、6 階層ガードレールで明示的に許可されたコマンドだけを実行
2. **証跡受領（manifest）** — `MANIFEST.txt`（SHA256）と `manifest_attestation.txt`（真正性 attestation）を受領し、整合性検証してからレビュー

指摘は 3 軸（Exploitability × Blast Radius × Service Criticality）でスコアリング。証跡から確認できない項目は黙って落とさず `observation_status` で管理し、確認済み／未確認の境界を明示します。最終化前のセルフレビューは必須。Windows / IIS 対象は v1 で hard fail します。

---

## 2. 前提条件

- Python 3.9 以上、PyYAML
- SSH モード: 踏み台／立会者承認、Read-Only 認証情報
- 証跡モード: `MANIFEST.txt`、`manifest_attestation.txt`、参照される証跡ファイル一式
- 対象: Linux（RHEL ファミリー優先 / nginx or apache）。Windows / IIS は v1 対象外。

---

## 3. クイックスタート

```bash
# ローカルにスキルをインストール
make install SKILL=web-server-security-reviewer

# または .skill パッケージを取得
curl -L -o web-server-security-reviewer.skill \
  https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/web-server-security-reviewer.skill

# 内部整合性検証（17 PASS 期待）
cd skills/web-server-security-reviewer && python3 scripts/verify_skill.py
```

Claude Code 内で対象プロファイル（ロール、OS、Web サーバ、環境）と証跡モードを伝えると、スキルがワークフローに沿って案内します。

---

## 4. 進め方

1. **スコープ＆target_profile** — `assets/target_profile_template.yaml` で対象を確定（ホストロール／OS／Web サーバ／環境）
2. **整合性ゲート** — manifest モードでは全ファイルの SHA256 を `MANIFEST.txt` と突合、`manifest_attestation.txt` の真正性レベルを確認
3. **9 観点スキャン** — `references/checklist_9axes.yaml` 定義のチェックを実行: OS／リソース／ログ／ネットワーク／サービス／認証／監視／バックアップ／証明書
4. **ガードレール強制** — 全コマンドを 6 階層フィルタへ通す: `allowed` / `conditional` / `conditional_sensitive` / `ask-first` / `exceptional_sensitive_read` / `forbidden`。禁止コマンドは 21 個明示
5. **重大度スコアリング** — 各指摘に Exploitability + Blast Radius + Service Criticality を付与。証跡から確認不能なものは `observation_status` で管理
6. **セルフレビュー** — `assets/self_review_template.md` での確認パスを最終化前に必須実施
7. **出力** — レポート／アクションプラン／指摘テーブルを生成。生証跡はレポートディレクトリと分離

---

## 5. 使用例

- 公開向け nginx の本番投入前ハードニングレビュー
- 直接 SSH 不可な内部 apache サーバの定期姿勢監査（manifest モード）
- 第三者から提供された証跡ダンプを integrity 証明とともにレビュー
- 確認できなかった項目を `observation_status` で次回スコープに繰越
- 運用引き渡し可能な action plan を生成

---

## 6. 出力の読み方

- **レポート** (`assets/report_template.md`) — 指摘・重大度・推奨対応を含むナラティブ
- **アクションプラン** (`assets/action_plan_template.md`) — 優先度付き対応バックログ
- **指摘テーブル** (`assets/finding_table_template.md`) — チケット取込用の構造化テーブル
- **セルフレビュー** (`assets/self_review_template.md`) — 最終化前完了
- **証跡ディレクトリ構成** (`assets/evidence_directory_layout.md`) — `evidence_dir/` と `raw_evidence_store/` の分離を強制

各指摘は 3 状態のいずれか: confirmed（証跡から確認済）／observed-pending（管理された未確認状態）／out-of-scope（例: Windows/IIS hard fail）。

---

## 7. ベストプラクティス

- `command_reference.yaml` のカタログ外コマンドは escalation なしに実行しない（カタログが立会者との契約）
- `observation_status` は回避策ではなく機能。確認不能な指摘を黙って消すのは品質ギャップ
- 生証跡（フル設定、鍵情報）は `raw_evidence_store/` に隔離し、レポートに直接埋め込まない
- manifest モードで attestation level が閾値未満なら作業を中止（`references/secret_masking.md` と `verification_summary.md` を参照）
- テンプレートや command_reference を変更したら必ず `scripts/verify_skill.py` を再実行

---

## 8. 他スキルとの連携

- レビューで実インシデントや侵害指標を検知した場合は `incident-rca-specialist` を併用
- J-SOX / SOX マッピングが必要な場合は `compliance-advisor` に指摘を引き渡し
- 関連ワークフローを探す場合は同カテゴリ一覧を参照: [カテゴリ一覧]({{ '/ja/skills/meta/' | relative_url }})
- 日本語スキルカタログ全体: [スキルカタログ]({{ '/ja/skill-catalog/' | relative_url }})

---

## 9. トラブルシューティング

- **`python3 scripts/verify_skill.py` が FAIL** — 22 件すべて PASS することが前提（section H wizard pipeline smoke を含む）。実運用前に原因調査
- **Manifest integrity が失敗** — 作業中止。証跡再収集 or `references/guardrails.md` に従ってエスカレーション
- **Windows / IIS 対象を検知** — v1 では設計的に hard fail。別プロセスを使用
- **未解決のテンプレート/コマンド ID** — `verify_skill.py` が表示。実レビュー前にクロスリファレンスを修正
- **レポートドラフトに機微情報が混入** — `raw_evidence_store/` へ移動し、`references/secret_masking.md` のマスキング規則を適用

---

## 10. リファレンス

**参照ガイド:**

- `skills/web-server-security-reviewer/references/checklist_9axes.yaml`
- `skills/web-server-security-reviewer/references/command_reference.yaml`
- `skills/web-server-security-reviewer/references/finding_taxonomy.md`
- `skills/web-server-security-reviewer/references/guardrails.md`
- `skills/web-server-security-reviewer/references/input_contract.md`
- `skills/web-server-security-reviewer/references/observation_status.md`
- `skills/web-server-security-reviewer/references/schema_validation.md`
- `skills/web-server-security-reviewer/references/secret_masking.md`
- `skills/web-server-security-reviewer/references/severity_criteria.md`
- `skills/web-server-security-reviewer/references/unsupported_matrix.md`
- `skills/web-server-security-reviewer/references/verification_summary.md`
- `skills/web-server-security-reviewer/references/role_extensions/_schema.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_edge.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_internal.yaml`
- `skills/web-server-security-reviewer/references/role_extensions/generic_public_facing.yaml`
- `skills/web-server-security-reviewer/references/interview_wizard.md` — Phase 0 対話ウィザード 7 stage 宣言的設問仕様 (v1.1+)

**スクリプト:**

- `skills/web-server-security-reviewer/scripts/verify_skill.py` — 内部整合性検証 (22 checks)
- `skills/web-server-security-reviewer/scripts/verification_run.py`
- `skills/web-server-security-reviewer/scripts/build_target_profile.py` — wizard 回答 JSON → target_profile.yaml ビルダー (default 補完 / 派生 / hard-fail gate)

**アセット:**

- `skills/web-server-security-reviewer/assets/target_profile_template.yaml`
- `skills/web-server-security-reviewer/assets/manifest_template.txt`
- `skills/web-server-security-reviewer/assets/manifest_attestation_template.txt`
- `skills/web-server-security-reviewer/assets/finding_table_template.md`
- `skills/web-server-security-reviewer/assets/report_template.md`
- `skills/web-server-security-reviewer/assets/action_plan_template.md`
- `skills/web-server-security-reviewer/assets/evidence_directory_layout.md`
- `skills/web-server-security-reviewer/assets/self_review_template.md`
- `skills/web-server-security-reviewer/assets/wizard_answers_example.json` — `build_target_profile.py` 用ウィザード回答サンプル

---

## English Version

- 詳細な解説、背景説明、個別の運用判断は [English version]({{ '/en/skills/meta/web-server-security-reviewer/' | relative_url }}) を参照してください。
