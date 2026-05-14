"""
astar.py — Búsqueda A* con heurística Manhattan.

Estrategia: expande el nodo con menor f(n) = g(n) + h(n), donde:
  g(n) = costo acumulado desde el inicio hasta n
  h(n) = heurística admisible: distancia Manhattan hasta la meta

Heurística Manhattan:
  h(n) = |fila_n - fila_meta| + |col_n - col_meta|

  Justificación de admisibilidad: en un laberinto con movimientos
  horizontales/verticales de costo 1, la distancia Manhattan es el
  número mínimo de pasos posibles ignorando obstáculos. Por tanto,
  NUNCA sobreestima el costo real → h es admisible → A* es óptimo.

Garantías:
  - Completo: sí
  - Óptimo: sí (heurística admisible)
Estructura de datos: cola de prioridad (heapq), ordenada por f = g + h.
"""

import heapq
import time
from typing import List, Optional, Tuple

from src.maze import Maze


def _manhattan(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """Distancia Manhattan entre dos posiciones."""
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar(maze: Maze) -> Tuple[Optional[List], int, int, float]:
    """
    Ejecuta A* sobre el laberinto.

    Returns:
        path          : lista de posiciones (fila, col) desde S hasta E, o None si no hay solución.
        cost          : costo total acumulado del camino encontrado.
        explored_count: cantidad de nodos expandidos.
        time_ms       : tiempo de ejecución en milisegundos.
    """
    start_time = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # Heap: (f, g, posición_actual, camino_hasta_aquí)
    # Se incluye g como desempate para evitar comparar listas
    h0 = _manhattan(start, goal)
    heap = [(h0, 0, start, [start])]

    # Mejor costo g conocido para cada posición
    best_g = {start: 0}
    explored_count = 0

    while heap:
        f, g, current, path = heapq.heappop(heap)
        explored_count += 1

        if current == goal:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return path, g, explored_count, elapsed_ms

        # Descartar si ya procesamos este nodo con menor costo
        if g > best_g.get(current, float("inf")):
            continue

        for neighbor in maze.neighbors(current):
            new_g = g + maze.step_cost(current, neighbor)
            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                new_f = new_g + _manhattan(neighbor, goal)
                heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return None, 0, explored_count, elapsed_ms