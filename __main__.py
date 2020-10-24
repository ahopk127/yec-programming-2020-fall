from pprint import *
from specimen_f import *

filename = input("Enter input filename: ")
fission = input("Enable fission? [Y/N] ").capitalize().startswith('Y')
run_file(filename, True, fission)
