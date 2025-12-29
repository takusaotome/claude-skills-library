# Language-Specific Checks

Python と JavaScript/TypeScript に特化した追加チェックポイント。

---

## Python Specific Checks

### 1. 型ヒント（Type Hints）

#### 型ヒントの有無

```python
# 悪い例：型ヒントなし
def process_data(data):
    return data.transform()

# 良い例：型ヒントあり
def process_data(data: DataFrame) -> DataFrame:
    return data.transform()
```

**チェックポイント**:
- [ ] 関数のパラメータに型ヒントがあるか
- [ ] 戻り値に型ヒントがあるか
- [ ] 複雑な型には `TypeVar`, `Generic` を使用しているか

#### Optional の適切な使用

```python
# 悪い例：None を返す可能性が不明
def find_user(user_id: int) -> User:
    user = db.query(user_id)
    return user  # None かもしれない

# 良い例：Optional で明示
from typing import Optional

def find_user(user_id: int) -> Optional[User]:
    user = db.query(user_id)
    return user

# より良い例：存在しない場合の処理を強制
def find_user(user_id: int) -> User:
    user = db.query(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user
```

#### Union と TypeVar

```python
# 悪い例：any の乱用
def merge(a: any, b: any) -> any:
    pass

# 良い例：適切な型制約
from typing import TypeVar, Union

T = TypeVar('T')

def merge(a: T, b: T) -> T:
    pass

# または
def process(value: Union[str, int]) -> str:
    pass
```

### 2. Pythonic Patterns

#### リスト内包表記

```python
# 非Pythonic
result = []
for item in items:
    if item.active:
        result.append(item.name)

# Pythonic
result = [item.name for item in items if item.active]

# ただし複雑すぎる内包表記は避ける
# 悪い例：読みにくい
result = [
    process(item.value)
    for item in items
    if item.active and item.value > 0 and validate(item)
]

# 良い例：関数に分離
def should_include(item):
    return item.active and item.value > 0 and validate(item)

result = [process(item.value) for item in items if should_include(item)]
```

#### 真偽値チェック

```python
# 非Pythonic
if len(items) == 0:
    pass
if items == []:
    pass
if items == None:
    pass

# Pythonic
if not items:
    pass
if items is None:
    pass
```

#### enumerate と zip

```python
# 非Pythonic
for i in range(len(items)):
    print(i, items[i])

# Pythonic
for i, item in enumerate(items):
    print(i, item)

# 非Pythonic
for i in range(len(list1)):
    print(list1[i], list2[i])

# Pythonic
for item1, item2 in zip(list1, list2):
    print(item1, item2)
```

#### コンテキストマネージャ

```python
# 悪い例：リソースリークの可能性
f = open('file.txt')
data = f.read()
f.close()  # 例外時に呼ばれない

# 良い例：with文
with open('file.txt') as f:
    data = f.read()
```

### 3. 例外処理

#### 具体的な例外をキャッチ

```python
# 悪い例：すべてキャッチ
try:
    process()
except Exception:
    pass

# 悪い例：裸のexcept
try:
    process()
except:
    pass

# 良い例：具体的な例外
try:
    process()
except ValueError as e:
    handle_value_error(e)
except KeyError as e:
    handle_key_error(e)
```

#### 例外の再送出

```python
# 悪い例：スタックトレースを失う
try:
    process()
except Exception as e:
    logger.error(e)
    raise Exception("Error occurred")  # 元の例外情報が失われる

# 良い例：チェーンを維持
try:
    process()
except Exception as e:
    logger.error(e)
    raise ProcessingError("Error occurred") from e
```

### 4. データクラスとNamedTuple

```python
# 悪い例：辞書の乱用
user = {
    'name': 'John',
    'email': 'john@example.com',
    'age': 30
}

# 良い例：dataclass
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int

# イミュータブルが必要な場合
@dataclass(frozen=True)
class User:
    name: str
    email: str
    age: int
```

### 5. Python特有のアンチパターン

```python
# 悪い例：ミュータブルなデフォルト引数
def add_item(item, items=[]):  # 危険！
    items.append(item)
    return items

# 良い例
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# 悪い例：グローバル変数の変更
config = {}

def setup():
    global config
    config['key'] = 'value'

# 良い例：依存性注入
def setup(config: dict):
    config['key'] = 'value'
```

---

## JavaScript / TypeScript Specific Checks

### 1. 型安全性（TypeScript）

#### any の乱用

```typescript
// 悪い例：anyの乱用
function process(data: any): any {
    return data.transform();
}

// 良い例：具体的な型
interface DataInput {
    transform(): DataOutput;
}

function process(data: DataInput): DataOutput {
    return data.transform();
}

// 型がわからない場合は unknown
function process(data: unknown): void {
    if (isValidData(data)) {
        // 型ガードで絞り込む
    }
}
```

#### strict null checks

```typescript
// 悪い例：nullチェックなし
function getName(user: User | null): string {
    return user.name;  // user が null の可能性
}

// 良い例：オプショナルチェーン
function getName(user: User | null): string | undefined {
    return user?.name;
}

// または事前チェック
function getName(user: User | null): string {
    if (user === null) {
        throw new Error('User is required');
    }
    return user.name;
}
```

#### 型アサーションの乱用

```typescript
// 悪い例：型アサーションで型チェックを回避
const user = data as User;  // data が本当に User か不明

// 良い例：型ガードを使用
function isUser(data: unknown): data is User {
    return (
        typeof data === 'object' &&
        data !== null &&
        'name' in data &&
        'email' in data
    );
}

if (isUser(data)) {
    // ここでは data は User 型
}
```

### 2. async/await パターン

#### 適切なエラーハンドリング

```typescript
// 悪い例：エラーハンドリングなし
async function fetchData() {
    const response = await fetch(url);
    return response.json();
}

// 良い例：try-catch
async function fetchData() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        logger.error('Fetch failed:', error);
        throw error;
    }
}
```

#### awaitの忘れ

```typescript
// 悪い例：awaitを忘れている
async function process() {
    fetch(url);  // Fire and forget!
    console.log('Done');
}

// 良い例
async function process() {
    await fetch(url);
    console.log('Done');
}
```

#### Promise.all の適切な使用

```typescript
// 悪い例：順次実行（遅い）
async function fetchAll() {
    const user = await fetchUser();
    const posts = await fetchPosts();
    const comments = await fetchComments();
    return { user, posts, comments };
}

// 良い例：並列実行（速い）
async function fetchAll() {
    const [user, posts, comments] = await Promise.all([
        fetchUser(),
        fetchPosts(),
        fetchComments()
    ]);
    return { user, posts, comments };
}
```

### 3. this バインディング

```typescript
// 悪い例：thisが意図通りにバインドされない
class Handler {
    name = 'Handler';

    handleClick() {
        console.log(this.name);  // コールバックで使うとundefined
    }
}

const handler = new Handler();
button.addEventListener('click', handler.handleClick);  // thisが壊れる

// 良い例1：アロー関数
class Handler {
    name = 'Handler';

    handleClick = () => {
        console.log(this.name);
    }
}

// 良い例2：bind
button.addEventListener('click', handler.handleClick.bind(handler));
```

### 4. == vs ===

```typescript
// 悪い例：緩い等価演算子
if (value == null) {  // undefined も含む
    // ...
}

if (value == 0) {  // '' や false も true になる
    // ...
}

// 良い例：厳密等価演算子
if (value === null || value === undefined) {
    // ...
}

if (value === 0) {
    // ...
}

// 例外：null と undefined の両方をチェックする場合
if (value == null) {  // これは許容される場合もある
    // ...
}
```

### 5. イミュータブルなデータ操作

```typescript
// 悪い例：ミュータブルな操作
const users = getUsers();
users.push(newUser);  // 元の配列を変更

// 良い例：イミュータブルな操作
const users = getUsers();
const updatedUsers = [...users, newUser];  // 新しい配列を作成

// オブジェクトの場合
// 悪い例
user.name = 'New Name';

// 良い例
const updatedUser = { ...user, name: 'New Name' };
```

### 6. JavaScript特有のアンチパターン

```typescript
// 悪い例：varの使用
var count = 0;  // スコープの問題

// 良い例：const/let
const count = 0;  // 再代入しない
let mutableCount = 0;  // 再代入する

// 悪い例：暗黙の型変換
const result = '5' + 3;  // '53'
const result2 = '5' - 3;  // 2

// 良い例：明示的な変換
const result = String(5) + '3';
const result2 = Number('5') - 3;

// 悪い例：コールバック地獄
getData(function(a) {
    getMoreData(a, function(b) {
        getEvenMoreData(b, function(c) {
            // ...
        });
    });
});

// 良い例：async/await
async function getData() {
    const a = await getData();
    const b = await getMoreData(a);
    const c = await getEvenMoreData(b);
}
```

---

## Quick Reference: Language Check Matrix

### Python

| カテゴリ | チェック項目 | 重大度 |
|---------|------------|--------|
| 型ヒント | 関数に型ヒントがあるか | Minor |
| 型ヒント | Optional が適切に使われているか | Major |
| Pythonic | リスト内包表記が使えるか | Info |
| Pythonic | enumerate/zip を使っているか | Info |
| 例外処理 | 具体的な例外をキャッチしているか | Major |
| 例外処理 | 例外チェーンを維持しているか | Minor |
| データ構造 | dataclass を使っているか | Info |
| アンチパターン | ミュータブルなデフォルト引数 | Critical |
| アンチパターン | グローバル変数の変更 | Major |

### JavaScript/TypeScript

| カテゴリ | チェック項目 | 重大度 |
|---------|------------|--------|
| 型安全性 | any を乱用していないか | Major |
| 型安全性 | strict null checks | Major |
| 型安全性 | 型アサーションの乱用 | Major |
| async/await | await を忘れていないか | Critical |
| async/await | エラーハンドリングがあるか | Major |
| async/await | Promise.all で並列化できないか | Info |
| thisバインディング | コールバックでthisが壊れないか | Major |
| 等価演算子 | === を使っているか | Minor |
| イミュータビリティ | 配列/オブジェクトをイミュータブルに操作 | Minor |
| アンチパターン | var を使っていないか | Minor |
| アンチパターン | コールバック地獄 | Major |
