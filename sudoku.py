import string
from random import choice, shuffle, randint
from os import system, name


def rm(filename: str):
    if name == 'nt':
        _ = system('del -f ' + filename)
    else:
        _ = system('rm -rf ' + filename)


class Sudoku:
    """A Sudoku 9*9 Board"""

    def __init__(self, board: list[list], emp=0) -> None:
        """Initializing basic attributes"""
        self.board = board
        self.emp = emp
        self.allpos = self.all_pos()
        self.empos = self.empty_pos()
        self.columns = self._columns()
        self.toprank, self.middlerank, self.bottomrank = self.ranks()
        self.block1, self.block2, self.block3, self.block4, self.block5, self.block6, self.block7, self.block8, self.block9 = self.blocks()
        self.leftstack, self.centrestack, self.rightstack = self.stacks()
        self.flat_string = self.flatten()

    def __str__(self) -> str:
        return self.display(self.board, emp=self.emp)

    def __repr__(self) -> str:
        return "Sudoku(" + str(self.board) + ")"

    def __getitem__(self, idx):
        return self.board[idx]

    def flatten(self):
        foo = []
        for i in self.board:
            foo.extend(i)
        return "".join([str(i) for i in foo])

    @staticmethod
    def parser(lst: list[int] or str, emp=0):
        """
        Create a Sudoku object from only a string / list
        of numbers ranging from 0 to 9
        # 0s are considered blank by default.
        """
        res = [[0 for _ in range(9)] for _ in range(9)]
        n = 0
        for y in range(9):
            for x in range(9):
                res[y][x] = int(lst[n])
                n += 1
        return Sudoku(res, emp=emp)

    @staticmethod
    def blocks_to_board(blocks: list[list]):
        res = [[] for _ in range(9)]
        for x in range(len(blocks)):
            for y in range(len(blocks[x])):
                for z in range(len(blocks[x][y])):
                    if x in [0, 1, 2]:
                        res[[0, 1, 2][y]].append(blocks[x][y][z])
                    elif x in [3, 4, 5]:
                        res[[3, 4, 5][y]].append(blocks[x][y][z])
                    elif x in [6, 7, 8]:
                        res[[6, 7, 8][y]].append(blocks[x][y][z])
        return Sudoku(res)

    def all_pos(self) -> list[tuple]:
        """Positioning all values"""
        all_p = []  # (x, y, z) = (board[index], baord[index][index], item)
        for i in range(0, 9):
            row = self.board[i]
            for n in range(0, 9):
                item = row[n]
                all_p.append((i, n, item))
        return all_p

    def empty_pos(self) -> list[tuple]:
        """Determining the empty values"""
        empty = []  # [x, y] = [board[index], baord[index][index]]
        for i in self.allpos:
            a, b, c = i
            if c == self.emp:
                empty.append((a, b))
        return empty

    def _columns(self) -> list[list]:
        res = [[] for _ in range(9)]
        for i in self.board:
            for n in range(len(i)):
                res[n].append(i[n])
        return res

    @staticmethod
    def display(board: list, emp=0) -> str:
        dis = ""
        for i in range(len(board)):
            row = board[i]
            line = ""
            for i in range(len(row)):
                line += str(row[i]).replace(str(emp), " ") + " "
                if i == 2 or i == 5:
                    line += "| "
            line += "\n"
            dis += line
        dis_l = dis.split("\n")
        dis = ""
        for i in range(len(dis_l)):
            check = dis_l[i]
            dis += check
            dis += "\n"
            if i == 2 or i == 5:
                dis += "------|-------|------"
                dis += "\n"
        return dis.strip("\n")

    def ranks(self) -> tuple[list]:
        board = self.board
        top_rank = []
        middle_rank = []
        bottom_rank = []
        for i in range(0, 9):
            row = board[i]
            if i < 3:
                top_rank.append(row)
            elif i < 6:
                middle_rank.append(row)
            else:
                bottom_rank.append(row)

        return top_rank, middle_rank, bottom_rank

    def blocks(self) -> tuple[list[list]]:
        top_rank, middle_rank, bottom_rank = self.ranks()
        b1 = [top_rank[0][0:3], top_rank[1][0:3], top_rank[2][0:3]]
        b2 = [top_rank[0][3:6], top_rank[1][3:6], top_rank[2][3:6]]
        b3 = [top_rank[0][6:9], top_rank[1][6:9], top_rank[2][6:9]]
        b4 = [middle_rank[0][0:3], middle_rank[1][0:3], middle_rank[2][0:3]]
        b5 = [middle_rank[0][3:6], middle_rank[1][3:6], middle_rank[2][3:6]]
        b6 = [middle_rank[0][6:9], middle_rank[1][6:9], middle_rank[2][6:9]]
        b7 = [bottom_rank[0][0:3], bottom_rank[1][0:3], bottom_rank[2][0:3]]
        b8 = [bottom_rank[0][3:6], bottom_rank[1][3:6], bottom_rank[2][3:6]]
        b9 = [bottom_rank[0][6:9], bottom_rank[1][6:9], bottom_rank[2][6:9]]
        blocks = (
            b1, b2, b3,
            b4, b5, b6,
            b7, b8, b9,
        )
        return blocks

    def stacks(self) -> tuple[list[list]]:
        blocks = self.blocks()
        left_stack = [blocks[0], blocks[3], blocks[6]]
        centre_stack = [blocks[1], blocks[4], blocks[7]]
        right_stack = [blocks[2], blocks[5], blocks[8]]
        return left_stack, centre_stack, right_stack

    def check(self, pos: tuple) -> int:
        """return value for any random position"""
        x, y = pos
        return self.board[x][y]


class Solver(Sudoku):
    """
    Provide solution of a solvable 9*9 Sudoku game
    """

    class NoSolutionFoundError(Exception):
        pass

    def __init__(self, board: list[list], max_count: int or float = float("inf")):
        """
        Initializing class attributes
        """
        super(Solver, self).__init__(board)
        self.max_count = max_count  # limit max number of possible solutions
        self.count = 0
        self._filename = self.gen_filename()
        self.soln = self.solved()
        self.solve_status = len(self.soln) != 0

    def __getitem__(self, idx):
        if self.solve_status:
            return self.soln[idx]
        else:
            raise self.NoSolutionFoundError("the board is not solvable.")

    def __del__(self):
        rm(self._filename)

    def gen_filename(self):
        v = string.ascii_letters + "".join([str(i) for i in range(0, 9)])
        n = choice(v) + choice(v) + choice(v) + choice(v) + choice(v) + ".txt"
        with open(n, 'w') as f:
            f.write('')
        return n

    def find_duplicate_rows(self):
        dup = []
        for i in range(len(self.board)):
            x = set(self.board[i])
            res = {}
            for m in x:
                res[m] = self.board[i].count(m)
            for i in range(1, 10):
                if i not in res:
                    res[i] = 0
            dup.append(res)
        return dup

    def find_duplicate_columns(self):
        dup = []
        for i in range(len(self.board)):
            x = set(self.board[i])
            res = {}
            for m in x:
                res[m] = self.board[i].count(m)
            dup.append(res)
        return dup

    def validity_check(self):
        "check if the generated board valid"
        a = self.find_duplicate_columns()
        for x in a:
            for n, i in x.items():
                if i != 1 or n == self.emp:
                    return False
        b = self.find_duplicate_rows()
        for x in b:
            for n, i in x.items():
                if i != 1 or n == self.emp:
                    return False
        return True

    def solved(self):
        self.solve()
        with open(self._filename) as f_obj:
            payload = [Sudoku(eval(i.rstrip('\n'))) for i in f_obj.readlines()]
        return payload

    def solve(self):

        board = self.board

        def check(y, x, n):
            """
            Check if 'n' is a probable value for (x, y) position
            """
            for i in range(9):
                if board[y][i] == n or board[i][x] == n:
                    return False
            x0, y0 = (x // 3) * 3, (y // 3) * 3
            for i in range(3):
                for j in range(3):
                    if board[y0 + i][x0 + j] == n:
                        return False
            return True

        def foo():
            nonlocal board
            for i in self.empos:
                if board[i[0]][i[1]] == 0:
                    for n in range(1, 10):
                        if check(i[0], i[1], n):
                            board[i[0]][i[1]] = n
                            if self.validity_check():
                                if self.count >= self.max_count:
                                    return
                                with open(self._filename, 'a') as f:
                                    f.write(str(board) + "\n")
                                self.count += 1
                            foo()
                            board[i[0]][i[1]] = 0
                    return
        foo()


class Sudoku_Board_Generator_i:
    """
    9*9 sudoku board generator
    >>> Sudoku_Board_Generator_i().gen
    """

    def __init__(self):
        """initializing attributes"""
        self.gen = self._gen()

    @staticmethod
    def block_generator():
        var = [i for i in range(1, 10)]
        shuffle(var)  # a good mix
        a = []
        for _ in range(3):
            a.append(var.pop())
        b = []
        for _ in range(3):
            b.append(var.pop())
        c = []
        for _ in range(3):
            c.append(var.pop())
        return [a, b, c]

    @classmethod
    def block_creator(cls):
        return tuple([cls.block_generator() for _ in range(9)])

    @classmethod
    def initial_boardmaker(cls, blocks=None):
        if blocks == None:
            blocks = cls.block_creator()
        zero0, one0, two0 = ([], [], [])
        zero1, one1, two1 = ([], [], [])
        zero2, one2, two2 = ([], [], [])
        for i in range(len(blocks)):
            if i < 3:
                for x in blocks[i]:
                    zero0.append(x[0])
                    one0.append(x[1])
                    two0.append(x[2])
            elif i > 2 and i < 6:
                for x in blocks[i]:
                    zero1.append(x[0])
                    one1.append(x[1])
                    two1.append(x[2])
            elif i > 5:
                for x in blocks[i]:
                    zero2.append(x[0])
                    one2.append(x[1])
                    two2.append(x[2])
        res = [zero0, one0, two0,
               zero1, one1, two1,
               zero2, one2, two2]
        return res

    def _gen(self):
        # print("Generating Sudoku board ...")
        while True:
            v = self.initial_boardmaker()
            for y in range(9):
                load = []
                for x in range(9):
                    if v[y][x] not in load and v[y][x] != 0:
                        load.append(v[y][x])
                    else:
                        v[y][x] = 0
            for y in range(9):
                load = []
                for x in range(9):
                    if v[x][y] not in load and v[x][y] != 0:
                        load.append(v[x][y])
                    else:
                        v[x][y] = 0
            foo = Solver(v)
            if foo.solve_status:
                return foo[0]


class Sudoku_Board_Generator_ii:
    """
    A faster way to generate Sudoku boards
    >>> Sudoku_Board_Generator_ii(100)
    returns a list containing 100 Sudoku boards
    """

    def __init__(self, max_count=float("inf")) -> None:
        self.max: int or float = max_count
        self.gen: list = self._gen()

    def __getitem__(self, idx):
        return self.gen[idx]

    def _gen(self) -> list:
        board = [[0 for _ in range(9)] for _ in range(9)]
        foo, mode, n = [i for i in range(1, 10)], randint(0, 4), randint(0, 8)
        shuffle(foo)
        for i in range(9):
            if mode == 0:
                board[n][i] = foo.pop()
            elif mode == 1:
                board[i][n] = foo.pop()
            elif mode == 2:
                board[i][8 - i] = foo.pop()
            elif mode == 3:
                board[n][i] = foo.pop()
            elif mode == 4:
                board[randint(0, 8)][randint(0, 8)] = foo.pop()
        bar = Solver(board, max_count=self.max)
        while True:
            if bar.solve_status:
                return bar.soln


class Sudoku_Board_Generator_iii:
    """
    >>> Sudoku_Board_Generator_iii().gen()
    this returns random generated Sudoku board
    """

    def __init__(self) -> None:

        self._board = [[0 for _ in range(9)] for _ in range(9)]
        self._processed_dict = {}
        for y in range(9):
            for x in range(9):
                self._processed_dict[(y, x)] = []

    def __repr__(self) -> str:
        return str(Sudoku_Board_Generator_iii().gen())

    def _check(self, y, x, n):
        """
        Check if 'n' is a probable value for (x, y) position
        """
        for i in range(9):
            if self._board[y][i] == n or self._board[i][x] == n:
                return False
        x0, y0 = (x // 3) * 3, (y // 3) * 3
        for i in range(3):
            for j in range(3):
                if self._board[y0 + i][x0 + j] == n:
                    return False
        return True

    def gen(self):
        for y in range(9):
            for x in range(9):
                if self._board[y][x] == 0:
                    bar = [i for i in range(1, 10)]
                    shuffle(bar)
                    for i in bar:
                        if self._check(y, x, i) and i not in self._processed_dict[(y, x)]:
                            self._board[y][x] = i
                            self._processed_dict[(y, x)].append(i)
                            break
                if self._board[y][x] == 0:
                    a, b = (y, x)
                    if x > 0:
                        b -= 1
                    elif x == 0 and y > 0:
                        a -= 1
                        b = 8
                    self._board[a][b] = 0
                    self._processed_dict[(y, x)] = []
                    self.gen()

        return Sudoku(self._board)


def game_builder(generator_version=3) -> Sudoku:
    """
    Generate random playable Sudoku board
    """
    if generator_version == 1:
        # mostly very slow but more permutations
        # sometimes it might seem like it's doing nothing
        # but fortunately it does work
        n = Sudoku_Board_Generator_i().gen.board
    elif generator_version == 2:
        # n = Sudoku_Board_Generator_ii(1000)[randint(0,999)].board
        # fast but (very) limited permutations
        # although, it's capable of generating all possible sudoku boards
        # if and only if super long time and cpu power is not a problem
        n = Sudoku_Board_Generator_ii(1)[0].board
    elif generator_version == 3:
        # fast and efficient
        # generates very random sudoku board
        # using backtracking
        n = Sudoku_Board_Generator_iii().gen().board
    clean = []
    for _ in range(randint(21, 31)):
        while True:
            o = (randint(0, 8), randint(0, 8))
            if o not in clean:
                break
        clean.append(o)
    for y in range(9):
        for x in (range(9)):
            if (y, x) in clean:
                n[y][x] = 0
    return Sudoku(n)


if __name__ == "__main__":
    print(Solver(Sudoku.parser(
        '002003060900008050000200300000007009094500200001000040500000004070030090803060000').board).soln[0])
