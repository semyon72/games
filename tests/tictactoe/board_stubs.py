# IDE: PyCharm
# Project: games
# Path: tests/tictactoe
# File: board_stubs.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-20 (y-m-d) 10:42 AM
from unittest import TestCase

from games.board.axis import Int1Axis, AsciiAxis
from games.board.board import Board, ConsoleRenderer
from games.items.items import XItem, OItem
from games.tictactoe.vector import TicTacToeVectorProvider
from tests.utils import _catch_stdout


class TicTacToeVectorProviderStub:

    def __init__(self) -> None:
        #  abcde
        # 1#####
        # 2#X#X#
        # 3#X#O#
        # 4##X##
        self.cnt_in_row = 3
        self.board = Board(AsciiAxis(5), Int1Axis(4))
        self.b2 = XItem(self.board, 'b', 2)
        self.d2 = XItem(self.board, 'd', 2)
        self.b3 = XItem(self.board, 'b', 3)
        self.c4 = XItem(self.board, 'c', 4)
        self.d3 = OItem(self.board, 'd', 3)
        rstr = " abcde\n1#####\n2#X#X#\n3#X#O#\n4##X##\n"
        TestCase().assertEqual(rstr, _catch_stdout(ConsoleRenderer(self.board).render))
        self.provider = TicTacToeVectorProvider(self.board, XItem.id, 3)

        self.diag_list = [
            {('a', 1): None, ('b', 2): self.b2, ('c', 3): None, ('d', 4): None},
            {('c', 1): None, ('d', 2): self.d2, ('e', 3): None},
            {('a', 2): None, ('b', 3): self.b3, ('c', 4): self.c4}
        ]

        self.diag_list_fwd = [
            {('e', 1): None, ('d', 2): self.d2, ('c', 3): None, ('b', 4): None},
            {('d', 1): None, ('c', 2): None, ('b', 3): self.b3, ('a', 4): None},
            {('c', 1): None, ('b', 2): self.b2, ('a', 3): None}
        ]

        self.row_list = [
            {('a', 1): None, ('b', 1): None, ('c', 1): None, ('d', 1): None, ('e', 1): None},
            {('a', 2): None, ('b', 2): self.b2, ('c', 2): None, ('d', 2): self.d2, ('e', 2): None},
            {('a', 3): None, ('b', 3): self.b3, ('c', 3): None},
            {('a', 4): None, ('b', 4): None, ('c', 4): self.c4, ('d', 4): None, ('e', 4): None}
        ]
        self.col_list = [
            {('a', 1): None, ('a', 2): None, ('a', 3): None, ('a', 4): None},
            {('b', 1): None, ('b', 2): self.b2, ('b', 3): self.b3, ('b', 4): None},
            {('c', 1): None, ('c', 2): None, ('c', 3): None, ('c', 4): self.c4},
            {('e', 1): None, ('e', 2): None, ('e', 3): None, ('e', 4): None}
        ]


class TicTacToeVectorProviderStub1:

    def __init__(self) -> None:
        #  abcde
        # 1##O##
        # 2#X#X#
        # 3#X#O#
        # 4##X##
        self.cnt_in_row = 2
        self.board = Board(AsciiAxis(5), Int1Axis(4))
        self.b2 = XItem(self.board, 'b', 2)
        self.d2 = XItem(self.board, 'd', 2)
        self.b3 = XItem(self.board, 'b', 3)
        self.c4 = XItem(self.board, 'c', 4)
        self.c1 = OItem(self.board, 'c', 1)
        self.d3 = OItem(self.board, 'd', 3)
        rstr = " abcde\n1##O##\n2#X#X#\n3#X#O#\n4##X##\n"
        TestCase().assertEqual(rstr, _catch_stdout(ConsoleRenderer(self.board).render))
        self.provider = TicTacToeVectorProvider(self.board, XItem.id, self.cnt_in_row)

        self.row_list = [
            {('a', 1): None, ('b', 1): None},
            {('d', 1): None, ('e', 1): None},
            {('a', 2): None, ('b', 2): self.b2, ('c', 2): None, ('d', 2): self.d2, ('e', 2): None},
            {('a', 3): None, ('b', 3): self.b3, ('c', 3): None},
            {('a', 4): None, ('b', 4): None, ('c', 4): self.c4, ('d', 4): None, ('e', 4): None}
        ]

        self.col_list = [
            {('a', 1): None, ('a', 2): None, ('a', 3): None, ('a', 4): None},
            {('b', 1): None, ('b', 2): self.b2, ('b', 3): self.b3, ('b', 4): None},
            {('c', 2): None, ('c', 3): None, ('c', 4): self.c4},
            {('d', 1): None, ('d', 2): self.d2},
            {('e', 1): None, ('e', 2): None, ('e', 3): None, ('e', 4): None}
        ]

        self.diag_list = [
            {('a', 1): None, ('b', 2): self.b2, ('c', 3): None, ('d', 4): None},
            {('b', 1): None, ('c', 2): None},
            {('d', 1): None, ('e', 2): None},
            {('d', 2): self.d2, ('e', 3): None},
            {('a', 2): None, ('b', 3): self.b3, ('c', 4): self.c4},
            {('a', 3): None, ('b', 4): None},
        ]

        self.diag_list_fwd = [
            {('e', 1): None, ('d', 2): self.d2, ('c', 3): None, ('b', 4): None},
            {('d', 1): None, ('c', 2): None, ('b', 3): self.b3, ('a', 4): None},
            {('b', 2): self.b2, ('a', 3): None},
            {('b', 1): None, ('a', 2): None},
            {('e', 3): None, ('d', 4): None},

        ]
