import json
import multiprocessing as mp
import os
import numpy as np
import time
import sys
import subprocess

import click

def op_np():
    r = np.arange(10000000)
    for j in range(100):
        r = r*2

def op_c():
    subprocess.check_call(["./bench"])

def func(i):
    t0 = time.time()

    {
        'np': op_np,
        'c': op_c
    }[version]()
        
    print("took", time.time() - t0)
    

def run(nproc: int, ntask: int, version: str) -> dict:
    t0 = time.time()

    with mp.Pool(nproc) as p:
        p.map(func, range(ntask))

    total_time = time.time() - t0
    print("total", total_time)

    return {
        "nproc": nproc,
        "ntask": ntask,
        "version": version,
        "total_time": total_time
    }

os.system("g++ -O3 -o bench bench.cxx")

nproc_s = [int(i) for i in sys.argv[1].split(",")]
ntask_s = [int(i) for i in sys.argv[2].split(",")]
version_s = sys.argv[3].split(",")

if not os.path.exists("reports"):
    os.makedirs("reports")

for nproc in nproc_s:
    for ntask in ntask_s:
        for version in version_s:
            print("nproc", nproc, "ntask", ntask, "version", version)

            r = run(nproc, ntask, version)

            with open(f"reports/{nproc}_{ntask}_{version}.json", "w") as f:
                json.dump(r, f)