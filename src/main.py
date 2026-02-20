import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from fastapi import FastAPI, Query
from pi import monte_carlo_pi

sys.set_int_max_str_digits(0)

app = FastAPI()


def _mpi_launcher():
    if sys.platform == "win32":
        candidates = ("mpiexec", "mpirun")
    else:
        candidates = ("mpirun", "mpiexec")
    for cmd in candidates:
        if shutil.which(cmd):
            return cmd
    return None


@app.get("/pi/sequential")
def pi_sequential(n: int = Query(..., ge=1, description="Number of samples")):
    start = time.perf_counter()
    result = monte_carlo_pi(n)
    duration_ms = (time.perf_counter() - start) * 1000
    return {"n": n, "result": round(result, 10), "duration_ms": round(duration_ms, 2)}


@app.get("/pi/parallel")
def pi_parallel(n: int = Query(..., ge=1, description="Number of samples")):
    launcher = _mpi_launcher()
    mpi_script = Path(__file__).parent / "mpi_pi.py"
    args = [launcher, "-n", "4", sys.executable, str(mpi_script), str(n)]
    args.insert(1, "--allow-run-as-root")
    start = time.perf_counter()
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    duration_ms = (time.perf_counter() - start) * 1000
    if proc.returncode != 0:
        return {
            "error": proc.stderr or "MPI execution failed",
            "n": n,
            "duration_ms": round(duration_ms, 2),
        }
    result = float(proc.stdout.strip())
    return {
        "n": n,
        "result": round(result, 10),
        "duration_ms": round(duration_ms, 2),
    }
