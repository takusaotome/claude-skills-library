"""
Pytest configuration and fixtures for hearing-to-requirements-mapper tests.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).resolve().parents[1]
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

import pytest


@pytest.fixture
def sample_hearing_ja():
    """Sample Japanese hearing sheet content."""
    return """# CRMシステム更新プロジェクト

## 背景・目的

- 現行システムが老朽化しており、パフォーマンスが低下している
- 顧客データの一元管理が必要
- 売上を20%向上させることが目標

## 機能要件

### ユーザー管理
- システムはユーザーのメールアドレス形式を検証する（必須）
- 管理者は全ユーザーの権限を管理できる必要がある
- ログイン失敗が3回でアカウントをロックする

### データ管理
- 顧客情報を高速に検索できること
- データは定期的にバックアップされる
- レポートをExcel、PDFなどで出力できること

## 非機能要件

- 応答時間は3秒以内とする
- 稼働率99.9%を目標とする
- セキュリティはPCI-DSS準拠が必須

## 制約条件

- 予算は5000万円以内
- 2025年4月までに本番稼働必須
- 既存のOracle DBを使用すること

## 前提条件

- ユーザーは安定したインターネット環境を持つと想定
- 現行業務プロセスは変更しない前提
"""


@pytest.fixture
def sample_hearing_en():
    """Sample English hearing sheet content."""
    return """# CRM System Renewal Project

## Background

- Current system is outdated and performance is declining
- Need centralized customer data management
- Goal is to increase sales by 20%

## Functional Requirements

### User Management
- System shall validate user email address format (required)
- Administrators must be able to manage permissions for all users
- System locks account after 3 failed login attempts

### Data Management
- Customer data should be searchable quickly
- Data is backed up periodically
- Reports can be exported to Excel, PDF, etc.

## Non-Functional Requirements

- Response time must be under 3 seconds
- Target 99.9% uptime availability
- Security must comply with PCI-DSS (mandatory)

## Constraints

- Budget must not exceed $500,000
- Production go-live required by April 2025
- Must use existing Oracle database

## Assumptions

- Assuming users have stable internet connectivity
- Current business processes will not change
"""


@pytest.fixture
def sample_hearing_mixed():
    """Sample mixed Japanese/English hearing sheet."""
    return """# Customer Portal Project / 顧客ポータルプロジェクト

## Requirements / 要件

- User authentication via OAuth 2.0 / OAuth 2.0による認証
- Dashboard displays KPI metrics / ダッシュボードでKPI表示
- Multi-language support (日本語/English)
- Response time < 2 seconds / 応答時間2秒以内
"""


@pytest.fixture
def tmp_hearing_file(tmp_path, sample_hearing_ja):
    """Create a temporary hearing file."""
    file_path = tmp_path / "hearing_sheet.md"
    file_path.write_text(sample_hearing_ja, encoding="utf-8")
    return file_path
