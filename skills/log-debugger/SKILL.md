---
name: log-debugger
description: |
  システムログを分析してエラーの根本原因を特定し、段階的に深堀りしていくデバッグ専門家スキル。
  アプリケーションログ、システムログ、クラウドサービスログなど様々な形式に対応。
  5 Whys、タイムライン分析、Fishbone分析などのRCA（根本原因分析）手法を用いて
  問題の本質を突き止め、再発防止策まで提案する。

  Use when analyzing system logs to find error root causes, debugging application issues,
  investigating incidents, or performing post-mortem analysis.

  Triggers: "analyze this log", "find the root cause", "debug this error",
  "why is this failing", "investigate this incident", "log analysis",
  "what caused this crash", "troubleshoot this issue"
---

# Log Debugger

## Overview

このスキルは、システムログを体系的に分析し、エラーの根本原因を特定するデバッグ専門家です。

**対応ログタイプ:**
- アプリケーションログ（Python/Java/Node.js例外、スタックトレース）
- システムログ（Linux syslog, journald, Windows Event Log）
- クラウドサービスログ（AWS CloudWatch, Azure Monitor, GCP Logging）
- Webサーバーログ（Apache, Nginx）
- Kubernetesログ

## 4-Phase Analysis Framework

```
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: TRIAGE（トリアージ）                                       │
│  「何が起きているのか？」                                             │
│  └─ ログ概要把握、エラー重要度判定、影響範囲の特定                     │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 2: PATTERN RECOGNITION（パターン認識）                        │
│  「どのようなパターンがあるか？」                                      │
│  └─ エラーパターン特定、関連イベント抽出、時系列整理                    │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 3: ROOT CAUSE ANALYSIS（根本原因分析）                        │
│  「なぜ起きたのか？」                                                 │
│  └─ 5 Whys分析、タイムライン再構築、因果関係特定                       │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 4: RESOLUTION & PREVENTION（解決と再発防止）                  │
│  「どう直し、どう防ぐか？」                                           │
│  └─ 修正提案、再発防止策、監視強化ポイント                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Triage（トリアージ）

### 目的
ログの全体像を把握し、問題の重要度と影響範囲を素早く判断する。

### 手順

1. **ログの取り込みと正規化**
   ```bash
   # log_analyzer.pyを使用してログを解析
   python scripts/log_analyzer.py analyze <logfile> --summary
   ```

2. **エラーレベルの集計**
   - FATAL/CRITICAL: 即時対応が必要
   - ERROR: 調査が必要
   - WARN: 監視対象
   - INFO/DEBUG: 参考情報

3. **影響範囲の特定**
   - 影響を受けたユーザー数/リクエスト数
   - 影響を受けたサービス/コンポーネント
   - 発生時間帯と継続時間

### チェックリスト
```markdown
□ ログの時間範囲を確認
□ エラー件数を集計
□ 最も深刻なエラーを特定
□ 影響範囲を推定
□ 緊急度を判定（P0/P1/P2/P3）
```

---

## Phase 2: Pattern Recognition（パターン認識）

### 目的
エラーのパターンを識別し、関連するイベントを抽出する。

### 手順

1. **エラーパターンの検出**
   ```bash
   # エラーキーワードで検索
   python scripts/log_analyzer.py search <logfile> --keywords "Exception,Error,Failed,Timeout"

   # 正規表現でパターン検出
   python scripts/log_analyzer.py search <logfile> --pattern "Connection.*refused|timeout.*\d+ms"
   ```

2. **頻度分析**
   ```bash
   # エラー頻度レポート
   python scripts/log_analyzer.py report <logfile> --frequency
   ```

3. **時系列パターンの確認**
   - 特定時刻に集中しているか
   - 周期的に発生しているか
   - 漸増/急増しているか

### パターン分類
| パターン | 特徴 | 典型的な原因 |
|----------|------|--------------|
| 突発的 | 特定時刻に急増 | デプロイ、設定変更、外部障害 |
| 周期的 | 一定間隔で発生 | cron、バッチ処理、リソース枯渇 |
| 漸増型 | 徐々に増加 | メモリリーク、ディスク枯渇 |
| 散発的 | ランダムに発生 | 競合状態、間欠的な外部障害 |

### 参照
- `references/log_patterns.md` - よくあるエラーパターン集

---

## Phase 3: Root Cause Analysis（根本原因分析）

### 目的
問題の根本原因を特定する。表面的な症状ではなく、本質的な原因を突き止める。

### 手法1: 5 Whys分析

**プロセス:**
1. 現象を明確に記述
2. 「なぜ？」を5回繰り返す
3. 各回答を検証可能な形で記録

**例:**
```
現象: APIが500エラーを返している

1. なぜ？ → データベースクエリがタイムアウトしている
2. なぜ？ → 特定のテーブルへのクエリが遅い
3. なぜ？ → テーブルにインデックスがない
4. なぜ？ → 新しいカラムを追加した際にインデックスを作成しなかった
5. なぜ？ → スキーマ変更時のインデックス確認プロセスがなかった

→ 根本原因: スキーマ変更時のレビュープロセスの不備
```

### 手法2: タイムライン分析

```bash
# タイムライン生成
python scripts/log_analyzer.py timeline <logfile> --from "2025-01-01 10:00" --to "2025-01-01 12:00"
```

**タイムライン作成手順:**
1. 関連するすべてのログソースを収集
2. タイムスタンプで統合・ソート
3. 重要イベントをマーク
4. 因果関係を推論

### 手法3: Fishbone（特性要因図）分析

6つのカテゴリで原因を分析:
- **People**: 人的要因（操作ミス、知識不足）
- **Process**: プロセス要因（手順の不備、承認漏れ）
- **Technology**: 技術要因（バグ、設計ミス）
- **Environment**: 環境要因（インフラ、ネットワーク）
- **Data**: データ要因（不正データ、データ量）
- **External**: 外部要因（サードパーティ障害）

### 参照
- `references/rca_methodology.md` - 根本原因分析手法の詳細

---

## Phase 4: Resolution & Prevention（解決と再発防止）

### 目的
問題を解決し、同様の問題の再発を防ぐ。

### 解決策の策定

1. **応急処置 (Immediate Fix)**
   - 影響を最小化する一時的な対応
   - ロールバック、リスタート、回避策

2. **恒久対策 (Permanent Fix)**
   - 根本原因を解消する本質的な修正
   - コード修正、設計変更、プロセス改善

### 再発防止策

1. **検知の強化**
   - アラート追加
   - ログレベル調整
   - メトリクス追加

2. **防止の強化**
   - バリデーション追加
   - テスト追加
   - レビュープロセス強化

3. **復旧の強化**
   - ランブック整備
   - 自動復旧機構
   - フェイルオーバー設定

### 出力
- `assets/rca_report_template.md` を使用してRCAレポートを作成

---

## Scripts

### log_analyzer.py

ログ解析を自動化するPythonツール。

**基本的な使い方:**
```bash
# エラー検出
python scripts/log_analyzer.py analyze <logfile>

# キーワード検索
python scripts/log_analyzer.py search <logfile> --keywords "timeout,error"

# タイムライン生成
python scripts/log_analyzer.py timeline <logfile>

# レポート生成
python scripts/log_analyzer.py report <logfile> --output report.md

# 複数ログの相関分析
python scripts/log_analyzer.py correlate app.log nginx.log db.log
```

**設定ファイル:**
`assets/analyzer_config_template.yaml` をコピーしてプロジェクト固有の設定を行う。

---

## Resources

### References
| ファイル | 用途 |
|----------|------|
| `references/rca_methodology.md` | 5 Whys、Fishbone等のRCA手法 |
| `references/log_patterns.md` | よくあるエラーパターン集 |
| `references/log_format_guide.md` | 各種ログフォーマット解説 |
| `references/debugging_strategies.md` | デバッグ戦略・思考法 |

### Assets
| ファイル | 用途 |
|----------|------|
| `assets/rca_report_template.md` | RCAレポートテンプレート |
| `assets/analyzer_config_template.yaml` | log_analyzer.py設定テンプレート |

---

## Usage Examples

### 例1: アプリケーションクラッシュの調査

```
User: このログを分析して、アプリがクラッシュした原因を見つけてください。
[ログファイルを添付]

Claude:
1. [Phase 1] ログを読み込み、FAITALエラーを検出
2. [Phase 2] スタックトレースを抽出、OutOfMemoryErrorを特定
3. [Phase 3] 5 Whys分析を実施
   - Why 1: OutOfMemoryError発生
   - Why 2: ヒープメモリが枯渇
   - Why 3: 大量のオブジェクトがGCされない
   - Why 4: キャッシュにサイズ制限がない
   - Why 5: キャッシュ設計時にメモリ管理を考慮していなかった
4. [Phase 4] 修正提案: LRUキャッシュ導入、ヒープサイズ調整
```

### 例2: 間欠的なタイムアウト調査

```
User: 時々APIがタイムアウトします。ログを見てください。

Claude:
1. [Phase 1] タイムアウトエラーを抽出、頻度を確認
2. [Phase 2] 時間帯分析 → 毎時0分に集中
3. [Phase 3] タイムライン分析 → cron jobと同時刻
4. [Phase 4] 提案: バッチ処理の時間分散、コネクションプール拡大
```

---

## Best Practices

### Do's
- 複数のログソースを突合して分析する
- タイムスタンプを正確に揃える
- 仮説を立てて検証する
- 根本原因まで深掘りする
- 再発防止策まで提案する

### Don'ts
- 最初に見つけたエラーだけで判断しない
- 相関関係を因果関係と混同しない
- 表面的な症状への対処で終わらせない
- 単一のログソースだけで結論を出さない
