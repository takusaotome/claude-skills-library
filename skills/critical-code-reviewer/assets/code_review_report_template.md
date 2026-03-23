# Critical Code Review Report

## Review Information

| Item | Value |
|------|-------|
| **Target** | [レビュー対象ファイル/ディレクトリ] |
| **Languages** | [Python, JavaScript, TypeScript, etc.] |
| **Review Date** | [YYYY-MM-DD] |
| **Reviewer Personas** | Veteran Engineer, TDD Expert, Clean Code Expert, Bug Hunter |

---

## Executive Summary

### Issue Summary

| Severity | Count | Action Required |
|----------|-------|-----------------|
| 🔴 Critical | X | Mandatory Fix (マージブロック) |
| 🟠 Major | X | Should Fix |
| 🟡 Minor | X | Recommended |
| 🔵 Info | X | Optional |
| **Total** | **X** | |

### Overall Assessment

[コード全体の品質評価を1-2段落で記述]

**Code Quality Score**: [A / B / C / D / F]

| 観点 | 評価 | コメント |
|------|------|---------|
| 設計品質 | ⭐⭐⭐⭐☆ | [コメント] |
| テスト容易性 | ⭐⭐⭐☆☆ | [コメント] |
| 可読性 | ⭐⭐⭐⭐⭐ | [コメント] |
| 堅牢性 | ⭐⭐⭐⭐☆ | [コメント] |

**Merge Readiness**: ⭕ Ready / 🔺 Conditional / ❌ Not Ready

**Conditions** (if Conditional):
- [必須対応事項]

---

## Findings

### 🔴 Critical

#### [CR-001] [タイトル]

| Item | Value |
|------|-------|
| **Location** | `[file:line]` |
| **Detected By** | [Veteran Engineer / TDD Expert / Clean Code Expert / Bug Hunter] |
| **Category** | [設計 / テスト容易性 / 可読性 / アンチパターン / 失敗モード / 言語固有] |

**Code:**
```[language]
// 問題のあるコード
```

**Problem:**
[何が問題か、なぜ問題かを具体的に説明]

**Impact:**
[この問題が放置された場合の影響]

**Recommended Fix:**
```[language]
// 修正後のコード例
```

---

### 🟠 Major

#### [MJ-001] [タイトル]

| Item | Value |
|------|-------|
| **Location** | `[file:line]` |
| **Detected By** | [ペルソナ名] |
| **Category** | [カテゴリ] |

**Code:**
```[language]
// 問題のあるコード
```

**Problem:**
[問題の説明]

**Recommended Fix:**
```[language]
// 修正後のコード例
```

---

### 🟡 Minor

#### [MN-001] [タイトル]

| Item | Value |
|------|-------|
| **Location** | `[file:line]` |
| **Detected By** | [ペルソナ名] |

**Code:**
```[language]
// 改善可能なコード
```

**Suggestion:**
[改善提案]

---

### 🔵 Info

#### [IN-001] [タイトル]

**Location:** `[file:line]`

**Comment:**
[参考情報や代替案の提案]

---

## Persona-Specific Insights

### 👴 Veteran Engineer Perspective

**Overall Assessment:**
[20年の経験から見たこのコードの評価]

**Key Observations:**
1. [観察1]
2. [観察2]

**Design Concerns:**
- [設計上の懸念点]

**Operational Concerns:**
- [運用上の懸念点]

**Experience-Based Advice:**
> [経験に基づくアドバイス]

---

### 🧪 TDD Expert Perspective

**Testability Assessment:**
[テスト容易性の評価]

**Key Observations:**
1. [観察1]
2. [観察2]

**Testability Issues:**
- [テストしにくい箇所]

**Dependency Management:**
- [依存関係の問題]

**Refactoring Safety:**
- [リファクタリング時のリスク]

**TDD Advice:**
> [TDDの観点からのアドバイス]

---

### ✨ Clean Code Expert Perspective

**Readability Assessment:**
[可読性の評価]

**Key Observations:**
1. [観察1]
2. [観察2]

**Naming Issues:**
- [命名の問題]

**Function Design:**
- [関数設計の問題]

**SOLID Compliance:**
| 原則 | 状態 | コメント |
|------|------|---------|
| SRP (単一責任) | ✅/⚠️/❌ | [コメント] |
| OCP (開放閉鎖) | ✅/⚠️/❌ | [コメント] |
| LSP (リスコフ置換) | ✅/⚠️/❌ | [コメント] |
| ISP (インターフェース分離) | ✅/⚠️/❌ | [コメント] |
| DIP (依存性逆転) | ✅/⚠️/❌ | [コメント] |

**Clean Code Advice:**
> [Clean Codeの観点からのアドバイス]

---

### 🔍 Bug Hunter Perspective

**Failure Mode Assessment:**
[失敗モード分析の評価]

**Key Observations:**
1. [観察1]
2. [観察2]

**Boundary Conditions:**
- [境界条件の問題]

**Idempotency & Concurrency:**
- [冪等性・並行実行の問題]

**Impact Analysis:**
| 観点 | 状態 | コメント |
|------|------|---------|
| 呼び出し元への影響 | ✅/⚠️/❌ | [コメント] |
| 後方互換性 | ✅/⚠️/❌ | [コメント] |
| リソース管理 | ✅/⚠️/❌ | [コメント] |

**P0/P1 Issues:**
- [壊れる・漏れる・戻せない問題]

**Bug Hunter Advice:**
> [失敗モード起点のアドバイス]

---

## Language-Specific Findings

### Python Specific (if applicable)

| Check | Status | Comment |
|-------|--------|---------|
| Type Hints | ✅/⚠️/❌ | [コメント] |
| Optional Usage | ✅/⚠️/❌ | [コメント] |
| Pythonic Patterns | ✅/⚠️/❌ | [コメント] |
| Exception Handling | ✅/⚠️/❌ | [コメント] |
| Context Managers | ✅/⚠️/❌ | [コメント] |

### JavaScript/TypeScript Specific (if applicable)

| Check | Status | Comment |
|-------|--------|---------|
| Type Safety | ✅/⚠️/❌ | [コメント] |
| any Usage | ✅/⚠️/❌ | [コメント] |
| async/await | ✅/⚠️/❌ | [コメント] |
| Error Handling | ✅/⚠️/❌ | [コメント] |
| this Binding | ✅/⚠️/❌ | [コメント] |

---

## Improvement Recommendations

### Priority 1: Must Fix (マージ前に対応必須)

- [ ] [CR-001] [アクション内容]
- [ ] [CR-002] [アクション内容]

### Priority 2: Should Fix (早期に対応推奨)

- [ ] [MJ-001] [アクション内容]
- [ ] [MJ-002] [アクション内容]

### Priority 3: Nice to Have (時間があれば対応)

- [ ] [MN-001] [アクション内容]

---

## Positive Highlights

このコードの良い点も記録します：

- ✅ [良い点1]
- ✅ [良い点2]
- ✅ [良い点3]

---

## Appendix

### A. Review Scope

| Item | Value |
|------|-------|
| Files Reviewed | [件数] |
| Lines of Code | [行数] |
| Review Method | Multi-Persona Critical Review |

### B. Severity Definitions

※判定基準の詳細は `references/severity_criteria.md` を参照。ここはレポート読者向けの概要のみ。

| Severity | Definition |
|----------|------------|
| Critical | バグ、セキュリティ、データ損失の可能性。マージブロック。 |
| Major | 保守性に重大な影響。技術的負債。要修正。 |
| Minor | 改善推奨だが緊急ではない。 |
| Info | ベストプラクティス提案。参考情報。 |

### C. Code Quality Score Guide

| Score | Criteria |
|-------|----------|
| A | Critical/Major なし。Minor は軽微。良質なコード。 |
| B | Critical なし。Major が軽微。全体的に良好。 |
| C | Critical なし。Major が数件。改善の余地あり。 |
| D | Critical なし。Major が多数。要改善。 |
| F | Critical あり。マージ不可。 |

---

*This report was generated by critical-code-reviewer skill*
