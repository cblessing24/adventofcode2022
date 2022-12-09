with open("data/day6.txt", "r") as file:
    puzzle_input = file.readline()


class Buffer:
    def __init__(self, length):
        self.length = length
        self._buffer = []

    def append(self, value):
        self._buffer.append(value)
        while len(self._buffer) > self.length:
            del self._buffer[0]

    def __iter__(self):
        return iter(self._buffer)


if __name__ == "__main__":
    length = 14
    buffer = Buffer(length=length)
    for i, char in enumerate(puzzle_input):
        buffer.append(char)
        if len(set(buffer)) == length:
            print(f"Start-of-packet marker '{''.join(buffer)}' received after {i + 1} characters")
            break
