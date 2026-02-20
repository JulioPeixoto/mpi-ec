# mpi-ec

API FastAPI para comparar processamento sequencial e paralelo (MPI). Inclui Fibonacci (didatico) e Monte Carlo Pi (ganho de performance real).

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- OpenMPI ou Microsoft MPI (apenas para os endpoints paralelos)

## Instalacao

```bash
uv sync
```

## Execucao local

```bash
uv run fastapi dev src/main.py
```

Os endpoints paralelos requerem `mpirun` (OpenMPI) ou `mpiexec` (Microsoft MPI) no PATH. Sem MPI instalado, retornam erro informativo.

## Docker

```bash
docker build -t mpi-ec .
docker run -p 8000:8000 mpi-ec
```

A imagem inclui OpenMPI. O endpoint paralelo funciona dentro do container.

## Endpoints

### Fibonacci

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/fib/sequential?n={N}` | Calcula fib(N) de forma sequencial |
| GET | `/fib/parallel?n={N}` | Calcula fib(N) em paralelo com MPI (3 ranks) |

### Monte Carlo Pi

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/pi/sequential?n={N}` | Estima pi com N amostras (sequencial) |
| GET | `/pi/parallel?n={N}` | Estima pi com N amostras (MPI, 4 ranks) |

### Parametros

- Fibonacci: `n` = indice (inteiro >= 0)
- Pi: `n` = numero de amostras (inteiro >= 1)

### Exemplo de uso

```bash
curl "http://localhost:8000/fib/sequential?n=30"
curl "http://localhost:8000/fib/parallel?n=30"
curl "http://localhost:8000/pi/sequential?n=100000000"
curl "http://localhost:8000/pi/parallel?n=100000000"
```

### Exemplo de resultado (Monte Carlo Pi, n=100000000)

Sequencial:

```json
{
  "n": 100000000,
  "result": 3.141568,
  "duration_ms": 9795.39
}
```

Paralelo:

```json
{
  "n": 100000000,
  "result": 3.14136512,
  "duration_ms": 3425.01
}
```

O paralelo reduz o tempo de ~9.8s para ~3.4s (cerca de 2.9x mais rapido com 4 ranks).

## Estrutura

```
src/
  main.py   - API FastAPI com os endpoints
  mpi.py    - script MPI para Fibonacci paralelo
  mpi_pi.py - script MPI para Monte Carlo Pi paralelo
  fib.py    - funcao Fibonacci iterativa
  pi.py     - funcao Monte Carlo Pi sequencial
```
