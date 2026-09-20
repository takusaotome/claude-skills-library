# Jev Artifact Style Review

日本語中心・英語対応で成果物の文体を多角的にレビューし、作成担当者への改善フィードバックを作るAgent Skillです。執筆者判定器ではありません。

セットアップと使い方: [日本語README](README_ja.md) · [English README](README_en.md)

エージェント用の入口: [SKILL.md](SKILL.md)

検証状況: [TEST_REPORT.md](TEST_REPORT.md)

## このリポジトリ版について

配布 zip (`jev-artifact-style-review-v1.0.0`) をそのまま取り込んだうえで、本リポジトリの
CI（`ruff check` / `ruff format --check`）に合わせて Python 11 ファイルを整形しています。
整形はフォーマットのみで、ロジックは変更していません。整形後に同梱テストを再実行し、
64 件合格（Python 3.10、任意依存を導入した状態）を確認済みです。

`MANIFEST.sha256` は整形後の内容で再生成してあるため、配布元 zip のハッシュとは一致しません。
