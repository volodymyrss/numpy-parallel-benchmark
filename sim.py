import json
import multiprocessing as mp
import os
import numpy as np
import time
import sys
import subprocess
import ctadata

import click

def op_np(memory, duration):
    r = np.arange(memory * 1000 * 1000, dtype=np.float64)
    for j in range(duration):
        r = r*2

def op_c(memory, duration):
    subprocess.check_call(["./bench " + str(memory) + " " + str(duration)], shell=True)


def func(args):
    i, version, memory, duration = args

    t0 = time.time()

    {
        'np': op_np,
        'c': op_c
    }[version](memory, duration)
        
    print("took", time.time() - t0)

    return time.time() - t0


def run(nproc: int, ntask: int, version: str, memory, duration) -> dict:
    t0 = time.time()


    with mp.Pool(nproc) as p:
        times = p.map(func, [(i, version, memory, duration) for i in range(ntask)])

    total_time = time.time() - t0
    print("total", total_time)

    return {
        "nproc": nproc,
        "ntask": ntask,
        "version": version,
        "total_time": total_time,
        "times": times
    }


@click.command()
@click.argument("nproc", type=str)
@click.argument("ntask", type=str)
@click.argument("version", type=str)
@click.option("-u", "--upload", is_flag=True)
@click.option("-n", "--name")
@click.option("-m", "--memory", type=int, default=10)
@click.option("-d", "--duration", type=int, default=100)
@click.option("-o", "--optimization", type=str, default="O3")
def main(nproc, ntask, version, upload, name, memory, duration, optimization):
    optimization_s = optimization.split(",")
    

    if '..' in nproc:
        nproc_s = range(*map(int, nproc.split("..")))
    else:
        nproc_s = [int(i) for i in nproc.split(",")]

    ntask_s = [int(i) for i in ntask.split(",")]
    version_s = sys.argv[3].split(",")

    if not os.path.exists(f"reports/{name}"):
        os.makedirs(f"reports/{name}")

    for optimization in optimization_s:
        if optimization in ["O3", "O2", "O1", "O0"]:    
            os.system(f"g++ -{optimization} -o bench bench.cxx")
        else:
            os.system("g++ -o bench bench.cxx")    

        for nproc in nproc_s:
            for ntask in ntask_s:
                for version in version_s:
                    print("nproc", nproc, "ntask", ntask, "version", version)

                    if version == "np" and optimization != "O3":
                        continue

                    r = run(nproc, ntask, version, memory, duration)
                    r["name"] = name
                    r["optimization"] = optimization

                    fn = f"reports/{name}/{nproc}_{ntask}_{version}_{optimization}.json"
                    with open(fn, "w") as f:
                        json.dump(r, f)

                    if upload:
                        r = ctadata.upload_file(fn, fn)
                        print(r)




if __name__ == "__main__":
    main()