from dataclasses import dataclass
from itertools import tee

from file import read_lines


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

    def __abs__(self):
        return Coordinate(abs(self.x), abs(self.y))

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    @property
    def sum(self):
        return self.x + self.y


def parse_sensors(lines):
    for line in lines:
        x = int(line.split("x")[1].split(",")[0][1:])
        y = int(line.split("y")[1].split(":")[0][1:])
        yield Coordinate(x, y)


def parse_beacons(lines):
    for line in lines:
        x = int(line.split("x")[2].split(",")[0][1:])
        y = int(line.split("y")[2][1:])
        yield Coordinate(x, y)


def manhattan_distance(coordinate1, coordinate2):
    return abs(coordinate1 - coordinate2).sum


def compute_covered_distances(sensors, beacons):
    for sensor, beacon in zip(sensors, beacons):
        yield manhattan_distance(sensor, beacon)


def compute_covered_coordinates(sensors, distances):
    for sensor, distance in zip(sensors, distances):
        for difference in range(1, distance + 1):
            yield sensor + Coordinate(difference, 0)
            yield sensor - Coordinate(difference, 0)
            yield sensor + Coordinate(0, difference)
            yield sensor - Coordinate(0, difference)
        for x_difference in range(1, distance):
            y_difference = distance - x_difference
            yield sensor + Coordinate(x_difference, y_difference)
            yield sensor - Coordinate(x_difference, y_difference)
            yield sensor + Coordinate(-x_difference, y_difference)
            yield sensor - Coordinate(-x_difference, y_difference)


def is_covered(coordinate, sensors, distances):
    is_covered = False
    for sensor, distance in zip(sensors, distances):
        is_covered = manhattan_distance(coordinate, sensor) <= distance
        if is_covered:
            break
    return is_covered


def main():
    lines1, lines2 = tee(read_lines("data/day15.txt"), 2)
    sensors = list(parse_sensors(lines1))
    beacons = list(parse_beacons(lines2))
    distances = list(compute_covered_distances(sensors, beacons))
    left_edge = min(s.x - d for s, d in zip(sensors, distances))
    right_edge = max(s.x + d for s, d in zip(sensors, distances))
    covered = []
    for i, x in enumerate(range(left_edge, right_edge + 1)):
        if i % 100_000 == 0:
            print(f"{i=:,}")
        coordinate = Coordinate(x, 2_000_000)
        if coordinate in beacons:
            continue
        covered.append(is_covered(coordinate, sensors, distances))
    print(f"{sum(covered)=:,}")


if __name__ == "__main__":
    main()
