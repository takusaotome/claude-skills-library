# Severity Criteria — 重大度判定基準（3 軸補助 + AND/OR 条件 + 昇降格）

各 Finding に Critical / High / Medium / Low / Observation の重大度を付与する。判定は単一軸でなく **3 軸補助スコア** と **現在の到達性・影響・再現性** を組み合わせて行う。

---

## 1. 重大度の SLA

| 重大度 | SLA | 扱い |
|---|---|---|
| **Critical** | 24 時間以内 | インシデント扱い、即時通知、シークレットローテーション含む |
| **High** | 2 週間以内 | システム防御層欠落、EOL、認証情報の構造的不備 |
| **Medium** | 1-2 ヶ月以内 | 設定品質、ベストプラクティス乖離、監査指摘可能 |
| **Low / Observation** | 検討事項 | ベストプラクティス改善提案 |

---

## 2. 3 軸補助スコア

各 Finding に以下 3 軸スコアを必須で記述。判定根拠の透明性を担保。

### 2.1 Exploitability（攻撃容易性）

| 値 | 条件 |
|---|---|
| `none` | 攻撃可能性が原理的にない（既存緩和策で完全遮断、外部から到達経路なし）|
| `low` | 内部ユーザのみ実行可、または複数の前提条件が必要 |
| `medium` | 内部ユーザまたは認証済外部から到達可、前提条件 1-2 個 |
| `high` | 外部から認証なしで到達可、または 1 アクションで成立 |

### 2.2 Blast Radius（影響範囲）

| 値 | 条件 |
|---|---|
| `self` | 当該サーバ・プロセスのみ |
| `lateral_internal` | 同一 VLAN / 内部ネットワークの他サーバへ波及可能 |
| `cross_service` | 他サービス・他システムへ波及（DB 共有、SSO 連携等）|
| `cross_org` | 顧客データ、組織外への波及（PII、決済情報、組織秘密）|

### 2.3 Service Criticality（業務重要度）

| 値 | 条件 |
|---|---|
| `non_critical` | 開発・検証環境、影響軽微 |
| `standard` | 本番だが業務影響限定的 |
| `business_critical` | 本番、業務クリティカル、ダウン時に売上・顧客影響 |
| `regulated` | 規制対象（PCI DSS、HIPAA、GDPR、SOX 等）|

**インシデント発生中**は自動的に `business_critical` 以上として扱う。

---

## 3. Critical 判定条件（OR、いずれか成立）

以下 4 条件のいずれか 1 つ以上が成立する場合、Critical と判定。

### 3.1 C1 機密外部到達

- Exploitability = `high` かつ
- 機密本文の取得経路が立証済（外部 curl での 200 返却、または外部到達経路の SG/ACL 設定立証）

例: nginx ドキュメントルート設定不備により `.env` / DB 認証情報が HTTPS で取得可能。

### 3.2 C2 サービス影響迫り

- Service Criticality ≥ `business_critical` かつ
- 以下のいずれか:
  - ディスク使用率 > 90%
  - 業務クリティカルパーティション > 85%
  - 直近 24 時間で使用率 > 5 ポイント急上昇
  - 過去 30 日に同種インシデント発生（再発条件成立）

注: 単に 91% だから Critical にするのではなく、**業務クリティカルパーティション** で **サービス影響が迫っている** ことが必要。

### 3.3 C3 root RCE 経路

観測ベースで「危険な状態」が成立しているだけでは Critical 断定不可。Critical 断定には以下のいずれかが必要:
- (a) 既知の active な攻撃経路の存在（CVE 等の紐付け）
- (b) 既存インシデントとの紐付け
- (c) 外部到達 + 認証バイパス + 権限昇格の **3 点立証**

観測のみで 3 点立証が困難な場合は High に留める。

例（C3 成立）: `Critical` — 公開 nginx に既知 CVE-XXXX-YYYY、外部 PoC 公開済み、当該サーバが該当バージョン稼働、外部到達経路立証済。

例（High 留め）: `High` — Node.js v11 EOL + root 実行 + 0.0.0.0 バインド。観測上は 3 点満たすが、active な CVE 紐付けなし、外部到達は SG で遮断中。

### 3.4 C4 認証情報漏洩前提

- 認証情報が**外部到達経路で取得可能**（C1 の派生として）
- または既知の漏洩兆候（GitHub 公開検索ヒット、不審ログイン、SIEM 検知等）

---

## 4. High 判定条件

Critical 条件不成立のうえ、以下のいずれか:

- **防御層欠落**: SELinux/AppArmor 無効、ホスト FW 不在、root SSH 鍵経路、sudoers NOPASSWD ALL
- **EOL/未パッチ**: ベンダーサポート終了済、180 日以上未パッチ、active な CVE あるが exploit 困難
- **認証情報の平文保存**: VPN / DB / API パスワードが世界読み取り可能ファイルに平文（外部到達経路は不要、横展開リスクで High）
- **インシデント直接再発要因の単独事象**: ログローテ未設定、削除スクリプトの cron 不在、journald 無制限（C2 の現行条件未成立時）

---

## 5. Medium 判定条件

- TLS 旧バージョン有効（TLSv1.0/1.1）
- 設定品質（typo、デフォルト値残置）
- 監査指摘可能事項（バックアップ取得不在、リストアテスト未実施）
- セキュリティヘッダ欠如（HSTS のみで CSP / X-Frame-Options / X-Content-Type-Options 不在）

---

## 6. Low / Observation 判定条件

- ベストプラクティス乖離（軽微）
- 改善提案（観測事項のみ、即時対応不要）

**注意**: `unknown_evidence_missing` や `not_applicable` を Low に格下げしてはならない。これらは observation_status enum で別管理し、レポート §3 の独立サブセクションに集約。

---

## 7. 昇格条件

複合発生・横展開・インシデント連動で重大度を昇格できる。

| 昇格パターン | 条件 | 昇格先 |
|---|---|---|
| Service Criticality 上昇 | インシデント発生中、または regulated 環境への波及 | 1 段階昇格 |
| 過去 30 日同種障害発生 | 直近 30 日に同 axis で同種 Finding によるインシデント発生 | High → Critical |
| 複合発生 | 同一 axis で複数の High が同時成立し攻撃チェーン形成可能 | 連鎖の根を Critical に昇格 |
| 横展開立証 | 同種 Finding が 3 サーバ以上で同時観測 | 各 Finding を 1 段階昇格 |

昇格時は判定根拠記述に「昇格条件: <パターン名> / 根拠: <観測事実>」を必須記述。

---

## 8. 降格条件

- **既存緩和策の動作確認済**: WAF、IP 制限、外部 SG 遮断、内部認証バイパス防止が **動作確認済** で High → Medium
- **動作未確認の場合**: 降格不可。observation_status を `confirmed_with_mitigation_unverified` とし、降格判断は緩和策動作確認後に再評価
- **対象環境では成立しない**: not_applicable で区別、降格でなく「該当なし」扱い

---

## 9. 判定根拠記述テンプレート

各 Finding に以下の構造化記述を必須:

```markdown
**Severity**: High

**3-Axis Score:**
- Exploitability: medium (外部到達は SG で遮断、内部到達のみ)
- Blast Radius: lateral_internal (該当 VLAN の他サーバへ波及可能)
- Service Criticality: business_critical (顧客向け本番)

**Conditions evaluated:**
- C1 機密外部到達: 不成立（SG で遮断、立証済）
- C2 サービス影響迫り: 不成立（使用率 65%、安定）
- C3 root RCE 経路: 不成立（CVE 紐付けなし、3 点立証不可）
- C4 認証情報漏洩: 不成立

**Severity decision**: High に留める。Critical 条件は不成立だが、防御層欠落（root 実行 + EOL）として High。

**Mitigation status**: 既存 SG ルール動作確認済 → High から Medium への降格を検討中、緩和策動作再確認後に再評価
```

---

## 10. observation_status との整合

- `confirmed`: 重大度判定可能
- `confirmed_with_mitigation_unverified`: 降格不可、判定は保守的に
- `likely`: 重大度判定可能だが、根拠欄に「likely」と明記
- `not_observed` / `not_applicable`: Finding 起票せず（または別セクションで言及のみ）
- `unknown_evidence_missing` / `blocked_by_permission`: 重大度判定保留、未確認事項サブセクションへ
- `out_of_scope_phase1`: 重大度判定せず Phase 2 へ送り
- `unsupported_in_v1`: hard fail で Phase 0 停止
