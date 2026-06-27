// Step 2: 依 count_threshold 過濾 (保留 count <= threshold 的專一 miRNA)
process FILTER_BY_COUNT {
    tag "filter(threshold=${count_threshold})"
    publishDir "${params.outdir}/output", mode: 'copy'

    input:
    path input_csv
    val count_threshold          // 以 val 注入參數，讓 module 保持可重用

    output:
    path "filtered_output.csv", emit: filtered

    script:
    """
    filter_by_count.py --input ${input_csv} --output filtered_output.csv --threshold ${count_threshold}
    """
}
