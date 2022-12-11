def read_lines(filename):
    with open(filename) as file:
        for line in file.readlines():
            yield line.strip()
