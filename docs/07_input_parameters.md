### Input Options

| Nextflow parameter name | Type | Description | Help | Default |
|-------------------------|------|-------------|------|---------|
| input_file_path | string | CSV file mapping each mRNA to its miRNAs. | Two columns: `mRNA` and `miRNAs` (comma-separated; `-` means none). | (required) |

### Analysis Options

| Nextflow parameter name | Type | Description | Help | Default |
|-------------------------|------|-------------|------|---------|
| count_threshold | integer | Keep only miRNAs targeting at most this many mRNAs. | Rows with `count <= threshold` are kept. Must be a positive integer. | 10 |

### Output Options

| Nextflow parameter name | Type | Description | Help | Default |
|-------------------------|------|-------------|------|---------|
| out_dir | string | Directory for output files. | All workflow results are written here. | output |

### Notification Options

| Nextflow parameter name | Type | Description | Help | Default |
|-------------------------|------|-------------|------|---------|
| email | string | Email address to notify on completion. | Requires SMTP credentials via `-c conf/email.config`. | (none) |
