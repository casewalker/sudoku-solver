class SVal:
    """This class represents a square in Sudoku. It either has 1 assigned value, or a set of possible values."""

    def __init__(self):
        """Start with no set value and all possible values."""
        self.possible_vals = [x for x in range(1, 10)]
        self.value = None

    def deep_copy(self):
        """Create a deep copy."""
        new_s_vals = SVal()
        if self.value is not None:
            new_s_vals.value = self.value
        else:
            new_s_vals.possible_vals = self.possible_vals[:]
        return new_s_vals

    def set_value(self, value):
        """Set the value."""
        self.value = value

    def remove_possible(self, value):
        """Remove a possible value."""
        if value in self.possible_vals:
            self.possible_vals.remove(value)

    def is_set(self):
        """Check if this value is set."""
        return self.value is not None

    def num_possible(self):
        """Return the number of possibilities this square has."""
        return len(self.possible_vals)

    def get_possible(self):
        """Return possible values for this square."""
        return self.possible_vals

    def __str__(self):
        """String for an SVals."""
        return str(self.value) if self.is_set() else " "
