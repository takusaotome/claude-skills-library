---
name: aws-cli-expert
description: AWS CLIの専門家スキル。EC2, S3, IAM, Lambda, RDS, ECS等の主要サービスのCLI操作を支援。IAMポリシー設計、クロスアカウント運用、セキュリティ設定、コスト最適化のベストプラクティスを提供。Use when working with AWS services via CLI, designing IAM policies, managing infrastructure, or automating cloud operations.
---

# AWS CLI Expert

## Overview

AWS CLIは、Amazon Web Servicesの200以上のサービスをコマンドラインから操作するための公式ツールです。このスキルは、企業環境で頻出するサービスのCLI操作、IAMポリシー設計、セキュリティベストプラクティスを提供します。

## When to Use This Skill

このスキルを使用するタイミング：

- AWS CLIコマンドの構文を知りたい
- IAMポリシーやロールを設計・確認したい
- EC2、S3、Lambdaなどのリソースを管理したい
- クロスアカウントアクセスを設定したい
- セキュリティ設定を確認・強化したい
- AWS操作を自動化したい

**Example triggers:**
- "EC2インスタンスの一覧を取得するコマンドは？"
- "S3バケットのパブリックアクセスを確認したい"
- "IAMロールでクロスアカウントアクセスを設定したい"
- "Lambda関数のログを確認したい"
- "セキュリティグループのインバウンドルールを確認したい"

## Prerequisites

### Installation

```bash
# macOS (Homebrew)
brew install awscli

# pip
pip install awscli

# バージョン確認
aws --version
```

### Authentication Setup

```bash
# 対話式設定
aws configure

# プロファイル指定で設定
aws configure --profile <profile-name>

# 設定ファイルの場所
# ~/.aws/credentials - 認証情報
# ~/.aws/config - 設定
```

### Profile Management

```bash
# デフォルトプロファイルを使用
aws s3 ls

# 特定プロファイルを使用
aws s3 ls --profile production

# 環境変数でプロファイル指定
export AWS_PROFILE=production
aws s3 ls
```

## Core Services

### 1. IAM (Identity and Access Management)

**ユーザー管理:**
```bash
# ユーザー一覧
aws iam list-users

# ユーザー詳細
aws iam get-user --user-name <username>

# ユーザー作成
aws iam create-user --user-name <username>

# アクセスキー作成
aws iam create-access-key --user-name <username>

# アクセスキー一覧
aws iam list-access-keys --user-name <username>

# MFAデバイス一覧
aws iam list-mfa-devices --user-name <username>
```

**ロール管理:**
```bash
# ロール一覧
aws iam list-roles

# ロール詳細
aws iam get-role --role-name <role-name>

# ロールの信頼ポリシー確認
aws iam get-role --role-name <role-name> --query 'Role.AssumeRolePolicyDocument'

# ロールにアタッチされたポリシー一覧
aws iam list-attached-role-policies --role-name <role-name>
```

**ポリシー管理:**
```bash
# 管理ポリシー一覧
aws iam list-policies --scope Local

# ポリシー詳細（バージョン指定）
aws iam get-policy-version --policy-arn <arn> --version-id v1

# ユーザーにポリシーをアタッチ
aws iam attach-user-policy --user-name <user> --policy-arn <arn>

# ロールにポリシーをアタッチ
aws iam attach-role-policy --role-name <role> --policy-arn <arn>
```

**AssumeRole (クロスアカウント/ロール切り替え):**
```bash
# ロールを引き受ける
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/RoleName \
  --role-session-name MySession

# MFA付きAssumeRole
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/RoleName \
  --role-session-name MySession \
  --serial-number arn:aws:iam::111111111111:mfa/user \
  --token-code 123456

# 一時認証情報を環境変数に設定
eval $(aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/RoleName \
  --role-session-name MySession \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text | \
  awk '{print "export AWS_ACCESS_KEY_ID="$1" AWS_SECRET_ACCESS_KEY="$2" AWS_SESSION_TOKEN="$3}')
```

### 2. EC2 (Elastic Compute Cloud)

**インスタンス管理:**
```bash
# インスタンス一覧（テーブル形式）
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,InstanceType,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# 実行中のインスタンスのみ
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# インスタンス起動
aws ec2 start-instances --instance-ids i-1234567890abcdef0

# インスタンス停止
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# インスタンス終了（削除）
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

**セキュリティグループ:**
```bash
# セキュリティグループ一覧
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].[GroupId,GroupName,Description]' \
  --output table

# 特定SGの詳細（インバウンドルール）
aws ec2 describe-security-groups \
  --group-ids sg-12345678 \
  --query 'SecurityGroups[].IpPermissions'

# 0.0.0.0/0 からのアクセスを許可しているSG（セキュリティ監査）
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName]' \
  --output table

# インバウンドルール追加
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 443 \
  --cidr 10.0.0.0/8
```

**VPC:**
```bash
# VPC一覧
aws ec2 describe-vpcs \
  --query 'Vpcs[].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# サブネット一覧
aws ec2 describe-subnets \
  --query 'Subnets[].[SubnetId,VpcId,CidrBlock,AvailabilityZone]' \
  --output table
```

### 3. S3 (Simple Storage Service)

**基本操作:**
```bash
# バケット一覧
aws s3 ls

# バケット内オブジェクト一覧
aws s3 ls s3://bucket-name/

# 再帰的にリスト（サイズ付き）
aws s3 ls s3://bucket-name/ --recursive --human-readable --summarize

# ファイルコピー
aws s3 cp file.txt s3://bucket-name/

# ディレクトリ同期
aws s3 sync ./local-dir s3://bucket-name/prefix/

# ファイル削除
aws s3 rm s3://bucket-name/file.txt

# バケット内全削除
aws s3 rm s3://bucket-name/ --recursive
```

**バケットポリシー・セキュリティ:**
```bash
# バケットポリシー確認
aws s3api get-bucket-policy --bucket <bucket-name>

# パブリックアクセスブロック確認
aws s3api get-public-access-block --bucket <bucket-name>

# バケットACL確認
aws s3api get-bucket-acl --bucket <bucket-name>

# 暗号化設定確認
aws s3api get-bucket-encryption --bucket <bucket-name>

# バージョニング状態確認
aws s3api get-bucket-versioning --bucket <bucket-name>

# パブリックアクセスブロック設定
aws s3api put-public-access-block \
  --bucket <bucket-name> \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### 4. Lambda

**関数管理:**
```bash
# 関数一覧
aws lambda list-functions \
  --query 'Functions[].[FunctionName,Runtime,LastModified]' \
  --output table

# 関数詳細
aws lambda get-function --function-name <function-name>

# 関数設定確認
aws lambda get-function-configuration --function-name <function-name>

# 関数呼び出し（同期）
aws lambda invoke \
  --function-name <function-name> \
  --payload '{"key": "value"}' \
  output.json

# 関数呼び出し（非同期）
aws lambda invoke \
  --function-name <function-name> \
  --invocation-type Event \
  --payload '{"key": "value"}' \
  output.json
```

**ログ確認:**
```bash
# ロググループ一覧
aws logs describe-log-groups \
  --query 'logGroups[].[logGroupName,storedBytes]' \
  --output table

# Lambda関数のログをtail
aws logs tail /aws/lambda/<function-name> --follow

# 最新ログを取得
aws logs tail /aws/lambda/<function-name> --since 1h

# ログフィルタ
aws logs filter-log-events \
  --log-group-name /aws/lambda/<function-name> \
  --filter-pattern "ERROR"
```

### 5. RDS (Relational Database Service)

```bash
# DBインスタンス一覧
aws rds describe-db-instances \
  --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceClass,Engine,DBInstanceStatus]' \
  --output table

# DBインスタンス詳細
aws rds describe-db-instances --db-instance-identifier <instance-id>

# スナップショット一覧
aws rds describe-db-snapshots \
  --query 'DBSnapshots[].[DBSnapshotIdentifier,DBInstanceIdentifier,SnapshotCreateTime]' \
  --output table

# スナップショット作成
aws rds create-db-snapshot \
  --db-instance-identifier <instance-id> \
  --db-snapshot-identifier <snapshot-name>
```

### 6. ECS (Elastic Container Service)

```bash
# クラスター一覧
aws ecs list-clusters

# サービス一覧
aws ecs list-services --cluster <cluster-name>

# タスク一覧
aws ecs list-tasks --cluster <cluster-name>

# サービス詳細
aws ecs describe-services \
  --cluster <cluster-name> \
  --services <service-name>

# タスク定義一覧
aws ecs list-task-definitions

# サービス更新（新しいデプロイ）
aws ecs update-service \
  --cluster <cluster-name> \
  --service <service-name> \
  --force-new-deployment
```

### 7. CloudWatch

**メトリクス:**
```bash
# 利用可能なメトリクス一覧
aws cloudwatch list-metrics --namespace AWS/EC2

# メトリクス取得
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Average
```

**アラーム:**
```bash
# アラーム一覧
aws cloudwatch describe-alarms \
  --query 'MetricAlarms[].[AlarmName,StateValue,MetricName]' \
  --output table

# ALARM状態のアラーム
aws cloudwatch describe-alarms --state-value ALARM
```

### 8. CloudFormation

```bash
# スタック一覧
aws cloudformation list-stacks \
  --query 'StackSummaries[?StackStatus!=`DELETE_COMPLETE`].[StackName,StackStatus,CreationTime]' \
  --output table

# スタック詳細
aws cloudformation describe-stacks --stack-name <stack-name>

# スタックイベント（デプロイ進捗）
aws cloudformation describe-stack-events \
  --stack-name <stack-name> \
  --query 'StackEvents[].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId]' \
  --output table

# スタック作成
aws cloudformation create-stack \
  --stack-name <stack-name> \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# スタック更新
aws cloudformation update-stack \
  --stack-name <stack-name> \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# スタック削除
aws cloudformation delete-stack --stack-name <stack-name>
```

## Authentication Patterns

### 1. Profile-based (開発環境)

```ini
# ~/.aws/credentials
[default]
aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[production]
aws_access_key_id = AKIAYYYYYYYYYYYYYYYY
aws_secret_access_key = yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

```ini
# ~/.aws/config
[default]
region = ap-northeast-1
output = json

[profile production]
region = us-east-1
output = json
```

### 2. SSO / IAM Identity Center

```bash
# SSO設定
aws configure sso

# SSOログイン
aws sso login --profile <sso-profile>
```

```ini
# ~/.aws/config
[profile sso-dev]
sso_start_url = https://my-company.awsapps.com/start
sso_region = us-east-1
sso_account_id = 123456789012
sso_role_name = DeveloperAccess
region = ap-northeast-1
```

### 3. AssumeRole (クロスアカウント)

```ini
# ~/.aws/config
[profile cross-account]
role_arn = arn:aws:iam::123456789012:role/CrossAccountRole
source_profile = default
region = ap-northeast-1

# MFA必須の場合
[profile cross-account-mfa]
role_arn = arn:aws:iam::123456789012:role/CrossAccountRole
source_profile = default
mfa_serial = arn:aws:iam::111111111111:mfa/username
region = ap-northeast-1
```

### 4. 環境変数

```bash
export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export AWS_DEFAULT_REGION=ap-northeast-1

# 一時認証情報
export AWS_SESSION_TOKEN=xxxxxxxx
```

## Common Patterns

### JSON Output with jq

```bash
# 特定フィールドを抽出
aws ec2 describe-instances --output json | jq '.Reservations[].Instances[].InstanceId'

# フィルタリング
aws iam list-users --output json | jq '.Users[] | select(.UserName | startswith("admin"))'

# 整形して出力
aws lambda list-functions --output json | jq '.Functions[] | {name: .FunctionName, runtime: .Runtime}'
```

### Batch Operations

```bash
# 複数インスタンスを停止
aws ec2 stop-instances --instance-ids i-111 i-222 i-333

# タグでフィルタして操作
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=development" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text | xargs aws ec2 stop-instances --instance-ids
```

### Pagination

```bash
# 自動ページネーション（デフォルト）
aws s3api list-objects-v2 --bucket <bucket>

# 手動ページネーション
aws s3api list-objects-v2 --bucket <bucket> --max-items 100 --starting-token <token>
```

## Troubleshooting

### 認証エラー

```bash
# 現在の認証情報を確認
aws sts get-caller-identity

# プロファイル一覧
aws configure list-profiles

# 認証情報の優先順位確認
aws configure list
```

### アクセス拒否

```bash
# IAMポリシーシミュレーター
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/username \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::bucket-name/*
```

### デバッグ

```bash
# 詳細出力
aws s3 ls --debug

# リクエスト/レスポンス確認
aws s3 ls --debug 2>&1 | grep -A 5 "Response body"
```

## Resources

詳細なガイドは以下のリファレンスを参照：

- `references/aws_cli_essentials.md` - CLIの基本操作とベストプラクティス
- `references/iam_guide.md` - IAMの詳細ガイド
- `references/security_best_practices.md` - セキュリティベストプラクティス

## Tips

1. **--query を活用**: JMESPathで必要なフィールドだけ抽出
2. **--output table**: 人間が読むときはtable形式が見やすい
3. **--dry-run**: EC2操作は --dry-run で事前確認
4. **プロファイル分離**: 本番/開発環境はプロファイルで分離
5. **MFA必須**: 本番環境へのアクセスはMFA必須に
6. **CloudTrail確認**: 操作ログはCloudTrailで監査可能
