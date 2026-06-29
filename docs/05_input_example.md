<!---Example of input format.--->
This workflow accepts a single CSV file via `--input_file_path`.

The CSV must have two columns with a header row:

```
mRNA,miRNAs
Y110A7A.10.1,cel-miR-229-5p
F27C8.1.1,"cel-miR-57-5p,cel-miR-1820-5p"
F07C3.7.1,"cel-miR-51-5p,cel-miR-82-3p,cel-miR-58a-3p"
geneD,-
```

+ `mRNA` — an mRNA identifier.
+ `miRNAs` — one or more miRNA identifiers separated by commas (quote the field if it
  contains commas). A value of `-` means the mRNA has no associated miRNA and is ignored.

A demo file is provided at `test_data/input.csv`.
