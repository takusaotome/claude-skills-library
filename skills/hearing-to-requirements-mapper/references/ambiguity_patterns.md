# Ambiguity Patterns in Requirements

This document identifies common ambiguity patterns to detect during requirements analysis.

## 1. Vague Quantifiers

### Pattern: Non-specific amounts or degrees

**Ambiguous words to flag:**
| Japanese | English | Category |
|----------|---------|----------|
| 多くの | many, much | Quantity |
| いくつかの | several, some | Quantity |
| 大量の | large amount | Quantity |
| 十分な | sufficient, enough | Quantity |
| 高速 | fast, quick | Performance |
| 迅速 | rapid, prompt | Performance |
| 適切な | appropriate | Subjective |
| 簡単 | easy, simple | Subjective |
| 効率的 | efficient | Subjective |

**Detection patterns:**
```
/多く|いくつか|大量|十分|高速|迅速|適切|簡単|効率的/
/many|several|some|enough|fast|quick|appropriate|easy|simple|efficient/i
```

**Resolution:** Request specific numbers, percentages, or measurable criteria.

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "多くのユーザー" | "初期1,000人、1年後5,000人" |
| "高速に動作" | "応答時間3秒以内" |
| "効率的に処理" | "処理時間を現行比50%削減" |

---

## 2. Undefined Subjects

### Pattern: Missing actor or system component

**Ambiguous structures:**
| Japanese Pattern | English Pattern | Issue |
|-----------------|-----------------|-------|
| "〜される" (passive) | "is processed" | Who/what does it? |
| "〜が必要" | "is needed" | Who needs it? |
| "対応する" | "handle/support" | What handles it? |

**Detection patterns:**
```
/される$|される必要|が必要$|対応する$/
/is processed|is handled|is needed|will be supported/i
```

**Resolution:** Identify the specific actor (user role or system component).

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "データが処理される" | "バッチサーバーがデータを処理する" |
| "承認が必要" | "部門マネージャーが承認する" |
| "エラーに対応する" | "システムがエラーをログに記録し、管理者に通知する" |

---

## 3. Incomplete Conditions

### Pattern: Missing when/if/unless conditions

**Incomplete structures:**
- "〜する" without conditions
- "〜の場合" without else/otherwise
- "〜時に" without all scenarios

**Detection patterns:**
```
/の場合[^、。]/  # "場合" without covering other cases
/場合を除き/     # exception without main case
```

**Examples:**
| Ambiguous | Complete |
|-----------|----------|
| "エラーの場合、通知する" | "エラーの場合、管理者にメール通知する。正常完了の場合、ログに記録のみ" |
| "ユーザーが削除する" | "ユーザーが削除ボタンを押下し、確認ダイアログでOKを選択した場合に削除する" |

---

## 4. Undefined Terms

### Pattern: Domain-specific or technical terms without definition

**Categories to flag:**
1. **Acronyms**: CRM, ERP, API, SaaS
2. **Business terms**: "顧客"、"担当者"、"案件"
3. **Technical terms**: "同期"、"リアルタイム"、"バッチ"
4. **Process terms**: "承認"、"申請"、"確定"

**Detection:** Build glossary and flag first occurrence of undefined terms.

**Resolution:** Add to glossary with clear definition.

**Glossary entry format:**
```
用語: 顧客 (Customer)
定義: システムに登録された取引先企業および担当者情報。個人顧客は含まない。
同義語: 取引先、クライアント
関連用語: 見込み顧客、既存顧客
```

---

## 5. Unbounded Lists

### Pattern: Open-ended enumerations

**Ambiguous markers:**
| Japanese | English |
|----------|---------|
| 〜など | etc., and so on |
| 〜等 | and others |
| 〜を含む | including |
| 等々 | and more |
| その他 | others |

**Detection patterns:**
```
/など$|等$|を含む$|等々|その他/
/etc\.|and so on|including|and more|and others/i
```

**Resolution:** Enumerate complete list or define criteria for inclusion.

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "Excel、PDF、CSVなど" | "Excel (.xlsx)、PDF、CSV、JSON" |
| "管理者を含む全ユーザー" | "一般ユーザー、管理者、システム管理者の3ロール" |

---

## 6. Comparative Without Baseline

### Pattern: Comparisons without reference point

**Ambiguous comparatives:**
| Japanese | English | Missing |
|----------|---------|---------|
| より速い | faster | Than what? |
| より良い | better | Than what? |
| 改善する | improve | From what baseline? |
| 増加/減少 | increase/decrease | By how much? |

**Detection patterns:**
```
/より.+い$|改善|向上|増加|減少/
/faster|better|improve|increase|decrease/i
```

**Resolution:** Specify baseline and target.

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "処理時間を改善する" | "処理時間を現行10分から3分に短縮する" |
| "ユーザー数を増加する" | "アクティブユーザー数を現行1,000人から3,000人に増加する" |

---

## 7. Temporal Ambiguity

### Pattern: Unclear timing or frequency

**Ambiguous terms:**
| Japanese | English | Issue |
|----------|---------|-------|
| すぐに | immediately | How soon? |
| 定期的に | periodically | How often? |
| 必要に応じて | as needed | When exactly? |
| 随時 | anytime | Triggered by what? |
| タイムリーに | in a timely manner | Deadline? |

**Detection patterns:**
```
/すぐに|即座に|定期的|必要に応じて|随時|タイムリー/
/immediately|periodically|as needed|anytime|timely/i
```

**Resolution:** Specify exact timing, frequency, or trigger conditions.

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "定期的に更新" | "毎日午前2時にバッチ更新" |
| "すぐに通知" | "イベント発生後5秒以内にプッシュ通知" |
| "必要に応じてエスカレーション" | "未対応が24時間超過した場合に上長へメール通知" |

---

## 8. Scope Ambiguity

### Pattern: Unclear boundaries

**Ambiguous markers:**
| Japanese | English | Issue |
|----------|---------|-------|
| 全て | all | All of what scope? |
| 任意の | any | Which set? |
| 一部の | some | Which ones? |
| 関連する | related | By what relationship? |
| 対象の | target | Selection criteria? |

**Detection patterns:**
```
/全て|任意の|一部の|関連する|対象の/
/all|any|some|related|target/i
```

**Resolution:** Define explicit scope boundaries.

**Examples:**
| Ambiguous | Specific |
|-----------|----------|
| "全てのユーザーデータ" | "顧客マスタ、取引履歴、問合せ履歴の3テーブル" |
| "関連する情報を表示" | "同一顧客の過去3ヶ月の取引履歴を表示" |

---

## 9. Conditional Completeness

### Pattern: Missing edge cases

**Required condition coverage:**
1. Normal case (正常系)
2. Alternative case (代替系)
3. Exception case (異常系)
4. Boundary case (境界条件)

**Checklist:**
- [ ] What happens on success?
- [ ] What happens on failure?
- [ ] What happens on timeout?
- [ ] What happens on invalid input?
- [ ] What happens at boundaries (min/max)?
- [ ] What happens with no data?
- [ ] What happens with duplicate data?

---

## 10. Passive Voice Hiding Actor

### Pattern: Passive construction obscures responsibility

**Japanese passive indicators:**
- 〜される
- 〜られる
- 〜が行われる

**English passive indicators:**
- is/are + past participle
- will be + past participle
- has been + past participle

**Resolution:** Convert to active voice with explicit actor.

**Examples:**
| Passive | Active |
|---------|--------|
| "データが更新される" | "日次バッチがデータを更新する" |
| "承認が完了される" | "部門マネージャーが承認を完了する" |
| "File is processed" | "Backend server processes the file" |

---

## Ambiguity Scoring

| Severity | Score | Description |
|----------|-------|-------------|
| Critical | 5 | Requirement cannot be implemented without clarification |
| High | 4 | Significant risk of misinterpretation |
| Medium | 3 | Moderate risk, may require follow-up |
| Low | 2 | Minor ambiguity, reasonable defaults exist |
| Info | 1 | Stylistic issue, no functional impact |

**Scoring criteria:**
- Critical: Missing core functionality definition, undefined data, conflicting requirements
- High: Vague quantifiers affecting cost/scope, undefined actors
- Medium: Open lists, incomplete conditions
- Low: Stylistic passive voice, minor temporal ambiguity
- Info: Undefined but common acronyms

---

## Automated Detection Rules

### Rule format:
```json
{
  "rule_id": "AMB-001",
  "pattern": "regex pattern",
  "pattern_type": "word|phrase|structure",
  "languages": ["ja", "en"],
  "severity": "critical|high|medium|low|info",
  "category": "category name",
  "message": "Description of the ambiguity",
  "suggestion": "How to resolve"
}
```

### Example rules:
```json
[
  {
    "rule_id": "AMB-001",
    "pattern": "(など|等|etc\\.|and so on)$",
    "pattern_type": "phrase",
    "languages": ["ja", "en"],
    "severity": "medium",
    "category": "unbounded_list",
    "message": "Open-ended list detected",
    "suggestion": "Enumerate all items or define inclusion criteria"
  },
  {
    "rule_id": "AMB-002",
    "pattern": "(高速|fast|quick|rapid)",
    "pattern_type": "word",
    "languages": ["ja", "en"],
    "severity": "high",
    "category": "vague_quantifier",
    "message": "Vague performance term without metric",
    "suggestion": "Specify measurable criteria (e.g., 'response time < 3 seconds')"
  },
  {
    "rule_id": "AMB-003",
    "pattern": "(される|is\\s+\\w+ed)$",
    "pattern_type": "structure",
    "languages": ["ja", "en"],
    "severity": "medium",
    "category": "passive_voice",
    "message": "Passive voice may hide responsible actor",
    "suggestion": "Convert to active voice with explicit actor"
  }
]
```
