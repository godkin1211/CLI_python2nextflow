from pathlib import Path
import sys
import traceback
import yaml

from CLI.analysis_pipeline_code.analysis_task import analysis_task


# 分析主程式架構
def run_analysis_pipeline(job_dir):

    # === Step 1: 設定 pipeline.log ===
    log_path = job_dir / "pipeline.log"
    class Tee:
        def __init__(self, *files):
            self.files = files
        def write(self, data):
            for f in self.files:
                f.write(data)
                f.flush()
        def flush(self):
            for f in self.files:
                f.flush()
    log_file = open(log_path, "w", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, log_file)
    sys.stderr = Tee(sys.stderr, log_file)
    print("📝 pipeline.log built:",log_path)


    try:
        # === Step 2: 讀取 job_id 資料夾的設定檔 config.yaml ===
        config_path = job_dir / "config.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"Cannot find config file: {config_path}")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            # 參數讀取因專案而異
            input_file_path = Path(config["input_file_path"]).resolve()
            count_threshold = config["count_threshold"]


        # === Step 3: Pipeline Steps ===
        # analysis_task 讀取參數因專案而異
        analysis_task(job_dir, input_file_path, count_threshold)


    except Exception as e:
        error_message = traceback.format_exc()
        print("❌ Pipeline Error：\n", error_message)

    finally:
        print("Analysis Finish!")
        # 恢復 stdout/stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        log_file.close()