# AWS CLI Essentials

## Installation

### macOS

```bash
# Homebrew (推奨)
brew install awscli

# pkg インストーラ
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

### Linux

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### pip

```bash
pip install awscli
```

### Verify

```bash
aws --version
# aws-cli/2.x.x Python/3.x.x Darwin/x.x.x
```

## Configuration Files

### ~/.aws/credentials

認証情報を保存。複数プロファイルを定義可能。

```ini
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

[production]
aws_access_key_id = AKIAI44QH8DHBEXAMPLE
aws_secret_access_key = je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY

[development]
aws_access_key_id = AKIAXXXXXXXXXXXXXXXX
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### ~/.aws/config

設定オプションを保存。

```ini
[default]
region = ap-northeast-1
output = json

[profile production]
region = us-east-1
output = json
role_arn = arn:aws:iam::123456789012:role/ProductionRole
source_profile = default

[profile development]
region = ap-northeast-1
output = table
```

## Output Formats

### json (デフォルト)

```bash
aws ec2 describe-instances --output json
```

プログラムでの処理、jqとの連携に最適。

### table

```bash
aws ec2 describe-instances --output table
```

人間が読むのに最適。ターミナルで確認する際に使用。

### text

```bash
aws ec2 describe-instances --output text
```

シェルスクリプトでの処理、grep/awk/cutとの連携に最適。

### yaml

```bash
aws ec2 describe-instances --output yaml
```

人間が読みやすく、設定ファイルとしても使いやすい。

## --query Option (JMESPath)

JMESPathを使用して出力をフィルタリング・整形。

### Basic Syntax

```bash
# 配列要素へのアクセス
aws ec2 describe-instances --query 'Reservations[0]'

# すべての要素
aws ec2 describe-instances --query 'Reservations[]'

# ネストしたアクセス
aws ec2 describe-instances --query 'Reservations[].Instances[]'

# 特定フィールドの選択
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId'

# 複数フィールドの選択
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]'

# オブジェクト形式
aws ec2 describe-instances --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name}'
```

### Filtering

```bash
# 条件でフィルタ
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name==`running`]'

# 複数条件
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name==`running` && InstanceType==`t2.micro`]'

# 否定
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?State.Name!=`terminated`]'

# 部分一致（contains）
aws iam list-users \
  --query 'Users[?contains(UserName, `admin`)]'

# 開始一致（starts_with）
aws iam list-users \
  --query 'Users[?starts_with(UserName, `dev-`)]'
```

### Functions

```bash
# 長さ
aws s3api list-objects --bucket mybucket \
  --query 'length(Contents)'

# ソート
aws ec2 describe-instances \
  --query 'sort_by(Reservations[].Instances[], &LaunchTime)'

# 最大/最小
aws ec2 describe-instances \
  --query 'max_by(Reservations[].Instances[], &LaunchTime)'

# 合計
aws ec2 describe-volumes \
  --query 'sum(Volumes[].Size)'
```

### Tag Filtering

```bash
# Name タグの値を取得
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0]]'

# タグでフィルタ
aws ec2 describe-instances \
  --query 'Reservations[].Instances[?Tags[?Key==`Environment` && Value==`production`]]'
```

## --filters Option

サーバーサイドでフィルタリング。クエリより効率的。

```bash
# 単一フィルタ
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running"

# 複数フィルタ（AND）
aws ec2 describe-instances \
  --filters \
    "Name=instance-state-name,Values=running" \
    "Name=instance-type,Values=t2.micro,t2.small"

# タグでフィルタ
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=production"

# 複数値（OR）
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running,stopped"
```

## Pagination

### Auto Pagination

デフォルトで全結果を取得（v2）。

```bash
aws s3api list-objects-v2 --bucket mybucket
# 全オブジェクトを自動取得
```

### Manual Pagination

```bash
# ページサイズ指定
aws s3api list-objects-v2 --bucket mybucket --max-items 100

# 次のページ
aws s3api list-objects-v2 --bucket mybucket --max-items 100 --starting-token <token>
```

### Disable Auto Pagination

```bash
aws s3api list-objects-v2 --bucket mybucket --no-paginate
```

## Wait Commands

リソースが特定の状態になるまで待機。

```bash
# インスタンスが running になるまで待機
aws ec2 wait instance-running --instance-ids i-1234567890abcdef0

# インスタンスが terminated になるまで待機
aws ec2 wait instance-terminated --instance-ids i-1234567890abcdef0

# DBインスタンスが available になるまで待機
aws rds wait db-instance-available --db-instance-identifier mydb

# スタックが完了するまで待機
aws cloudformation wait stack-create-complete --stack-name mystack
```

## Environment Variables

優先順位（高い順）:
1. コマンドラインオプション
2. 環境変数
3. 設定ファイル

```bash
# 認証情報
export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export AWS_SESSION_TOKEN=xxxxxx  # 一時認証情報用

# リージョン
export AWS_DEFAULT_REGION=ap-northeast-1
export AWS_REGION=ap-northeast-1

# プロファイル
export AWS_PROFILE=production

# 出力形式
export AWS_DEFAULT_OUTPUT=json

# 設定ファイルパス
export AWS_CONFIG_FILE=~/.aws/config
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/credentials
```

## Shell Completion

### Bash

```bash
# .bashrc に追加
complete -C '/usr/local/bin/aws_completer' aws
```

### Zsh

```bash
# .zshrc に追加
autoload bashcompinit && bashcompinit
complete -C '/usr/local/bin/aws_completer' aws
```

## Debugging

```bash
# 詳細出力
aws s3 ls --debug

# HTTPリクエスト/レスポンス
aws s3 ls --debug 2>&1 | grep -E "(Request|Response)"

# CLI設定確認
aws configure list

# 現在の認証情報確認
aws sts get-caller-identity
```

## Best Practices

1. **プロファイルを使い分ける**: 本番/開発/ステージングで分離
2. **--query で必要な情報だけ取得**: 出力が見やすくなり処理も速い
3. **--filters でサーバーサイドフィルタ**: 大量データの場合に効率的
4. **wait コマンドを活用**: スクリプトでのリソース状態待機
5. **--dry-run でテスト**: EC2操作は事前に確認
6. **環境変数を活用**: CI/CDでの認証情報管理
7. **MFA必須**: 本番環境へのアクセスにはMFAを強制
