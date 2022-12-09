from abc import ABC, abstractmethod


class Element(ABC):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

    @property
    @abstractmethod
    def size(self):
        pass

    def __repr__(self):
        return f"Element(name={self.name}, parent={self.parent})"


class File(Element):
    def __init__(self, name, parent, size):
        super().__init__(name, parent)
        self._size = size

    @property
    def size(self):
        return self._size


class Directory(Element):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self._elements = []

    @property
    def size(self):
        return sum(e.size for e in self._elements)

    def add(self, element):
        self._elements.append(element)

    @property
    def directories(self):
        directories = (e for e in self._elements if isinstance(e, Directory))
        for directory in directories:
            yield directory
            yield from directory.directories


root_directory = Directory("/")
current_directory = root_directory
with open("data/day7.txt", "r") as file:
    for line in file:
        split_line = line.strip().split(" ")
        if split_line[0] == "dir":
            continue
        if split_line[0].isnumeric():
            size, filename = split_line
            current_directory.add(File(filename, current_directory, int(size)))
        if split_line[0] == "$":
            if split_line[1] == "ls":
                continue
            destination = split_line[2]
            if destination == "..":
                current_directory = current_directory.parent
                continue
            destination_directory = Directory(destination, parent=current_directory)
            current_directory.add(destination_directory)
            current_directory = destination_directory

cap = 100_000
total = sum(d.size for d in root_directory.directories if d.size < cap)
print(f"The total size of all directories with a size of at most {cap:,} is {total:,}")

required = 30_000_000 - (70_000_000 - root_directory.size)
smallest = min(d.size for d in root_directory.directories if d.size > required)
print(f"The smallest directory that has the required size of {required:,} has a size of {smallest:,}")
