from enum import Enum

class Square(Enum):
    UNINHABITED = 0
    INHABITED = 1

class Board:
    """A board for the challenge.  Indices 1-x are used for the board.

An extra surrounding border is included."""

    @staticmethod
    def from_file(f):
        """Gets a Board from a file object."""
        pass # TODO implement me

    def __init__(self, squares):
        self.squares = squares

    def status(self, row, col):
        """Returns the CURRENT status of square with row row and column col."""
        return self.squares[row][col]

    def next_status(self, row, col):
        """Returns the status of square [row, col] in the next turn."""
        pass # TODO implement me

    def update(self):
        """Updates the board, setting every square to its next state."""
        pass # TODO implement me
