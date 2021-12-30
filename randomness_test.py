from sudoku import Sudoku_Board_Generator_iii, Sudoku

# tests to check the randomness of Sudoku_Board_Generator_iii


def test1(n: int = 100):

    res = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    for _ in range(n):

        v = Sudoku_Board_Generator_iii()

        res[v[0][0]] += 1

    for k, v in res.items():

        res[k] = (v / n) * 100

        print(k, '->', res[k], '%')

    print("total: {0} %".format(str(sum([i for i in res.values()]))))


def test2(n: int = 2):
    _bar = [Sudoku_Board_Generator_iii().board for _ in range(n)]

    commons_board, count = [[0 for _ in range(9)] for _ in range(9)], 0

    for y in range(9):
        for x in range(9):
            bar = set([_bar[i][y][x] for i in range(n)])
            if len(bar) == 1:
                commons_board[y][x] = _bar[0][y][x]
                count += 1
    print("Commons:\n" + str(Sudoku(commons_board)))
    print("Match: " + str((count / 81) * 100) + ' %')


print("Test 1")
test1()
input("\nPress Enter to continue ...\n")
print("Test 2")
test2(2)
