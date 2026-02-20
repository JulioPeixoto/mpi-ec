import random
import sys

from mpi4py import MPI


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        local_n = n // size + n % size
    else:
        local_n = n // size

    random.seed(rank)
    inside = 0
    for _ in range(local_n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside += 1

    total_inside = comm.reduce(inside, op=MPI.SUM, root=0)
    if rank == 0:
        pi = 4.0 * total_inside / n
        print(pi)


if __name__ == "__main__":
    main()
