"""
bfs.py — Búsqueda por Amplitud (Breadth-First Search).

Estrategia: explora nivel por nivel desde el nodo inicial.
Garantías:
  - Completo: sí (siempre encuentra solución si existe)
  - Óptimo: sí (cuando todos los costos son iguales, como en este laberinto)
Estructura de datos: cola FIFO (collections.deque)
"""

import time
from collections import deque
from typing import List, Optional, Tuple

from src.maze import Maze


def bfs(maze: Maze) -> Tuple[Optional[List], int, int, float]:
    """
    Ejecuta BFS sobre el laberinto.

    Returns:
        path          : lista de posiciones (fila, col) desde S hasta E, o None si no hay solución.
        cost          : número de pasos del camino encontrado.
        explored_count: cantidad de nodos expandidos.
        time_ms       : tiempo de ejecución en milisegundos.
    """
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # Cada elemento de la cola: (posición_actual, camino_hasta_aquí)
    queue = deque()
    queue.append((start, [start]))

    visited = {start}
    explored_count = 0

    while queue:
        current, path = queue.popleft()
        explored_count += 1

        if current == goal:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            cost = len(path) - 1  # pasos = nodos - 1
            return path, cost, explored_count, elapsed_ms

        for neighbor in maze.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return None, 0, explored_count, elapsed_ms