# Changelog

All notable changes to this workflow are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [v1.0.0]

### Added
- Initial release as an EPI2ME Labs-compatible workflow.
- `REVERSE_AGGREGATE`: reverse an mRNA->miRNA table into a miRNA->mRNA table with counts.
- `FILTER_BY_COUNT`: keep miRNAs with target count <= `--count_threshold`.
- Input snapshot, parameter snapshot (`params_used.yaml`) and execution reports.
- `nextflow_schema.json` (draft-07) and `output_definition.json` for the EPI2ME desktop app.
- nf-test test suite (module + pipeline, positive and negative) and GitHub Actions CI.
- Optional Gmail notification via `conf/email.config`.

### Notes
- Ported from a Python command-line tool; outputs are byte-for-byte identical to the
  original reference answer.
