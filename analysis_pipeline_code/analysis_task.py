import pandas as pd
import time

# 因專案而異

def analysis_task(job_dir, input_file_path, count_threshold):

    # Step 1
    start_time = time.time()
    df = reverse_mrna_mirna(input_file_path)
    df.to_csv(job_dir / "output" / "output.csv", index=False)
    print("Analysis Step 1: Input file reverse COMPLETE, using ", round(time.time() - start_time, 3), "sec.")


    # Step 2
    start_time = time.time()
    filtered_df = filter(df, count_threshold)
    filtered_df.to_csv(job_dir / "output" / "filtered_output.csv", index=False)
    print("Analysis Step 2: Filter by count_threshold COMPLETE, using ", round(time.time() - start_time, 3), "sec.")

# 作業部份
def reverse_mrna_mirna(input_file_path):
    return reversed_df

# 作業部份
def filter(df, count_threshold):
    return filtered_df