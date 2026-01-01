# Common Log Error Patterns

## Overview

よくあるエラーパターンとその典型的な原因、調査ポイントをまとめたリファレンスです。

---

## Application Layer Errors

### NullPointerException / TypeError / AttributeError

**パターン例:**
```
java.lang.NullPointerException: Cannot invoke method on null object
TypeError: Cannot read property 'name' of undefined
AttributeError: 'NoneType' object has no attribute 'get'
```

**典型的な原因:**
- 未初期化の変数へのアクセス
- APIレスポンスが想定外（null/undefined）
- データベースクエリが空の結果を返した
- 設定ファイルの読み込み失敗

**調査ポイント:**
- [ ] スタックトレースで発生箇所を特定
- [ ] 該当オブジェクトがnullになる経路を追跡
- [ ] 入力データの検証
- [ ] 関連する上流処理のログ確認

---

### OutOfMemoryError / MemoryError

**パターン例:**
```
java.lang.OutOfMemoryError: Java heap space
MemoryError: Unable to allocate array
FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory
```

**典型的な原因:**
- メモリリーク（解放されないオブジェクト）
- 大量データの一括ロード
- キャッシュのサイズ制限なし
- 無限ループによるオブジェクト生成

**調査ポイント:**
- [ ] ヒープダンプ/メモリプロファイルの取得
- [ ] GCログの確認
- [ ] 発生直前の処理内容
- [ ] データ量の確認
- [ ] 長時間実行後に発生するか、即時発生するか

---

### Connection Timeout / Socket Timeout

**パターン例:**
```
java.net.SocketTimeoutException: connect timed out
Error: connect ETIMEDOUT 10.0.0.1:5432
ConnectionError: HTTPConnectionPool: Max retries exceeded (Connection timeout)
```

**典型的な原因:**
- ネットワーク到達不能
- ファイアウォール/セキュリティグループの設定
- 接続先サービスの過負荷
- DNS解決の問題
- コネクションプールの枯渇

**調査ポイント:**
- [ ] 接続先の状態確認
- [ ] ネットワーク経路の確認（ping, traceroute）
- [ ] ファイアウォール設定
- [ ] DNS解決の確認
- [ ] コネクションプールの状態
- [ ] 同時発生している他のエラー

---

### Connection Refused

**パターン例:**
```
java.net.ConnectException: Connection refused
Error: connect ECONNREFUSED 127.0.0.1:6379
ConnectionRefusedError: [Errno 111] Connection refused
```

**典型的な原因:**
- 接続先サービスが起動していない
- ポートが間違っている
- サービスがリッスンしていない（bind先の問題）
- 接続数制限に達した

**調査ポイント:**
- [ ] 接続先サービスの稼働状態
- [ ] ポート番号の確認
- [ ] リッスンアドレスの確認（0.0.0.0 vs 127.0.0.1）
- [ ] 接続数制限の確認
- [ ] プロセスの状態確認（ps, netstat）

---

### Deadlock

**パターン例:**
```
ERROR: deadlock detected
DETAIL: Process 12345 waits for ShareLock on transaction 67890
Deadlock found when trying to get lock
javax.persistence.PessimisticLockException: could not execute statement
```

**典型的な原因:**
- 複数トランザクションの循環待ち
- ロック取得順序の不統一
- 長時間トランザクション

**調査ポイント:**
- [ ] デッドロックに関与したプロセス/トランザクション
- [ ] ロックされたリソース
- [ ] 実行されていたSQL/操作
- [ ] 発生頻度とパターン

---

## Infrastructure Layer Errors

### Disk Full / No Space Left

**パターン例:**
```
OSError: [Errno 28] No space left on device
ENOSPC: no space left on device
ERROR: could not extend file: No space left on device
```

**典型的な原因:**
- ログファイルの肥大化
- 一時ファイルの蓄積
- バックアップファイルの蓄積
- データベースのWAL/binlogの肥大化

**調査ポイント:**
- [ ] ディスク使用状況（df -h）
- [ ] 大きなファイルの特定（du, find）
- [ ] ログローテーション設定
- [ ] 一時ディレクトリの状態
- [ ] inode使用状況（df -i）

---

### OOM Killer

**パターン例:**
```
Out of memory: Kill process 12345 (java) score 900 or sacrifice child
Killed process 12345 (python) total-vm:8000000kB, anon-rss:4000000kB
```

**典型的な原因:**
- システム全体のメモリ不足
- 特定プロセスのメモリ過剰消費
- メモリ制限（cgroup）の設定が厳しすぎる
- メモリリーク

**調査ポイント:**
- [ ] dmesg/syslogでOOM Killerのログ確認
- [ ] 対象プロセスのメモリ使用履歴
- [ ] 他のプロセスのメモリ使用状況
- [ ] swap使用状況
- [ ] cgroup/コンテナのメモリ制限

---

### Permission Denied

**パターン例:**
```
PermissionError: [Errno 13] Permission denied: '/var/log/app.log'
EACCES: permission denied, open '/etc/config.json'
java.io.FileNotFoundException: /data/file.txt (Permission denied)
```

**典型的な原因:**
- ファイル/ディレクトリの権限不足
- SELinux/AppArmor による制限
- 実行ユーザーの変更
- マウントオプション（ro, noexec）

**調査ポイント:**
- [ ] ファイル/ディレクトリの権限確認（ls -la）
- [ ] 実行ユーザー/グループの確認
- [ ] SELinux/AppArmor の状態確認
- [ ] マウントオプションの確認

---

### Network Unreachable

**パターン例:**
```
Network is unreachable
ENETUNREACH: network is unreachable
OSError: [Errno 101] Network is unreachable
```

**典型的な原因:**
- ルーティングテーブルの問題
- ネットワークインターフェースのダウン
- VPN/トンネルの切断
- ネットワーク設定の誤り

**調査ポイント:**
- [ ] ネットワークインターフェースの状態（ip a）
- [ ] ルーティングテーブル（ip route）
- [ ] デフォルトゲートウェイへの疎通
- [ ] DNS設定

---

## Cloud Service Errors

### Rate Limiting / Throttling

**パターン例:**
```
TooManyRequestsException: Rate exceeded
HTTP 429 Too Many Requests
ThrottlingException: Rate exceeded
SlowDown: Please reduce your request rate
```

**典型的な原因:**
- APIコール数が制限を超過
- 短時間に大量リクエスト
- バッチ処理による集中アクセス
- リトライによる雪だるま効果

**調査ポイント:**
- [ ] API呼び出し頻度の確認
- [ ] リトライ設定（指数バックオフ）
- [ ] バッチサイズの確認
- [ ] 並列度の確認
- [ ] サービスの制限値確認

---

### Service Unavailable (503)

**パターン例:**
```
HTTP 503 Service Unavailable
ServiceUnavailableException: The service is currently unavailable
temporarily unavailable, please try again later
```

**典型的な原因:**
- サービス側のメンテナンス
- サービス側の障害
- サービス側の過負荷
- ヘルスチェック失敗

**調査ポイント:**
- [ ] サービスのステータスページ確認
- [ ] 公式の障害情報確認
- [ ] 他のリージョン/エンドポイントの状態
- [ ] 発生時刻とサービスのメンテナンス予定

---

### Authentication Failure

**パターン例:**
```
AuthenticationException: Invalid credentials
HTTP 401 Unauthorized
AccessDeniedException: User is not authorized
InvalidSignatureException: The request signature we calculated does not match
```

**典型的な原因:**
- 認証情報の期限切れ
- 認証情報の誤り
- 権限の不足
- 時刻同期のずれ（署名ベース認証）
- 認証情報のローテーション失敗

**調査ポイント:**
- [ ] 認証情報の有効期限確認
- [ ] 認証情報の正確性確認
- [ ] IAMポリシー/権限の確認
- [ ] システム時刻の確認（NTP同期）
- [ ] 認証情報のローテーション履歴

---

## Database Errors

### Query Timeout

**パターン例:**
```
QueryTimeoutException: Query timed out after 30000 ms
canceling statement due to statement timeout
Error: Query timeout expired
```

**典型的な原因:**
- 非効率なクエリ
- インデックス欠如
- テーブルロック
- データ量の増大
- リソース不足

**調査ポイント:**
- [ ] 実行計画（EXPLAIN）の確認
- [ ] インデックスの確認
- [ ] テーブル統計の確認
- [ ] 同時実行クエリの確認
- [ ] データ量の確認

---

### Connection Pool Exhausted

**パターン例:**
```
Cannot acquire connection from pool
HikariPool-1 - Connection is not available, request timed out
pool is draining, cannot acquire connection
```

**典型的な原因:**
- コネクションリーク
- プールサイズが小さすぎる
- 長時間実行クエリ
- トランザクションの未クローズ

**調査ポイント:**
- [ ] プール設定（最大サイズ、タイムアウト）
- [ ] アクティブコネクション数
- [ ] 長時間実行クエリの確認
- [ ] コネクション取得/返却のバランス

---

## Error Pattern Quick Reference

| パターン | 主な原因カテゴリ | 最初に確認すべきこと |
|----------|------------------|---------------------|
| NullPointer | Application | スタックトレース |
| OutOfMemory | Resource | ヒープ使用量、GCログ |
| Timeout | Network/Resource | 接続先の状態 |
| Connection Refused | Service | サービス稼働状態 |
| Deadlock | Concurrency | ロック情報 |
| Disk Full | Resource | df -h, du |
| OOM Killer | Resource | dmesg, メモリ使用量 |
| Permission Denied | Security | ls -la, 実行ユーザー |
| Rate Limit | External | API呼び出し頻度 |
| 503 | External | サービスステータス |
| Auth Failure | Security | 認証情報、権限 |
| Query Timeout | Database | EXPLAIN、インデックス |
| Pool Exhausted | Resource | プール設定、リーク |
