"""
dfs.py — Búsqueda por Profundidad (Depth-First Search).

Estrategia: explora tan profundo como sea posible antes de retroceder.
Garantías:
  - Completo: sí (con detección de ciclos en espacios finitos)
  - Óptimo: NO (puede encontrar un camino más largo que el óptimo)
Estructura de datos: pila LIFO (lista de Python)
"""

import time
from typing import List, Optional, Tuple

from src.maze import Maze


def dfs(maze: Maze) -> Tuple[Optional[List], int, int, float]:
    """
    Ejecuta DFS sobre el laberinto.

    Returns:
        path          : lista de posiciones (fila, col) desde S hasta E, o None si no hay solución.
        cost          : número de pasos del camino encontrado.
        explored_count: cantidad de nodos expandidos.
        time_ms       : tiempo de ejecución en milisegundos.
    """
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # Cada elemento de la pila: (posición_actual, camino_hasta_aquí)
    stack = [(start, [start])]

    visited = {start}
    explored_count = 0

    while stack:
        current, path = stack.pop()
        explored_count += 1

        if current == goal:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            cost = len(path) - 1
            return path, cost, explored_count, elapsed_ms

        for neighbor in maze.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return None, 0, explored_count, elapsed_ms
