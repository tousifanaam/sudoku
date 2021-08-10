from sudoku import Solver, Sudoku_Board_Generator_ii, game_builder
from time import perf_counter
import json


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
    n = game_builder()
    print(n)
    # solve any valid sudoku board
    print("\n" + "Solving Puzzle ...")
    n = Solver(n.board)
    while True:
        if n.solve_status:
            for i in n.soln:
                print(i)
            break
    print("Total Number of Blanks: " + str(len(n.empos)))
    print("Total Number of Solutions: " + str(len(n.soln)))


@timer
def gen_board(filename: str):
    """
    Generate 1000 Sudoku Board and
    store it in a json file
    """
    print("---\n" + "Running ...")
    load = []
    for i in Sudoku_Board_Generator_ii(1000).gen:
        load.append(i.board)
    while True:
        try:
            with open(filename) as f_obj:
                payload = json.load(f_obj)
            break
        except FileNotFoundError:
            print("** file not found.")
            with open(filename, 'w') as f_obj:
                json.dump([], f_obj)
    payload = payload + load
    with open(filename, 'w') as f:
        json.dump(payload, f)
    print("Current len: " + str(len(payload)))


if __name__ == "__main__":

    def foo1():
        main()

    def foo2():
        """
        generate 20k board and save in "generated.json"
        """
        for _ in range(20):
            gen_board("generated.json")

    foo1()
    # foo2()
