import string
import json
from random import choice, shuffle
from os import system, name
from time import time


def timer(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        res = func(*args, **kwargs)
        t2 = time()
        print(f"{func.__name__}(): {t2 - t1} seconds.")
        return res
    return wrapper


def rm(filename: str):
    if name == 'nt':
        _ = system('del -f ' + filename)
    else:
        _ = system('rm -rf ' + filename)


class Sudoku:
    """A Sudoku 9*9 Board"""

    def __init__(self, board: list[list]) -> None:
        """Initializing basic attributes"""
        self.board = board
        self.allpos = self.all_pos()
        self.empos = self.empty_pos()
        self.columns = self._columns()
        self.toprank, self.middlerank, self.bottomrank = self.ranks()
        self.block1, self.block2, self.block3, self.block4, self.block5, self.block6, self.block7, self.block8, self.block9 = self.blocks()
        self.leftstack, self.centrestack, self.rightstack = self.stacks()

    def __str__(self) -> str:
        return self.display(self.board) + "\n"

    def __repr__(self) -> str:
        return "Sudoku(" + str(self.board) + ")"

    def all_pos(self) -> list[tuple]:
        """Positioning all values"""
        all_p = []  # (x, y, z) = (board[index], baord[index][index], item)
        for i in range(0, 9):
            row = self.board[i]
            for n in range(0, 9):
                item = row[n]
                all_p.append((i, n, item))
        return all_p

    def empty_pos(self, emp = 0) -> list[tuple]:
        """Determining the empty values"""
        empty = []  # [x, y] = [board[index], baord[index][index]]
        for i in self.allpos:
            a, b, c = i
            if c == emp:
                empty.append((a, b))
        return empty

    def _columns(self) -> list[list]:
        res = [[] for _ in range(9)]
        for i in self.board:
            for n in range(len(i)):
                res[n].append(i[n])
        return res

    @staticmethod
    def display(board: list) -> str:
        dis = ""
        for i in range(len(board)):
            row = board[i]
            line = ""
            for i in range(len(row)):
                line += str(row[i]).replace("0", " ") + " "
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

    def __init__(self, *args, **kwargs):
        """
        Initializing class attributes
        """
        super(Solver, self).__init__(*args, **kwargs)
        self._filename = self.gen_filename()
        self.soln = self.solved()
        self.solve_status = len(self.soln) != 0

    def __del__(self):
        rm(self._filename)

    def gen_filename(self):
        v = string.ascii_letters + "".join([str(i) for i in range(0, 9)])
        n = choice(v) + choice(v) + choice(v) + choice(v) + choice(v) + ".json"
        load = []
        with open(n, 'w') as f:
            json.dump(load, f)
        return n

    @staticmethod
    def find_duplicate_rows(board):
        dup = []
        for i in range(len(board)):
            x = set(board[i])
            res = {}
            for m in x:
                res[m] = board[i].count(m)
            for i in range(1, 10):
                if i not in res:
                    res[i] = 0
            dup.append(res)
        return dup

    @staticmethod
    def find_duplicate_columns(board):
        dup = []
        for i in range(len(board)):
            x = set(board[i])
            res = {}
            for m in x:
                res[m] = board[i].count(m)
            dup.append(res)
        return dup

    @classmethod
    def validity_check(cls, board, emp=0):
        "check if the generated board valid"
        a = cls.find_duplicate_columns(board)
        for x in a:
            for n, i in x.items():
                if i != 1 or n == emp:
                    return False
        b = cls.find_duplicate_rows(board)
        for x in b:
            for n, i in x.items():
                if i != 1 or n == emp:
                    return False
        return True

    def solved(self):
        self.solve()
        with open(self._filename) as f_obj:
            payload = json.load(f_obj)
        res = []
        for i in payload:
            res.append(Sudoku(i))
        return res

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
                            if self.validity_check(board):
                                with open(self._filename) as f:
                                    payload = json.load(f)
                                payload.append(board)
                                with open(self._filename, 'w') as f_obj:
                                    json.dump(payload, f_obj)
                            foo()
                            board[i[0]][i[1]] = 0
                    return
        foo()


class Sudoku_Board_Generator:
    """
    9*9 sudoku board generator
    >>> Sudoku_Board_Generator().gen
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
                return foo.soln[0]
