import yaml
from pathlib import Path

# 建立 config.yaml (Web  和 CLI 共用)
# 參數因專案而異
def create_config(job_dir, input_file_path, count_threshold):
    config = {
        "input_file_path": str(input_file_path), 
        "count_threshold": int(count_threshold)
    }

    output_path = job_dir / "config.yaml"

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

    print(f"📝 config.yaml built → {output_path}")
