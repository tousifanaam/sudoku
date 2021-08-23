from sudoku import Solver, game_builder
from time import perf_counter


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        res = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"{func.__name__}(): {t2 - t1} seconds.")
        return res
    return wrapper


@timer
def main():
    # Generate random Sudoku board
    print("Generating Sudoku board ...")
    n = game_builder(generator_version=3)
    print(n)
    # solve any valid sudoku board
    print("\n" + "Solving Puzzle ...")
    n = Solver(n.board)
    while True:
        if n.solve_status:
            for i in n.soln:
                print(str(i) + "\n")
            break
    print("Total Number of Blanks: " + str(len(n.empos)))
    print("Total Number of Solutions: " + str(len(n.soln)))


if __name__ == "__main__":

    main()
