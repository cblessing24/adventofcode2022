import math
import operator
from dataclasses import dataclass
from enum import Enum

from file import read_lines


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


def get_head_positions(directions, initial):
    position = initial
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


def get_knot_positions(earlier_knot_positions, initial):
    current_knot_position = initial
    for earlier_knot_position in earlier_knot_positions:
        difference = earlier_knot_position - current_knot_position
        if difference.length < 2.0:
            yield current_knot_position
            continue
        current_knot_position = current_knot_position + difference - difference.unit
        yield current_knot_position


def get_tail_positions(head_positions, n_knots, initial):
    knot_positions = head_positions
    for _ in range(n_knots - 1):
        knot_positions = get_knot_positions(knot_positions, initial=initial)
    for knot_position in knot_positions:
        yield knot_position


def get_tail_positions_count(filename, n_knots, initial):
    lines = read_lines(filename)
    directions = parse_directions(lines)
    head_positions = get_head_positions(directions, initial=initial)
    tail_positions = get_tail_positions(head_positions, n_knots=n_knots, initial=initial)
    return len(set(tail_positions))


if __name__ == "__main__":
    for n_knots in [2, 10]:
        n_tail_positions = get_tail_positions_count("data/day9.txt", n_knots=n_knots, initial=Vector(0, 0))
        print(f"The tail of a rope with {n_knots} knots visited {n_tail_positions} positions at least once")
