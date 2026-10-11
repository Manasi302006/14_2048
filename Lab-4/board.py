import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.last_move_points = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def _slide_line_with_points(line):
        values = [value for value in line if value]
        result = []
        points = 0
        index = 0
        while index < len(values):
            value = values[index]
            if index + 1 < len(values) and value == values[index + 1]:
                value *= 2
                points += value
                index += 1
            result.append(value)
            index += 1
        return result + [0] * (SIZE - len(result)), points

    @staticmethod
    def slide_line(line):
        return Board._slide_line_with_points(line)[0]

    def _move_rows(self, reverse=False):
        changed = False
        points = 0
        for r in range(SIZE):
            old = self.grid[r][:]
            line = list(reversed(old)) if reverse else old
            new, line_points = self._slide_line_with_points(line)
            if reverse:
                new.reverse()
            self.grid[r] = new
            changed |= old != new
            points += line_points
        self.last_move_points = points
        self.score += points
        return changed

    def _move_columns(self, reverse=False):
        changed = False
        points = 0
        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            line = list(reversed(old)) if reverse else old
            new, line_points = self._slide_line_with_points(line)
            if reverse:
                new.reverse()
            for r in range(SIZE):
                self.grid[r][c] = new[r]
            changed |= old != new
            points += line_points
        self.last_move_points = points
        self.score += points
        return changed

    def move_left(self):
        return self._move_rows()

    def move_right(self):
        return self._move_rows(reverse=True)

    def move_up(self):
        return self._move_columns()

    def move_down(self):
        return self._move_columns(reverse=True)

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def has_won(self):
        return any(value >= 2048 for row in self.grid for value in row)
