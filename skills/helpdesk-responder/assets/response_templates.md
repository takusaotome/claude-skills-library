# Helpdesk Response Templates

Ready-to-use response templates for various support scenarios. Copy and customize for your organization.

---

## Core Response Templates

### 1. Solution Provided (High Confidence)

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding {{ticket_subject}}.

Based on the information provided, this appears to be a {{device_type}} {{error_code}} issue. Here are the steps to resolve this:

**Troubleshooting Steps:**
{{kb_steps}}

**Estimated Resolution Time:** {{resolution_time}}

If the issue persists after completing these steps, please reply to this email and we will escalate to our technical team.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

[Company]サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

ご報告いただいた内容から、{{device_type}}の{{error_code}}問題と思われます。
以下の手順で解決できる可能性がございます：

**トラブルシューティング手順：**
{{kb_steps}}

**想定解決時間:** {{resolution_time}}

上記の手順でも解決しない場合は、このメールにご返信ください。技術チームへエスカレーションいたします。

[Company] サポートチーム
```

---

### 2. Information Request (Medium Confidence)

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding {{ticket_subject}}.

To better assist you with this issue, could you please provide the following information:

1. What is the exact error message or code displayed on the screen?
2. Which product/device/account is affected?
3. When did this issue first occur?
4. Were you able to [perform the action] before? If so, when did it stop working?
5. Have you tried any troubleshooting steps already?

Once we receive this information, we will provide you with specific next steps.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

[Company]サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

より適切なサポートをご提供するため、以下の情報をお知らせください：

1. 画面に表示されているエラーメッセージやコードは何ですか？
2. どの製品/デバイス/アカウントで発生していますか？
3. この問題はいつ頃から発生していますか？
4. 以前は[その操作]ができていましたか？できなくなったのはいつからですか？
5. 何かトラブルシューティングはすでにお試しになりましたか？

情報をいただき次第、具体的な対応方法をご案内いたします。

[Company] サポートチーム
```

---

### 3. Escalation Notice (Low Confidence)

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding {{ticket_subject}}.

We have reviewed your request and determined that this issue requires detailed investigation by our technical team.

**Escalation Reason:** {{escalation_reason}}

Next Steps:
1. Our technical team will analyze the system logs and configuration
2. We will coordinate with relevant teams/vendors if needed
3. You will receive an update within [X hours/days]

In the meantime, please note any additional symptoms or changes that may occur.

We appreciate your patience.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

[Company]サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

ご報告いただいた内容を確認した結果、技術チームによる詳細調査が必要と判断いたしました。

**エスカレーション理由:** {{escalation_reason}}

今後の対応：
1. 技術チームがシステムログと設定を分析します
2. 必要に応じて関連チーム/ベンダーと連携します
3. [X時間/日]以内に進捗をご報告します

その間、追加の症状や変化があればお知らせください。

ご理解のほどよろしくお願いいたします。

[Company] サポートチーム
```

---

## Specialized Templates

### 4. Known Issue Acknowledgment

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding {{ticket_subject}}.

We are aware of this issue and our team is actively working on a resolution.

**Issue Status:**
- Issue ID: {{issue_id}}
- Status: Under Investigation
- Expected Resolution: {{expected_resolution_date}}

**Workaround (if available):**
{{workaround_steps}}

We will notify you once the issue has been resolved. You can also check our status page at [status_page_url] for updates.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

[Company]サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

この問題については既に認識しており、解決に向けて対応中です。

**問題のステータス：**
- 問題ID: {{issue_id}}
- 状態: 調査中
- 解決予定: {{expected_resolution_date}}

**回避策（利用可能な場合）：**
{{workaround_steps}}

問題が解決次第、ご連絡いたします。最新の状況は[status_page_url]でもご確認いただけます。

[Company] サポートチーム
```

---

### 5. Resolution Confirmation

#### English
```
Dear {{customer_name}},

This is a follow-up regarding your support request: {{ticket_subject}} (Ticket #{{ticket_number}}).

Based on the information you provided, we believe this issue has been resolved. Here's a summary of what was done:

**Resolution Summary:**
{{resolution_summary}}

**Steps Taken:**
{{steps_taken}}

Please confirm that the issue is resolved by replying to this email. If you are still experiencing problems, please let us know and we will investigate further.

If we don't hear from you within 5 business days, we will assume the issue has been resolved and close this ticket.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

お問い合わせいただいた「{{ticket_subject}}」（チケット番号: {{ticket_number}}）についてご連絡いたします。

ご報告いただいた問題は解決したと思われます。対応内容の概要は以下の通りです。

**解決内容：**
{{resolution_summary}}

**実施した手順：**
{{steps_taken}}

問題が解決したかどうか、このメールへのご返信でお知らせください。まだ問題が発生している場合は、ご連絡いただければ引き続き調査いたします。

5営業日以内にご返信がない場合は、問題が解決したものとしてチケットをクローズさせていただきます。

[Company] サポートチーム
```

---

### 6. Hardware Replacement Required

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding {{ticket_subject}}.

After reviewing the troubleshooting steps taken, we have determined that the {{device_type}} requires hardware replacement.

**Recommended Action:**
{{replacement_recommendation}}

**Next Steps:**
1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

**Vendor Information (if applicable):**
- Vendor: {{vendor_name}}
- Contact: {{vendor_contact}}
- Reference: {{reference_number}}

Please let us know if you need any assistance with the replacement process.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

[Company]サポートへお問い合わせいただきありがとうございます。
「{{ticket_subject}}」についてご連絡いただきました。

トラブルシューティングの結果、{{device_type}}のハードウェア交換が必要と判断いたしました。

**推奨対応：**
{{replacement_recommendation}}

**今後の手順：**
1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

**ベンダー情報（該当する場合）：**
- ベンダー: {{vendor_name}}
- 連絡先: {{vendor_contact}}
- 参照番号: {{reference_number}}

交換手続きについてご不明な点がございましたら、お知らせください。

[Company] サポートチーム
```

---

### 7. Password/Account Reset

#### English
```
Dear {{customer_name}},

Thank you for contacting [Company] Support regarding your account access issue.

For security purposes, we have initiated a password reset for your account.

**Next Steps:**
1. Check your registered email address ({{masked_email}}) for a password reset link
2. Click the link and create a new password
3. Log in with your new credentials

**Important Notes:**
- The reset link will expire in 24 hours
- If you don't receive the email, check your spam folder
- Contact us if you no longer have access to this email address

For security, never share your password with anyone. [Company] staff will never ask for your password.

Best regards,
[Company] Support Team
```

#### Japanese
```
{{customer_name}} 様

アカウントアクセスについてお問い合わせいただきありがとうございます。

セキュリティのため、アカウントのパスワードリセットを開始しました。

**次のステップ：**
1. ご登録のメールアドレス（{{masked_email}}）でパスワードリセットリンクをご確認ください
2. リンクをクリックして新しいパスワードを設定してください
3. 新しい認証情報でログインしてください

**重要な注意事項：**
- リセットリンクは24時間で期限切れになります
- メールが届かない場合は迷惑メールフォルダをご確認ください
- このメールアドレスにアクセスできない場合はご連絡ください

セキュリティのため、パスワードは誰にも共有しないでください。[Company]のスタッフがパスワードをお尋ねすることはありません。

[Company] サポートチーム
```

---

## Quick Response Templates

### Acknowledgment (Same-day)
```
Dear {{customer_name}},

Thank you for your inquiry. We have received your request and are currently reviewing it.

Ticket Number: #{{ticket_number}}

You can expect a detailed response within [X hours].

Best regards,
[Company] Support Team
```

### Weekend/Holiday Auto-Response
```
Dear {{customer_name}},

Thank you for contacting [Company] Support.

Your message has been received. Please note that our office is currently closed for [weekend/holiday name].

We will respond to your inquiry when we reopen on [next business day].

For urgent issues, please [emergency contact instructions].

Best regards,
[Company] Support Team
```

### Ticket Closure (No Response)
```
Dear {{customer_name}},

We are following up on your support request: {{ticket_subject}} (Ticket #{{ticket_number}}).

As we have not received a response, we will close this ticket. If you still need assistance, please reply to this email or submit a new request.

Best regards,
[Company] Support Team
```

---

## Template Customization Checklist

When implementing these templates:

- [ ] Replace `[Company]` with your organization name
- [ ] Update signature block with correct department name
- [ ] Add your status page URL where applicable
- [ ] Define SLA timeframes (X hours/days)
- [ ] Set ticket auto-close period (5 business days or your policy)
- [ ] Add phone number for urgent issues if applicable
- [ ] Include links to self-service resources
- [ ] Translate to additional languages as needed
