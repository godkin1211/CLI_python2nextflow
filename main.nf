#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

/*
 * CLI_python2nextflow (EPI2ME Labs 相容)
 *
 *   Step 1 REVERSE_AGGREGATE : mRNA->miRNAs  =>  miRNA->mRNAs (含 count)
 *   Step 2 FILTER_BY_COUNT   : 保留 count <= count_threshold 的專一 miRNA
 *
 * 參數由 EPI2ME 桌面 App 或命令列提供 (見 nextflow_schema.json)。
 */

include { STAGE_INPUT       } from './modules/local/stage_input'
include { REVERSE_AGGREGATE } from './modules/local/reverse_aggregate'
include { FILTER_BY_COUNT   } from './modules/local/filter_by_count'
include { RECORD_PARAMS     } from './modules/local/record_params'
include { MAKE_REPORT       } from './modules/local/make_report'

workflow {
    // ---------- 參數驗證 (輕量手動檢查) ----------
    // 註: nextflow_schema.json 為 EPI2ME draft-07 格式 (供桌面 App UI 用)，
    //     與 nf-schema 2.x plugin (要 draft 2020-12) 不相容，故命令列改用手動驗證。
    // (26.04 strict: 執行陳述必須放在 workflow 內)
    if (params.validate_params) {
        if (!params.input_file_path) {
            error "缺少必填參數 --input_file_path (輸入 CSV: mRNA, miRNAs)"
        }
        // 註: 命令列 --count_threshold 傳入為字串, -params-file 傳入為整數;
        //     用 isInteger() 同時接受兩者。
        if (!"${params.count_threshold}".isInteger() || "${params.count_threshold}".toInteger() < 1) {
            error "Validation of pipeline parameters failed: --count_threshold 必須是 >= 1 的整數 (目前: ${params.count_threshold})"
        }
    }

    // ---------- 組出「使用之參數」摘要 ----------
    def summary_map = [
        'Job ID'           : params.job_id,
        'Run name'         : workflow.runName,
        'input_file_path'  : params.input_file_path,
        'count_threshold'  : params.count_threshold,
        'out_dir'          : params.out_dir,
        'Nextflow version' : workflow.nextflow.version,
        'Launch dir'       : workflow.launchDir,
        'Start time'       : new java.util.Date().format('yyyy-MM-dd HH:mm:ss'),
    ]
    def summary_yaml = summary_map.collect { k, v -> "${k}: ${v}" }.join('\n')

    // 啟動時印到 console + .nextflow.log
    log.info(
        "\n" +
        "====================================================\n" +
        " mRNA -> miRNA reverse-aggregate pipeline\n" +
        "----------------------------------------------------\n" +
        summary_map.collect { k, v -> String.format('  %-18s: %s', k, v) }.join('\n') + "\n" +
        "====================================================\n"
    )

    ch_input = Channel.fromPath(params.input_file_path, checkIfExists: true)

    // 把輸入複製進 out_dir/input/ (輸入快照)
    STAGE_INPUT( ch_input )

    // 把使用之參數寫成 out_dir/params_used.yaml (設定快照)
    RECORD_PARAMS( Channel.value(summary_yaml) )

    // Step 1 -> Step 2，輸出發布到 out_dir/output/
    REVERSE_AGGREGATE( ch_input )
    FILTER_BY_COUNT( REVERSE_AGGREGATE.out.aggregated, params.count_threshold )

    // HTML 報告 (供 EPI2ME Labs 內嵌呈現)，發布到 out_dir/report.html
    MAKE_REPORT(
        REVERSE_AGGREGATE.out.aggregated,
        FILTER_BY_COUNT.out.filtered,
        params.count_threshold,
        params.job_id
    )

    // (26.04 strict: handler 需用 = 賦值,並放在 workflow 內)
    workflow.onComplete = {
        log.info( workflow.success
            ? "\n✅ Pipeline 完成! Job ID: ${params.job_id}\n   輸出目錄: ${params.out_dir}/\n   ├─ report.html      (EPI2ME HTML 報告)\n   ├─ input/           (輸入快照)\n   ├─ output/          (output.csv, filtered_output.csv)\n   ├─ params_used.yaml (設定快照)\n   └─ execution/       (執行報告)\n"
            : "\n❌ Pipeline 失敗 (Job ID: ${params.job_id}, exit: ${workflow.exitStatus})\n" )
    }
}
