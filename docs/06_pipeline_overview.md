### 1. Stage input

The input CSV is copied into the output directory (`input/`) as a snapshot, so each
run keeps a record of exactly what was analysed.

### 2. Reverse-aggregate (Step 1)

The `mRNA -> miRNAs` table is reversed into a `miRNA -> mRNAs` table. For each miRNA:

+ the mRNAs that target it are collected, de-duplicated while preserving first-seen
  order;
+ a `count` column records how many mRNAs that is;
+ miRNAs are written in alphabetical order; placeholder `-` values are skipped.

Output: `output/output.csv` with columns `miRNA, count, mRNA`.

### 3. Filter by count (Step 2)

Rows are filtered to keep only miRNAs with `count <= --count_threshold` (the more
specific miRNAs).

Output: `output/filtered_output.csv`.

### 4. Record parameters

The parameters used for the run (Job ID, threshold, versions, time) are written to
`params_used.yaml`.
