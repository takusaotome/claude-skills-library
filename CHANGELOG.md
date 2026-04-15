# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `LICENSE` (MIT) for open-source distribution
- `AGENTS.md` symlink to `CLAUDE.md`
- `CHANGELOG.md` (this file)
- CI matrix strategy: 16 skills now tested in parallel (was 2)
- `.gitignore` rules for runtime analysis outputs and WIP skills

### Changed
- Skill catalog count corrected: 93 → 96 in README.md
- Project Management category count: 4 → 6
- CI workflow refactored from sequential test steps to `test-skills` matrix job

### Removed
- 12 skeleton skill directories (pyc-only, no source code committed)
- Stale `macro_regime_*` analysis output files from repository root

## [Previous]

See the **Version History** section in [README.md](README.md) for historical per-skill release entries.
