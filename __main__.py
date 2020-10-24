from pprint import *
from specimen_f import *

# testing code
f = open("4S-N25.txt", "r")
b = Board.from_file(f)

print("0 hours")
print(b)
for i in range(1, 7):
    b.update()
    print(i * 4, "hours", end='')
    if b.is_breached():
        print(" - BREACH")
    else:
        print()
    print(b)
