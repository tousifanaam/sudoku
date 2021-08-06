from sudoku import Sudoku, Sudoku_Board_Generator_i, Solver, Sudoku_Board_Generator_ii
from random import randint
from time import time


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        res = func(*args, **kwargs)
        t2 = time()
        print(f"{func.__name__}(): {t2 - t1} seconds.")
        return res
    return wrapper

@timer
def main():
    # Generate random Sudoku board
    print("Generating sudoku board ...")

    # n = Sudoku_Board_Generator_i().gen.board # slower
    n = Sudoku_Board_Generator_ii(1).gen[0].board # faster

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

if __name__ == "__main__":
    main()