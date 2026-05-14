"""
visualizer.py — Visualización del laberinto en consola.

Leyenda de caracteres:
  #  -> pared
  ' '-> pasillo libre
  S  -> inicio
  E  -> meta
  .  -> camino encontrado por el algoritmo
  *  -> nodos explorados (modo detallado)
"""

from typing import List, Optional, Set, Tuple

from src.maze import Maze


def print_maze(
    maze: Maze,
    path: Optional[List[Tuple[int, int]]] = None,
    explored: Optional[Set[Tuple[int, int]]] = None,
    show_explored: bool = False,
) -> None:
    """
    Imprime el laberinto en consola.

    Args:
        maze:           Instancia del laberinto.
        path:           Lista de posiciones que forman el camino solución.
        explored:       Conjunto de posiciones exploradas durante la búsqueda.
        show_explored:  Si True, marca con '*' los nodos explorados (no parte del camino).
    """
    path_set = set(path) if path else set()
    explored_set = explored if explored else set()

    # Construir representación visual
    visual = [list(row) for row in maze.grid]

    if show_explored:
        for row, col in explored_set:
            if visual[row][col] not in ("#", "S", "E"):
                visual[row][col] = "*"

    for row, col in path_set:
        if visual[row][col] not in ("#", "S", "E"):
            visual[row][col] = "."

    # Imprimir con colores ANSI básicos si el terminal lo soporta
    COLOR = {
        "#": "\033[90m#\033[0m",   # gris oscuro
        "S": "\033[92mS\033[0m",   # verde
        "E": "\033[91mE\033[0m",   # rojo
        ".": "\033[94m.\033[0m",   # azul
        "*": "\033[93m*\033[0m",   # amarillo
        " ": " ",
    }

    print()
    for row in visual:
        print("".join(COLOR.get(cell, cell) for cell in row))
    print()


def print_stats(
    algorithm_name: str,
    path: Optional[List[Tuple[int, int]]],
    cost,
    explored_count: int,
    time_ms: float,
) -> None:
    """Imprime las métricas de ejecución de un algoritmo."""
    sep = "-" * 40
    print(sep)
    print(f"  Algoritmo    : {algorithm_name}")
    if path:
        print(f"  Camino       : {len(path) - 1} pasos")
        print(f"  Costo total  : {cost}")
    else:
        print("  Resultado    : NO se encontró solución")
    print(f"  Nodos expl.  : {explored_count}")
    print(f"  Tiempo       : {time_ms:.3f} ms")
    print(sep)
