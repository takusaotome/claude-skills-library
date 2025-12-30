# IAM (Identity and Access Management) Guide

## Core Concepts

### Principal Types

| Type | Description | Use Case |
|------|-------------|----------|
| **IAM User** | 人間またはアプリケーション用の恒久的な認証情報 | 開発者アクセス、サービスアカウント |
| **IAM Role** | 一時的な認証情報、AssumeRole で取得 | EC2/Lambda、クロスアカウント、Federation |
| **IAM Group** | ユーザーをまとめて権限を付与 | チーム/部門単位の権限管理 |
| **Root User** | AWSアカウントの最高権限ユーザー | 請求設定、アカウント閉鎖のみに使用 |

### Policy Types

| Type | Description | Example |
|------|-------------|---------|
| **AWS Managed Policy** | AWS提供の汎用ポリシー | AdministratorAccess, ReadOnlyAccess |
| **Customer Managed Policy** | 自作のポリシー | カスタム権限セット |
| **Inline Policy** | 特定のユーザー/ロール/グループに直接埋め込み | 一時的/特殊な権限 |

## Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DescriptiveStatementId",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "192.168.1.0/24"
        }
      }
    }
  ]
}
```

### Elements

- **Version**: 常に "2012-10-17" を使用
- **Statement**: ポリシーステートメントの配列
- **Sid**: 任意の識別子
- **Effect**: "Allow" または "Deny"
- **Action**: 許可/拒否するアクション
- **Resource**: 対象リソースのARN
- **Condition**: 追加の条件

## Common Actions

### Wildcard Patterns

```json
{
  "Action": "s3:*",          // S3の全アクション
  "Action": "s3:Get*",       // s3:GetObject, s3:GetBucketPolicy など
  "Action": ["s3:Get*", "s3:List*"]  // 読み取り系
}
```

### Service-specific Actions

```json
// EC2
"Action": ["ec2:DescribeInstances", "ec2:StartInstances", "ec2:StopInstances"]

// S3
"Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]

// Lambda
"Action": ["lambda:InvokeFunction", "lambda:GetFunction"]

// IAM (危険: 慎重に)
"Action": ["iam:CreateUser", "iam:AttachUserPolicy"]
```

## Resource ARN Format

```
arn:aws:service:region:account-id:resource-type/resource-id
```

### Examples

```
# S3バケット
arn:aws:s3:::my-bucket
arn:aws:s3:::my-bucket/*

# EC2インスタンス
arn:aws:ec2:ap-northeast-1:123456789012:instance/i-1234567890abcdef0

# Lambda関数
arn:aws:lambda:ap-northeast-1:123456789012:function:my-function

# IAMロール
arn:aws:iam::123456789012:role/my-role

# IAMユーザー
arn:aws:iam::123456789012:user/username
```

## Conditions

### Common Condition Keys

```json
// IPアドレス制限
"Condition": {
  "IpAddress": {
    "aws:SourceIp": ["192.168.1.0/24", "10.0.0.0/8"]
  }
}

// MFA必須
"Condition": {
  "Bool": {
    "aws:MultiFactorAuthPresent": "true"
  }
}

// 時間制限
"Condition": {
  "DateGreaterThan": {"aws:CurrentTime": "2024-01-01T00:00:00Z"},
  "DateLessThan": {"aws:CurrentTime": "2024-12-31T23:59:59Z"}
}

// タグベース
"Condition": {
  "StringEquals": {
    "ec2:ResourceTag/Environment": "development"
  }
}

// SSL必須
"Condition": {
  "Bool": {
    "aws:SecureTransport": "true"
  }
}
```

## Trust Policy (AssumeRole)

ロールを引き受けられるプリンシパルを定義。

### EC2からの引き受け

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### Lambda からの引き受け

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### クロスアカウント

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

### 特定のロールからの引き受け

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:role/SourceRole"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Least Privilege Patterns

### Read-Only Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

### Write Access to Specific Prefix

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/uploads/${aws:username}/*"
    }
  ]
}
```

### Tag-based Access Control

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/Owner": "${aws:username}"
        }
      }
    }
  ]
}
```

## CLI Commands

### User Management

```bash
# ユーザー一覧
aws iam list-users

# ユーザー作成
aws iam create-user --user-name new-user

# アクセスキー作成
aws iam create-access-key --user-name new-user

# パスワード設定（コンソールアクセス）
aws iam create-login-profile --user-name new-user --password 'TempPassword123!'

# ユーザー削除（関連リソースも削除必要）
aws iam delete-login-profile --user-name user-to-delete
aws iam list-access-keys --user-name user-to-delete
aws iam delete-access-key --user-name user-to-delete --access-key-id AKIAXXXXXXXX
aws iam list-attached-user-policies --user-name user-to-delete
aws iam detach-user-policy --user-name user-to-delete --policy-arn <arn>
aws iam delete-user --user-name user-to-delete
```

### Role Management

```bash
# ロール一覧
aws iam list-roles

# ロール作成
aws iam create-role \
  --role-name MyRole \
  --assume-role-policy-document file://trust-policy.json

# ロールにポリシーをアタッチ
aws iam attach-role-policy \
  --role-name MyRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# インラインポリシーを追加
aws iam put-role-policy \
  --role-name MyRole \
  --policy-name InlinePolicy \
  --policy-document file://inline-policy.json
```

### Policy Management

```bash
# ポリシー作成
aws iam create-policy \
  --policy-name MyPolicy \
  --policy-document file://policy.json

# ポリシーバージョン一覧
aws iam list-policy-versions --policy-arn <arn>

# ポリシー更新（新バージョン作成）
aws iam create-policy-version \
  --policy-arn <arn> \
  --policy-document file://policy-v2.json \
  --set-as-default
```

### AssumeRole

```bash
# ロールを引き受ける
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name MySession

# 出力を環境変数に設定
eval $(aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name MySession \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text | \
  awk '{print "export AWS_ACCESS_KEY_ID="$1" AWS_SECRET_ACCESS_KEY="$2" AWS_SESSION_TOKEN="$3}')
```

## Security Best Practices

1. **Root ユーザーを使わない**: MFA設定後、ほぼ使用しない
2. **最小権限**: 必要最小限の権限のみ付与
3. **グループで権限管理**: ユーザーへの直接ポリシー付与を避ける
4. **ロールを活用**: アプリケーションは IAM ロールを使用
5. **アクセスキーをローテーション**: 定期的に更新
6. **MFA 必須**: 特に本番環境へのアクセス
7. **条件を活用**: IP制限、時間制限、MFA要求
8. **定期的な監査**: 未使用のユーザー/ロール/キーを削除
