# Failure Mode Patterns for Bug Hunter

不具合検出に特化したBug Hunterペルソナが参照する失敗モードパターン集。

---

## 5-Pass Workflow（Codex式レビュー手順）

### Pass 1: 意図を固定する（2分）

**目的**: 変更の成功条件を明確化

**アクション**:
1. PR説明/コミットメッセージから「何を直したいのか」を1行で要約
2. 成功条件を2〜3個で書く（例：空入力でも500にならない、権限なしは401）

**チェック**:
```markdown
□ PRの目的を1行で言える
□ 成功条件が明確
□ 失敗条件も想像できる
```

### Pass 2: 差分の"入口→出口"をトレース（5〜15分）

**目的**: データフローを追跡し、変換ポイントを特定

**トレース順序**:
```
入力 → バリデーション → 変換 → 主要ロジック → 出力
```

**各ステップでの確認**:
| ステップ | 確認事項 |
|---------|---------|
| 入力 | パラメータ/JSON/DB/外部API |
| バリデーション | 型、範囲、null、フォーマット |
| 変換 | 正規化、丸め、timezone、エンコード |
| 主要ロジック | 分岐、ループ、状態遷移 |
| 出力 | レスポンス/DB更新/イベント/ログ |

### Pass 3: diffの外に出て"影響範囲"を潰す（5〜10分）

**目的**: 変更の波及効果を検出

**必須チェック**:
```markdown
□ 呼び出し元検索: シグネチャ変更・挙動変更が他に波及してないか
□ 同名/同責務の実装確認: 既存パターンと整合しているか
□ 設定・feature flag・ロールアウト: 互換性が壊れてないか
□ テストコード: 既存テストが失敗しないか
```

### Pass 4: 失敗モード（壊れ方）起点で眺める（5分）

**目的**: 正常系より先に「壊しに行く」

**テンプレート**:
```markdown
□ 空 / null / 未指定 / 0 / 負数 / 最大長
□ タイムアウト / リトライ / 二重送信（冪等性）
□ 並行実行（ロック、競合、順序）
□ 部分失敗（DB成功→外部API失敗 等）
□ 例外の握りつぶし、ログだけ出して成功扱い
```

### Pass 5: 検証（テスト・lint・再現手順）を見る（3〜10分）

**目的**: 変更を守るテストがあるか確認

**チェック**:
```markdown
□ テストがあるか（ないなら、どの失敗モードを守るテストが必要かをコメント）
□ 既存テストの意図に合ってるか（意味のないアサートになってないか）
□ ローカルで最小の再現手順が用意されているか
```

---

## Failure Mode Categories

### Category 1: 境界条件（Boundary Conditions）

**検出対象**:
```python
# 1.1 空コレクション
items[0]              # IndexError if empty
first = items.pop()   # IndexError if empty
max(values)           # ValueError if empty

# 1.2 ゼロ除算
result = total / count       # count=0
average = sum(vals) / len(vals)  # empty list

# 1.3 負数
items[-1]             # Last item, but what if intentional?
range(n)              # n < 0 gives empty range
sleep(seconds)        # seconds < 0?

# 1.4 最大値
array[MAX_INT]        # Overflow?
str * count           # count が巨大だとメモリ溢れ
"x" * 10**9           # Memory explosion
```

**質問テンプレート**:
- このコレクションが空の時どうなる？
- この数値が0の時どうなる？
- この数値が負の時どうなる？
- この入力が最大長の時どうなる？

### Category 2: Null/None/NaN処理

**検出対象**:
```python
# 2.1 メソッドチェーン
user.address.city.name  # どこかがNone

# 2.2 属性アクセス
name.lower()           # AttributeError if None

# 2.3 NaN伝播（pandas）
df['result'] = df['a'] + df['b']  # NaN propagates

# 2.4 暗黙のNone
def process(x):
    if x > 0:
        return x * 2
    # else returns None implicitly!

# 2.5 辞書アクセス
value = data['key']           # KeyError
value = data.get('key') + 1   # TypeError if None
```

**質問テンプレート**:
- この値がNoneの時どうなる？
- NaNが混入した時、どこまで伝播する？
- このパスを通るとNoneが返る可能性は？

### Category 3: 冪等性（Idempotency）

**検出対象**:
```python
# 3.1 カウンター増加
def process_order(order_id):
    increment_counter()  # 2回呼ばれたら2回増加
    do_work()

# 3.2 課金処理
def charge_customer(customer_id, amount):
    payment_gateway.charge(amount)  # 2回呼ばれたら2回課金

# 3.3 通知送信
def send_notification(user_id, message):
    email_service.send(user_id, message)  # 重複送信

# 3.4 データ挿入
def save_data(data):
    db.insert(data)  # 重複レコード
```

**質問テンプレート**:
- この処理が2回実行されたらどうなる？
- リトライ時に副作用が重複しない？
- 一意キーや重複チェックの仕組みはある？

### Category 4: 並行実行（Concurrency）

**検出対象**:
```python
# 4.1 TOCTOU (Time-of-check to time-of-use)
if balance >= amount:
    # Another thread may modify balance here!
    balance -= amount

# 4.2 Read-Modify-Write
counter = get_counter()
counter += 1
set_counter(counter)  # Lost update

# 4.3 共有状態への非同期アクセス
class Cache:
    data = {}  # Shared mutable state
    def set(self, key, value):
        self.data[key] = value  # Race condition

# 4.4 順序依存
async def process():
    result1 = await task1()
    result2 = await task2()  # task2 depends on task1?
```

**質問テンプレート**:
- 同時に2つのリクエストが来たらどうなる？
- この共有状態への同時アクセスは安全？
- チェックと使用の間に状態が変わる可能性は？

### Category 5: 部分失敗（Partial Failure）

**検出対象**:
```python
# 5.1 複数操作の途中失敗
def transfer_funds(from_account, to_account, amount):
    withdraw(from_account, amount)  # 成功
    deposit(to_account, amount)     # 失敗 → 資金消失

# 5.2 外部API呼び出しチェーン
def process_order(order):
    save_to_db(order)           # 成功
    send_to_payment(order)      # 成功
    notify_warehouse(order)     # 失敗 → 不整合

# 5.3 ロールバック漏れ
try:
    step1()
    step2()
    step3()
except:
    rollback_step1()  # step2のロールバックは？
```

**質問テンプレート**:
- 途中で失敗したら、どこまでロールバックできる？
- トランザクション境界は適切？
- 失敗時のクリーンアップは完全？

### Category 6: リソース管理（Resource Management）

**検出対象**:
```python
# 6.1 ファイルハンドルリーク
def read_file(path):
    f = open(path)
    return f.read()  # f.close() never called

# 6.2 コネクションリーク
def query_db():
    conn = get_connection()
    result = conn.execute(sql)
    if error:
        raise Exception()  # conn not closed
    conn.close()
    return result

# 6.3 ロック解放漏れ
def critical_section():
    lock.acquire()
    risky_operation()  # 例外発生時、lock.release()されない
    lock.release()
```

**質問テンプレート**:
- リソースは必ず解放される？
- 例外発生時のクリーンアップは？
- context manager（with文）を使うべき？

### Category 7: タイムアウト/リトライ

**検出対象**:
```python
# 7.1 タイムアウトなし
response = requests.get(url)  # 無限に待つ

# 7.2 無限リトライ
while True:
    try:
        result = call_api()
        break
    except:
        time.sleep(1)  # 永遠にリトライ

# 7.3 リトライによる副作用重複
for attempt in range(3):
    try:
        send_payment()  # 各リトライで課金される
        break
    except Timeout:
        continue
```

**質問テンプレート**:
- タイムアウトは設定されている？
- リトライ上限はある？
- リトライ時に副作用が重複しない？

### Category 8: 例外処理

**検出対象**:
```python
# 8.1 例外の握りつぶし
try:
    risky_operation()
except Exception:
    pass  # Silent failure

# 8.2 広すぎるexcept
try:
    process()
except Exception as e:  # KeyboardInterrupt も捕まえる
    log(e)

# 8.3 不適切な例外型
try:
    items[0]
except ValueError:  # IndexError なのに
    handle_error()

# 8.4 ログのみで続行
try:
    validate(data)
except ValidationError as e:
    logger.warning(e)
    # continues with invalid data!
```

**質問テンプレート**:
- この例外は本当に無視していい？
- 例外型は正しい？
- ログだけで続行して問題ない？

---

## P0/P1 Priority Checklist

### P0: 壊れる・漏れる・戻せない

**Correctness（仕様どおりか）**:
- [ ] 既存仕様の暗黙の不変条件（invariant）を壊してないか
- [ ] 条件分岐の抜け（特に else 側）・順序依存
- [ ] 型変換・丸め・timezone・locale

**Reliability（落ちない・詰まらない）**:
- [ ] 例外の握りつぶし、戻り値の誤魔化し
- [ ] リトライで重複実行されると壊れる処理（冪等性）
- [ ] リソースクリーンアップ（ファイル、コネクション、ロック）

### P1: パフォーマンス・コスト

- [ ] ループ内のI/O（DB/API）増加
- [ ] キャッシュ無効化、N+1
- [ ] 重い計算がリクエストパスに乗ってないか

---

## Impact Analysis Questions

### 呼び出し元への影響

```markdown
□ この関数のシグネチャが変わった？ → 呼び出し元を全て確認
□ 戻り値の型や構造が変わった？ → 呼び出し元の処理を確認
□ 例外の型が変わった？ → 呼び出し元のcatchを確認
□ 副作用が追加された？ → 呼び出し元の期待と整合
```

### 後方互換性

```markdown
□ APIのレスポンス形式が変わった？ → 既存クライアントは動く？
□ デフォルト値が変わった？ → 既存の呼び出しに影響は？
□ 必須パラメータが追加された？ → 既存の呼び出しは失敗する？
□ 設定ファイルの形式が変わった？ → 既存設定との互換性は？
```

### 同名実装との整合性

```markdown
□ 同じ名前の関数/クラスが他にある？ → 挙動は整合している？
□ 同じ責務を持つ実装が他にある？ → パターンは統一されている？
□ インターフェースの実装がある？ → 契約は守られている？
```

---

## Quick Reference: Red Flags

| パターン | 想定される問題 |
|---------|--------------|
| `except: pass` | 例外の握りつぶし |
| `[0]` without length check | 空コレクションでIndexError |
| `.lower()` without null check | NoneでAttributeError |
| `requests.get(url)` | タイムアウトなし |
| `while True: try: ... except: ...` | 無限リトライ |
| Shared mutable state | レースコンディション |
| Multiple operations without transaction | 部分失敗 |
| `open()` without `with` | リソースリーク |
| Check then use pattern | TOCTOU脆弱性 |
| No deduplication key | 冪等性欠如 |
