from dataclasses import dataclass, field
from enum import Enum


def read_lines(filename):
    with open(filename, "r") as file:
        for line in file.readlines():
            yield line.strip()


class State(Enum):
    PENDING = 1
    RUNNING = 2
    FINISHED = 3


@dataclass
class Instruction:
    n_cycles: int
    value: int
    state: State = State.PENDING
    _i_cycle: int = field(default=0, init=False)

    def start(self):
        if self.state is not State.PENDING:
            raise RuntimeError
        self.state = State.RUNNING

    def advance(self):
        if self.state is not State.RUNNING:
            raise RuntimeError
        self._i_cycle += 1
        if self._i_cycle == self.n_cycles:
            self.state = State.FINISHED


def parse_lines(lines):
    for line in lines:
        try:
            _, raw_value = line.split(" ")
            yield Instruction(n_cycles=2, value=int(raw_value))
        except ValueError:
            yield Instruction(n_cycles=1, value=0)


def compute_register_values(instructions, n_cycles, initial):
    instruction = next(instructions)
    for i_cycle in range(1, n_cycles + 1):
        yield i_cycle, initial
        if instruction.state is State.PENDING:
            instruction.start()
        if instruction.state is State.RUNNING:
            instruction.advance()
        if instruction.state is State.FINISHED:
            initial += instruction.value
            instruction = next(instructions)


def compute_signal_strength(register_values):
    for i_cycle, register_value in register_values:
        yield i_cycle, i_cycle * register_value


def filter_signal_strengths(signal_strengths, cycles):
    for i_cycle, signal_strength in signal_strengths:
        if i_cycle in cycles:
            yield i_cycle, signal_strength


if __name__ == "__main__":
    cycles = [20, 60, 100, 140, 180, 220]
    lines = read_lines("data/day10.txt")
    instructions = parse_lines(lines)
    register_values = compute_register_values(instructions, n_cycles=max(cycles), initial=1)
    signal_strengths = compute_signal_strength(register_values)
    filtered_signal_strengths = filter_signal_strengths(signal_strengths, cycles=cycles)
    sum_signal_strengts = sum(s[1] for s in filtered_signal_strengths)
    print(f"The sum of the signal strengths is {sum_signal_strengts}")
