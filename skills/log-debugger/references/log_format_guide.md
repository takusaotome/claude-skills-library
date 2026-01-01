# Log Format Guide

## Overview

様々なログフォーマットの解説と、解析時のポイントをまとめたリファレンスです。

---

## 1. JSON Structured Logs

### 特徴
- 機械可読性が高い
- フィールドが明確
- クエリ/フィルタリングが容易

### 一般的な構造

```json
{
  "timestamp": "2025-01-15T10:30:45.123Z",
  "level": "ERROR",
  "logger": "com.example.service.UserService",
  "message": "Failed to process user request",
  "thread": "http-nio-8080-exec-1",
  "context": {
    "userId": "12345",
    "requestId": "abc-def-123",
    "traceId": "xyz-789"
  },
  "exception": {
    "class": "java.lang.NullPointerException",
    "message": "Cannot invoke method on null object",
    "stackTrace": [
      "com.example.service.UserService.processUser(UserService.java:45)",
      "com.example.controller.UserController.handleRequest(UserController.java:23)"
    ]
  }
}
```

### 解析ポイント

| フィールド | 用途 |
|-----------|------|
| timestamp | 時系列分析、タイムライン作成 |
| level | 重要度フィルタリング |
| logger | 発生源の特定 |
| message | エラー内容の把握 |
| context | トレース、ユーザー特定 |
| exception | スタックトレース分析 |

### jqでの解析例

```bash
# ERRORレベルのログを抽出
cat app.log | jq 'select(.level == "ERROR")'

# 特定ユーザーのログを抽出
cat app.log | jq 'select(.context.userId == "12345")'

# タイムスタンプでソート
cat app.log | jq -s 'sort_by(.timestamp)'

# エラーメッセージの頻度集計
cat app.log | jq -r 'select(.level == "ERROR") | .message' | sort | uniq -c | sort -rn
```

---

## 2. Apache/Nginx Access Log

### Apache Combined Log Format

```
192.168.1.100 - john [15/Jan/2025:10:30:45 +0900] "GET /api/users/123 HTTP/1.1" 200 1234 "https://example.com/page" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

### フォーマット分解

| 位置 | 内容 | 例 |
|-----|------|-----|
| 1 | クライアントIP | 192.168.1.100 |
| 2 | identd | - |
| 3 | ユーザー名 | john |
| 4 | タイムスタンプ | [15/Jan/2025:10:30:45 +0900] |
| 5 | リクエスト | "GET /api/users/123 HTTP/1.1" |
| 6 | ステータスコード | 200 |
| 7 | レスポンスサイズ | 1234 |
| 8 | リファラー | "https://example.com/page" |
| 9 | User-Agent | "Mozilla/5.0..." |

### Nginx Log Format

```
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent" "$http_x_forwarded_for"
```

### 解析ポイント

- **ステータスコード**: 4xx/5xx の急増に注目
- **レスポンスタイム**: 追加設定で記録可能
- **リクエストパス**: エラーが集中するパスを特定
- **クライアントIP**: 特定IPからの異常アクセス

### awkでの解析例

```bash
# 5xxエラーを抽出
awk '$9 ~ /^5/ {print}' access.log

# ステータスコード別の集計
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# IPアドレス別のリクエスト数
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -20

# 時間帯別のリクエスト数
awk '{print $4}' access.log | cut -d: -f1,2 | uniq -c
```

---

## 3. Syslog (RFC 5424)

### フォーマット

```
<priority>version timestamp hostname app-name procid msgid structured-data msg
```

### 例

```
<34>1 2025-01-15T10:30:45.123456+09:00 myhost myapp 12345 ID47 [exampleSDID@32473 iut="3" eventSource="Application"] Application started
```

### Priority計算

```
priority = facility * 8 + severity
```

| Facility | 値 | 説明 |
|----------|---|------|
| kern | 0 | カーネルメッセージ |
| user | 1 | ユーザーレベルメッセージ |
| mail | 2 | メールシステム |
| daemon | 3 | システムデーモン |
| auth | 4 | セキュリティ/認証 |
| syslog | 5 | syslogd内部 |
| local0-7 | 16-23 | ローカル使用 |

| Severity | 値 | 説明 |
|----------|---|------|
| emerg | 0 | システム使用不可 |
| alert | 1 | 即座に対処が必要 |
| crit | 2 | 重大な状態 |
| err | 3 | エラー |
| warning | 4 | 警告 |
| notice | 5 | 正常だが重要 |
| info | 6 | 情報 |
| debug | 7 | デバッグ |

### journalctlでの解析

```bash
# 特定サービスのログ
journalctl -u nginx.service

# 特定期間のログ
journalctl --since "2025-01-15 10:00" --until "2025-01-15 12:00"

# エラー以上のログ
journalctl -p err

# JSON形式で出力
journalctl -o json-pretty

# リアルタイム監視
journalctl -f
```

---

## 4. AWS CloudWatch Logs

### 構造

```json
{
  "logGroup": "/aws/lambda/my-function",
  "logStream": "2025/01/15/[$LATEST]abc123",
  "timestamp": 1705289445123,
  "message": "START RequestId: abc-def-123 Version: $LATEST"
}
```

### Lambda ログパターン

```
START RequestId: abc-def-123 Version: $LATEST
2025-01-15T10:30:45.123Z abc-def-123 INFO Processing request
2025-01-15T10:30:45.456Z abc-def-123 ERROR Failed to process: NullPointerException
END RequestId: abc-def-123
REPORT RequestId: abc-def-123 Duration: 123.45 ms Billed Duration: 124 ms Memory Size: 128 MB Max Memory Used: 64 MB
```

### CloudWatch Logs Insightsクエリ

```sql
-- エラーログの抽出
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

-- Lambda実行時間の分析
fields @timestamp, @message
| filter @type = "REPORT"
| parse @message "Duration: * ms" as duration
| stats avg(duration), max(duration), min(duration) by bin(1h)

-- エラーの頻度集計
fields @timestamp, @message
| filter @message like /Exception/
| stats count() by bin(5m)
```

---

## 5. Kubernetes Logs

### Pod ログ構造

```
2025-01-15T10:30:45.123456789Z stdout F {"level":"info","msg":"Server started","port":8080}
```

| 部分 | 説明 |
|------|------|
| タイムスタンプ | RFC3339Nano形式 |
| stdout/stderr | 出力ストリーム |
| F/P | 完全(F)または部分(P)ログ |
| メッセージ | 実際のログ内容 |

### kubectlでの取得

```bash
# Podのログ
kubectl logs my-pod

# 特定コンテナのログ
kubectl logs my-pod -c my-container

# 過去1時間のログ
kubectl logs my-pod --since=1h

# リアルタイム監視
kubectl logs -f my-pod

# ラベルでフィルタ
kubectl logs -l app=myapp

# 全Podのログ
kubectl logs -l app=myapp --all-containers
```

### イベントログ

```bash
# 全イベント
kubectl get events --sort-by='.lastTimestamp'

# 特定Namespaceのイベント
kubectl get events -n my-namespace

# Warning以上のイベント
kubectl get events --field-selector type=Warning
```

---

## 6. Stack Trace Patterns

### Java

```
java.lang.NullPointerException: Cannot invoke method on null object
    at com.example.service.UserService.processUser(UserService.java:45)
    at com.example.service.UserService.handleRequest(UserService.java:23)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:897)
Caused by: java.sql.SQLException: Connection refused
    at com.mysql.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:2181)
    ... 15 more
```

### Python

```
Traceback (most recent call last):
  File "/app/main.py", line 45, in process_request
    result = service.execute(data)
  File "/app/service.py", line 23, in execute
    return self.db.query(sql)
  File "/app/database.py", line 78, in query
    cursor.execute(sql)
psycopg2.OperationalError: connection to server at "localhost" failed
```

### JavaScript/Node.js

```
Error: ECONNREFUSED 127.0.0.1:5432
    at TCPConnectWrap.afterConnect [as oncomplete] (net.js:1141:16)
    at Protocol._enqueue (/app/node_modules/mysql/lib/protocol/Protocol.js:144:48)
    at Connection.query (/app/node_modules/mysql/lib/Connection.js:198:25)
    at /app/src/database.js:45:12
    at processTicksAndRejections (internal/process/task_queues.js:93:5)
```

### スタックトレース解析のポイント

1. **最初のエラー**: 一番上のエラーメッセージを確認
2. **発生箇所**: 自分のコードの最初の行を特定
3. **Caused by**: 根本原因となった例外を確認
4. **フレームワーク層**: フレームワーク内部は通常スキップ

---

## 7. Timestamp Format Reference

| 形式 | 例 | 用途 |
|------|-----|------|
| ISO 8601 | 2025-01-15T10:30:45.123Z | JSON、API |
| RFC 3339 | 2025-01-15T10:30:45+09:00 | Kubernetes |
| Common Log | 15/Jan/2025:10:30:45 +0900 | Apache |
| Syslog | Jan 15 10:30:45 | Linux syslog |
| Unix Epoch | 1705289445 | 内部処理 |
| Unix Epoch ms | 1705289445123 | CloudWatch |

### タイムゾーン注意点

- UTCとローカル時刻の混在に注意
- サーバー間で時刻がずれている可能性
- 夏時間（DST）の影響
- タイムスタンプの解析時はタイムゾーンを明示
