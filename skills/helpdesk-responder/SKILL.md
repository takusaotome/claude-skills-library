---
name: helpdesk-responder
description: Generic helpdesk first-response skill for creating KB-based response drafts. Use when handling support tickets, creating response templates, or building a structured helpdesk workflow. Supports error code detection, keyword matching, confidence scoring, multi-language templates, and escalation workflows. Customize by providing your own KB articles and configuration.
---

# Helpdesk First Response Skill

A generic helpdesk first-response skill that creates KB-based response drafts for support tickets. Adaptable to any industry or product support context.

## Trigger Conditions

Use this skill when:
- Handling customer support tickets or inquiries
- Creating response drafts based on knowledge base articles
- Building a structured helpdesk workflow
- Training support staff on response patterns

---

## Skill Workflow

```
+---------------------------------------------------------------------+
|                    Phase 1: Inquiry Analysis                        |
|  - Extract ticket information                                       |
|  - Auto-detect patterns (error codes, device names, symptoms)       |
+---------------------------------------------------------------------+
                              |
              +---------------+---------------+
              v               v               v
    +-------------+   +-------------+   +-------------+
    | Error Code  |   | Device/     |   | Keyword     |
    | Detection   |   | Product     |   | Detection   |
    +-------------+   +-------------+   +-------------+
              |               |               |
              +---------------+---------------+
                              v
+---------------------------------------------------------------------+
|                   Phase 2: KB Search & Matching                     |
|  - Reference kb_index.json                                          |
|  - Primary KB prioritization                                        |
|  - Confidence score calculation                                     |
+---------------------------------------------------------------------+
                              |
              +---------------+---------------+
              v               v               v
    +-------------+   +-------------+   +-------------+
    | High Conf.  |   | Medium Conf.|   | Low Conf.   |
    |   (>=80%)   |   |  (50-79%)   |   |   (<50%)    |
    +-------------+   +-------------+   +-------------+
              |               |               |
              v               v               v
    +-------------+   +-------------+   +-------------+
    | Template 1  |   | Template 2  |   | Template 3  |
    | Solution    |   | Info Request|   | Escalation  |
    +-------------+   +-------------+   +-------------+
                              |
                              v
+---------------------------------------------------------------------+
|                     Phase 3: Response Draft Generation              |
|  - Template variable substitution                                   |
|  - KB steps integration                                             |
|  - Escalation determination                                         |
+---------------------------------------------------------------------+
```

---

## Phase 1: Inquiry Analysis

### 1.1 Information Extraction

Extract from the ticket:
- Customer name and contact info
- Subject/title
- Ticket number/ID
- Full description
- Previous correspondence (if any)

### 1.2 Auto-Detection Patterns

Configure patterns in `references/kb_index.json`:

| Priority | Pattern Type | Example Regex | Example Match |
|----------|-------------|---------------|---------------|
| 1 | Error Code | `[Ee]rror\s*(\d{5})` | Error 30001 |
| 2 | Code Alternative | `code\s*(\d{5})` | code 20002 |
| 3 | Device + Symptom | `(device_name)\s*(not working\|offline)` | printer not working |
| 4 | Hardware Symptom | `(not printing\|won't boot\|blue screen)` | not printing |

### 1.3 Problem Category Identification

Map detected patterns to KB categories:

| Category | Detection Criteria | Typical KB |
|----------|-------------------|------------|
| Error Codes | Numeric error patterns | Error reference guides |
| Hardware Issues | Physical device symptoms | Troubleshooting guides |
| Software Issues | Application errors | Software guides |
| Account/Access | Login, permissions | Account management |
| Connectivity | Network, offline | Network troubleshooting |

---

## Phase 2: KB Search and Confidence Scoring

### 2.1 Confidence Score Calculation

| Match Type | Score | Example |
|-----------|-------|---------|
| Error code exact match | +50 | Error 30001 in KB |
| Device/product name match | +20 | "printer" mentioned |
| Keyword match | +15 | "not printing" |
| Symptom similarity | +10 | Similar symptom pattern |
| Category match | +5 | Hardware category |

### 2.2 Confidence Thresholds

| Level | Score | Action |
|-------|-------|--------|
| **High** | >= 80 | Provide solution directly |
| **Medium** | 50-79 | Request additional information |
| **Low** | < 50 | Escalate for investigation |

### 2.3 Multiple KB Match Priority

When multiple KB articles match:
1. Use `primary_kb` field if specified
2. Prefer `detailed_kb: true` articles
3. Prefer specific articles over general references

---

## Phase 3: Response Draft Generation

### 3.1 Template Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `{{customer_name}}` | Customer name | Ticket contact |
| `{{ticket_subject}}` | Subject line | Ticket subject |
| `{{ticket_number}}` | Ticket ID | Ticket system |
| `{{error_code}}` | Error code | Pattern detection |
| `{{device_type}}` | Device/product type | Pattern detection |
| `{{kb_article}}` | KB article name | KB match |
| `{{kb_steps}}` | Troubleshooting steps | KB content |
| `{{resolution_time}}` | Estimated time | KB metadata |
| `{{escalation_reason}}` | Escalation reason | Analysis result |

---

## Response Templates

### Template 1: Clear Solution Available (High Confidence)

**English:**
```
Dear {{customer_name}},

Thank you for contacting our support team regarding {{ticket_subject}}.

Based on the information provided, this appears to be a {{device_type}} {{error_code}} issue. Here are the steps to resolve this:

**Troubleshooting Steps:**
{{kb_steps}}

**Estimated Resolution Time:** {{resolution_time}}

If the issue persists after completing these steps, please let us know and we will escalate to our technical team.

Best regards,
Support Team
```

**Japanese:**
```
{{customer_name}} 様

サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

ご報告いただいた内容から、{{device_type}}の{{error_code}}エラーと思われます。
以下の手順で解決できる可能性がございます：

**トラブルシューティング手順：**
{{kb_steps}}

**想定解決時間:** {{resolution_time}}

上記の手順でも解決しない場合は、技術チームへエスカレーションいたします。

サポートチーム
```

### Template 2: Additional Information Needed (Medium Confidence)

**English:**
```
Dear {{customer_name}},

Thank you for contacting our support team regarding {{ticket_subject}}.

To better assist you with this issue, could you please provide the following information:

1. What is the exact error message or code displayed?
2. Which device/product is affected?
3. When did this issue first occur?
4. Have you tried any troubleshooting steps?
5. Has anything changed recently (updates, configuration)?

Once we receive this information, we will provide specific troubleshooting steps.

Best regards,
Support Team
```

**Japanese:**
```
{{customer_name}} 様

サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

より適切なサポートをご提供するため、以下の情報をお知らせください：

1. 表示されているエラーメッセージやコードは何ですか？
2. どの製品/デバイスで発生していますか？
3. この問題はいつ頃から発生していますか？
4. トラブルシューティングは試されましたか？
5. 最近何か変更はありましたか（更新、設定変更など）？

情報をいただき次第、具体的な対応方法をご案内いたします。

サポートチーム
```

### Template 3: Escalation Required (Low Confidence)

**English:**
```
Dear {{customer_name}},

Thank you for contacting our support team regarding {{ticket_subject}}.

We have reviewed your request and determined that this issue requires detailed investigation by our technical team.

**Escalation Reason:** {{escalation_reason}}

We will:
1. Analyze the system logs and configuration
2. Coordinate with relevant teams if needed
3. Provide you with an update within [SLA timeframe]

In the meantime, please note any additional symptoms that may appear.

We appreciate your patience.

Best regards,
Support Team
```

**Japanese:**
```
{{customer_name}} 様

サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

ご報告いただいた内容を確認した結果、技術チームによる詳細調査が必要と判断いたしました。

**エスカレーション理由:** {{escalation_reason}}

以下の対応を進めます：
1. システムログと設定の分析
2. 必要に応じて関連チームとの連携
3. [SLA時間]以内に進捗をご報告

その間、追加の症状があればお知らせください。

ご理解のほどよろしくお願いいたします。

サポートチーム
```

---

## Escalation Criteria

### Automatic Escalation Conditions

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Repeat same error | 3+ times in 7 days | Request pattern analysis |
| Unknown error code | Not in KB index | Recommend new KB creation |
| Multi-system failure | 2+ systems | Immediate escalation |
| Hardware replacement | KB determination | Vendor coordination |

### Priority Escalation Factors

Configure based on your business:
- VIP customers/locations
- High-traffic time periods
- Weekend/holiday handling
- SLA requirements

---

## Escalation Handoff Format

When escalating to next-level support:

```markdown
## Escalation Request

**Ticket Number:** #{{ticket_number}}
**Customer:** {{customer_name}}
**Issue Summary:** {{ticket_subject}}
**Confidence Score:** {{confidence_score}}

### Detected Information
- Error Code: {{error_code}}
- Device: {{device_type}}
- Symptoms: {{detected_keywords}}

### First Response Actions
- Referenced KB: {{kb_article}}
- Match Reason: {{match_reason}}
- Why Not Resolved: {{non_match_reason}}

### Escalation Reason
{{escalation_reason}}

### Recommended Investigation
1. {{investigation_item_1}}
2. {{investigation_item_2}}
3. {{investigation_item_3}}

### Related Information
- Similar past tickets: {{related_tickets}}
- Vendor contact needed: {{vendor_contact_needed}}
```

---

## KB Index Configuration

Create a `kb_index.json` file with this structure:

```json
{
  "version": "1.0",
  "kb_base_path": "./kb_articles",

  "auto_detection_patterns": {
    "error_code": {
      "pattern": "[Ee]rror\\s*(\\d+)",
      "priority": 1
    }
  },

  "confidence_thresholds": {
    "high": {"min_score": 80},
    "medium": {"min_score": 50, "max_score": 79},
    "low": {"min_score": 0, "max_score": 49}
  },

  "error_codes": {
    "10001": {
      "kb": "error_reference.md",
      "section": "Network Errors",
      "description": "Network connection error",
      "confidence": "high",
      "resolution_time": "5-15min"
    }
  },

  "keywords": {
    "printer": {
      "kb": ["printer_troubleshooting.md"],
      "aliases": ["printing", "print"],
      "confidence": "high",
      "category": "hardware"
    }
  },

  "categories": {
    "hardware": {
      "kb": ["hardware_guide.md"],
      "typical_resolution_time": "15-30min"
    }
  }
}
```

See `references/kb_schema.json` for the complete schema.

---

## Usage Instructions

### Basic Usage

1. **With ticket ID:**
   ```
   /helpdesk-responder Ticket #1234 response draft
   ```

2. **With pasted content:**
   ```
   /helpdesk-responder
   Please respond to:
   [paste email content]
   ```

3. **With specific error:**
   ```
   /helpdesk-responder Error code 30001 troubleshooting
   ```

4. **In Japanese:**
   ```
   /helpdesk-responder チケット#1234 日本語で回答
   ```

### Output Format

The skill outputs:

1. **Problem Analysis**
   - Detected error codes
   - Identified devices/products
   - Symptom keywords
   - Confidence score

2. **Referenced KB**
   - Matched KB articles
   - Relevant sections
   - Solution applicability

3. **Response Draft**
   - Template applied
   - Copy-paste ready
   - Language option

4. **Additional Actions**
   - Follow-up questions (if info needed)
   - Escalation info (if required)
   - Vendor contacts (if applicable)

---

## Customization Guide

### Adapting to Your Organization

1. **Create KB Articles**
   - Write troubleshooting guides in Markdown
   - Use consistent structure

2. **Configure kb_index.json**
   - Map error codes to KB articles
   - Define keywords and aliases
   - Set confidence thresholds

3. **Customize Templates**
   - Update company name
   - Adjust tone and style
   - Add signature blocks

4. **Set Escalation Rules**
   - Define VIP criteria
   - Configure SLA timeframes
   - List vendor contacts

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-28 | Initial generic version |
