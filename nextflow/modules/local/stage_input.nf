// 把輸入檔複製進 job 目錄的 input/ 子資料夾。
// 對應原本 Python 版「shutil.copy(input → jobs/<id>/input/)」的輸入快照,
// 確保每個 job 都保留當下使用的輸入,日後可完整重現。
process STAGE_INPUT {
    tag "stage_input"
    publishDir "${params.outdir}/input", mode: 'copy'

    input:
    path input_csv

    output:
    path input_csv, includeInputs: true     // 把 input 本身當 output 收集 → 被 publishDir 複製

    script:
    """
    true
    """
}
