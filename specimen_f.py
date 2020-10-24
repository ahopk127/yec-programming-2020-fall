from enum import Enum

# In the example for Part3, the outside of the testing grounds is not considered
# otherwise, a breach would occur at 4 hours (before the example ends!)
# and there would be more fission mass
# Setting BORDER_ENABLED to False simulates this
BORDER_ENABLED = True

# limit for how many hours to simulate
# 0 = no limit
SIMULATION_LIMIT = 0

# Possible states for a grid square
class Square(Enum):
    UNINHABITED = 0
    INFECTED = 1
    FISSION = 2
    TOWER = 3 # there is a corrosive tower here
    LIQUID = 4 # there is corrosive liquid here

class Board:
    """A board for the challenge.  Indices 1-x are used for the board.

An extra surrounding border is included."""

    @staticmethod
    def from_file(f, fission=True):
        """Gets a Board from a file object."""
        virus = f.readlines()
        squares = []
        row_length = 0

        for line in virus:
            # add a border on the left
            temp = [Square.UNINHABITED]

            # read characters one at a time
            for character in line:
                if character == ".":
                    temp.append(Square.UNINHABITED)
                elif character == "O":
                    temp.append(Square.INFECTED)
                elif character == "M":
                    temp.append(Square.FISSION)
                elif character == "Y":
                    temp.append(Square.TOWER)
                elif character == "+":
                    temp.append(Square.LIQUID)

            # add a border on the right
            temp.append(Square.UNINHABITED)

            row_length = len(temp)
            squares.append(temp)

        # add border on the top and bottom
        squares.insert(0, [Square.UNINHABITED] * row_length)
        squares.append([Square.UNINHABITED] * row_length)

        return Board(squares, fission)

    def __init__(self, squares, fission=True):
        """Gets the Board.

"squares" is the array of squares in the board.  It should be a rectangular array
of Square objects.
"fission" is whether or not the fission-mass mechanic is supported."""
        self.squares = squares
        self.fission = fission

    def __eq__(self, other):
        """Returns true if this == other."""
        return self.squares == other.squares and self.fission == other.fission

    def __repr__(self, include_border=False):
        row_start = 0 if include_border else 1
        row_end = self.size(True)[0] - 1

        column_start = 0 if include_border else 1
        column_end = self.size(True)[1] - 1

        txt = ""
        for r in range(row_start, row_end):
            for c in range(column_start, column_end):
                if self.status(r, c) == Square.UNINHABITED:
                    txt += ".,"
                elif self.status(r, c) == Square.INFECTED:
                    txt += "O,"
                elif self.status(r, c) == Square.FISSION:
                    txt += "M,"
                elif self.status(r, c) == Square.TOWER:
                    txt += "Y,"
                elif self.status(r, c) == Square.LIQUID:
                    txt += "+,"
            txt += "\n"
        return txt

    def __str__(self, include_border=False):
        row_start = 0 if include_border else 1
        row_end = self.size(True)[0] - 1

        column_start = 0 if include_border else 1
        column_end = self.size(True)[1] - 1

        txt = ""
        for r in range(row_start, row_end):
            for c in range(column_start, column_end):
                if self.status(r, c) == Square.UNINHABITED:
                    txt += "."
                elif self.status(r, c) == Square.INFECTED:
                    txt += "O"
                elif self.status(r, c) == Square.FISSION:
                    txt += "M"
                elif self.status(r, c) == Square.TOWER:
                    txt += "Y"
                elif self.status(r, c) == Square.LIQUID:
                    txt += "+"
            txt += "\n"
        return txt

    def status(self, row, col):
        """Returns the CURRENT status of square with row row and column col."""
        return self.squares[row][col]

    def is_breached(self):
        """The testing grounds have been breached if there are any INFECTED
within the border region.

If there is a breach, returns the coordinates of the breach."""

        if not BORDER_ENABLED:
            # when BORDER_ENABLED is false, breaches are disabled
            return False

        size = self.size()

        # test border rows (top and bottom), column by column
        for col in range(size[1]):
            if self.status(0, col) == Square.INFECTED:
                return (0, col)
            if self.status(size[0] - 1, col) == Square.INFECTED:
                return (size[0] - 1, col)

        # test border columns (leftmost and rightmost), row by row
        for row in range(size[0]):
            if self.status(row, 0) == Square.INFECTED:
                return (row, 0)
            if self.status(row, size[1] - 1) == Square.INFECTED:
                return (row, size[1] - 1)

        # if we get here, no breach has been found
        return False

    def is_dead(self):
        """Returns true if there are no INFECTED squares on the board."""
        size = self.size()

        # test squares one-by-one
        for r in range(size[0]):
            for c in range(size[1]):
                if self.status(r, c) == Square.INFECTED:
                    return False

        return True

    def size(self, include_border=True):
        """Returns the size of the board.

The returned value is a 2-element tuple (# rows, # columns)."""
        if include_border:
            return (len(self.squares), len(self.squares[0]))
        else:
            return (len(self.squares) - 2, len(self.squares[0]) - 2)

    def _infected_neighbours(self, row, col):
        """Returns the number of INFECTED neighbours."""
        infected = 0
        for r in range(row - 1, row + 2):

            # check for invalid row, if row is invalid continue
            if r < 0 or r >= self.size()[0]:
                continue

            # check for invalid row in non-BORDER_ENABLED mode
            if not BORDER_ENABLED and (r < 1 or r >= self.size()[0] - 1):
                continue

            for c in range(col - 1, col + 2):
                if r == row and c == col:
                    # don't count the square itself, only the neighbours
                    continue

                # check for invalid column, if col is invalid continue
                elif c < 0 or c >= self.size()[1]:
                    continue

                # check for invalid column in non-BORDER_ENABLED mode
                if not BORDER_ENABLED and (c < 1 or c >= self.size()[1] - 1):
                    continue

                if self.status(r, c) == Square.INFECTED:
                    infected += 1
        return infected

    def _tower_neighbours(self, row, col):
        """Returns the number of TOWER neighbours, excluding diagonals."""
        towers = 0

        # check each of the four neighbours individually
        if row > 0 and self.status(row - 1, col) == Square.TOWER:
            if BORDER_ENABLED or row != 1: # don't count border rows if
                                           # BORDER_ENABLED is false
                towers += 1
        elif col > 0 and self.status(row, col - 1) == Square.TOWER:
            if BORDER_ENABLED or col != 1:
                towers += 1
        elif (row < self.size()[0] - 1
              and self.status(row + 1, col) == Square.TOWER):
            if BORDER_ENABLED or row != self.size()[0] - 2:
                towers += 1
        elif (col < self.size()[1] - 1
              and self.status(row, col + 1) == Square.TOWER):
            if BORDER_ENABLED or row != self.size()[1] - 2:
                towers += 1
        return towers

    def next_status_tower(self, row, col):
        """Returns the status of square [row, col] after towers do their thing."""

        # check direct neighbours for tower/liquid stuff
        towers = self._tower_neighbours(row, col)

        # get current state
        state = self.status(row, col)

        # tower-related code
        if towers:
            if state == Square.UNINHABITED:
                return Square.LIQUID # towers created liquid
            elif state == Square.INFECTED:
                return Square.UNINHABITED # towers killed virus

        # towers didn't do anything
        return state

    def next_status_infection(self, row, col):
        """Returns the status of square [row, col] in the next turn."""

        # Check all of the squares around and count the # of infected
        infected = self._infected_neighbours(row, col)

        # get current state
        state = self.status(row, col)

        # use the number of infected neighbours to find next state
        # if square is INFECTED and has <3 infected neighbours it will become
        # UNINHABITED.
        # if square is UNINHABITED and has >= 3 infected neighbours it will
        # become INFECTED.
        if state == Square.UNINHABITED:
            if infected >= 3:
                state = Square.INFECTED # new infection
            else:
                state = Square.UNINHABITED # no change
        elif state == Square.INFECTED:
            if infected < 3:
                state = Square.UNINHABITED # death
            elif infected >= 8 and self.fission:
                state = Square.FISSION # becomes fission mass
            else:
                state = Square.INFECTED # no change
        else: # fission, tower and liquid are all permanent - do nothing
            pass

        return state

    def update(self):
        """Updates the board, setting every square to its next state."""

        # because we don't want to modify anything, make a new array
        # and set the new states there

        # squares after towers
        new_squares_towers = []

        for r in range(self.size()[0]):
            row = []
            for c in range(self.size()[1]):
                row.append(self.next_status_tower(r, c))
            new_squares_towers.append(row)

        self.squares = new_squares_towers

        # squares after infection
        new_squares_infection = []

        for r in range(self.size()[0]):
            row = []
            for c in range(self.size()[1]):
                row.append(self.next_status_infection(r, c))
            new_squares_infection.append(row)

        self.squares = new_squares_infection

    def updated(self):
        """Updates the board, setting every square to its next state.

Returns an updated version of this board.  This board is not changed."""
        board = Board(self.squares, self.fission)
        board.update()
        return board


class ExitStatus(Enum):
    """A possible exit status for the run() method."""
    BREACH = 0    # the virus has breached the grounds
    DEAD = 1      # the virus has died out
    STUCK = 2     # the virus will never breach the grounds, but is not dead

def run(board, verbose=True):
    """Simulates the lifetime of the virus on board.

Returns a tuple containing three values: the last hour simulated, the exit status
, and the final board.

For example, if the board breaches at 20 hours, returns
(20, ExitStatus.BREACH, [final board]).

If "verbose" is true, outputs extra information."""

    # store all past states - this will be useful later
    past_boards = []

    past_boards.append(board)

    current_board = board # board at current hour
    hour = 0

    # print initial info
    if verbose:
        if board.fission:
            print("Fission is ENABLED")
        else:
            print("Fission is DISABLED")
        print("Hour: {}".format(hour))
        print("Current Board State:")
        print(current_board)

    # incase the initial board is already breached
    if board.is_breached():
        return (0, ExitStatus.BREACH, board)

    # simulate hours
    while True:
        # simulate board and update hour
        hour += 4
        current_board = current_board.updated()

        # determine whether or not to exit
        if current_board.is_breached():
            breach = current_board.is_breached()
            if verbose:
                print("Hour: {}, breach has occurred at row {}, col {}.".format(
                    hour, breach[0] - 1, breach[1] - 1))
                print("Current Board State:")
                print(current_board)
            return (hour, ExitStatus.BREACH, current_board)
        elif current_board.is_dead():
            if verbose:
                print("Hour: {}, virus has died off.".format(hour))
                print("Current Board State:")
                print(current_board)
            return (hour, ExitStatus.DEAD, current_board)

        # look for stuck board
        # if this state has already happened, we know it's in a loop
        # because the rules only depend on the previous state
        elif current_board in past_boards:
            if verbose:
                print("Hour: {}, virus is stuck in a loop.".format(hour))
                print("Current Board State:")
                print(current_board)
            return (hour, ExitStatus.STUCK, current_board)
        else:
            if verbose:
                print("Hour: {}".format(hour))
                print("Current Board State:")
                print(current_board)

        past_boards.append(current_board)

        # if simulation limit is passed, assume stuck
        if SIMULATION_LIMIT > 0 and hour >= SIMULATION_LIMIT: 
            return (hour, ExitStatus.STUCK, current_board)

def run_file(filename, verbose=True, fission=True):
    """Gets a board from filename filename, runs it, then makes an output file.

"verbose", if true, outputs verbose information to standard output.
"fission" represents whether or not fission is enabled."""
    # load file
    f = open(filename, "r")
    b = Board.from_file(f, fission)
    f.close()

    # simulate
    hour, status, final_board = run(b, verbose)

    # output - replace "filename.txt" with "filename(Solution).txt"
    output_filename = filename[:-4] + "(Solution).txt"
    of = open(output_filename, 'w')

    if status == ExitStatus.BREACH:
        if verbose:
            print("Wrote final state to", output_filename)
        of.write(repr(final_board))
    else:
        if verbose:
            print("Wrote \"GG\" to", output_filename)
        of.write("GG")
    of.close()

def run_and_output(board):
    """Runs and prints human-readable output"""
    hour, status, final_board = run(board)
    if status == ExitStatus.BREACH:
        print("A breach occured after {} hours".format(hour))
    elif status == ExitStatus.DEAD:
        print("The virus died off after {} hours".format(hour))
    print("Final board:")
    print(final_board)

# Testing/execution code
if __name__ == "__main__":
    filename = input("Enter input filename: ")
    fission = input("Enable fission? [Y/N] ").capitalize().startswith('Y')
    run_file(filename, True, fission)
