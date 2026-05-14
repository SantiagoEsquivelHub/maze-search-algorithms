"""
maze.py — Representación del laberinto.

Formato de archivo .txt:
  #  -> pared
  ' ' -> celda libre
  S  -> posición inicial
  E  -> posición de salida (meta)
"""

from typing import List, Optional, Tuple


class Maze:
    def __init__(self, filepath: str):
        self.grid = []
        self.start = None
        self.goal = None
        self._load(filepath)

    def _load(self, filepath: str):
        with open(filepath, "r") as f:
            for row_idx, line in enumerate(f):
                row = list(line.rstrip("\n"))
                for col_idx, cell in enumerate(row):
                    if cell == "S":
                        self.start = (row_idx, col_idx)
                    elif cell == "E":
                        self.goal = (row_idx, col_idx)
                self.grid.append(row)

        if self.start is None or self.goal is None:
            raise ValueError(f"El laberinto '{filepath}' debe contener 'S' (inicio) y 'E' (meta).")

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return max(len(row) for row in self.grid)

    def is_valid(self, pos: Tuple[int, int]) -> bool:
        """Retorna True si la posición es transitable (no es pared ni está fuera de rango)."""
        row, col = pos
        if row < 0 or row >= self.rows:
            return False
        if col < 0 or col >= len(self.grid[row]):
            return False
        return self.grid[row][col] != "#"

    def neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Retorna las posiciones vecinas válidas (arriba, abajo, izquierda, derecha)."""
        row, col = pos
        candidates = [
            (row - 1, col),  # arriba
            (row + 1, col),  # abajo
            (row, col - 1),  # izquierda
            (row, col + 1),  # derecha
        ]
        return [p for p in candidates if self.is_valid(p)]

    def step_cost(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> int:
        """Costo de moverse de from_pos a to_pos (uniforme = 1)."""
        return 1
