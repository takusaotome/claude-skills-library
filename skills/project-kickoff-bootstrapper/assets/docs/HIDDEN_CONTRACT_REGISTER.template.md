# HIDDEN_CONTRACT_REGISTER

## Purpose

既存関数・共通サービス・外部モジュール・ライブラリ利用時の「名前から見えない契約」を記録する。

## Register

| Item | Location | Why It Was Risky | Assumed Contract | Actual Contract | Side Effects / Error Behavior | Environment Assumptions | Verification Evidence | Owner |
|---|---|---|---|---|---|---|---|---|
| Example: `keepTwoDecimal` | `utils/money.py` | 名前から数値返却に見えた | float を返すと思った | string を返す | 文字列比較・型変換が必要 | locale / format 依存あり | 実装読解 / 実テスト |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

## Investigation Checklist

- [ ] 関数名 / API 名だけで判断していない
- [ ] 戻り値型を確認した
- [ ] 例外発生条件を確認した
- [ ] 副作用を確認した
- [ ] mock と実実装の差を確認した
- [ ] 環境差分の影響を確認した
