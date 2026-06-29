# CLI_python2nextflow

Reverse-aggregate an mRNA->miRNA mapping table and filter by target count.

> This README is assembled from the numbered files in `docs/`, following the EPI2ME
> Labs workflow convention.

## Introduction

This workflow takes a CSV table mapping each mRNA to the miRNAs that target it, and
reverses the relationship to produce, for each miRNA, the list of mRNAs it targets
together with a `count` of how many mRNAs that is. It then keeps only the more specific
miRNAs (those targeting at most `--count_threshold` mRNAs).

Ported from a Python command-line tool and adapted to the EPI2ME Labs workflow format
so it can run from the EPI2ME desktop application or the command line.

## Compute requirements

Recommended: 2 CPUs, 4 GB memory. Minimum: 1 CPU, 1 GB memory. ARM supported.

## Install and run

```
# demo dataset bundled in this repository
nextflow run main.nf --input_file_path test_data/input.csv --count_threshold 10

# or with the example params file
nextflow run main.nf -params-file config.yaml

# containerised
nextflow run main.nf --input_file_path test_data/input.csv -profile docker
```

Outputs are written to `--out_dir` (default `output`).

## Input example

A single CSV via `--input_file_path` with columns `mRNA,miRNAs` (miRNAs comma-separated;
`-` means none). See `test_data/input.csv` and `docs/05_input_example.md`.

## Pipeline overview

1. **Stage input** — snapshot the input into `output/input/`.
2. **Reverse-aggregate** — `mRNA->miRNAs` becomes `miRNA->mRNAs` with a `count` column
   (`output/output.csv`).
3. **Filter by count** — keep `count <= count_threshold` (`output/filtered_output.csv`).
4. **Record parameters** — write `params_used.yaml`.

## Input parameters

See `docs/07_input_parameters.md` (and `nextflow_schema.json`). Key parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `input_file_path` | string | (required) | Input CSV (`mRNA, miRNAs`). |
| `count_threshold` | integer | 10 | Keep miRNAs with `count <= threshold`. |
| `out_dir` | string | output | Output directory. |
| `email` | string | (none) | Optional completion notification. |

## Outputs

| File | Description |
|------|-------------|
| `output/output.csv` | Full reversed table `miRNA, count, mRNA`. |
| `output/filtered_output.csv` | Filtered (`count <= threshold`). |
| `input/input.csv` | Input snapshot. |
| `params_used.yaml` | Parameters used. |
| `execution/` | Nextflow timeline / report / trace. |

## Testing

```
nf-test test
```

## EPI2ME Labs compatibility

This repository follows the EPI2ME Labs workflow layout: `main.nf`, `nextflow.config`
(with an EPI2ME `manifest` and `epi2melabs { tags }` block), `nextflow_schema.json`
(draft-07, with parameter groups, `format`, `help_text` and `demo_url`),
`output_definition.json`, `MANIFEST`, `docs/` and `CHANGELOG.md`.

## License

MIT — see `LICENSE`.
