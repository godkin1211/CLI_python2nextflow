Output files are written to the directory given by `--out_dir` (default `output`).

| Title | File path | Description | Per sample or aggregated |
|-------|-----------|-------------|--------------------------|
| Workflow report | report.html | Self-contained HTML report (summary cards, count distribution, retained miRNAs); shown in the EPI2ME desktop app. | aggregated |
| Reversed miRNA table | output/output.csv | Full reversed table: each miRNA with its target count and the mRNAs it targets. | aggregated |
| Filtered miRNA table | output/filtered_output.csv | miRNAs with target count <= count_threshold. | aggregated |
| Input snapshot | input/input.csv | Copy of the input CSV used for this run. | aggregated |
| Parameters used | params_used.yaml | Snapshot of parameters (Job ID, threshold, versions, time). | aggregated |
| Execution report | execution/report.html | Nextflow resource-usage report. | aggregated |
