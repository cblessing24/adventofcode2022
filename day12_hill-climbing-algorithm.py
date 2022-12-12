from collections import deque
from dataclasses import dataclass
from string import ascii_lowercase

from file import read_lines


@dataclass(frozen=True)
class Position:
    row: int
    column: int

    @property
    def neighbors(self):
        for value in [-1, 1]:
            yield Position(self.row + value, self.column)
            yield Position(self.row, self.column + value)


class Grid:
    def __init__(self, grid):
        self._grid = list(list(r) for r in grid)

    def __getitem__(self, position):
        if position.row < 0 or position.column < 0:
            raise IndexError
        return self._grid[position.row][position.column]

    def __setitem__(self, position, value):
        self._grid[position.row][position.column] = value

    def __str__(self):
        rows = ("".join(r) for r in self._grid)
        return "\n".join(rows)

    @property
    def size(self):
        return len(self._grid), len(self._grid[0])

    @property
    def positions(self):
        n_rows, n_columns = self.size
        for i_row in range(n_rows):
            for i_column in range(n_columns):
                yield Position(i_row, i_column)

    def find(self, token):
        return (p for p in self.positions if self[p] == token)


class HeightMap:
    def __init__(self, grid):
        self.grid = grid

    def get_possible_destinations(self, position):
        current_height = ascii_lowercase.index(self.grid[position])
        for destination in position.neighbors:
            try:
                raw_height = self.grid[destination]
            except IndexError:
                continue
            destination_height = ascii_lowercase.index(raw_height)
            if destination_height - current_height <= 1:
                yield destination


def compute_n_steps(height_map, start, end):
    queue = deque()
    explored = set()
    explored.add(start)
    queue.append(start)
    parents = {}
    while queue:
        current = queue.popleft()
        if current == end:
            n_steps = 0
            while True:
                try:
                    current = parents[current]
                except KeyError:
                    return n_steps
                n_steps += 1
        for destination in height_map.get_possible_destinations(current):
            if destination not in explored:
                explored.add(destination)
                parents[destination] = current
                queue.append(destination)


if __name__ == "__main__":
    lines = read_lines("data/day12.txt")
    grid = Grid(lines)
    start = next(grid.find("S"))
    end = next(grid.find("E"))
    grid[start] = "a"
    grid[end] = "z"
    n_steps = (compute_n_steps(HeightMap(grid), s, end) for s in grid.find("a"))
    print(f"The fewest number of steps is {min(v for v in n_steps if v is not None)}")
