// 把「本次執行使用之參數」寫成 params_used.yaml，發布到 outdir。
// 對應原本 Python 版的 create_config() —— 為每次執行留下參數快照,確保可重現。
process RECORD_PARAMS {
    tag "record_params"
    publishDir "${params.outdir}", mode: 'copy'

    input:
    val summary_yaml

    output:
    path "params_used.yaml"

    script:
    // 用 quoted heredoc ('EOF') 避免 summary 內容中的特殊字元被 shell 解析;
    // \${summary_yaml} 由 Nextflow 在渲染 script 時先行替換為實際內容。
    """
    cat <<'EOF' > params_used.yaml
# ====== 本次執行使用之參數 (params_used.yaml) ======
${summary_yaml}
EOF
    """
}
