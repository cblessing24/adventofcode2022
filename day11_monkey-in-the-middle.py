import operator
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass
from math import prod
from typing import Callable

from file import read_lines


def parse_lines(lines):
    observation = []
    for line in lines:
        if line == "":
            yield observation
            observation = []
            continue
        observation.append(line)
    yield observation


class Parser(ABC):

    _next_parser = None

    def set_next(self, parser):
        self._next_parser = parser
        return parser

    @abstractmethod
    def parse(self, line):
        if self._next_parser:
            return self._next_parser.parse(line)
        return None


class NumberParser(Parser):
    def parse(self, line):
        if line.startswith("Monkey"):
            _, raw_number = line.split(" ")
            return "number", int(raw_number[0])
        return super().parse(line)


class StartingItemsParser(Parser):
    def parse(self, line):
        if line.startswith("Starting items"):
            _, raw_items = line.split(":")
            return "items", deque(int(i) for i in raw_items.split(", "))
        return super().parse(line)


class OperationParser(Parser):
    _operator_map = {"*": operator.mul, "+": operator.add}

    def parse(self, line):
        if line.startswith("Operation"):
            _, raw_operation = line.split(":")
            _, right_hand_side = raw_operation.split("=")
            _, op, right = right_hand_side.strip().split(" ")

            def operation(old):
                if right == "old":
                    return self._operator_map[op](old, old)
                return self._operator_map[op](old, int(right))

            return "operation", operation
        return super().parse(line)


class TestParser(Parser):
    def parse(self, line):
        if line.startswith("Test"):
            *_, raw_value = line.split(" ")
            return "test", int(raw_value)
        return super().parse(line)


class ConditionParser(Parser):
    def parse(self, line):
        if line.startswith("If"):
            _, raw_condition, *_, raw_value = line.split(" ")
            condition = raw_condition.split(":")[0]
            return condition, int(raw_value)
        return super().parse(line)


@dataclass
class Monkey:
    number: int
    items: deque[int]
    operation: Callable[[int], int]
    test: int
    true: int
    false: int
    n_inspections: int = 0

    def inspect(self, item):
        self.n_inspections += 1
        return self.operation(item)

    def decide(self, item):
        if item % self.test == 0:
            return self.true
        return self.false

    def catch(self, item):
        self.items.append(item)

    def __iter__(self):
        for item in self.items:
            yield item


def parse_observations(raw_observations):
    parser = NumberParser()
    parser.set_next(StartingItemsParser()).set_next(OperationParser()).set_next(TestParser()).set_next(
        ConditionParser()
    )
    for raw_observation in raw_observations:
        observation = {}
        for line in raw_observation:
            attribute, value = parser.parse(line)
            observation[attribute] = value
        yield Monkey(**observation)


def play_rounds(troop, n_rounds):
    for _ in range(n_rounds):
        for monkey in troop.values():
            while len(monkey.items):
                item = monkey.items.popleft()
                item = monkey.inspect(item)
                item = item // 3
                troop[monkey.decide(item)].catch(item)
        yield troop


if __name__ == "__main__":
    lines = read_lines("data/day11.txt")
    raw_observations = parse_lines(lines)
    monkeys = parse_observations(raw_observations)
    troop = {m.number: m for m in monkeys}
    troop = play_rounds(troop, 20)
    for troop in troop:
        pass
    print(prod(sorted([m.n_inspections for m in troop.values()])[-2:]))
