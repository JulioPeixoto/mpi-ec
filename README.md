# mpi-ec

API FastAPI para comparar processamento sequencial e paralelo (MPI) usando Monte Carlo Pi.

### Monte Carlo Pi (resumo)

Gera N pontos aleatorios no quadrado [0,1]x[0,1], conta quantos caem dentro do circulo unitario (x^2 + y^2 <= 1) e estima pi = 4 * (dentro / total). Com N pequeno o resultado varia a cada execucao; com N grande a estimativa converge para pi.

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

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | `/pi/sequential?n={N}` | Estima pi com N amostras (sequencial) |
| GET | `/pi/parallel?n={N}` | Estima pi com N amostras (MPI, 4 ranks) |

### Parametros

- `n` = numero de amostras (inteiro >= 1)

### Exemplo de uso

```bash
curl "http://localhost:8000/pi/sequential?n=100000000"
curl "http://localhost:8000/pi/parallel?n=100000000"
```

### Exemplo de resultado (Monte Carlo Pi, n=100)

Com N pequeno, o overhead do MPI domina e o sequencial e muito mais rapido.

Sequencial:

```json
{
  "n": 100,
  "result": 3.24,
  "duration_ms": 0.02
}
```

Paralelo:

```json
{
  "n": 100,
  "result": 2.76,
  "duration_ms": 249.56
}
```

### Exemplo de resultado (Monte Carlo Pi, n=100000000)

Com N grande, o paralelo compensa o overhead.

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
  mpi_pi.py - script MPI para Monte Carlo Pi paralelo
  pi.py     - funcao Monte Carlo Pi sequencial
```
