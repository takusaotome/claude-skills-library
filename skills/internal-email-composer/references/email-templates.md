# Email Templates Reference

This document provides template patterns for each supported email type in both Japanese and English.

## 1. Vendor RFQ Forwarding (vendor_rfq)

### Japanese Template

```
件名: 見積依頼の件（{project_name}）

{recipient_name}様

お疲れ様です。{sender_department}の{sender_name}です。

{project_name}に関する見積依頼書を送付いたします。
下記の内容をご確認の上、各ベンダーへのご連絡をお願いできますでしょうか。

【依頼内容】
・対象ベンダー：{vendor_list}
・見積回答期限：{deadline}
・添付資料：{attachments}

【プロジェクト概要】
{project_summary}

【見積要件】
{requirements}

ご不明点がございましたら、お気軽にお問い合わせください。
よろしくお願いいたします。

---
{sender_name}
{sender_department}
{sender_contact}
```

### English Template

```
Subject: RFQ Request - {project_name}

Dear {recipient_name},

I hope this email finds you well.

I am writing to forward the Request for Quotation (RFQ) documents for the {project_name} project. Could you please coordinate with the following vendors to obtain their quotes?

**Request Details:**
- Target Vendors: {vendor_list}
- Quote Deadline: {deadline}
- Attachments: {attachments}

**Project Overview:**
{project_summary}

**Quote Requirements:**
{requirements}

Please let me know if you have any questions or need additional information.

Best regards,
{sender_name}
{sender_department}
{sender_contact}
```

## 2. Task Delegation (task_delegation)

### Japanese Template

```
件名: 【依頼】{task_title}

{recipient_name}様

お疲れ様です。{sender_name}です。

下記の作業をお願いしたくご連絡いたしました。

【タスク概要】
{task_description}

【期待する成果物】
{deliverables}

【期限】
{deadline}

【参考資料】
{resources}

【備考】
{notes}

ご質問や不明点がございましたら、いつでもお声がけください。
お忙しいところ恐れ入りますが、よろしくお願いいたします。

---
{sender_name}
```

### English Template

```
Subject: Task Request: {task_title}

Hi {recipient_name},

I hope you're doing well. I'd like to request your assistance with the following task.

**Task Overview:**
{task_description}

**Expected Deliverables:**
{deliverables}

**Deadline:**
{deadline}

**Reference Materials:**
{resources}

**Additional Notes:**
{notes}

Please feel free to reach out if you have any questions or need clarification.

Thank you for your help.

Best regards,
{sender_name}
```

## 3. Status Update (status_update)

### Japanese Template

```
件名: 【進捗報告】{project_name}（{report_date}時点）

各位

お疲れ様です。{sender_name}です。
{project_name}の進捗状況をご報告いたします。

【全体ステータス】
{overall_status}

【前回からの進捗】
{progress_summary}

【完了タスク】
{completed_tasks}

【進行中タスク】
{ongoing_tasks}

【課題・リスク】
{issues}

【次のステップ】
{next_steps}

【アクションアイテム】
{action_items}

ご質問がございましたらお知らせください。

---
{sender_name}
```

### English Template

```
Subject: Status Update: {project_name} (as of {report_date})

Team,

Please find below the status update for the {project_name} project.

**Overall Status:** {overall_status}

**Progress Since Last Update:**
{progress_summary}

**Completed Tasks:**
{completed_tasks}

**Ongoing Tasks:**
{ongoing_tasks}

**Issues & Risks:**
{issues}

**Next Steps:**
{next_steps}

**Action Items:**
{action_items}

Please let me know if you have any questions.

Regards,
{sender_name}
```

## 4. Follow-up Request (follow_up)

### Japanese Template

```
件名: 【再送】{original_subject}

{recipient_name}様

お疲れ様です。{sender_name}です。

{original_date}にお送りした{original_subject}について、
確認のためご連絡いたしました。

【元の依頼内容】
{original_request}

【期限】
当初期限：{original_deadline}
更新期限：{new_deadline}

お忙しいところ恐れ入りますが、ご確認・ご対応いただけますと幸いです。
何かお手伝いできることがございましたら、お知らせください。

よろしくお願いいたします。

---
{sender_name}
```

### English Template

```
Subject: Follow-up: {original_subject}

Dear {recipient_name},

I hope this email finds you well. I wanted to follow up on my previous email regarding {original_subject}, sent on {original_date}.

**Original Request:**
{original_request}

**Timeline:**
- Original Deadline: {original_deadline}
- Updated Deadline: {new_deadline}

I understand you may have a busy schedule. Please let me know if you need any additional information or if there's anything I can do to help move this forward.

Thank you for your attention to this matter.

Best regards,
{sender_name}
```

## 5. Escalation (escalation)

### Japanese Template

```
件名: 【エスカレーション】{issue_title}

{recipient_name}様

お疲れ様です。{sender_name}です。

{issue_title}について、エスカレーションのためご連絡いたします。

【概要】
{issue_summary}

【影響範囲】
{impact_assessment}

【これまでの対応】
{actions_taken}

【解決に向けて必要なこと】
{support_needed}

【希望期限】
{requested_timeline}

ご多用のところ恐れ入りますが、ご支援いただけますと幸いです。
詳細についてご説明が必要でしたら、いつでもお時間を頂戴できればと存じます。

よろしくお願いいたします。

---
{sender_name}
```

### English Template

```
Subject: [Escalation] {issue_title}

Dear {recipient_name},

I am writing to escalate an issue that requires your attention and support.

**Issue Summary:**
{issue_summary}

**Impact Assessment:**
{impact_assessment}

**Actions Taken:**
{actions_taken}

**Support Needed:**
{support_needed}

**Requested Timeline:**
{requested_timeline}

I would appreciate your guidance on how to proceed. Please let me know if you would like to schedule a meeting to discuss this further.

Thank you for your attention to this urgent matter.

Best regards,
{sender_name}
```

## 6. Information Request (info_request)

### Japanese Template

```
件名: 【情報提供のお願い】{request_title}

{recipient_name}様

お疲れ様です。{sender_name}です。

{purpose}のため、下記の情報をご提供いただきたくお願いいたします。

【必要な情報】
{information_needed}

【目的・背景】
{context}

【希望フォーマット】
{format_requirements}

【回答期限】
{deadline}

ご不明点がございましたら、お気軽にお問い合わせください。
お手数をおかけしますが、よろしくお願いいたします。

---
{sender_name}
```

### English Template

```
Subject: Information Request: {request_title}

Dear {recipient_name},

I hope this message finds you well. I am reaching out to request the following information for {purpose}.

**Information Needed:**
{information_needed}

**Purpose & Context:**
{context}

**Preferred Format:**
{format_requirements}

**Response Deadline:**
{deadline}

Please let me know if you have any questions or need clarification on the request.

Thank you in advance for your assistance.

Best regards,
{sender_name}
```

## Template Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{recipient_name}` | Name of email recipient | 田中様, John |
| `{sender_name}` | Name of email sender | 山田太郎, Jane Smith |
| `{sender_department}` | Sender's department | システム開発部, IT Department |
| `{sender_contact}` | Sender's contact info | 内線: 1234, ext. 1234 |
| `{project_name}` | Name of related project | AWSインフラ移行 |
| `{deadline}` | Due date for response/action | 12月20日, December 20 |
| `{attachments}` | List of attached files | RFQ文書一式 |

## Tone Adjustment Guidelines

### Formal Tone (Japanese)
- Use です・ます調 consistently
- Include 恐れ入りますが, お手数をおかけしますが
- Use longer, more polite expressions

### Casual Tone (Japanese)
- Still maintain です・ます調
- Reduce excessive honorifics
- More direct requests acceptable

### Formal Tone (English)
- Use "Dear" for salutation
- Full sentences, no contractions
- "I would appreciate" instead of "Please"

### Casual Tone (English)
- Use "Hi" or "Hello" for salutation
- Contractions acceptable
- More direct language
