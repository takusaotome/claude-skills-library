# Self Review Template

レビューレポート完成後、SKILL.md §8 に基づき必ず実施。チェック未通過の項目は §10 改善提案に明記。

---

## 1. 観点網羅性

- [ ] A1 OS・カーネル: Finding 起票 or `not_observed` 記録あり
- [ ] A2 リソース: 同上
- [ ] A3 ログ設定: 同上
- [ ] A4 ネットワーク: 同上
- [ ] A5 サービス・プロセス: 同上
- [ ] A6 認証・アクセス制御: 同上
- [ ] A7 監視: 同上
- [ ] A8 バックアップ: 同上
- [ ] A9 証明書・時刻同期: 同上

未網羅の観点があれば未確認事項サブセクション §3.5 に追加。

---

## 2. 断定 / 推測の区別

- [ ] 全 Finding に `observation_status` 付与
- [ ] `likely` の Finding は根拠欄に「likely」明記 + 追加検証推奨を P0/P1 に含む
- [ ] `confirmed_with_mitigation_unverified` の Finding は重大度を降格していない
- [ ] 観測のみで断定できない C3（root RCE 経路）を Critical 断定していない（CVE/インシデント/3 点立証のいずれかが必要）

---

## 3. ID 採番整合性

- [ ] 全 Finding ID が `<ROLE>-F<3 桁>` 形式
- [ ] 欠番再利用なし（統合・吸収時は `_merged_into` で参照、新規 ID は採番せず欠番化）
- [ ] 横展開元 Finding には `related_findings` で参照記載

---

## 4. 機密混入チェック（4 段階 AND）

### (d-1) 既知パターン grep
```bash
grep -nE '(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*[^*]' <report>
grep -nE 'Authorization:\s*[A-Za-z]+\s+[A-Za-z0-9]' <report>
grep -nE 'Bearer\s+[A-Za-z0-9]' <report>
grep -nE '-----BEGIN ' <report>
grep -nE 'AKIA[0-9A-Z]{16}' <report>
grep -nE 'AIza[0-9A-Za-z_-]{35}' <report>
grep -nE 'xox[abprs]-' <report>
grep -nE 'ghp_[A-Za-z0-9]{36,}' <report>
```
- [ ] ヒット数 (d-1): _____ 件

### (d-2) 高エントロピー文字列検出
```bash
grep -nE '[A-Za-z0-9+/]{32,}={0,2}' <report>
grep -nE '[a-f0-9]{32,}' <report>
```
- [ ] ヒット数 (d-2): _____ 件

### (d-3) allowlist による FP 除外
- [ ] `secret_allowlist.txt` 適用
- [ ] 残ヒット数: _____ 件

### (d-4) 立会者目視承認
- [ ] `secret_scan_attestation.txt` 作成済
- [ ] `true_secrets_found: 0` を立会者が署名

---

## 5. 観測ステータス紛れ込みチェック

- [ ] `unknown_evidence_missing` を Low や Observation に格下げしていない
- [ ] `blocked_by_permission` を Low や Observation に格下げしていない
- [ ] `not_observed` を Finding 表に載せていない（観点別サマリ §4 でのみ言及）
- [ ] `not_applicable` を Finding 表に載せていない（同上）
- [ ] `out_of_scope_phase1` を §3.6 Phase 2 引き継ぎに集約
- [ ] `unsupported_in_v1` を検知したら Phase 0 で停止していた

---

## 6. read-only ガード遵守

- [ ] forbidden コマンド実行 0 件（command_log.jsonl で確認）
- [ ] target host 上の書込（`>`/`>>`/`tee`/`sed -i` 等）0 件
- [ ] conditional_sensitive 実行は全件マスク済要約のみ evidence_dir 転記
- [ ] exceptional_sensitive_read 実行は全件二重承認取得済（target_profile.yaml の `exceptional_approvals` で立証）

---

## 7. integrity 検証

- [ ] MANIFEST.txt の sha256 一致確認済
- [ ] manifest_attestation.txt の `manifest_sha256` と実値一致
- [ ] authenticity_level に応じた追加検証（GPG/SSH 署名）通過

---

## 8. 過学習・固有名詞混入チェック

第 2 コーパス（健全 nginx、Apache 内部等）でレビュー実施時:

- [ ] 元プロジェクト（例: 過去のレビュー対象）の固有名詞が出力に混入していない
- [ ] grep で固有名詞ヒット 0 件

```bash
# プロジェクト固有名詞のリストを target_profile.scope に応じて調整
grep -nE '<禁止固有名詞リスト>' <report>
```

---

## 9. レポート構造の確認

- [ ] §1 エグゼクティブサマリに Cluster A/B/C 形式の重大事項要約あり
- [ ] §2 件数表が §3 内訳と一致
- [ ] §3 Finding に Critical 単独セクション + High/Medium/Low 表 + 未確認事項 + Phase 2 引き継ぎ
- [ ] §4 観点別サマリで全 9 観点に言及
- [ ] §7 アクションプランに担当・期日・完了判定・ロールバックがすべて記載
- [ ] §8 ログ衛生事項に保持期間・削除計画記載
- [ ] §10 自己レビュー（本ファイル）の結果記載

---

## 10. 改善提案

レビュー実施を通じて見つかった、次回への改善点:

```
- <改善点 1>
- <改善点 2>
```

---

## 11. 自己評価

- 発見の質: ___ / 10
- レビュー規律（read-only、機密管理）: ___ / 10
- レポート完成度: ___ / 10
- 総合: ___ / 10

10 点満点でない場合の根拠を明記。次回への申し送り事項として活用。
