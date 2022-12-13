from itertools import chain

from file import read_lines


def parse_packets(lines):
    for line in lines:
        if line == "":
            yield None
            continue
        yield eval(line)


def create_pairs(packets):
    pair = []
    for packet in chain(packets, [None]):
        if packet is None:
            yield tuple(pair)
            pair = []
            continue
        pair.append(packet)


def check_order(left, right):
    in_order = None
    for left_element, right_element in zip(left, right):
        if isinstance(left_element, list) and isinstance(right_element, list):
            in_order = check_order(left_element, right_element)
        if isinstance(left_element, int) and isinstance(right_element, list):
            in_order = check_order([left_element], right_element)
        if isinstance(left_element, list) and isinstance(right_element, int):
            in_order = check_order(left_element, [right_element])
        if isinstance(left_element, int) and isinstance(right_element, int):
            if left_element < right_element:
                in_order = True
            if left_element > right_element:
                in_order = False
        if in_order is not None:
            break
    if in_order is None:
        if len(left) < len(right):
            in_order = True
        if len(left) > len(right):
            in_order = False
    return in_order


def check_orders(pairs):
    for left, right in pairs:
        yield check_order(left, right)


if __name__ == "__main__":
    lines = read_lines("data/day13.txt")
    packets = parse_packets(lines)
    pairs = create_pairs(packets)
    in_orders = check_orders(pairs)
    sum_in_order = sum(i + 1 for i, b in enumerate(in_orders) if b)
    print(sum_in_order)
