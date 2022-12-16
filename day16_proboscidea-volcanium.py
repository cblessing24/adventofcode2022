from __future__ import annotations

import cProfile
import re
from collections import deque
from dataclasses import dataclass
from itertools import pairwise, permutations

from file import read_lines


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    destinations: frozenset[str]


def parse_valves(lines):
    pattern = re.compile(
        r"Valve (?P<name>[A-Z]{2}) has flow rate=(?P<flow_rate>\d+); "
        r"tunnels* leads* to valves* (?P<destinations>(?:[A-Z]{2}, )*[A-Z]{2})"
    )
    for line in lines:
        match = pattern.match(line)
        assert match
        yield Valve(
            match.group("name"), int(match.group("flow_rate")), frozenset(match.group("destinations").split(", "))
        )


def compute_valve_distances(valves, origin):
    queue = deque()
    queue.append((origin, 0))
    distances = {origin.name: 0}
    while queue:
        valve, distance = queue.popleft()
        for destination_name in valve.destinations:
            destination = next(v for v in valves if v.name == destination_name)
            if destination_name not in distances:
                distances[destination_name] = distance + 1
                queue.append((destination, distance + 1))
    return distances


def compute_distances(valves):
    distances = {}
    for origin in valves:
        distances[origin.name] = compute_valve_distances(valves, origin)
    return distances


def find_functional_valves(valves):
    for valve in valves:
        if valve.flow_rate == 0:
            continue
        yield valve


def find_paths(valves, origin):
    assert origin not in valves
    for path_length in range(1, len(valves) + 1):
        for path in permutations(valves, path_length):
            yield [origin] + list(path)


def filter_paths_by_time(paths, distances, limit):
    for path in paths:
        time = 0
        for origin, destination in pairwise(path):
            time += distances[origin][destination] + 1
            if time > limit:
                break
        else:
            yield path


def compute_flow(paths, distances, limit):
    for path in paths:
        flow = 0
        remaining = limit
        for origin, destination in pairwise(path):
            remaining -= distances[origin.name][destination.name] + 1
            if remaining < 0:
                break
            flow += destination.flow_rate * remaining
        yield flow


def main():
    lines = read_lines("data/day16.txt")
    valves = list(parse_valves(lines))
    distances = compute_distances(valves)
    functional_valves = list(find_functional_valves(valves))
    origin = next(v for v in valves if v.name == "AA")
    paths = find_paths(functional_valves, origin)
    limit = 30
    flows = compute_flow(paths, distances, limit=limit)
    max_flow = 0
    for i, flow in enumerate(flows):
        if i % 100_000 == 0:
            print(f"{i=:,}, {max_flow=:,}")
        if flow <= max_flow:
            continue
        max_flow = flow
    print(f"The most pressure that can be released is {max_flow:,}")


if __name__ == "__main__":
    cProfile.run("main()", "stats")
