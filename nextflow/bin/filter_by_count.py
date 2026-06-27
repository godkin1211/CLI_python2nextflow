#!/usr/bin/env python3
"""Step 2: 依 count_threshold 過濾。

設計重點 (對齊參考答案 jobs/291fa9e9_參考答案/output/filtered_output.csv):
  - 保留 count <= threshold 的列 (保留「對應 mRNA 數量少、較專一」的 miRNA)。
  - 這與直覺的 >= 相反，是本 pipeline 的關鍵語意。
"""
import argparse
import csv


def filter_by_count(input_path: str, output_path: str, threshold: int) -> int:
    kept = 0
    with open(input_path, newline="", encoding="utf-8") as f, \
         open(output_path, "w", newline="", encoding="utf-8") as out:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in reader:
            if int(row["count"]) <= threshold:   # 保留專一的 miRNA (count <= threshold)
                writer.writerow(row)
                kept += 1
    return kept


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Filter miRNA rows by count_threshold (keep count <= threshold)")
    p.add_argument("--input", required=True, help="輸入 CSV (欄位: miRNA, count, mRNA)")
    p.add_argument("--output", required=True, help="輸出過濾後 CSV")
    p.add_argument("--threshold", required=True, type=int, help="count 上限 (保留 count <= threshold)")
    args = p.parse_args()
    n = filter_by_count(args.input, args.output, args.threshold)
    print(f"[filter_by_count] kept {n} rows (count <= {args.threshold}) -> {args.output}")
