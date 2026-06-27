from pathlib import Path
import uuid
import os
import yaml
import shutil

from CLI.analysis_pipeline_code.run_analysis_pipeline import run_analysis_pipeline
from CLI.analysis_pipeline_code.create_config import create_config


# command line 模式分析流程啟動程式
if __name__ == "__main__":

    # === Step 1 : 取得專案根目錄 ===
    CLI_root = Path(__file__).resolve().parent.parent


    # === Step 2 : 生成不重複的 JobID 資料夾 (while 無限生成直到不重複) ===
    while True:
        job_id = uuid.uuid4().hex[:8]
        job_dir = CLI_root / "jobs" / job_id
        if not job_dir.exists():
            break   # ✅ 找到不重複 ID
    print(f"✅ Generate unique job_id: {job_id}")
    job_dir.mkdir(parents=True, exist_ok=True)
    

    # === Step 3 : 建立 input / output 資料夾 ===
    input_dir = job_dir / "input"
    output_dir = job_dir / "output"
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)


    # === Step 4 : 讀取 CLI_config.yaml 的參數 ===
    with open(CLI_root / "static" / "CLI_input_file"/ "CLI_config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        # 參數讀取因專案而異
        input_file_path = Path(config["input_file_path"]).resolve()
        count_threshold = config["count_threshold"]

        # 修改 input 檔案的路徑，從 CLI_config 指定的改為 job_id 資料夾，並複製一份到 job_id 資料夾
        save_path = job_dir / "input" / input_file_path.name
        shutil.copy(input_file_path, save_path)
        print(f"📁 Input file ( {input_file_path.name} ) copied to: {save_path}")


    # === Step 5 : 在 job_dir 建立 config.yaml ===
    # 參數輸入因專案而異
    create_config(
        job_dir=job_dir,
        input_file_path=save_path,
        count_threshold = count_threshold
    )

    # === Step 6 : 執行正式分析 run_analysis_pipeline ===
    run_analysis_pipeline(job_dir)
