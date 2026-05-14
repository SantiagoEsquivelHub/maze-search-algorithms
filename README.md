# Maze search algorithms

Maze solving with BFS, DFS, UCS and A* search algorithms — Python

## Overview

A Python application that solves 2D grid mazes using four classic AI search algorithms. Each algorithm is evaluated on path quality (optimality), nodes explored, and execution time, allowing a direct comparison of their behavior on the same problem.

## Algorithms

| Algorithm | Optimal | Strategy |
|-----------|:-------:|----------|
| BFS | Yes | Explores level by level (FIFO queue) |
| DFS | No | Explores as deep as possible (LIFO stack) |
| UCS | Yes | Expands lowest cumulative cost first (min-heap) |
| A* | Yes | UCS + Manhattan heuristic `f = g + h` |

The **Manhattan distance** heuristic used by A* is admissible because it never overestimates the actual cost — obstacles can only increase the real path length, never reduce it.

## Project Structure

```
maze-search-algorithms/
├── src/
│   ├── maze.py              # Maze class: load, validate, expand neighbors
│   ├── visualizer.py        # Console output and stats
│   ├── main.py              # CLI entry point
│   └── algorithms/
│       ├── bfs.py
│       ├── dfs.py
│       ├── ucs.py
│       └── astar.py
└── mazes/
    ├── maze_small.txt       # 11 x 10
    ├── maze_medium.txt      # 21 x 20
    └── maze_large.txt       # 30 x 30
```

## Maze Format

Mazes are plain `.txt` files using these characters:

```
#   wall
    free cell (space)
S   start position
E   goal position
```

## Usage

```bash
# Single algorithm
python -m src.main --maze small --algorithm bfs
python -m src.main --maze medium --algorithm dfs
python -m src.main --maze large --algorithm astar

# Run all four and print a comparison table
python -m src.main --maze medium --algorithm all
```

**Arguments:**

| Argument | Values |
|---|---|
| `--maze` | `small` \| `medium` \| `large` \| `<path/to/file.txt>` |
| `--algorithm` | `bfs` \| `dfs` \| `ucs` \| `astar` \| `all` |

## Requirements

Python 3.6+. No external dependencies — only standard library (`collections`, `heapq`, `time`).
