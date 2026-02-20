import shutil
import subprocess
import sys
import time
from pathlib import Path

from fastapi import FastAPI, Query
from fib import fib

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


@app.get("/fib/sequential")
def fib_sequential(n: int = Query(..., ge=0, description="Fibonacci index")):
    start = time.perf_counter()
    result = fib(n)
    duration_ms = (time.perf_counter() - start) * 1000
    return {"n": n, "result": result, "method": "sequential", "duration_ms": round(duration_ms, 2)}


@app.get("/fib/parallel")
def fib_parallel(n: int = Query(..., ge=0, description="Fibonacci index")):
    launcher = _mpi_launcher()
    if not launcher:
        return {
            "error": "mpirun/mpiexec not found in PATH. Install OpenMPI or Microsoft MPI.",
            "n": n,
        }
    mpi_script = Path(__file__).parent / "mpi.py"
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [launcher, "-n", "3", sys.executable, str(mpi_script), str(n)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
    except FileNotFoundError:
        return {
            "error": f"{launcher} not found in PATH. Install OpenMPI or Microsoft MPI.",
            "n": n,
        }
    duration_ms = (time.perf_counter() - start) * 1000
    if proc.returncode != 0:
        return {"error": proc.stderr or "MPI execution failed", "n": n, "duration_ms": round(duration_ms, 2)}
    result = int(proc.stdout.strip())
    return {"n": n, "result": result, "method": "parallel", "duration_ms": round(duration_ms, 2)}
