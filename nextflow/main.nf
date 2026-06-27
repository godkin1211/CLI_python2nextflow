#!/usr/bin/env nextflow
nextflow.enable.dsl = 2

/*
 * mRNA -> miRNA reverse-aggregate pipeline (Nextflow / nf-core 風格)
 *
 * 由原本的 Python CLI pipeline 改寫:
 *   Step 1 REVERSE_AGGREGATE : mRNA->miRNAs  =>  miRNA->mRNAs (含 count)
 *   Step 2 FILTER_BY_COUNT   : 保留 count <= count_threshold 的專一 miRNA
 *
 * 設定沿用原本的 YAML (config.yaml)，透過 -params-file 載入。
 */

// nf-schema plugin: 對照 nextflow_schema.json 驗證參數
include { validateParameters } from 'plugin/nf-schema'
include { paramsSummaryLog   } from 'plugin/nf-schema'

include { STAGE_INPUT       } from './modules/local/stage_input'
include { REVERSE_AGGREGATE } from './modules/local/reverse_aggregate'
include { FILTER_BY_COUNT   } from './modules/local/filter_by_count'
include { RECORD_PARAMS     } from './modules/local/record_params'

// ---------- 參數驗證 (由 nf-schema 依 nextflow_schema.json 自動執行) ----------
// 檢查: 必填 (required)、型別 (integer/string)、format (file-path 是否存在)、
//       pattern (.csv)、minimum 等，失敗會立即中止並給出明確訊息。
validateParameters()

// nf-schema 內建的參數摘要 (只列出與預設不同 / 有意義的參數)
log.info paramsSummaryLog(workflow)

// ---------- 組出「使用之參數」摘要 ----------
def summary_map = [
    'Job ID'           : params.job_id,
    'Run name'         : workflow.runName,
    'input_file_path'  : params.input_file_path,
    'count_threshold'  : params.count_threshold,
    'outdir'           : params.outdir,
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

workflow {
    ch_input = Channel.fromPath(params.input_file_path, checkIfExists: true)

    // 把輸入複製進 jobs/<job_id>/input/ (輸入快照)
    STAGE_INPUT( ch_input )

    // 把使用之參數寫成 jobs/<job_id>/params_used.yaml (設定快照)
    RECORD_PARAMS( Channel.value(summary_yaml) )

    // Step 1 -> Step 2，輸出發布到 jobs/<job_id>/output/
    REVERSE_AGGREGATE( ch_input )
    FILTER_BY_COUNT( REVERSE_AGGREGATE.out.aggregated, params.count_threshold )
}

workflow.onComplete {
    log.info( workflow.success
        ? "\n✅ Pipeline 完成! Job ID: ${params.job_id}\n   輸出目錄: ${params.outdir}/\n   ├─ input/           (輸入快照)\n   ├─ output/          (output.csv, filtered_output.csv)\n   ├─ params_used.yaml (設定快照)\n   └─ pipeline_info/   (執行報告)\n"
        : "\n❌ Pipeline 失敗 (Job ID: ${params.job_id}, exit: ${workflow.exitStatus})\n" )
}
