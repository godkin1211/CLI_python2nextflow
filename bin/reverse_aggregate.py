#!/usr/bin/env python3
"""Step 1: 把 mRNA -> miRNAs 對應表反轉聚合成 miRNA -> mRNAs (含 count)。

設計重點 (對齊參考答案 jobs/291fa9e9_參考答案/output/output.csv):
  - 輸入 miRNAs 欄為「逗號分隔」且可能被引號包住 (csv 模組自動處理)。
  - 外層 miRNA 以字母升序輸出 (sorted)。
  - 內層 mRNA 清單「保序去重」(首次出現順序)，因此使用 dict.fromkeys 而非 set。
  - 欄位順序固定為: miRNA, count, mRNA。
"""
import argparse
import csv
from collections import defaultdict


def reverse_aggregate(input_path: str, output_path: str) -> int:
    # miRNA -> dict(用作 ordered-set，保留 mRNA 首次出現順序並去重)
    mapping: dict[str, dict] = defaultdict(dict)

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mrna = row["mRNA"].strip()
            mirnas_field = (row.get("miRNAs") or "").strip()
            if not mirnas_field:
                continue
            for mirna in mirnas_field.split(","):
                mirna = mirna.strip()
                if mirna and mirna != "-":          # 跳過缺值佔位符 "-"
                    mapping[mirna][mrna] = None      # 保序去重

    with open(output_path, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out, lineterminator="\n")  # 對齊 pandas 預設 \n
        writer.writerow(["miRNA", "count", "mRNA"])
        for mirna in sorted(mapping):          # 外層 miRNA 字母升序
            mrnas = list(mapping[mirna])        # 已保序去重
            writer.writerow([mirna, len(mrnas), ",".join(mrnas)])

    return len(mapping)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Reverse-aggregate mRNA->miRNA into miRNA->mRNA")
    p.add_argument("--input", required=True, help="輸入 CSV (欄位: mRNA, miRNAs)")
    p.add_argument("--output", required=True, help="輸出 CSV (欄位: miRNA, count, mRNA)")
    args = p.parse_args()
    n = reverse_aggregate(args.input, args.output)
    print(f"[reverse_aggregate] wrote {n} miRNA rows -> {args.output}")
