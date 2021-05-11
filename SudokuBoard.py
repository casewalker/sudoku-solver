from SudokuValue import SVal


class Board:
    """A board of Sudoku values."""

    def __init__(self, empty=False):
        """Create a board with all new SVals (unless specified to be instantiated as empty)."""
        if empty:
            self.board = []
        else:
            self.board = [
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()],
                [SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal(), SVal()]
            ]

    def deep_copy(self):
        """Return a copy of this board."""
        new_board = Board(empty=True)
        for line in self.board:
            new_line = []
            new_board.board.append(new_line)
            for val in line:
                new_line.append(val.deep_copy())
        return new_board

    def num_possible(self, row, col):
        """Return the number of possible values for the square at (row, col)."""
        return self.board[row][col].num_possible()

    def is_set(self, row, col):
        """Return whether the square at (row, col) is set."""
        return self.board[row][col].is_set()

    def set_value(self, row, col, value):
        """Set the value for the square at (row, col)."""
        self.board[row][col].set_value(value)

    def get_minimal_possibilities_square(self):
        """Return (row, col) of a square with minimal remaining possibilities."""
        min_possible = 10
        (min_r, min_c) = (-1, -1)
        for r, line in enumerate(self.board):
            for c, val in enumerate(line):
                if not val.is_set() and val.num_possible() < min_possible:
                    min_possible = val.num_possible()
                    (min_r, min_c) = (r, c)
        return min_r, min_c

    def get_possible_boards(self, row, col):
        """Return a list of boards created by filling the specified square with each of its possibilities in turn, and
        then removing impossible values from the rest of the board.
        """
        possible_boards = []
        possible_vals = self.board[row][col].get_possible()
        for val in possible_vals:
            new_board = self.deep_copy()
            new_board.board[row][col].set_value(val)
            new_board._remove_possible_row(row, val)
            new_board._remove_possible_col(col, val)
            new_board._remove_possible_inner_square(row, col, val)
            possible_boards.append(new_board)
        return possible_boards

    def fix_board(self):
        """Account for all of the existing values on an input board in the other val possibilities."""
        for r, line in enumerate(self.board):
            for c, val in enumerate(line):
                if val.is_set():
                    self._remove_possible_row(r, val.value)
                    self._remove_possible_col(c, val.value)
                    self._remove_possible_inner_square(r, c, val.value)

    def is_complete(self):
        """Check if all values are set, then the board is complete."""
        for line in self.board:
            for val in line:
                if not val.is_set():
                    return False
        return True

    def contains_empty(self):
        """Check if the board contains any vals with an empty list of possibilities, thus indicating a "dead end."
        """
        for line in self.board:
            for val in line:
                if not val.is_set() and val.num_possible() == 0:
                    return True
        return False

    def _remove_possible_row(self, idx, value):
        """Remove the specified value from possible values for all SVals in a row."""
        for val in self.board[idx]:
            val.remove_possible(value)

    def _remove_possible_col(self, idx, value):
        """Remove the specified value from possible values for all SVals in a column. Needs to iterate over all rows."""
        for row in self.board:
            row[idx].remove_possible(value)

    def _remove_possible_inner_square(self, row, col, value):
        """Remove the specified value from the list of possible values for all SVals in the 3x3 Sudoku sub-square.

        Needs to determine the sub-square upper left corner, and then iterate over all contained values.
         * Upper left corner Row = ((row / 3) * 3)
         * Upper left corner Col = ((col / 3) * 3)
        """
        upper_left_r = row // 3 * 3
        upper_left_c = col // 3 * 3
        for r in range(upper_left_r, upper_left_r + 3):
            for c in range(upper_left_c, upper_left_c + 3):
                self.board[r][c].remove_possible(value)

    def __repr__(self):
        """String representation of the board.

        Desired output:
          +---------+---
          | 1  2  3 | 4 ...
          | 4  5  6 | 7 ...
          | 7  8  9 | 1 ...
          +---------+---
          | 2  3  4 | 5 ...
          ...

        If a square is not set, just include a space.
        """
        r_spacer = "    " + ("+" + ("---" * 3)) * 3 + "+"
        c_spacer = "|"

        string = ""
        for l_idx, line in enumerate(self.board):
            if l_idx % 3 == 0:
                string += r_spacer + "\n"
            for v_idx, val in enumerate(line):
                if v_idx % 3 == 0:
                    if v_idx == 0:
                        string += "    "
                    string += c_spacer
                string += " " + str(val) + " "
            string += c_spacer + "\n"
        string += r_spacer
        return string
