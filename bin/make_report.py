#!/usr/bin/env python3
"""產生自包含的 HTML 報告供 EPI2ME Labs 內嵌呈現。

只用 Python 標準庫 (csv/html/datetime)，無外部相依、離線可用。
讀取 Step1 (reversed) 與 Step2 (filtered) 的 CSV，輸出單一 HTML 檔。
"""
import argparse
import csv
import html
from collections import Counter
from datetime import datetime


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_html(reversed_rows, filtered_rows, threshold, job_id):
    total_mirna = len(reversed_rows)
    kept = len(filtered_rows)
    removed = total_mirna - kept
    counts = [int(r["count"]) for r in reversed_rows]
    total_targets = sum(counts)
    max_count = max(counts) if counts else 0

    # count 分布: 1..threshold 各幾個, 以及 > threshold
    dist = Counter()
    for c in counts:
        key = str(c) if c <= threshold else f">{threshold}"
        dist[key] = dist.get(key, 0) + 1
    # 排序: 數字優先, ">N" 放最後
    def sort_key(kv):
        k = kv[0]
        return (1, 0) if k.startswith(">") else (0, int(k))
    dist_items = sorted(dist.items(), key=sort_key)
    dist_max = max(dist.values()) if dist else 1

    # 過濾後 (專一 miRNA) 表格, 依 count 降冪取前 50
    top = sorted(filtered_rows, key=lambda r: -int(r["count"]))[:50]

    def esc(s):
        return html.escape(str(s))

    # 分布長條 (純 CSS, 無外部相依)
    bars = []
    for label, n in dist_items:
        pct = round(100 * n / dist_max, 1)
        bars.append(
            f'<div class="bar-row"><span class="bar-label">count {esc(label)}</span>'
            f'<span class="bar-track"><span class="bar-fill" style="width:{pct}%"></span></span>'
            f'<span class="bar-val">{n}</span></div>'
        )

    rows_html = []
    for r in top:
        mrnas = esc(r["mRNA"])
        if len(mrnas) > 120:
            mrnas = mrnas[:120] + "&hellip;"
        rows_html.append(
            f"<tr><td>{esc(r['miRNA'])}</td><td class='num'>{esc(r['count'])}</td>"
            f"<td class='mrna'>{mrnas}</td></tr>"
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>miRNA reverse-aggregate report</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; background: #f5f7fa; color: #1a2733; }}
  .wrap {{ max-width: 980px; margin: 0 auto; padding: 24px; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .sub {{ color: #5b6b7b; font-size: 13px; margin-bottom: 20px; }}
  .cards {{ display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 28px; }}
  .card {{ flex: 1 1 150px; background: #fff; border-radius: 10px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .card .v {{ font-size: 26px; font-weight: 700; color: #0a6ebd; }}
  .card .l {{ font-size: 12px; color: #5b6b7b; margin-top: 4px; }}
  h2 {{ font-size: 16px; margin: 26px 0 12px; }}
  .panel {{ background: #fff; border-radius: 10px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .bar-row {{ display: flex; align-items: center; gap: 10px; margin: 5px 0; font-size: 13px; }}
  .bar-label {{ width: 90px; color: #5b6b7b; }}
  .bar-track {{ flex: 1; background: #eef2f6; border-radius: 5px; height: 16px; overflow: hidden; }}
  .bar-fill {{ display: block; height: 100%; background: linear-gradient(90deg,#0a6ebd,#3aa0e8); }}
  .bar-val {{ width: 50px; text-align: right; color: #1a2733; font-variant-numeric: tabular-nums; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ text-align: left; padding: 7px 10px; border-bottom: 1px solid #eef2f6; }}
  th {{ color: #5b6b7b; font-weight: 600; }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  td.mrna {{ color: #5b6b7b; font-family: ui-monospace, Menlo, monospace; font-size: 11px; word-break: break-all; }}
  .foot {{ color: #97a6b5; font-size: 11px; margin-top: 24px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>miRNA reverse-aggregate report</h1>
  <div class="sub">Job ID: {esc(job_id)} &nbsp;&middot;&nbsp; generated {now}</div>

  <div class="cards">
    <div class="card"><div class="v">{total_mirna}</div><div class="l">miRNAs (total)</div></div>
    <div class="card"><div class="v">{total_targets}</div><div class="l">mRNA targets (total)</div></div>
    <div class="card"><div class="v">{kept}</div><div class="l">kept (count &le; {threshold})</div></div>
    <div class="card"><div class="v">{removed}</div><div class="l">filtered out</div></div>
    <div class="card"><div class="v">{max_count}</div><div class="l">max targets / miRNA</div></div>
  </div>

  <h2>Target-count distribution</h2>
  <div class="panel">{''.join(bars)}</div>

  <h2>Retained miRNAs (count &le; {threshold}, top {len(top)} by count)</h2>
  <div class="panel">
    <table>
      <thead><tr><th>miRNA</th><th class="num">count</th><th>target mRNAs</th></tr></thead>
      <tbody>{''.join(rows_html)}</tbody>
    </table>
  </div>

  <div class="foot">godkin1211/CLI_python2nextflow &middot; reverse-aggregate mRNA&rarr;miRNA</div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Build self-contained HTML report")
    p.add_argument("--reversed", required=True, help="Step1 output.csv (miRNA,count,mRNA)")
    p.add_argument("--filtered", required=True, help="Step2 filtered_output.csv")
    p.add_argument("--threshold", required=True, type=int)
    p.add_argument("--job-id", default="-")
    p.add_argument("--output", required=True, help="輸出 HTML 路徑")
    args = p.parse_args()

    rev = read_rows(args.reversed)
    filt = read_rows(args.filtered)
    out_html = build_html(rev, filt, args.threshold, args.job_id)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out_html)
    print(f"[make_report] wrote HTML report -> {args.output}")
