# Network Diagnostics Report Template

<!-- Template for Claude to generate network quality reports. -->
<!-- Fill in values from DiagnosticsResult JSON. -->
<!-- Use box-drawing characters for tables. -->

## Report Format

```
# ネットワーク診断レポート

実行日時: {{timestamp}}
プラットフォーム: {{platform}}

## 1. 接続情報

┌─────────────────┬──────────────────────────────────────┐
│ 項目             │ 値                                   │
├─────────────────┼──────────────────────────────────────┤
│ インターフェース │ {{connection.interface}}              │
│ 接続タイプ       │ {{connection.type}}                  │
│ IPアドレス       │ {{connection.ip}}/{{connection.cidr}} │
│ ゲートウェイ     │ {{connection.gateway}}               │
│ DNS              │ {{connection.dns | join(", ")}}      │
│ ISP              │ {{connection.isp | default("不明")}} │
│ MAC              │ {{connection.mac}}                   │
│ MTU              │ {{connection.mtu}}                   │
└─────────────────┴──────────────────────────────────────┘

## 2. レイテンシ（Ping テスト）

┌──────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ ターゲット       │ 平均     │ 最小     │ 最大     │ Jitter   │ Loss     │ 評価     │
├──────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ {{name}} ({{ip}})│ {{avg}}ms│ {{min}}ms│ {{max}}ms│ {{std}}ms│ {{loss}}%│ {{rate}} │
│ ...              │          │          │          │          │          │          │
└──────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

<!-- For 100% packet loss targets, show N/A for avg/min/max/stddev -->
<!-- Rating: GOOD / WARNING / CRITICAL based on connection type thresholds -->

## 3. ダウンロード速度

┌──────────────────────────┬────────────┬─────────────┬──────────┐
│ サーバー                 │ 速度       │ サイズ      │ 評価     │
├──────────────────────────┼────────────┼─────────────┼──────────┤
│ {{label}}                │ {{speed}} Mbps │ {{size}} │ {{rate}} │
│ ...                      │            │             │          │
├──────────────────────────┼────────────┼─────────────┼──────────┤
│ 中央値                   │ {{median}} Mbps │ -       │ {{rate}} │
└──────────────────────────┴────────────┴─────────────┴──────────┘

<!-- Use median speed for overall evaluation -->

## 4. HTTP 接続タイミング

┌──────────────────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ URL                      │ DNS      │ TCP      │ TLS      │ TTFB     │ Total    │
├──────────────────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ {{url}}                  │ {{dns}}ms│ {{tcp}}ms│ {{tls}}ms│ {{ttfb}}ms│{{total}}ms│
│ ...                      │          │          │          │          │          │
└──────────────────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

<!-- Each timing metric evaluated independently per common thresholds -->

## 5. 経路解析（Traceroute）

宛先: {{target_name}} ({{target}})

┌──────┬──────────────────────────────┬─────────────┬──────────┐
│ Hop  │ ホスト                       │ RTT         │ 状態     │
├──────┼──────────────────────────────┼─────────────┼──────────┤
│  1   │ {{hostname}} ({{ip}})        │ {{rtt}} ms  │ OK       │
│  2   │ * * *                        │ -           │ Timeout  │
│ ...  │                              │             │          │
└──────┴──────────────────────────────┴─────────────┴──────────┘

合計ホップ数: {{total_hops}} → {{rate}}

## 6. 総合評価

┌─────────────────┬──────────┐
│ カテゴリ         │ 評価     │
├─────────────────┼──────────┤
│ レイテンシ       │ {{rate}} │
│ パケットロス     │ {{rate}} │
│ ダウンロード速度 │ {{rate}} │
│ HTTP タイミング  │ {{rate}} │
│ 経路             │ {{rate}} │
├─────────────────┼──────────┤
│ 総合             │ {{rate}} │
└─────────────────┴──────────┘

<!-- Overall: CRITICAL if any CRITICAL, WARNING if any WARNING, else GOOD -->

## 7. 検出された問題（問題がある場合のみ表示）

<!-- List WARNING/CRITICAL items with specific values and thresholds -->

### 問題 1: {{category}} - {{severity}}
- **検出値**: {{value}}
- **閾値**: {{threshold}}
- **影響**: {{impact}}

<!-- Repeat for each issue -->

## 8. 深堀り分析（CRITICAL/WARNING 検出時のみ）

<!-- Load deep_dive_procedures.md and execute relevant investigation -->
<!-- Include additional test results and root cause analysis -->

### 調査結果
- **根本原因**: {{root_cause}}
- **追加テスト結果**: {{additional_results}}
- **推奨対策**: {{remediation}}

---

## エラー・スキップ情報

<!-- Show only if errors[] or skipped_tests[] are non-empty -->

### エラー
{{#each errors}}
- {{this}}
{{/each}}

### スキップされたテスト
{{#each skipped_tests}}
- {{this}}
{{/each}}
```

## Report Generation Rules

1. Use connection type (Ethernet/Wi-Fi) to select appropriate thresholds
2. Round all timing values to 1 decimal place in report
3. Round speed values to 2 decimal places
4. Use median download speed for overall speed evaluation
5. Show N/A for metrics that could not be collected
6. Omit sections where all tests were skipped
7. Always include the error/skip section if non-empty
8. For ISP field, show "不明" if null
