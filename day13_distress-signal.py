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


def order_packets(packets):
    ordered = [next(packets)]
    for packet in packets:
        if packet is None:
            continue
        i = 0
        for ordered_packet in ordered:
            if not check_order(packet, ordered_packet):
                break
            i += 1
        ordered.insert(i, packet)
    return ordered


if __name__ == "__main__":
    lines = read_lines("data/day13.txt")
    packets = parse_packets(lines)
    divider = [[[2]], [[6]]]
    key = 1
    for i, packet in enumerate(reversed(order_packets(chain(packets, divider))), start=1):
        if packet in divider:
            key *= i
    print(key)
