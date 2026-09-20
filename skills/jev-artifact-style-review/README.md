# Jev Artifact Style Review

日本語中心・英語対応で成果物の文体を多角的にレビューし、作成担当者への改善フィードバックを作るAgent Skillです。執筆者判定器ではありません。

セットアップと使い方: [日本語README](README_ja.md) · [English README](README_en.md)

エージェント用の入口: [SKILL.md](SKILL.md)

検証状況: [TEST_REPORT.md](TEST_REPORT.md)

## このリポジトリ版について

配布 zip `jev-artifact-style-review-v1.0.0` をそのまま取り込んでいますが、意図的な変更が
2 点あります。

1 つ目は Python 11 ファイルの整形です。本リポジトリの CI が `ruff check` と
`ruff format --check` を実行するため、それに合わせました。整形はフォーマットのみで、ロジックは
変更していません。整形後に同梱テストを再実行し、Python 3.10 で任意依存を導入した状態で
64 件全ての合格を確認済みです。

2 つ目は `TEST_REPORT.md` のヘッダー 3 行です。行末 2 スペースによる改行を使っていましたが、
本リポジトリの pre-commit フックが行末スペースを除去するため、そのままでは 3 行が 1 段落に
結合されます。箇条書きへ変換しました。文言は変えていません。

`MANIFEST.sha256` はこの 2 点を反映して再生成してあるため、配布元 zip のハッシュとは
一致しません。
