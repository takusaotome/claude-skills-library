# Japanese Enterprise Document Types

## Overview

This reference defines the specifications and requirements for each document type supported by the Japanese enterprise document formatter.

---

## 1. 稟議書 (Ringi - Approval Request)

### Purpose

Formal document requesting approval for decisions that exceed an individual's authority. Used for budget allocations, contract approvals, policy changes, and significant business decisions.

### Required Sections

| Section | Japanese | Required | Description |
|---------|----------|----------|-------------|
| Subject | 件名 | ✓ | Clear, concise title of the approval request |
| Draft Date | 起案日 | ✓ | Date the document was created |
| Drafter | 起案者 | ✓ | Name and employee ID of the person drafting |
| Department | 起案部署 | ✓ | Department initiating the request |
| Approval Deadline | 決裁期限 | ✓ | Date by which approval is needed |
| Purpose | 目的 | ✓ | What is being requested and why |
| Background | 背景 | ✓ | Context and circumstances leading to request |
| Details | 内容 | ✓ | Specific details of the proposal |
| Benefits | 効果 | ✓ | Expected benefits and outcomes |
| Risks | リスク | ✓ | Potential risks and mitigation measures |
| Cost | 費用 | ✓ | Total cost breakdown |
| Alternatives | 代替案 | ○ | Alternative options considered |
| Approval Section | 承認欄 | ✓ | Space for approval signatures/stamps |

### Approval Hierarchy

```
役員 (Executive) ← 最終決裁
  ↑
本部長 (Division Head)
  ↑
部長 (Department Manager)
  ↑
課長 (Section Manager)
  ↑
起案者 (Drafter)
```

### Cost Thresholds (Example)

| Amount | Required Approvers |
|--------|-------------------|
| ~100万円 | 部長 |
| 100万円~500万円 | 本部長 |
| 500万円~1000万円 | 担当役員 |
| 1000万円~ | 取締役会 |

### Keigo Level

- **Target**: 役員 (Executive)
- **Level**: 最上級敬語 (Highest formal)
- **Style**: ～させていただきます, ～いただきたく存じます

---

## 2. 購入申請書 (Purchase Request)

### Purpose

Request for purchasing goods or services. Used for equipment, software, supplies, and external services.

### Required Sections

| Section | Japanese | Required | Description |
|---------|----------|----------|-------------|
| Subject | 件名 | ✓ | "○○の購入について" format |
| Application Date | 申請日 | ✓ | Date of application |
| Applicant | 申請者 | ✓ | Name and department |
| Item Name | 品名 | ✓ | What is being purchased |
| Quantity | 数量 | ✓ | Number of items |
| Unit Price | 単価 | ✓ | Price per unit |
| Total Amount | 合計金額 | ✓ | Total cost |
| Vendor | 購入先 | ✓ | Supplier/vendor information |
| Reason | 購入理由 | ✓ | Why the purchase is needed |
| Delivery Date | 希望納期 | ✓ | When items are needed |
| Budget Code | 予算コード | ○ | Budget allocation code |
| Attachments | 添付資料 | ○ | Quotes, specifications, etc. |

### Standard Format

```
【購入申請書】

申請日：2024年○月○日
申請者：○○部 ○○○○
申請番号：PO-2024-XXX

■ 購入品目
品名：
数量：
単価：
合計金額：

■ 購入先
会社名：
担当者：
連絡先：

■ 購入理由
[理由を記載]

■ 希望納期
2024年○月○日

■ 添付資料
□ 見積書
□ カタログ/仕様書
□ その他（　　　　）
```

### Keigo Level

- **Target**: 部長 (Department Manager)
- **Level**: 標準敬語 (Standard formal)
- **Style**: ～いたします, ～をお願いいたします

---

## 3. 提案書 (Internal Proposal)

### Purpose

Document proposing a new initiative, project, or improvement to management. Used for new business ideas, process improvements, and strategic initiatives.

### Required Sections

| Section | Japanese | Required | Description |
|---------|----------|----------|-------------|
| Title | 表題 | ✓ | Proposal title |
| Proposal Date | 提案日 | ✓ | Date of proposal |
| Proposer | 提案者 | ✓ | Name and department |
| Executive Summary | 要旨 | ✓ | Brief summary (3-5 sentences) |
| Current Issues | 現状の課題 | ✓ | Problems being addressed |
| Proposal Content | 提案内容 | ✓ | Detailed proposal |
| Expected Benefits | 期待効果 | ✓ | Quantified benefits |
| Implementation Plan | 実施計画 | ✓ | Timeline and milestones |
| Required Resources | 必要リソース | ✓ | Budget, personnel, tools |
| Risk Analysis | リスク分析 | ○ | Potential risks |
| Success Metrics | 成功指標 | ○ | KPIs for measuring success |

### Structure Template

```markdown
# [提案書タイトル]

## 要旨
[3-5文で提案の概要を記載]

## 1. 現状の課題
### 1.1 課題の背景
### 1.2 課題の影響

## 2. 提案内容
### 2.1 提案の概要
### 2.2 提案の詳細

## 3. 期待効果
### 3.1 定量的効果
### 3.2 定性的効果

## 4. 実施計画
### 4.1 スケジュール
### 4.2 体制

## 5. 必要リソース
### 5.1 予算
### 5.2 人員
### 5.3 その他

## 6. リスク分析
### 6.1 想定リスク
### 6.2 対策

## 7. 成功指標（KPI）
```

### Keigo Level

- **Target**: 部長/役員
- **Level**: 上級敬語 (Upper formal)
- **Style**: ～いたします, ～と考えております

---

## 4. 報告書 (Report)

### Purpose

Document reporting on completed activities, incidents, or research findings. Used for project completion reports, incident reports, and analysis reports.

### Required Sections

| Section | Japanese | Required | Description |
|---------|----------|----------|-------------|
| Title | 表題 | ✓ | Report title |
| Report Date | 報告日 | ✓ | Date of report |
| Reporter | 報告者 | ✓ | Name and department |
| Summary | 概要 | ✓ | Executive summary |
| Background | 経緯 | ✓ | How events unfolded |
| Results | 結果 | ✓ | Outcomes and findings |
| Analysis | 分析 | ○ | Analysis of results |
| Future Actions | 今後の対応 | ✓ | Next steps |
| Attachments | 添付資料 | ○ | Supporting documents |

### Keigo Level

- **Target**: 部長
- **Level**: 標準敬語 (Standard formal)
- **Style**: ～いたしました, ～でございます

---

## 5. 依頼書 (Request Form)

### Purpose

Document requesting action or cooperation from another department or individual. Used for cross-departmental requests, support requests, and collaboration requests.

### Required Sections

| Section | Japanese | Required | Description |
|---------|----------|----------|-------------|
| Title | 件名 | ✓ | Request title |
| Request Date | 依頼日 | ✓ | Date of request |
| Requester | 依頼者 | ✓ | Name and department |
| Recipient | 依頼先 | ✓ | Target department/person |
| Request Details | 依頼事項 | ✓ | What is being requested |
| Reason | 依頼理由 | ✓ | Why the request is made |
| Deadline | 期限 | ✓ | When response is needed |
| Contact | 連絡先 | ✓ | How to respond |
| Notes | 備考 | ○ | Additional information |

### Keigo Level

- **Target**: 課長/部長
- **Level**: 丁寧語～標準敬語
- **Style**: ～をお願いいたします, ～いただけますでしょうか

---

## Section Writing Guidelines

### Subject (件名)

- **Format**: 「○○について」or「○○の件」
- **Length**: 20-40 characters
- **Content**: Clear indication of document purpose

**Good Examples:**
- 「新規システム導入について」
- 「2024年度予算増額の件」
- 「○○プロジェクト開始承認のお願い」

**Bad Examples:**
- 「システムの件」(too vague)
- 「新規システム導入について、当部における業務効率化および...」(too long)

### Purpose (目的)

- **Format**: 結論先行 (Conclusion first)
- **Structure**: What + Why + Expected Outcome
- **Length**: 2-4 paragraphs

**Template:**
```
本稟議は、[具体的な依頼内容]についてご承認をいただきたく、起案するものでございます。

[依頼の理由/背景を簡潔に説明]

本件の実施により、[期待される効果]が見込まれます。
```

### Cost (費用)

- **Format**: Breakdown table with totals
- **Include**: Tax indication, payment terms, budget source

**Template:**
```
| 項目 | 金額 |
|------|------|
| ○○費 | ¥XXX,XXX |
| △△費 | ¥XXX,XXX |
| 小計 | ¥XXX,XXX |
| 消費税（10%） | ¥XX,XXX |
| **合計** | **¥X,XXX,XXX** |

※予算科目：○○費（予算残高：¥X,XXX,XXX）
```

### Risk (リスク)

- **Format**: Risk + Impact + Mitigation
- **Structure**: Table or numbered list

**Template:**
```
| リスク | 影響度 | 発生可能性 | 対策 |
|--------|--------|------------|------|
| ○○リスク | 高 | 中 | △△により対応 |
| □□リスク | 中 | 低 | ××により軽減 |
```

---

## Numbering Conventions

### Document Numbering

| Type | Format | Example |
|------|--------|---------|
| 稟議書 | RINGI-YYYY-NNN | RINGI-2024-001 |
| 購入申請書 | PO-YYYY-NNN | PO-2024-042 |
| 提案書 | PROP-YYYY-NNN | PROP-2024-015 |
| 報告書 | RPT-YYYY-NNN | RPT-2024-103 |
| 依頼書 | REQ-YYYY-NNN | REQ-2024-028 |

### Section Numbering

```
1. 大見出し
  1.1 中見出し
    1.1.1 小見出し
    1.1.2 小見出し
  1.2 中見出し
2. 大見出し
```

---

## Attachments (添付資料) Guidelines

### Common Attachments by Document Type

| Document Type | Required Attachments | Optional Attachments |
|---------------|---------------------|---------------------|
| 稟議書 | 見積書, 費用明細 | 参考資料, 比較表 |
| 購入申請書 | 見積書, カタログ | 仕様書, 比較検討表 |
| 提案書 | なし | 詳細資料, データ分析 |
| 報告書 | なし | エビデンス, ログ |
| 依頼書 | なし | 参考資料 |

### Attachment Naming Convention

```
[文書番号]_[添付番号]_[内容].[拡張子]
例：RINGI-2024-001_A1_見積書.pdf
```
