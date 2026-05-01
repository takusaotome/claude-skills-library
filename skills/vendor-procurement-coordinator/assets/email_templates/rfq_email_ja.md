# RFQ送付メールテンプレート（日本語）

## 件名

【お見積依頼】{{PROJECT_NAME}} のシステム開発について

## 本文

```
{{VENDOR_CONTACT_NAME}} 様

いつもお世話になっております。
{{SENDER_COMPANY}}の{{SENDER_NAME}}でございます。

この度、弊社クライアント様向けの「{{PROJECT_NAME}}」につきまして、
貴社にお見積をご依頼させていただきたく、ご連絡いたしました。

■ プロジェクト概要
{{PROJECT_SUMMARY}}

■ 添付資料
- 見積依頼書（RFQ）: {{RFQ_FILENAME}}
{{#if ATTACHMENTS}}
{{#each ATTACHMENTS}}
- {{this}}
{{/each}}
{{/if}}

■ ご回答期限
{{DEADLINE}}（{{DEADLINE_DAY}}）までにご回答をお願いいたします。

■ ご質問について
ご不明点がございましたら、{{QA_DEADLINE}}までに本メールへの返信にて
お問い合わせください。いただいたご質問と回答は、公平性の観点から、
すべての見積依頼先様に共有させていただきます。

■ ご回答先
{{SUBMISSION_EMAIL}}
※件名に「【見積回答】{{PROJECT_NAME}}」とご記載ください。

なお、本件につきましては、貴社以外にも数社様にお見積を
ご依頼させていただいておりますこと、ご了承ください。

ご多忙の中恐縮ですが、ご検討のほどよろしくお願いいたします。

以上、よろしくお願い申し上げます。

─────────────────────────
{{SENDER_NAME}}
{{SENDER_COMPANY}}
{{SENDER_DEPARTMENT}}
Tel: {{SENDER_PHONE}}
Email: {{SENDER_EMAIL}}
─────────────────────────
```

## 変数リスト

| 変数名 | 説明 | 例 |
|--------|------|-----|
| PROJECT_NAME | プロジェクト名 | ERPシステム刷新プロジェクト |
| VENDOR_CONTACT_NAME | 宛先担当者名 | 山田太郎 |
| SENDER_COMPANY | 送信元会社名 | 株式会社ABC |
| SENDER_NAME | 送信者名 | 鈴木一郎 |
| SENDER_DEPARTMENT | 送信者部署 | システム部 |
| SENDER_PHONE | 送信者電話番号 | 03-1234-5678 |
| SENDER_EMAIL | 送信者メール | suzuki@abc.co.jp |
| PROJECT_SUMMARY | プロジェクト概要（2-3行） | 現行基幹システムの刷新... |
| RFQ_FILENAME | RFQファイル名 | RFQ_ERP刷新_v1.0.pdf |
| ATTACHMENTS | 追加添付ファイルリスト | - |
| DEADLINE | 回答期限日 | 2024年3月15日 |
| DEADLINE_DAY | 回答期限曜日 | 金 |
| QA_DEADLINE | 質問受付期限 | 2024年3月8日（金） |
| SUBMISSION_EMAIL | 回答送付先 | rfq@abc.co.jp |
