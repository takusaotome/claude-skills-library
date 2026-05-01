---
layout: default
title: "DuckDB Expert"
grand_parent: English
parent: Software Development
nav_order: 17
lang_peer: /ja/skills/dev/duckdb-expert/
permalink: /en/skills/dev/duckdb-expert/
---

# DuckDB Expert
{: .no_toc }

DuckDBを使用した大規模データ分析の専門スキル。DuckDBのアーキテクチャ、SQL構文、パフォーマンス最適化、各種ファイル形式（CSV、Parquet、JSON等）の効率的な読み込み・書き出しを熟知。メモリ効率の良い分析、複雑なクエリの最適化、データパイプライン構築を支援。Use when analyzing large datasets, querying CSV/Parquet/JSON files directly, building data pipelines, or optimizing analytical queries with DuckDB.
{: .fs-6 .fw-300 }

<span class="badge badge-free">No API Required</span>

[Download Skill Package (.skill)](https://github.com/takusaotome/claude-skills-library/raw/main/skill-packages/duckdb-expert.skill){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View Source on GitHub](https://github.com/takusaotome/claude-skills-library/tree/main/skills/duckdb-expert){: .btn .fs-5 .mb-4 .mb-md-0 }

<details open markdown="block">
  <summary>Table of Contents</summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 1. Overview

DuckDBは、OLAP（オンライン分析処理）に最適化された組み込み型の列指向データベースです。このスキルは、DuckDBを使用した効率的なデータ分析、大規模データセットの処理、パフォーマンス最適化を支援します。

---

## 2. Prerequisites

- **Python 3.8+** with `duckdb` package installed
- Optional: `pandas`, `polars`, `pyarrow` for DataFrame integration

```bash
# Install DuckDB (required)
pip install duckdb

# Optional: Install DataFrame libraries
pip install pandas polars pyarrow
```

---

## 3. Quick Start

```bash
1. Connect to DuckDB (in-memory or persistent)
2. Load/query data files directly (CSV, Parquet, JSON)
3. Transform and analyze using SQL
4. Export results (DataFrame, file, or database)
```

---

## 4. How It Works

```
1. Connect to DuckDB (in-memory or persistent)
2. Load/query data files directly (CSV, Parquet, JSON)
3. Transform and analyze using SQL
4. Export results (DataFrame, file, or database)
```

---

## 5. Usage Examples

- 大規模なCSV、Parquet、JSONファイルを直接クエリしたい
- メモリに収まらない大きなデータセットを分析したい
- SQLを使ってデータ変換やETLパイプラインを構築したい
- pandas/Polarsと連携した高速なデータ処理を行いたい
- ファイルベースのデータウェアハウスを構築したい
- 複雑な分析クエリのパフォーマンスを最適化したい

---

## 6. Understanding the Output

- **Data Profile Report**: Markdown/JSON report with schema, statistics, quality metrics
- **Query Results**: pandas/Polars DataFrame, Arrow table, or raw tuples
- **Transformed Files**: Parquet, CSV, or JSON with optional compression/partitioning

---

## 7. Tips & Best Practices

- Begin with the smallest realistic sample input so you can validate the workflow before scaling up.
- Keep `skills/duckdb-expert/SKILL.md` open while working; it remains the authoritative source for the full procedure.
- Review the most relevant reference files first instead of scanning every guide: duckdb_functions_reference.md, file_formats_guide.md, performance_tuning_guide.md.
- Run helper scripts on test data before using them on final assets or production-bound inputs: etl_pipeline.py, duckdb_analyzer.py.
- Preserve intermediate outputs so you can explain assumptions, diffs, and follow-up actions clearly.

---

## 8. Combining with Other Skills

- Combine this skill with adjacent skills in the same category when the work spans planning, implementation, and review.
- Browse the broader category for neighboring workflows: [category index]({{ '/en/skills/dev/' | relative_url }}).
- Use the English skill catalog when you need to chain this workflow into a larger end-to-end process.

---

## 9. Troubleshooting

- Re-check prerequisites first: missing runtime dependencies and unsupported file formats are the most common failures.
- If a helper script is involved, run it with a minimal sample input before applying it to a full dataset or repository.
- Compare your input shape against the reference files to confirm expected fields, sections, or metadata are present.
- Confirm the expected Python version and required packages are installed in the active environment.
- When output looks incomplete, inspect the script arguments and rerun with explicit input/output paths.

---

## 10. Reference

**References:**

- `skills/duckdb-expert/references/duckdb_functions_reference.md`
- `skills/duckdb-expert/references/file_formats_guide.md`
- `skills/duckdb-expert/references/performance_tuning_guide.md`

**Scripts:**

- `skills/duckdb-expert/scripts/duckdb_analyzer.py`
- `skills/duckdb-expert/scripts/etl_pipeline.py`
