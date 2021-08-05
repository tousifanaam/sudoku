from sudoku import Sudoku, Sudoku_Board_Generator, Solver
from random import randint

# Generate random Sudoku board
print("Generating sudoku board ...")
n = Sudoku_Board_Generator().gen.board

# creating a playable board
clean = []
for _ in range(randint(21, 41)):
    clean.append((randint(0, 8), randint(0, 8)))

for y in range(9):
    for x in (range(9)):
        if (y, x) in clean:
            n[y][x] = 0
print(Sudoku(n))

# solve any valid sudoku board
print("\n" + "Solving Puzzle ...")
n = Solver(n)
while True:
    if n.solve_status:
        for i in n.soln:
            print(i)
        break