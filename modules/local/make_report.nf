// 產生自包含 HTML 報告供 EPI2ME Labs 內嵌呈現 (mime-type text/html)。
process MAKE_REPORT {
    tag "make_report"
    publishDir "${params.out_dir}", mode: 'copy'

    input:
    path reversed_csv
    path filtered_csv
    val count_threshold
    val job_id

    output:
    path "report.html", emit: report

    script:
    """
    make_report.py \\
        --reversed ${reversed_csv} \\
        --filtered ${filtered_csv} \\
        --threshold ${count_threshold} \\
        --job-id ${job_id} \\
        --output report.html
    """
}
