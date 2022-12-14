import math
from dataclasses import dataclass
from functools import cached_property
from itertools import tee

from file import read_lines


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    @property
    def length(self):
        return (self.start - self.end).length

    def __contains__(self, point):
        return point in self.points

    @property
    def nodes(self):
        return {self.start, self.end}

    @cached_property
    def points(self):
        points = set()
        difference = self.end - self.start
        if abs(difference).x > abs(difference).y:
            for x in range(round(difference.length) + 1):
                if self.end.x >= self.start.x:
                    points.add(self.start + Point(x, 0))
                else:
                    points.add(self.start - Point(x, 0))
        else:
            for y in range(round(difference.length) + 1):
                if self.end.y >= self.start.y:
                    points.add(self.start + Point(0, y))
                else:
                    points.add(self.start - Point(0, y))
        return points


def parse_points(lines):
    for line in lines:
        split = line.split(" -> ")
        string_points = [tuple(p.split(",")) for p in split]
        points = [Point(*(int(c) for c in p)) for p in string_points]
        yield from (p for p in points)
        yield None


def construct_segments(points):
    starts, ends = tee(points, 2)
    _ = next(ends)
    for start, end in zip(starts, ends):
        if start is None:
            continue
        if end is None:
            yield None
            continue
        yield Segment(start, end)


@dataclass(frozen=True)
class Line:
    segments: list[Segment]

    def __contains__(self, point):
        return point in self.points

    @cached_property
    def nodes(self):
        nodes = set()
        for segment in self.segments:
            nodes.update(segment.nodes)
        return nodes

    @cached_property
    def points(self):
        points = set()
        for segment in self.segments:
            points.update(segment.points)
        return points


@dataclass(frozen=True)
class Scan:
    lines: list[Line]

    def __contains__(self, point):
        return point in self.points

    @cached_property
    def nodes(self):
        nodes = set()
        for line in self.lines:
            nodes.update(line.nodes)
        return nodes

    @cached_property
    def points(self):
        points = set()
        for line in self.lines:
            points.update(line.points)
        return points

    @cached_property
    def upper_left(self):
        x = min(n.x for n in self.nodes)
        y = min(n.y for n in self.nodes)
        return Point(x, y)

    @cached_property
    def lower_right(self):
        x = max(n.x for n in self.nodes)
        y = max(n.y for n in self.nodes)
        return Point(x, y)

    def __str__(self):
        lines = []
        for y in range(self.upper_left.y, self.lower_right.y + 1):
            line = ""
            for x in range(self.upper_left.x, self.lower_right.x + 1):
                if Point(x, y) in self:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        return "\n".join(lines)


def construct_lines(segments):
    line_segments = []
    for segment in segments:
        if segment is None:
            yield Line(line_segments)
            line_segments = []
            continue
        line_segments.append(segment)


def in_abyss(scan, position):
    return position.x < scan.upper_left.x or position.x > scan.lower_right.x or position.y > scan.lower_right.y


def get_resting_sand(scan, start):
    resting_sand = set()
    position = start
    while not in_abyss(scan, position):
        down = position - Point(0, -1)
        if down not in scan and down not in resting_sand:
            position = down
            continue
        diagonally_left = position - Point(1, -1)
        if diagonally_left not in scan and diagonally_left not in resting_sand:
            position = diagonally_left
            continue
        diagonally_right = position - Point(-1, -1)
        if diagonally_right not in scan and diagonally_right not in resting_sand:
            position = diagonally_right
            continue
        resting_sand.add(position)
        if position == start:
            break
        position = start
    return resting_sand


def main():
    text_lines = read_lines("data/day14.txt")
    points = parse_points(text_lines)
    segments = construct_segments(points)
    lines = list(construct_lines(segments))
    lower_edge = max(n.y for l in lines for n in l.nodes)
    floor = Line([Segment(Point(0, lower_edge + 2), Point(1_0000, lower_edge + 2))])
    lines += [floor]
    scan = Scan(lines)
    resting_sand = get_resting_sand(scan, start=Point(500, 0))
    print(f"{len(resting_sand)} units of sand came to rest")


if __name__ == "__main__":
    main()
