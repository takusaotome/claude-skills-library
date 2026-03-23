# File Type Classification

レビュー対象ファイルの自動分類ルール。統合コマンド (`/critical-review`) および
コードレビュースキル (`/critical-code-reviewer`) の Phase 1 で使用する。

## 判定優先順位

1. **ファイル名/明示パターン** — 特定ファイル名で即判定（openapi.json, package.json 等）
2. **拡張子ルール** — 拡張子テーブルに基づく判定
3. **Content Sniffing** — 先頭20行のパターンで判定
4. **確認** — 上記全て不明の場合のみ AskUserQuestion

---

## 拡張子ベース分類

### コードレビュー対象

| 拡張子 | 言語/形式 | Tier |
|--------|----------|------|
| .py | Python | 1 |
| .js, .ts, .jsx, .tsx | JavaScript/TypeScript | 1 |
| .go | Go | 2 |
| .java | Java | 2 |
| .rs | Rust | 2 |
| .c, .cpp, .h, .hpp | C/C++ | 2 |
| .cs | C# | 3 |
| .rb | Ruby | 3 |
| .php | PHP | 3 |
| .swift | Swift | 3 |
| .kt | Kotlin | 3 |
| .scala | Scala | 3 |
| .sh, .bash, .zsh | Shell | 3 |
| .sql | SQL | 3 |
| .vue, .svelte | Frontend Framework | 3 |
| .css, .scss, .less | Stylesheet | 3 |

**Tier の意味**:
- **Tier 1**: 詳細チェック（型安全性、エコシステム固有パターン、追加ルール適用）
- **Tier 2**: 基本チェック（汎用パターン + 言語固有の重大問題検出）
- **Tier 3**: 汎用チェックのみ（全言語共通のコードレビュー観点）

### ドキュメントレビュー対象

| 拡張子/パターン | レビュー観点 |
|---------------|-----------|
| .md, .txt, .rst, .adoc | テキスト文書 |
| .docx, .pdf, .rtf | バイナリ文書 |
| .html, .htm | ドキュメント（非コード用途と判断した場合） |

---

## ファイル名パターン判定

### コードレビュー（設定ファイル）

| ファイル名/パターン | チェック観点 |
|-------------------|-----------|
| package.json | 依存バージョン固定、scripts 定義、engines 制約 |
| tsconfig.json | strict mode 設定、path aliases |
| Dockerfile | non-root 実行、multi-stage ビルド、レイヤー最適化 |
| docker-compose.yml / docker-compose.yaml | リソース制限、ヘルスチェック、環境変数管理 |
| Jenkinsfile | パイプライン構造、secret 取扱い |
| Makefile | ターゲット構造、シェルコマンド安全性 |
| *.tf | Terraform: state 管理、variable validation、module 構造 |
| .github/workflows/*.yml | CI/CD: secret 取扱い、timeout 設定、権限スコープ |
| pom.xml | Maven: 依存管理、プラグイン設定 |
| build.gradle | Gradle: 依存管理、タスク定義 |
| pyproject.toml | Python プロジェクト設定、依存管理 |
| .proto | Protocol Buffers: スキーマ設計、命名規則 |
| Chart.yaml, values.yaml | Helm chart: K8s リソース制限、ヘルスチェック |

### ドキュメントレビュー（スキーマ/仕様）

| ファイル名/パターン | レビュー観点 |
|-------------------|-----------|
| openapi.json, openapi.yaml | API 仕様の正確性、スキーマ整合性 |
| swagger.json, swagger.yaml | 同上（レガシー形式） |
| *.schema.json | JSON Schema 設計の妥当性 |

### 拡張子なしファイル

| ファイル名 | 分類 |
|-----------|------|
| Dockerfile | コード（Config） |
| Jenkinsfile | コード（Config） |
| Makefile | コード（Config） |
| Procfile | コード（Config） |
| Vagrantfile | コード（Config） |

---

## Content Sniffing

拡張子・ファイル名で判定不可の場合、先頭20行を読み以下のパターンで判定:

| パターン | 判定 |
|---------|------|
| `apiVersion:` + `kind:` | K8s manifest → コードレビュー |
| `openapi:` or `swagger:` | OpenAPI spec → ドキュメントレビュー |
| `provider "` or `resource "` | Terraform → コードレビュー |
| `FROM ` (行頭) | Dockerfile → コードレビュー |
| `pipeline {` or `node {` | Jenkinsfile → コードレビュー |
| 上記いずれにも該当しない | AskUserQuestion で確認 |

---

## ディレクトリの場合

配下ファイルの拡張子分布で判定:
- コード系が多数 → コードレビュー
- ドキュメント系が多数 → ドキュメントレビュー
- 混在 → AskUserQuestion で確認
