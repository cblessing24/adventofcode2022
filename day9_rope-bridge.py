import math
import operator
from dataclasses import dataclass
from enum import Enum


def read_lines(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield line.strip()


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass(frozen=True)
class Command:
    direction: Direction
    distance: int


def parse_directions(lines):
    direction_map = {"U": Direction.UP, "R": Direction.RIGHT, "D": Direction.DOWN, "L": Direction.LEFT}
    for line in lines:
        direction, distance = line.split(" ")
        for _ in range(int(distance)):
            yield direction_map[direction]


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def unit(self):
        return Vector(round(self.x / self.length), round(self.y / self.length))


def get_head_positions(directions):
    position = Vector(0, 0)
    movements = {
        Direction.UP: (operator.add, Vector(0, 1)),
        Direction.RIGHT: (operator.add, Vector(1, 0)),
        Direction.DOWN: (operator.sub, Vector(0, 1)),
        Direction.LEFT: (operator.sub, Vector(1, 0)),
    }
    for direction in directions:
        op, vector = movements[direction]
        position = op(position, vector)
        yield position


def get_tail_positions(head_positions):
    tail_position = Vector(0, 0)
    for head_position in head_positions:
        difference = head_position - tail_position
        if difference.length < 2.0:
            yield tail_position
            continue
        tail_position = tail_position + difference - difference.unit
        yield tail_position


if __name__ == "__main__":
    lines = read_lines("data/day9.txt")
    directions = parse_directions(lines)
    head_positions = get_head_positions(directions)
    tail_positions = get_tail_positions(head_positions)
    print(f"The tail visited {len(set(tail_positions))} positions at least once")
