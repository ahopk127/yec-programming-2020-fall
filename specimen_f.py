from enum import Enum

class Square(Enum):
    UNINHABITED = 0
    INFECTED = 1

class Board:
    """A board for the challenge.  Indices 1-x are used for the board.

An extra surrounding border is included."""

    @staticmethod
    def from_file(f):
        """Gets a Board from a file object."""
        pass # TODO implement me

    def __init__(self, squares):
        """Gets the Board.

"squares" is the array of squares in the board.  It should be a rectangular array
of Square objects."""
        self.squares = squares

    def status(self, row, col):
        """Returns the CURRENT status of square with row row and column col."""
        return self.squares[row][col]

    def size(self):
        """Returns the size of the board.

The returned value is a 2-element tuple (# rows, # columns)."""
        return (len(self.squares), len(self.squares[0]))

    def next_status(self, row, col):
        """Returns the status of square [row, col] in the next turn."""

        # Check all of the squares around and count the # of infected
        infected = 0
        for r in range(row - 1, row + 2):

            # check for invalid row, if row is invalid continue
            if r < 0 or r >= self.size[0]:
                continue

            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    # don't count the square itself, only the neighbours
                    continue

                # check for invalid column, if col is invalid continue
                elif c < 0 or r >= self.size[1]:
                    continue

                if self.status(r, c) == Square.INFECTED:
                    infected += 1

        # use the number of infected neighbours to find next state
        # if square is INFECTED and has <3 infected neighbours it will become
        # UNINHABITED.
        # if square is UNINHABITED and has >= 3 infected neighbours it will
        # become INFECTED.
        if self.status(row, col) == Square.UNINHABITED:
            if infected >= 3:
                return Square.INFECTED # new infection
            else:
                return Square.UNINHABITED # no change
        elif self.status(row, col) == Square.INFECTED:
            if infected < 3:
                return Square.UNINHABITED # death
            else:
                return Square.INFECTED # no change
        else: # should not be able to happen, throw error
            assert False

    def update(self):
        """Updates the board, setting every square to its next state."""
        pass # TODO implement me
