from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            return False
        previous_grid = [row[:] for row in self.board.grid]
        previous_score = self.board.score
        changed = moves[key]()
        if changed:
            self.history = [(previous_grid, previous_score)]
            self.board.add_random_tile()
            self.best_score = max(self.best_score, self.board.score)
        return changed

    def undo(self):
        if not self.history:
            return False
        self.board.grid, self.board.score = self.history.pop()
        self.board.last_move_points = 0
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            if self.board.has_won():
                print("You reached 2048!")
                return
            if not self.board.can_move():
                print("No legal moves remain.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key == "u":
                if self.undo():
                    print("Undo restored the previous move.")
                else:
                    print("There is no move to undo.")
                continue
            if key not in ("w", "a", "s", "d"):
                print("Use W/A/S/D, U to undo, or Q to quit.")
                continue
            if self.move(key):
                if self.board.last_move_points:
                    print(
                        f"Move made. Merged tiles for "
                        f"{self.board.last_move_points} points."
                    )
                else:
                    print("Move made.")
            else:
                print("That move did not change the board.")
