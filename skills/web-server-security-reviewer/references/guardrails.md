# Guardrails — Read-only Guard Hierarchy & Approval Flow

レビュー実施時に守るべきガード規律。SKILL.md §0 の中核。違反時はレビュー中断、立会者へエスカレーション。

---

## 1. 6 階層 read-only ガード分類

### 1.1 allowed — 包括承認で実行可

立会者承認のもと、特に注意なく実行できるコマンド。

| カテゴリ | 例 |
|---|---|
| ファイル情報 | `ls`, `ls -l`, `stat`, `file`, `wc -l`, `wc -c` |
| プロセス | `ps`, `ps -ef`, `pgrep` |
| ネットワーク状態 | `ss`, `netstat -tlnp`（read-only）|
| systemd 状態 | `systemctl status`, `systemctl is-active`, `systemctl is-enabled` |
| OS 情報 | `uname`, `uname -r`, `cat /etc/os-release`, `getenforce`, `hostnamectl` |
| ディスク・メモリ | `df`, `df -h`, `free`, `free -h` |
| 範囲制限 du | `du -h -d 2 -x /var /home /opt /usr` ← `command_reference.yaml` の制約に従う |
| `cat <非秘密>` | `cat /etc/os-release`, `cat /proc/cpuinfo` |

### 1.2 conditional — 観点・対象を明示し承認後実行

出力に秘密値が出ない既知のコマンド。実行前に「この観点でこのコマンドを実行する」と立会者に明示し、承認を得る。

| カテゴリ | 例 |
|---|---|
| ネットワーク詳細 | `iptables -L`, `ip route`, `ip addr`, `firewall-cmd --list-all` |
| ファイルシステム探索 | `find <制限> -type f -perm <制限>`（`command_reference.yaml` の制約厳守）|
| ログ閲覧 | `journalctl --since '24 hours ago' --no-pager` (時間窓・行数制限)、`tail -n 100 /var/log/<file>` |
| パッケージ情報 | `rpm -qa`, `dpkg -l`, `npm list --depth=0`, `pip list` |
| 設定確認 | `crontab -l`（要 conditional_sensitive 検討、§1.3 参照）|

### 1.3 conditional_sensitive — 出力後マスク必須

コマンド自体は read-only だが、**出力に秘密値が含まれる可能性がある**。出力後に必ずマスクし、raw を `raw_evidence_store` に直接保存、要約のみ `evidence_dir` に転記する。

| 例 | 漏洩リスク |
|---|---|
| `nginx -T` | 証明書パス、upstream、Basic 認証、Environment= |
| `apachectl -S` | VirtualHost 設定、ファイルパス |
| `systemctl cat <unit>` | `Environment=` に秘密値 |
| `sshd -T` | AuthorizedKeysCommand、TrustedUserCAKeys |
| `crontab -l` (root) | バッチに含まれる秘密値・URL |
| `iptables-save` | コメント・カスタムチェイン名 |
| `nft list ruleset` | 同上 |

**実行手順**:
1. 立会者に「出力に秘密値が含まれる可能性あり」を通知し承認取得
2. 出力本体は `raw_evidence_store/raw_outputs/` に保存
3. `secret_masking.md` の正規表現でマスク後、要約を `evidence_dir/<axis>/` に転記
4. Finding 根拠欄には「`nginx -T` 出力で確認、本文は raw_evidence_store/<path> 参照」のように記述
5. offline_evidence で raw が提供されない場合は `unknown_evidence_missing` 扱い、追加証跡要求リストへ

### 1.4 ask-first — 都度承認

read-only でも本番負荷上昇または広範囲スキャンとなるため、実行前に都度承認を取る。

| 例 | 理由 |
|---|---|
| `tcpdump`, `tshark` | ネットワーク負荷、長時間ストリーム |
| `strace`, `ltrace` | 性能影響 |
| `journalctl -f` | 長時間ストリーム |
| 広範囲 `grep -r` | I/O 負荷 |
| `nmap localhost` | スキャン挙動 |
| `lsof` | 大規模システムで重い |

### 1.5 exceptional_sensitive_read — 二重承認 + raw 限定保管 + 要約転記禁止

Phase 1 で本文取得が必要な限定ケース。**立会者 + シークレットオーナーの二重承認**が必要。

**Phase 1 で本文取得が必要な例（限定的）:**
- `sudo cat /etc/sudoers`（sudoers 構文・NOPASSWD 確認）
- `sudo cat /etc/vpnc/<config>`（VPN 平文認証情報の存在確認、値はマスク）
- `sudo cat /etc/nginx/conf.d/<vhost>.conf`（conditional_sensitive で代替可能なら不要）

**完全禁止（本文取得・要約取得ともに exceptional_sensitive_read 区分）:**
- `/etc/shadow` の **全アクセス**（`cat`、`head`、`tail`、`awk`、`grep` 等）。**Phase 1 では原則実施しない**
- `*.key`、`id_rsa` 等の秘密鍵本文（`stat`/`ls -l` のみ allowed）
- DB データベースダンプ本文（schema 構造のみ別途）

**やむを得ず /etc/shadow を限定要約する場合**:
- 区分: exceptional_sensitive_read（**conditional 区分にしない**）
- 必須: 二重承認（立会者 + シークレットオーナー）
- 出力: `awk -F: '{print $1, length($2)}'` 等の **長さ・形式のみ** に限定
- 保管: raw_evidence_store 直接保存、evidence_dir には件数のみ要約転記
- Finding 根拠欄に本文転記禁止

**実行手順**:
1. 立会者と秘密オーナーから二重承認を取得（target_profile.yaml の追記必須）
2. 実行コマンドと取得理由を `raw_command_log.jsonl` に記録
3. 出力は `raw_evidence_store/raw_outputs/` にのみ保存
4. 要約版・Finding 根拠欄には **本文を一切転記せず**、「取得済み・raw_evidence_store/<path> 参照」で済ませる
5. 取得後 90 日（または target_profile の retention に従う）で raw を削除

### 1.6 forbidden — 絶対禁止

target host を変更する操作。違反時はレビュー中断、立会者にエスカレーション。

| カテゴリ | 例 |
|---|---|
| target host 上の書込 | `>`, `>>`, `tee`（target で実行）|
| ファイル変更 | `sed -i`, `truncate`, `rm`, `mv`, `cp`（書込先）, `chmod`, `chown` |
| サービス制御 | `systemctl restart`, `systemctl stop`, `systemctl start`, `systemctl reload`, `systemctl enable`, `systemctl disable`, `service ... restart` |
| crontab 変更 | `crontab -e`, `crontab <file>` |
| ログローテ | `logrotate -f` |
| 証明書更新 | `certbot renew`, `certbot run` |
| ファイアウォール変更 | `ufw <変更>`, `firewall-cmd <変更>`, `iptables <変更>`, `nft add/delete/flush` |
| コンテナ操作 | `docker compose up/down`, `docker run/start/stop`, `podman ...` |
| パッケージ変更 | `dnf/apt/yum install/remove/update/upgrade` |
| プロセス制御 | `kill`, `pkill`, `killall` |
| 認証情報変更 | `passwd`, `chpasswd`, `usermod`, `groupmod` |

---

## 2. 実行コンテキストの分離（remote vs local 書込）

forbidden の `>`/`>>`/`tee`/`cp` 等は **target host 上で実行された場合に限る**。SSH 経由で出力を採取者ローカル端末に保存するのは allowed。

### 2.1 SSH redirect の 4 ケース

| ケース | コマンド | 動作 | 扱い |
|---|---|---|---|
| ① 引用の外で redirect | `ssh host 'cat /etc/foo' > ./evidence/file` | local（採取者端末）に書込 | **allowed** |
| ② 引用の中で redirect | `ssh host 'cat /etc/foo > /tmp/x'` | target host に書込 | **forbidden** |
| ③ パイプ後 local tee | `ssh host 'cat /etc/foo' \| tee ./evidence/file` | local に書込 | **allowed** |
| ④ 引用の中で tee | `ssh host 'cat /etc/foo \| tee /tmp/x'` | target host に書込 | **forbidden** |

### 2.2 判定ルール

redirect / tee の対象パスが SSH 引用符の **外側** ならローカル書込（allowed）、**内側** なら target 書込（forbidden）。引用符の位置で挙動が変わる点を実行前に必ず確認。

### 2.3 target 上一時ファイル経由の禁止

| ケース | 扱い |
|---|---|
| `ssh host 'sudo cat /etc/sudoers > /tmp/x' && scp host:/tmp/x local && ssh host 'rm /tmp/x'` | **forbidden** |

target 上に一時ファイル作成は変更とみなす。代替策: `ssh host 'sudo cat /etc/sudoers' > local_file` のように **stdout を SSH 経由で local へ流す**形を取る。

### 2.4 採取者ローカルへの保存（allowed）

| 例 | 扱い |
|---|---|
| `ssh host 'cmd' > local_file` | allowed |
| `scp host:remote local` | allowed |
| `ssh host 'cmd' \| tee local_file`（local 側 tee）| allowed |
| `rsync -e ssh host:remote local`（read-only）| allowed |

---

## 3. 立会者承認フロー

### 3.1 包括承認（allowed コマンド向け）

target_profile.yaml の以下フィールドで一括承認を確認:
- `ssh.approved_by`: 立会者氏名
- `ssh.approved_at`: ISO8601 タイムスタンプ
- `scope.axes_in_scope`: 実行する観点
- `scope.role_extensions`: 適用する役割拡張

承認外コマンドの実行検知時はレビュー中断。

### 3.2 都度承認（conditional / conditional_sensitive / ask-first）

各実行前に以下を立会者に提示:
- 観点 (axis_id) と check_id
- 実行コマンド（`command_resolved`、placeholder 解決済み）
- 想定される出力範囲とサイズ上限
- 漏洩リスク（conditional_sensitive の場合）

立会者の承認を `command_log.jsonl` の `approved_by` フィールドに記録。

### 3.3 二重承認（exceptional_sensitive_read）

立会者承認に加え、**シークレットオーナーの承認**が必要。target_profile.yaml に以下を追記:

```yaml
exceptional_approvals:
  - command: "sudo cat /etc/sudoers"
    purpose: "NOPASSWD 行確認"
    approved_by_witness: "<立会者氏名>"
    approved_by_secret_owner: "<シークレットオーナー氏名>"
    approved_at: "<ISO8601>"
    raw_storage_path: "raw_evidence_store/raw_outputs/sudoers.txt"
```

### 3.4 違反時の対応

forbidden コマンドの実行検知 / 承認外コマンドの実行 / evidence_dir に raw 混入の検知時:
1. 直ちにレビュー中断
2. `_violation_log.jsonl` に違反内容を記録
3. 立会者にエスカレーション
4. 影響範囲（target 変更の有無、漏洩した秘密の特定）を確認
5. 必要なら認証情報ローテーション、incident_context.active_incident=true で再開

---

## 4. 区分判定のチェックリスト（コマンド実行前）

新規コマンドを実行する前に以下を確認:

- [ ] 出力に秘密値が含まれる可能性は？（あれば conditional_sensitive 以上）
- [ ] target host 上で書込が発生するか？（する場合は forbidden）
- [ ] 本番負荷を上げる可能性は？（ある場合は ask-first 以上）
- [ ] command_reference.yaml に許可された実行パターンがあるか？（ない場合は ask-first 以上）
- [ ] placeholder は target_profile から解決済みか？（未解決なら実行ブロック）
- [ ] 立会者承認は得ているか？（なければ実行不可）

判断に迷う場合は ask-first として扱い、立会者に確認。
