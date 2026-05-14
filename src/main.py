"""
main.py — Punto de entrada de la aplicación.

Uso:
  python -m src.main --maze small --algorithm bfs
  python -m src.main --maze medium --algorithm all
  python -m src.main --maze mazes/mi_laberinto.txt --algorithm astar
  python -m src.main --maze large --algorithm all --show-explored

Argumentos:
  --maze          : small | medium | large | <ruta al archivo .txt>
  --algorithm     : bfs | dfs | ucs | astar | all
  --show-explored : (flag) muestra con '*' los nodos explorados en el mapa
"""

import argparse
import os
import sys
from typing import List

from src.maze import Maze
from src.visualizer import print_maze, print_stats
from src.algorithms.bfs import bfs
from src.algorithms.dfs import dfs
from src.algorithms.ucs import ucs
from src.algorithms.astar import astar


# Rutas predefinidas para los laberintos
MAZE_PRESETS = {
    "small":  os.path.join("mazes", "maze_small.txt"),
    "medium": os.path.join("mazes", "maze_medium.txt"),
    "large":  os.path.join("mazes", "maze_large.txt"),
}

# Registro de algoritmos disponibles
ALGORITHMS = {
    "bfs":   ("BFS   — Búsqueda por Amplitud",      bfs),
    "dfs":   ("DFS   — Búsqueda por Profundidad",    dfs),
    "ucs":   ("UCS   — Búsqueda de Costo Uniforme",  ucs),
    "astar": ("A*    — A* con heurística Manhattan", astar),
}


def resolve_maze_path(maze_arg: str) -> str:
    """Devuelve la ruta al archivo de laberinto según el argumento recibido."""
    if maze_arg in MAZE_PRESETS:
        return MAZE_PRESETS[maze_arg]
    return maze_arg  # ruta personalizada


def run_algorithm(name: str, label: str, fn, maze: Maze, show_explored: bool) -> dict:
    """Ejecuta un algoritmo, imprime resultados y retorna las métricas."""
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"{'='*50}")

    path, cost, explored_count, time_ms = fn(maze)

    explored_set = None
    if show_explored and path:
        # Reconstruir explorados no es parte de la firma, se omite aquí
        explored_set = None

    print_maze(maze, path=path, show_explored=False)
    print_stats(label, path, cost, explored_count, time_ms)

    return {
        "algorithm": name,
        "path_length": len(path) - 1 if path else None,
        "cost": cost,
        "explored": explored_count,
        "time_ms": time_ms,
        "found": path is not None,
    }


def print_comparison_table(results: List[dict]) -> None:
    """Imprime tabla comparativa cuando se ejecutan todos los algoritmos."""
    print("\n" + "="*60)
    print("  TABLA COMPARATIVA")
    print("="*60)
    header = f"{'Algoritmo':<10} {'Encontró':>8} {'Pasos':>7} {'Costo':>7} {'Explorados':>11} {'Tiempo(ms)':>11}"
    print(header)
    print("-"*60)
    for r in results:
        found  = "Sí" if r["found"] else "No"
        steps  = str(r["path_length"]) if r["path_length"] is not None else "-"
        cost   = str(r["cost"]) if r["cost"] else "-"
        print(
            f"{r['algorithm']:<10} {found:>8} {steps:>7} {cost:>7} "
            f"{r['explored']:>11} {r['time_ms']:>10.3f}"
        )
    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Resolvedor de laberintos con algoritmos de búsqueda IA",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--maze",
        required=True,
        metavar="LABERINTO",
        help="Laberinto a usar: small | medium | large | <ruta.txt>",
    )
    parser.add_argument(
        "--algorithm",
        required=True,
        metavar="ALGORITMO",
        choices=list(ALGORITHMS.keys()) + ["all"],
        help="Algoritmo: bfs | dfs | ucs | astar | all",
    )
    parser.add_argument(
        "--show-explored",
        action="store_true",
        help="Marcar con '*' los nodos explorados en el mapa",
    )

    args = parser.parse_args()

    # Resolver ruta del laberinto
    maze_path = resolve_maze_path(args.maze)
    if not os.path.exists(maze_path):
        print(f"[ERROR] No se encontró el archivo: '{maze_path}'")
        sys.exit(1)

    # Cargar laberinto
    try:
        maze = Maze(maze_path)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"\nLaberinto : {maze_path}  ({maze.rows}x{maze.cols})")
    print(f"Inicio    : {maze.start}  |  Meta: {maze.goal}")

    # Ejecutar algoritmo(s)
    selected = list(ALGORITHMS.items()) if args.algorithm == "all" else [(args.algorithm, ALGORITHMS[args.algorithm])]

    results = []
    for name, (label, fn) in selected:
        metrics = run_algorithm(name, label, fn, maze, args.show_explored)
        results.append(metrics)

    if len(results) > 1:
        print_comparison_table(results)


if __name__ == "__main__":
    main()
