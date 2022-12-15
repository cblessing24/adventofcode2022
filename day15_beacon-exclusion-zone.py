from dataclasses import dataclass
from itertools import pairwise, tee

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


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    @property
    def length(self):
        return self.end - self.start


def compute_covered_ranges(sensors, distances, y):
    for sensor, distance in zip(sensors, distances):
        vertical_distance = manhattan_distance(sensor, Coordinate(sensor.x, y))
        if vertical_distance > distance:
            continue
        horizontal_distance = distance - vertical_distance
        left_border = Coordinate(sensor.x, y) - Coordinate(horizontal_distance, 0)
        right_border = Coordinate(sensor.x, y) + Coordinate(horizontal_distance, 0)
        assert manhattan_distance(left_border, sensor) == distance
        assert manhattan_distance(right_border, sensor) == distance
        yield Range(left_border.x, right_border.x)


def merge_ranges(range1, range2):
    merged = None
    if range1.end + 1 >= range2.start and range1.start <= range2.start:
        if range2.end <= range1.end:
            merged = range1
        else:
            merged = Range(range1.start, range2.end)
    if range2.end + 1 >= range1.start and range2.start <= range1.start:
        if range1.end <= range2.end:
            merged = range2
        else:
            merged = Range(range2.start, range1.end)
    return merged


def reduce_ranges(ranges):
    ranges = iter(sorted(ranges, key=lambda r: (r.start, r.end)))
    current = next(ranges)
    merged_ranges = []
    for range_ in ranges:
        merged_range = merge_ranges(current, range_)
        if not merged_range:
            merged_ranges.append(current)
            current = next(ranges)
            continue
        current = merged_range
    merged_ranges.append(current)
    return merged_ranges


def find_beacon(sensors, distances, vertical_search_space, horizontal_search_space):
    for y in range(vertical_search_space[0], vertical_search_space[1] + 1):
        ranges = reduce_ranges(compute_covered_ranges(sensors, distances, y))
        for range1, range2 in pairwise(ranges):
            between_range = Range(range1.end + 1, range2.start - 1)
            if between_range.start < horizontal_search_space[0] or between_range.end > horizontal_search_space[1]:
                continue
            assert between_range.length == 0
            return Coordinate(between_range.start, y)


def main():
    lines1, lines2 = tee(read_lines("data/day15.txt"), 2)
    sensors = list(parse_sensors(lines1))
    beacons = list(parse_beacons(lines2))
    distances = list(compute_covered_distances(sensors, beacons))
    beacon = find_beacon(sensors, distances, (0, 4_000_000), (0, 4_000_000))
    assert beacon
    frequency = beacon.x * 4_000_000 + beacon.y
    print(f"The tuning frequency is {frequency:,}")


if __name__ == "__main__":
    main()
