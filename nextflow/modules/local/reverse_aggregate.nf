// Step 1: 反轉聚合 mRNA -> miRNA  =>  miRNA -> mRNAs (含 count)
process REVERSE_AGGREGATE {
    tag "reverse_aggregate"
    publishDir "${params.outdir}/output", mode: 'copy'

    input:
    path input_csv

    output:
    path "output.csv", emit: aggregated

    script:
    """
    reverse_aggregate.py --input ${input_csv} --output output.csv
    """
}
