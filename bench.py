#! /usr/bin/env python3 

import json
import subprocess

import pandas as pd

def main():
    inputs = [
        (2, 32),
        (4, 64),
        (8, 128),
        (16, 256),
        (16, 16),
        (32, 32),
        (64, 64),
        (128, 128),
    ]
    df = pd.DataFrame(columns = ["dim", "fact", "throughput"])

    for dim, fact in inputs:
        m = 2**20
        cmd = f"./bin/ops/join --d={dim*m} --n={fact*m}"
        print(f"🚗  {cmd}")
        out = subprocess.check_output(cmd.split()).decode()
        for l in out.splitlines():
            if "throughput" in l:
                j = json.loads(l)
                df = df.append({
                    "dim": j["num_dim"],
                    "fact": j["num_fact"],
                    "throughput": j["throughput"],
                }, ignore_index=True)

    df.to_csv("join.csv")

if __name__ == "__main__":
    main()