from pprint import *
from specimen_f import *

# testing code
f = open("4S-N25.txt", "r")
b = Board.from_file(f)

run_and_output(b)
