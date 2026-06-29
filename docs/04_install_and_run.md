These are instructions to install and run the workflow on the command line. You can
also access the workflow via the [EPI2ME desktop application](https://labs.epi2me.io/downloads/).

The workflow uses [Nextflow](https://www.nextflow.io/) to manage execution. The
analysis scripts only require Python 3 (standard library), so the default profile runs
directly with your system `python3`. A container profile is also provided.

It is not necessary to clone or download the repository in order to run the workflow.
For more information on running EPI2ME Labs workflows, [visit our website](https://labs.epi2me.io/wfindex).

**Workflow options**

To obtain the workflow, having installed Nextflow, run:

```
nextflow run godkin1211/CLI_python2nextflow --help
```

To run the workflow with a demo dataset bundled in this repository:

```
nextflow run main.nf --input_file_path test_data/input.csv --count_threshold 10
```

Outputs are written to the directory given by `--out_dir` (default `output`).
