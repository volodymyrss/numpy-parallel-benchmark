import json
import multiprocessing as mp
import os
import numpy as np
import time
import sys
import subprocess
import ctadata

import click

def op_np():
    r = np.arange(10000000)
    for j in range(30):
        r = r*2

def op_c():
    subprocess.check_call(["./bench"])


def func(args):
    i, version = args

    t0 = time.time()

    {
        'np': op_np,
        'c': op_c
    }[version]()
        
    print("took", time.time() - t0)

    return time.time() - t0


def run(nproc: int, ntask: int, version: str) -> dict:
    t0 = time.time()


    with mp.Pool(nproc) as p:
        times = p.map(func, [(i, version) for i in range(ntask)])

    total_time = time.time() - t0
    print("total", total_time)

    return {
        "nproc": nproc,
        "ntask": ntask,
        "version": version,
        "total_time": total_time,
        "times": times
    }

os.system("g++ -O3 -o bench bench.cxx")


@click.command()
@click.argument("nproc", type=str)
@click.argument("ntask", type=str)
@click.argument("version", type=str)
@click.option("-u", "--upload", is_flag=True)
@click.option("-n", "--name")
def main(nproc, ntask, version, upload, name):
    nproc_s = [int(i) for i in sys.argv[1].split(",")]
    ntask_s = [int(i) for i in sys.argv[2].split(",")]
    version_s = sys.argv[3].split(",")

    if not os.path.exists(f"reports/{name}"):
        os.makedirs(f"reports/{name}")

    for nproc in nproc_s:
        for ntask in ntask_s:
            for version in version_s:
                print("nproc", nproc, "ntask", ntask, "version", version)

                r = run(nproc, ntask, version)
                r["name"] = name

                fn = f"reports/{name}/{nproc}_{ntask}_{version}.json"
                with open(fn, "w") as f:
                    json.dump(r, f)

                if upload:
                    r = ctadata.upload_file(fn, fn)
                    print(r)




if __name__ == "__main__":
    main()