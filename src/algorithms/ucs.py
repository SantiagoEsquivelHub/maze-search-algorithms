"""
ucs.py — Búsqueda de Costo Uniforme (Uniform Cost Search).

Estrategia: expande siempre el nodo de menor costo acumulado g(n).
Garantías:
  - Completo: sí
  - Óptimo: sí (encuentra el camino de menor costo)
Estructura de datos: cola de prioridad (heapq), ordenada por costo acumulado.

Nota: en este laberinto todos los pasos cuestan 1, por lo que UCS y BFS
producirán el mismo camino óptimo, pero UCS es generalizable a costos variables.
"""

import heapq
import time
from typing import List, Optional, Tuple

from src.maze import Maze


def ucs(maze: Maze) -> Tuple[Optional[List], int, int, float]:
    """
    Ejecuta UCS sobre el laberinto.

    Returns:
        path          : lista de posiciones (fila, col) desde S hasta E, o None si no hay solución.
        cost          : costo total acumulado del camino encontrado.
        explored_count: cantidad de nodos expandidos.
        time_ms       : tiempo de ejecución en milisegundos.
    """
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # Heap: (costo_acumulado, posición_actual, camino_hasta_aquí)
    heap = [(0, start, [start])]

    # Mejor costo conocido para cada posición
    best_cost = {start: 0}
    explored_count = 0

    while heap:
        cost, current, path = heapq.heappop(heap)
        explored_count += 1

        if current == goal:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return path, cost, explored_count, elapsed_ms

        # Si ya encontramos un camino más barato a este nodo, ignorar
        if cost > best_cost.get(current, float("inf")):
            continue

        for neighbor in maze.neighbors(current):
            new_cost = cost + maze.step_cost(current, neighbor)
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor, path + [neighbor]))

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return None, 0, explored_count, elapsed_ms
