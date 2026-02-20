import sys
from mpi4py import MPI

from fib import fib


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if n <= 1:
        if rank == 0:
            result = n if n == 1 else 0
            print(result)
        return

    if size < 3 and rank == 0:
        print(fib(n))
        return

    if rank == 0:
        comm.send(n - 1, dest=1, tag=0)
        comm.send(n - 2, dest=2, tag=0)
        result = comm.recv(source=1, tag=1) + comm.recv(source=2, tag=1)
        print(result)
    elif rank == 1:
        k = comm.recv(source=0, tag=0)
        comm.send(fib(k), dest=0, tag=1)
    elif rank == 2:
        k = comm.recv(source=0, tag=0)
        comm.send(fib(k), dest=0, tag=1)


if __name__ == "__main__":
    main()
