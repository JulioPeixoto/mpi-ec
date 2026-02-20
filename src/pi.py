import random


def monte_carlo_pi(n: int, seed: int | None = None) -> float:
    if seed is not None:
        random.seed(seed)
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside += 1
    return 4.0 * inside / n
