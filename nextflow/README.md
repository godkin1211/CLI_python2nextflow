# mirna-reverse-aggregate (Nextflow / nf-core 風格)

將原本的 Python CLI pipeline 改寫為 Nextflow DSL2 版本。設定沿用原本的 YAML（`config.yaml`），透過 `-params-file` 載入；每次執行產生獨立的 `jobs/<job_id>/` 目錄（對應原本 Python 的 Job ID 機制）。

## 流程

| 步驟 | Process | 功能 |
|------|---------|------|
| — | `STAGE_INPUT` | 把輸入檔複製進 `jobs/<job_id>/input/`（輸入快照，對應原本 `shutil.copy`）。 |
| — | `RECORD_PARAMS` | 把本次「使用之參數」寫成 `params_used.yaml`（對應原本 `create_config()`）。 |
| Step 1 | `REVERSE_AGGREGATE` | `mRNA -> miRNAs` 反轉聚合成 `miRNA -> mRNAs`（含 `count`）。miRNA 字母升序、mRNA 保序去重、跳過缺值 `-`。 |
| Step 2 | `FILTER_BY_COUNT` | 保留 `count <= count_threshold` 的（較專一的）miRNA。 |

## 專案結構

```
nextflow/
├── main.nf                       # 進入點 workflow + 參數驗證 + 摘要 + 郵件 onComplete
├── nextflow.config               # 預設參數 (含 job_id/outdir) / profiles / 執行報告
├── nextflow_schema.json          # nf-core 風格參數 schema (供 nf-schema 驗證)
├── config.yaml                   # 沿用原本設定，供 -params-file 使用
├── nf-test.config                # nf-test 設定
├── bin/                          # 實際分析腳本 (自動加入 PATH)
│   ├── reverse_aggregate.py
│   └── filter_by_count.py
├── conf/
│   └── email.config              # (可選) Gmail 通知設定，用 -c 引入
├── modules/local/
│   ├── stage_input.nf
│   ├── reverse_aggregate.nf
│   ├── filter_by_count.nf
│   └── record_params.nf
└── tests/                        # nf-test 測試
    ├── data/                     # 小而可手算的固定資料
    ├── reverse_aggregate.nf.test (+ .snap)
    ├── filter_by_count.nf.test   (+ .snap)
    └── main.nf.test              # pipeline 正向 + 負向測試
```

> CI 在 repo 根的 `.github/workflows/ci.yml`（push / PR 時自動跑 nf-test）。

## 執行

```bash
cd nextflow
nextflow run main.nf -params-file config.yaml
```

覆寫單一參數：
```bash
nextflow run main.nf -params-file config.yaml --count_threshold 5
```

固定輸出位置（預設是 `jobs/<job_id>/`）：
```bash
nextflow run main.nf -params-file config.yaml --outdir results
```

容器化執行（需 Docker）：
```bash
nextflow run main.nf -params-file config.yaml -profile docker
```

查看參數說明（由 schema 自動產生）：
```bash
nextflow run main.nf --help
```

## 參數

| 參數 | 型別 | 說明 |
|------|------|------|
| `input_file_path` | string（必填） | 輸入 CSV（欄位 `mRNA, miRNAs`，逗號分隔） |
| `count_threshold` | integer（≥1，預設 10） | 保留 `count <= threshold` 的 miRNA |
| `outdir` | string | 輸出目錄，預設 `jobs/<job_id>/` |
| `job_id` | string | 本次執行唯一 ID，預設自動產生 `<時間戳>_<亂數>` |
| `email` | string | 收件信箱，設定後結束寄通知信（需搭配 `-c conf/email.config`） |

參數由 **nf-schema** 依 `nextflow_schema.json` 在啟動前驗證（型別 / 必填 / 範圍 / 格式），不合法立即中止（fail fast）。

## 輸出結構

每次執行產生獨立的 job 目錄：

```
jobs/<job_id>/
├── input/input.csv               # 輸入快照
├── output/
│   ├── output.csv                # 完整反轉表 miRNA, count, mRNA
│   └── filtered_output.csv       # 過濾後 (count <= threshold)
├── params_used.yaml              # 使用之參數快照 (含 Job ID / 版本 / 時間)
└── pipeline_info/                # 執行報告 (timeline / report / trace)
```

> 已驗證：`output.csv` 與 `filtered_output.csv` 與參考答案 `../jobs/291fa9e9_參考答案/output/` **位元組完全相同**。

## 測試

```bash
nf-test test                       # 跑全部 (4 個測試)
nf-test test --update-snapshot     # 有意改變輸出後更新 snapshot 基準
```

| 測試 | 類型 | 驗證 |
|------|------|------|
| `REVERSE_AGGREGATE` | process 正向 | 反轉聚合（跳過 `-`、保序去重、count） |
| `FILTER_BY_COUNT` | process 正向 | 過濾方向 `count <= threshold` |
| `main.nf`（正向） | pipeline | 真實資料對齊參考答案（260 / 120 列） |
| `main.nf`（負向） | pipeline | `count_threshold=0` 被 `validateParameters()` 擋下 |

## 郵件通知（可選）

Gmail 完成 / 失敗通知，前置作業：

```bash
# 1. Google 帳號開啟兩步驟驗證 → 產生「應用程式密碼」(App Password, 16 碼)
# 2. 存成 Nextflow secret (不寫進檔案)
nextflow secrets set GMAIL_APP_PASSWORD "xxxx xxxx xxxx xxxx"
# 3. (可選) 設定寄件帳號;未設則用 conf/email.config 內的預設
export GMAIL_USER="your@gmail.com"
```

執行時用 `-c` 引入並指定收件人：

```bash
nextflow run main.nf -params-file config.yaml \
    -c conf/email.config --email your@gmail.com
```

> SMTP 走 `smtp.gmail.com:587` + STARTTLS（`ssl.protocols = 'TLSv1.2'`）。密碼一律存在 `nextflow secrets`，切勿寫進檔案或進版控。
