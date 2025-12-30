# AWS Security Best Practices

## 1. Root Account Protection

### Must Do

```bash
# Root アカウントにMFAを設定
# AWS Console > IAM > Root user > MFA の設定

# Root アカウントのアクセスキーを削除
aws iam delete-access-key --access-key-id AKIAXXXXXXXX
# ※ Root のアクセスキーは作成しない
```

### Guidelines

- Root アカウントは請求情報の確認、アカウント設定変更のみに使用
- 日常業務には IAM ユーザーまたは IAM Identity Center を使用
- Root アカウントのパスワードは強力なものを設定し、安全に保管
- ハードウェア MFA デバイスを推奨

## 2. IAM User Security

### Password Policy

```bash
# パスワードポリシーを設定
aws iam update-account-password-policy \
  --minimum-password-length 14 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 12

# 現在のポリシーを確認
aws iam get-account-password-policy
```

### MFA Enforcement

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowViewAccountInfo",
      "Effect": "Allow",
      "Action": [
        "iam:GetAccountPasswordPolicy",
        "iam:ListVirtualMFADevices"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowManageOwnMFA",
      "Effect": "Allow",
      "Action": [
        "iam:CreateVirtualMFADevice",
        "iam:EnableMFADevice",
        "iam:ResyncMFADevice"
      ],
      "Resource": [
        "arn:aws:iam::*:mfa/${aws:username}",
        "arn:aws:iam::*:user/${aws:username}"
      ]
    },
    {
      "Sid": "DenyAllExceptMFAManagement",
      "Effect": "Deny",
      "NotAction": [
        "iam:CreateVirtualMFADevice",
        "iam:EnableMFADevice",
        "iam:GetUser",
        "iam:ListMFADevices",
        "iam:ListVirtualMFADevices",
        "iam:ResyncMFADevice",
        "sts:GetSessionToken"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### Access Key Rotation

```bash
# アクセスキーの最終使用日を確認
aws iam get-access-key-last-used --access-key-id AKIAXXXXXXXX

# 新しいアクセスキーを作成
aws iam create-access-key --user-name username

# アプリケーションを新しいキーに更新後、古いキーを無効化
aws iam update-access-key \
  --user-name username \
  --access-key-id AKIAOLDKEYXX \
  --status Inactive

# 動作確認後、古いキーを削除
aws iam delete-access-key \
  --user-name username \
  --access-key-id AKIAOLDKEYXX
```

### Unused Credentials Report

```bash
# 認証情報レポートを生成
aws iam generate-credential-report

# レポートを取得
aws iam get-credential-report --output text --query Content | base64 -d > credential-report.csv
```

## 3. S3 Security

### Public Access Block

```bash
# アカウントレベルでパブリックアクセスをブロック
aws s3control put-public-access-block \
  --account-id 123456789012 \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# バケットレベルでパブリックアクセスをブロック
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Server-Side Encryption

```bash
# デフォルト暗号化を設定 (SSE-S3)
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# KMSキーを使用 (SSE-KMS)
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"alias/my-key"}}]}'
```

### Bucket Policy - HTTPS Only

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

### Versioning and Logging

```bash
# バージョニングを有効化
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# アクセスログを有効化
aws s3api put-bucket-logging \
  --bucket my-bucket \
  --bucket-logging-status '{
    "LoggingEnabled": {
      "TargetBucket": "my-log-bucket",
      "TargetPrefix": "s3-access-logs/"
    }
  }'
```

## 4. CloudTrail

### Enable CloudTrail

```bash
# 組織全体のトレイルを作成
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail \
  --enable-log-file-validation

# トレイルを開始
aws cloudtrail start-logging --name my-trail

# トレイルの状態を確認
aws cloudtrail get-trail-status --name my-trail
```

### CloudTrail Configuration

```bash
# 管理イベントとデータイベントを記録
aws cloudtrail put-event-selectors \
  --trail-name my-trail \
  --event-selectors '[
    {
      "ReadWriteType": "All",
      "IncludeManagementEvents": true,
      "DataResources": [
        {
          "Type": "AWS::S3::Object",
          "Values": ["arn:aws:s3:::my-important-bucket/"]
        }
      ]
    }
  ]'
```

## 5. GuardDuty

```bash
# GuardDutyを有効化
aws guardduty create-detector --enable

# 検出結果を取得
aws guardduty list-findings --detector-id <detector-id>

# 高重要度の検出結果
aws guardduty list-findings \
  --detector-id <detector-id> \
  --finding-criteria '{"Criterion":{"severity":{"Gte":7}}}'
```

## 6. Security Hub

```bash
# Security Hubを有効化
aws securityhub enable-security-hub

# CIS AWS Foundations Benchmark を有効化
aws securityhub batch-enable-standards \
  --standards-subscription-requests \
  '[{"StandardsArn":"arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0"}]'

# 検出結果を取得
aws securityhub get-findings \
  --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}]}'
```

## 7. VPC Security

### Security Groups Audit

```bash
# 0.0.0.0/0 からのアクセスを許可しているSG
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
  --output table

# 使用されていないSGを検出
aws ec2 describe-network-interfaces \
  --query 'NetworkInterfaces[].Groups[].GroupId' | sort -u > used-sgs.txt
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].GroupId' | sort -u > all-sgs.txt
comm -23 all-sgs.txt used-sgs.txt
```

### VPC Flow Logs

```bash
# VPC Flow Logsを有効化
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-1234567890abcdef0 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs
```

### Network ACLs

```bash
# NACLs を確認
aws ec2 describe-network-acls \
  --query 'NetworkAcls[].[NetworkAclId,Associations[].SubnetId,Entries]'
```

## 8. EC2 Security

### IMDSv2 Enforcement

```bash
# 新しいインスタンスでIMDSv2を必須に
aws ec2 run-instances \
  --image-id ami-xxxxxxxx \
  --instance-type t3.micro \
  --metadata-options "HttpTokens=required,HttpPutResponseHopLimit=1"

# 既存インスタンスを更新
aws ec2 modify-instance-metadata-options \
  --instance-id i-1234567890abcdef0 \
  --http-tokens required \
  --http-put-response-hop-limit 1
```

### EBS Encryption

```bash
# アカウントレベルでEBS暗号化をデフォルト有効化
aws ec2 enable-ebs-encryption-by-default

# 暗号化されていないボリュームを検出
aws ec2 describe-volumes \
  --query 'Volumes[?!Encrypted].[VolumeId,State]' \
  --output table
```

## 9. Secrets Management

### Secrets Manager

```bash
# シークレットを作成
aws secretsmanager create-secret \
  --name my-secret \
  --secret-string '{"username":"admin","password":"MyPassword123!"}'

# シークレットを取得
aws secretsmanager get-secret-value --secret-id my-secret

# シークレットをローテーション
aws secretsmanager rotate-secret --secret-id my-secret
```

### Parameter Store (SSM)

```bash
# SecureString パラメータを作成
aws ssm put-parameter \
  --name /app/database/password \
  --value "MyPassword123!" \
  --type SecureString

# パラメータを取得
aws ssm get-parameter \
  --name /app/database/password \
  --with-decryption
```

## 10. Monitoring and Alerting

### CloudWatch Alarms for Security

```bash
# Root アカウントのログインを検知
aws cloudwatch put-metric-alarm \
  --alarm-name RootAccountUsage \
  --alarm-description "Alarm when root account is used" \
  --metric-name RootAccountUsage \
  --namespace CloudTrailMetrics \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:region:account:topic
```

### Config Rules

```bash
# AWS Config を有効化してルールを設定
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-public-read-prohibited",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
    }
  }'
```

## Security Checklist

### Account Level
- [ ] Root アカウントに MFA 設定済み
- [ ] Root アカウントのアクセスキーなし
- [ ] パスワードポリシー設定済み
- [ ] CloudTrail 有効（全リージョン）
- [ ] GuardDuty 有効
- [ ] Security Hub 有効
- [ ] Config 有効

### IAM
- [ ] 最小権限の原則を適用
- [ ] MFA 必須（特に本番アクセス）
- [ ] 未使用のユーザー/ロール/キーを削除
- [ ] アクセスキーを定期ローテーション

### S3
- [ ] パブリックアクセスブロック有効
- [ ] デフォルト暗号化有効
- [ ] バージョニング有効（重要バケット）
- [ ] アクセスログ有効

### EC2/VPC
- [ ] セキュリティグループで 0.0.0.0/0 を最小化
- [ ] IMDSv2 を必須に
- [ ] EBS 暗号化をデフォルト有効
- [ ] VPC Flow Logs 有効

### Data Protection
- [ ] 機密データは暗号化
- [ ] シークレットは Secrets Manager/SSM で管理
- [ ] KMS キーを適切に管理
