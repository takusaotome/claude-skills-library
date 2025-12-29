# Code Smell Patterns

コードレビューで検出すべきコードスメル（悪臭）とアンチパターンのカタログ。

## 1. Bloaters（肥大化）

コードが大きくなりすぎて扱いにくくなったもの。

### Long Method / Long Function

```python
# 悪い例：長すぎる関数（20行超）
def process_order(order):
    # 検証
    if not order.items:
        raise ValueError("Empty order")
    if not order.customer:
        raise ValueError("No customer")
    # ... 50行以上続く

# 良い例：分割された関数
def process_order(order):
    validate_order(order)
    calculate_total(order)
    apply_discounts(order)
    process_payment(order)
    send_confirmation(order)
```

**検出基準**: 20行を超える関数

### Large Class / God Object

```python
# 悪い例：何でもやるクラス
class OrderManager:
    def create_order(self): ...
    def validate_order(self): ...
    def calculate_tax(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    def backup_database(self): ...
    # 責務が多すぎる

# 良い例：責務を分離
class OrderService: ...
class TaxCalculator: ...
class EmailService: ...
class ReportGenerator: ...
```

**検出基準**: 10以上のパブリックメソッド、複数の異なる責務

### Primitive Obsession

```python
# 悪い例：プリミティブ値の乱用
def create_user(name: str, email: str, phone: str,
                street: str, city: str, zip_code: str):
    pass

# 良い例：ドメインオブジェクトを使用
@dataclass
class Address:
    street: str
    city: str
    zip_code: str

@dataclass
class User:
    name: str
    email: Email  # バリデーション付き
    phone: Phone  # フォーマット付き
    address: Address
```

### Long Parameter List

```python
# 悪い例：パラメータが多すぎる
def send_email(to, cc, bcc, subject, body, attachments,
               reply_to, priority, template, tracking_id):
    pass

# 良い例：オブジェクトにまとめる
@dataclass
class EmailRequest:
    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    # ...

def send_email(request: EmailRequest):
    pass
```

**検出基準**: 4個以上のパラメータ

---

## 2. Object-Orientation Abusers（OO乱用）

オブジェクト指向の原則に反する使い方。

### Switch Statements / Type Checking

```python
# 悪い例：型による分岐
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    elif shape.type == "triangle":
        return 0.5 * shape.base * shape.height

# 良い例：ポリモーフィズム
class Circle:
    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle:
    def area(self):
        return self.width * self.height
```

### Refused Bequest（拒否された遺産）

```python
# 悪い例：親クラスのメソッドを無効化
class Bird:
    def fly(self):
        return "Flying"

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly")  # 継承の誤用
```

### Inappropriate Intimacy（不適切な親密さ）

```python
# 悪い例：他クラスの内部に深く依存
class Order:
    def get_customer_discount(self):
        # Customer の内部実装に依存
        if self.customer._membership_level == 'gold':
            if self.customer._years_active > 5:
                return self.customer._base_discount * 1.5
```

---

## 3. Change Preventers（変更妨害）

変更を困難にするパターン。

### Divergent Change（発散的変更）

一つのクラスが複数の理由で変更される。

```python
# 悪い例：変更理由が複数
class Report:
    def calculate_metrics(self): ...  # ビジネスロジック変更で修正
    def format_html(self): ...        # UI変更で修正
    def send_email(self): ...         # インフラ変更で修正
```

### Shotgun Surgery（散弾銃手術）

一つの変更が多くのクラスに影響する。

```python
# 悪い例：顧客名の表示形式を変えると全箇所を修正
class OrderView:
    def show(self):
        print(f"{customer.first_name} {customer.last_name}")

class InvoiceView:
    def show(self):
        print(f"{customer.first_name} {customer.last_name}")

# 良い例：表示ロジックを一箇所に
class Customer:
    def display_name(self):
        return f"{self.first_name} {self.last_name}"
```

### Parallel Inheritance Hierarchies

新しいサブクラスを作ると、別の階層にも同時にサブクラスが必要になる。

---

## 4. Dispensables（不要物）

なくても問題ないコード。

### Dead Code

```python
# 悪い例：使われないコード
def old_calculate_tax(amount):  # どこからも呼ばれない
    return amount * 0.08

# コメントアウトされたコード
# def legacy_process():
#     ...
```

### Speculative Generality（投機的汎用性）

```python
# 悪い例：使われない汎用化
class AbstractStrategyFactoryBuilderProvider:
    # 将来使うかもしれない...でも使わない
    pass
```

### Lazy Class / Freeloader

```python
# 悪い例：存在意義が薄いクラス
class StringWrapper:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value
```

### Comments（過剰なコメント）

```python
# 悪い例：悪いコードを説明するコメント
# iを1増やす
i = i + 1

# 顧客情報を取得する
customer_info = get_customer_info()

# 悪い例：嘘のコメント
# 税込み価格を返す
def get_price(item):
    return item.base_price  # 税込みではない！
```

---

## 5. Couplers（結合問題）

クラス間の過度な結合。

### Feature Envy（機能の横恋慕）

```python
# 悪い例：他のオブジェクトのデータばかり使う
class Order:
    def calculate_discount(self):
        if self.customer.loyalty_points > 1000:
            if self.customer.membership_years > 5:
                return self.customer.base_discount * 1.5
        return self.customer.base_discount

# 良い例：データを持つオブジェクトにメソッドを移動
class Customer:
    def calculate_discount(self):
        if self.loyalty_points > 1000 and self.membership_years > 5:
            return self.base_discount * 1.5
        return self.base_discount
```

### Message Chains（メッセージの連鎖）

```python
# 悪い例：長いメソッドチェーン
total = order.get_customer().get_account().get_balance().get_available()

# 良い例：Law of Demeter
total = order.get_customer_available_balance()
```

### Middle Man（中間者）

```python
# 悪い例：委譲だけのクラス
class Manager:
    def __init__(self, worker):
        self.worker = worker

    def do_work(self):
        return self.worker.do_work()  # 単なる委譲

    def get_result(self):
        return self.worker.get_result()  # 単なる委譲
```

---

## 6. Anti-Patterns（アンチパターン）

### Singleton Abuse

```python
# 悪い例：テスト不可能なシングルトン
class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

# 使用箇所
db = Database.get_instance()  # グローバル状態、テスト困難
```

### Service Locator

```python
# 悪い例：依存関係が隠れる
class OrderService:
    def process(self, order):
        db = ServiceLocator.get("database")  # 依存が隠れている
        email = ServiceLocator.get("email")  # テスト時に何をモックすべきかわからない
```

### God Class / Blob

```python
# 悪い例：全てを知り、全てを行うクラス
class Application:
    def handle_request(self): ...
    def validate_input(self): ...
    def query_database(self): ...
    def send_email(self): ...
    def generate_report(self): ...
    def log_activity(self): ...
    def manage_cache(self): ...
    # アプリケーションの全機能がここに
```

### Spaghetti Code

```python
# 悪い例：制御フローが絡み合っている
def process(data):
    if data:
        for item in data:
            if item.active:
                if item.type == 'A':
                    if item.value > 100:
                        # 深いネスト
                        for sub in item.children:
                            if sub.valid:
                                # さらに深く...
```

### Copy-Paste Programming

```python
# 悪い例：コピペされたコード
def process_order(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    return total * 1.1  # 税込み

def process_invoice(invoice):
    total = 0
    for item in invoice.items:
        total += item.price * item.quantity  # 同じロジック
    return total * 1.1
```

---

## 7. Error Handling Smells

### Empty Catch / Silent Failure

```python
# 悪い例：エラーを握りつぶす
try:
    process_data()
except Exception:
    pass  # 何が起きても無視

# 悪い例：ログだけで継続
try:
    critical_operation()
except Exception as e:
    logger.error(e)  # ログを出すが処理は続行
```

### Exception Abuse

```python
# 悪い例：制御フローに例外を使用
def find_user(users, name):
    try:
        for user in users:
            if user.name == name:
                raise StopIteration(user)
    except StopIteration as e:
        return e.args[0]
    return None
```

### Catch-All

```python
# 悪い例：すべての例外をキャッチ
try:
    complex_operation()
except Exception:  # 何でもキャッチ
    handle_error()

# 良い例：具体的な例外をキャッチ
try:
    complex_operation()
except ValueError as e:
    handle_value_error(e)
except IOError as e:
    handle_io_error(e)
```

---

## 8. Naming Smells

### Misleading Names

```python
# 悪い例：名前と動作が一致しない
def get_user(user_id):
    user = db.find(user_id)
    user.last_accessed = datetime.now()
    db.save(user)  # getなのに副作用がある
    return user
```

### Cryptic Names

```python
# 悪い例：暗号的な名前
def p(d, f):  # 何の関数？
    return d * f + d

# 良い例
def calculate_price_with_fee(base_price, fee_rate):
    return base_price * fee_rate + base_price
```

### Inconsistent Names

```python
# 悪い例：一貫性のない命名
get_user()
fetch_customer()
retrieve_product()
load_order()
# 全部「取得」だが名前がバラバラ
```

---

## Quick Reference: Smell Detection

| カテゴリ | スメル | 検出キーワード |
|---------|--------|--------------|
| **Bloaters** | Long Method | 20行超の関数 |
| | Long Parameter List | 4個以上のパラメータ |
| | Large Class | 10+メソッド、複数責務 |
| **OO Abusers** | Switch on Type | `if type ==`, `isinstance` の連鎖 |
| | Refused Bequest | `raise NotImplementedError` in override |
| **Change Preventers** | Divergent Change | 1クラスに複数の変更理由 |
| | Shotgun Surgery | 1変更で複数ファイル修正 |
| **Dispensables** | Dead Code | 未使用の関数/クラス |
| | Excessive Comments | コードを説明するコメント |
| **Couplers** | Feature Envy | 他オブジェクトのデータを多用 |
| | Message Chains | `a.b().c().d()` |
| **Anti-Patterns** | Singleton | `get_instance()` |
| | God Class | 何でもやるクラス |
| **Error Handling** | Silent Failure | `except: pass` |
| | Catch-All | `except Exception` |
| **Naming** | Cryptic Names | 1-2文字変数 |
| | Misleading Names | 名前と動作の不一致 |
