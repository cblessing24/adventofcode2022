class Grid:
    def __init__(self, n_rows, n_cols, initial=0):
        self._grid = [[initial for _ in range(n_cols)] for _ in range(n_rows)]

    def __getitem__(self, position):
        i_row, i_col = position
        return self._grid[i_row][i_col]

    def __setitem__(self, position, value):
        i_row, i_col = position
        self._grid[i_row][i_col] = value

    @property
    def shape(self):
        return (len(self._grid), len(self._grid[0]))

    @classmethod
    def from_iterable(cls, iterable):
        raw = [list(row) for row in iterable]
        assert len({len(row) for row in raw}) == 1, "Rows have different lengths"
        grid = Grid(len(raw), len(raw[0]))
        for i_row, row in enumerate(raw):
            for i_col, value in enumerate(row):
                grid[i_row, i_col] = value
        return grid

    @property
    def rows(self):
        for row in self._grid:
            yield row

    @property
    def cols(self):
        for i_col in range(self.shape[1]):
            yield [row[i_col] for row in self._grid]

    def sum(self):
        return sum(sum(row) for row in self._grid)

    def max(self):
        return max(max(row) for row in self._grid)


trees = []
with open("data/day8.txt", "r") as file:
    for line in file.readlines():
        trees.append([int(s) for s in line.strip()])
trees = Grid.from_iterable(trees)


def visible_trees(view):
    tallest_tree = -1
    for i, tree in enumerate(view):
        if tree > tallest_tree:
            yield i
            tallest_tree = tree


def bidirectional_visible_trees(view):
    yield from visible_trees(view)
    for i in visible_trees(reversed(view)):
        yield -i - 1


visibility = Grid(*trees.shape, initial=False)
for i_row, row in enumerate(trees.rows):
    for i_col in bidirectional_visible_trees(row):
        visibility[i_row, i_col] = True
for i_col, col in enumerate(trees.cols):
    for i_row in bidirectional_visible_trees(col):
        visibility[i_row, i_col] = True
print(f"{visibility.sum()} trees are visible from outside the grid")


def compute_scenic_score(tree, view):
    visible_trees = 0
    for other_tree in view:
        visible_trees += 1
        if other_tree >= tree:
            break
    return visible_trees


scenic_score = Grid(*trees.shape, initial=1)
for i_row, row in enumerate(trees.rows):
    for i_col, tree in enumerate(row):
        scenic_score[i_row, i_col] *= compute_scenic_score(tree, row[i_col + 1 :])
        scenic_score[i_row, i_col] *= compute_scenic_score(tree, reversed(row[:i_col]))
for i_col, col in enumerate(trees.cols):
    for i_row, tree in enumerate(col):
        scenic_score[i_row, i_col] *= compute_scenic_score(tree, col[i_row + 1 :])
        scenic_score[i_row, i_col] *= compute_scenic_score(tree, reversed(col[:i_row]))
print(f"The highest scenic score possible for any tree is: {scenic_score.max()}")
