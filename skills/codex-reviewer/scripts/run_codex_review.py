#!/usr/bin/env python3
"""
Codex Review Runner

OpenAI Codex CLIを使用してコードやドキュメントのレビューを実行するスクリプト。
最も深い思考が可能なモデル GPT-5.1-Codex-Max を高推論モード(high)で呼び出します。

Usage:
    python3 run_codex_review.py --type code --target src/ --output ./reviews
    python3 run_codex_review.py --type document --target docs/spec.md --output ./reviews
"""

import argparse
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List


# レビュータイプ別のデフォルトプロンプト
REVIEW_PROMPTS = {
    "code": """以下のコードを詳細にレビューしてください。

## レビュー観点
1. **セキュリティ**: 脆弱性、インジェクション、認証・認可の問題
2. **パフォーマンス**: 非効率なアルゴリズム、メモリリーク、N+1問題
3. **保守性**: コードの可読性、命名規則、コメント、複雑度
4. **ベストプラクティス**: 言語・フレームワークの規約、デザインパターン
5. **エラーハンドリング**: 例外処理、エッジケース、入力検証
6. **テスト可能性**: テストのしやすさ、依存性注入、モック可能性

## 出力形式
各問題について以下の形式で報告してください:
- **重要度**: Critical / High / Medium / Low
- **カテゴリ**: セキュリティ / パフォーマンス / 保守性 / etc.
- **場所**: ファイル名:行番号
- **問題**: 問題の説明
- **推奨**: 改善案

対象: {target}""",

    "document": """以下のドキュメントを詳細にレビューしてください。

## レビュー観点
1. **完全性**: 必要な情報がすべて含まれているか
2. **正確性**: 技術的に正しいか、矛盾がないか
3. **明確性**: 理解しやすく書かれているか、曖昧な表現がないか
4. **一貫性**: 用語、フォーマット、スタイルが統一されているか
5. **実装可能性**: この仕様で実装可能か、不明点がないか
6. **トレーサビリティ**: 要件との対応が取れているか

## 出力形式
各指摘について以下の形式で報告してください:
- **重要度**: Critical / High / Medium / Low
- **カテゴリ**: 完全性 / 正確性 / 明確性 / etc.
- **場所**: セクション名または行番号
- **問題**: 問題の説明
- **推奨**: 改善案

対象: {target}""",

    "design": """以下の設計ドキュメントを詳細にレビューしてください。

## レビュー観点
1. **アーキテクチャ**: 設計の妥当性、コンポーネント分割
2. **スケーラビリティ**: 負荷増加への対応力
3. **デザインパターン**: 適切なパターンの適用
4. **結合度・凝集度**: モジュール間の依存関係
5. **拡張性**: 将来の変更への対応力
6. **非機能要件**: セキュリティ、可用性、性能

## 出力形式
各指摘について以下の形式で報告してください:
- **重要度**: Critical / High / Medium / Low
- **カテゴリ**: アーキテクチャ / スケーラビリティ / etc.
- **場所**: 該当セクション
- **問題**: 問題の説明
- **推奨**: 改善案

対象: {target}""",

    "test": """以下のテストコード/テスト計画を詳細にレビューしてください。

## レビュー観点
1. **カバレッジ**: テスト対象の網羅性
2. **エッジケース**: 境界値、異常系のテスト
3. **独立性**: テスト間の依存関係がないか
4. **テストデータ**: 適切なテストデータの使用
5. **アサーション**: 検証内容の適切さ
6. **自動化**: CI/CD統合の容易さ

## 出力形式
各指摘について以下の形式で報告してください:
- **重要度**: Critical / High / Medium / Low
- **カテゴリ**: カバレッジ / エッジケース / etc.
- **場所**: テストファイル名:テスト名
- **問題**: 問題の説明
- **推奨**: 改善案

対象: {target}"""
}

# フォーカスエリア別の追加プロンプト
FOCUS_PROMPTS = {
    "security": "\n\n特にセキュリティに重点を置いてレビューしてください。OWASP Top 10、CWE、CVEなどの観点から脆弱性を特定してください。",
    "performance": "\n\n特にパフォーマンスに重点を置いてレビューしてください。時間計算量、空間計算量、I/O効率、キャッシュ戦略などを評価してください。",
    "maintainability": "\n\n特に保守性に重点を置いてレビューしてください。SOLID原則、DRY、コード複雑度、ドキュメント化などを評価してください。",
    "completeness": "\n\n特に完全性に重点を置いてレビューしてください。不足している情報、未定義の用語、曖昧な記述を特定してください。",
    "accuracy": "\n\n特に正確性に重点を置いてレビューしてください。技術的な誤り、矛盾、最新性を確認してください。",
    "clarity": "\n\n特に明確性に重点を置いてレビューしてください。わかりにくい表現、曖昧な定義、改善が必要な図表を特定してください。",
    "architecture": "\n\n特にアーキテクチャに重点を置いてレビューしてください。システム構成、コンポーネント分割、依存関係を評価してください。",
    "scalability": "\n\n特にスケーラビリティに重点を置いてレビューしてください。水平/垂直スケーリング、ボトルネック、分散処理を評価してください。",
    "patterns": "\n\n特にデザインパターンに重点を置いてレビューしてください。適切なパターンの使用、アンチパターンの回避を確認してください。",
    "coverage": "\n\n特にテストカバレッジに重点を置いてレビューしてください。ブランチカバレッジ、条件カバレッジ、パスカバレッジを評価してください。",
    "edge-cases": "\n\n特にエッジケースに重点を置いてレビューしてください。境界値、null/空値、異常入力のテストを確認してください。",
    "quality": "\n\n特にテスト品質に重点を置いてレビューしてください。テストの信頼性、独立性、保守性を評価してください。"
}

# プロファイル別のデフォルト設定
PROFILES = {
    "quick-review": {
        "model": "gpt-5-codex",
        "reasoning": "medium",
        "description": "軽量レビュー（高速）"
    },
    "deep-review": {
        "model": "gpt-5.1-codex-max",
        "reasoning": "high",
        "description": "標準レビュー（推奨）"
    },
    "xhigh-review": {
        "model": "gpt-5.1-codex-max",
        "reasoning": "xhigh",
        "description": "超詳細分析（非常に遅い）"
    }
}


def check_codex_installed() -> bool:
    """Codex CLIがインストールされているか確認"""
    try:
        result = subprocess.run(
            ["codex", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def build_prompt(review_type: str, target: str, focus_areas: Optional[List[str]] = None,
                 custom_prompt: Optional[str] = None) -> str:
    """レビュープロンプトを構築"""
    if custom_prompt:
        # str.replace() を使用して安全に置換（{} を含むコード片でもクラッシュしない）
        return custom_prompt.replace("{target}", target)

    base_prompt = REVIEW_PROMPTS.get(review_type, REVIEW_PROMPTS["code"])
    prompt = base_prompt.replace("{target}", target)

    if focus_areas:
        for focus in focus_areas:
            if focus in FOCUS_PROMPTS:
                prompt += FOCUS_PROMPTS[focus]

    return prompt


def generate_output_filename(review_type: str, target: str, output_dir: str) -> str:
    """出力ファイル名を生成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_name = Path(target).stem if Path(target).is_file() else Path(target).name
    filename = f"{review_type}_review_{target_name}_{timestamp}.md"
    return str(Path(output_dir) / filename)


def run_codex_review(
    review_type: str,
    target: str,
    output_dir: str,
    profile: str = "deep-review",
    focus_areas: Optional[List[str]] = None,
    custom_prompt: Optional[str] = None,
    working_dir: Optional[str] = None,
    model: Optional[str] = None,
    reasoning: Optional[str] = None,
    verbose: bool = False
) -> tuple[bool, str]:
    """
    Codex CLIを使用してレビューを実行

    Returns:
        tuple: (成功フラグ, 出力ファイルパス or エラーメッセージ)
    """
    # 出力ディレクトリの作成
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 出力ファイルパスの生成
    output_file = generate_output_filename(review_type, target, output_dir)

    # プロンプトの構築
    prompt = build_prompt(review_type, target, focus_areas, custom_prompt)

    # プロファイルからモデルと推論レベルを取得
    profile_config = PROFILES.get(profile, PROFILES["deep-review"])
    use_model = model if model else profile_config["model"]
    use_reasoning = reasoning if reasoning else profile_config["reasoning"]

    # コマンドの構築
    cmd = ["codex", "exec"]

    # モデルの指定（プロファイルまたはオーバーライド）
    cmd.extend(["--model", use_model])

    # 推論レベルの指定
    cmd.extend(["--config", f"model_reasoning_effort={use_reasoning}"])

    # 自動実行モード（承認スキップ）
    cmd.append("--full-auto")

    # 作業ディレクトリの設定
    if working_dir:
        cmd.extend(["-C", working_dir])

    # 出力ファイルの指定
    cmd.extend(["-o", output_file])

    # プロンプトの追加
    cmd.append(prompt)

    if verbose:
        print(f"実行コマンド: {' '.join(cmd)}")
        print(f"出力先: {output_file}")

    # Codex CLIの実行
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10分タイムアウト
        )

        if result.returncode == 0:
            return True, output_file
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return False, f"Codex実行エラー: {error_msg}"

    except subprocess.TimeoutExpired:
        return False, "タイムアウト: レビューに10分以上かかりました"
    except Exception as e:
        return False, f"実行エラー: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Codex CLIを使用してコード/ドキュメントのレビューを実行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # コードレビュー（デフォルト: gpt-5.1-codex-max + high）
  python3 run_codex_review.py --type code --target src/ --output ./reviews

  # セキュリティ重視のコードレビュー
  python3 run_codex_review.py --type code --target src/ --output ./reviews --focus security

  # 超詳細分析でドキュメントレビュー（xhigh推論）
  python3 run_codex_review.py --type document --target docs/spec.md --output ./reviews --profile xhigh-review

  # カスタムプロンプトでレビュー
  python3 run_codex_review.py --type code --target src/ --output ./reviews --custom-prompt "APIエンドポイントのセキュリティを確認してください。対象: {target}"

利用可能なプロファイル:
  deep-review   : 標準レビュー（gpt-5.1-codex-max, high）- 推奨
  xhigh-review  : 超詳細分析（gpt-5.1-codex-max, xhigh）
  quick-review  : 軽量レビュー（gpt-5-codex, medium）- 高速
        """
    )

    parser.add_argument(
        "--type", "-t",
        choices=["code", "document", "design", "test"],
        required=True,
        help="レビュータイプ"
    )

    parser.add_argument(
        "--target",
        required=True,
        help="レビュー対象のファイルまたはディレクトリ"
    )

    parser.add_argument(
        "--output", "-o",
        default="./reviews",
        help="レビュー結果の出力ディレクトリ（デフォルト: ./reviews）"
    )

    parser.add_argument(
        "--profile", "-p",
        choices=list(PROFILES.keys()),
        default="deep-review",
        help="使用するプロファイル（デフォルト: deep-review）"
    )

    parser.add_argument(
        "--focus", "-f",
        help="重点を置くエリア（カンマ区切り: security,performance,maintainability等）"
    )

    parser.add_argument(
        "--custom-prompt",
        help="カスタムプロンプト（{target}がターゲットに置換される）"
    )

    parser.add_argument(
        "--working-dir", "-C",
        help="作業ディレクトリ"
    )

    parser.add_argument(
        "--model", "-m",
        help="モデルをオーバーライド（例: gpt-5.1-codex-max）"
    )

    parser.add_argument(
        "--reasoning", "-r",
        choices=["low", "medium", "high", "xhigh"],
        help="推論レベルをオーバーライド"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="詳細出力を有効化"
    )

    args = parser.parse_args()

    # Codex CLIのインストール確認
    if not check_codex_installed():
        print("エラー: Codex CLIがインストールされていません。")
        print("インストール方法:")
        print("  npm install -g @openai/codex")
        print("  または")
        print("  brew install --cask codex")
        sys.exit(1)

    # フォーカスエリアのパース
    focus_areas = None
    if args.focus:
        focus_areas = [f.strip() for f in args.focus.split(",")]

    # プロファイル情報の取得
    profile_info = PROFILES.get(args.profile, PROFILES["deep-review"])
    use_model = args.model if args.model else profile_info["model"]
    use_reasoning = args.reasoning if args.reasoning else profile_info["reasoning"]

    print(f"レビュー開始:")
    print(f"  タイプ: {args.type}")
    print(f"  対象: {args.target}")
    print(f"  モデル: {use_model}")
    print(f"  推論レベル: {use_reasoning}")
    if focus_areas:
        print(f"  フォーカス: {', '.join(focus_areas)}")
    print()

    # レビュー実行
    success, result = run_codex_review(
        review_type=args.type,
        target=args.target,
        output_dir=args.output,
        profile=args.profile,
        focus_areas=focus_areas,
        custom_prompt=args.custom_prompt,
        working_dir=args.working_dir,
        model=args.model,
        reasoning=args.reasoning,
        verbose=args.verbose
    )

    if success:
        print(f"レビュー完了!")
        print(f"結果ファイル: {result}")
        sys.exit(0)
    else:
        print(f"レビュー失敗: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
