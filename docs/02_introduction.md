This workflow takes a CSV table mapping each mRNA to the miRNAs that target it, and
reverses the relationship to produce, for each miRNA, the list of mRNAs it targets
together with a `count` of how many mRNAs that is.

It then filters the reversed table by `count`, keeping only the more specific
miRNAs (those targeting at most `--count_threshold` mRNAs).

The workflow was ported from a Python command-line tool into Nextflow and adapted to
the EPI2ME Labs workflow format so it can be run from the EPI2ME desktop application
or the command line.
