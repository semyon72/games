# IDE: PyCharm
# Project: games
# Path: tests/test_tictactoe
# File: moves.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-20 (y-m-d) 9:36 AM
from unittest import TestCase

from games.items.items import OItem
from games.tictactoe.moves import TicTacToeIntersectionMove, TicTacToeWinMove, TicTacToeOpponentWinMove
from tests.tictactoe.board_stubs import TicTacToeVectorProviderStub


class TestTicTacToeIntersectionMove(TestCase):

    def setUp(self) -> None:
        self.provider = TicTacToeVectorProviderStub().provider

    def test_resolve(self):
        self.assertIn(TicTacToeIntersectionMove(self.provider).resolve(), (('c', 1), ('c', 3)))


class TestTicTacToeWinMove(TestCase):
    # 3 in row
    #  abcde
    # 1#####
    # 2#X#X#
    # 3#X#O#
    # 4##X##

    def setUp(self) -> None:
        self.provider = TicTacToeVectorProviderStub().provider
        self.win_cases = (('c', 2), ('b', 1), ('b', 4), ('a', 2))
        self.d2 = self.b2 = self.c3 = self.b3 = self.b4 = 'some not None value'

    def test_test_win_case(self):
        wd = TicTacToeWinMove(self.provider)
        self.assertIsNone(wd.test_win_case({('c', 1): None, ('d', 2): self.d2, ('e', 3): None}))

        self.assertEqual(
            ('c', 2),
            wd.test_win_case({('a', 2): None, ('b', 2): self.b2, ('c', 2): None, ('d', 2): self.d2, ('e', 2): None})
        )
        self.assertEqual(('a', 2), wd.test_win_case({('a', 2): None, ('c', 3): self.c3, ('b', 4): self.b4}))
        self.assertIn(wd.test_win_case({('b', 1): None, ('b', 2): self.b2, ('b', 3): self.b3, ('b', 4): None}),
                      (('b', 1), ('b', 4)))

    def test_resolve(self):
        self.assertIn(TicTacToeWinMove(self.provider).resolve(), self.win_cases)


class TestTicTacToeOpponentWinMove(TestCase):
    # 3 in row
    #  abcde
    # 1#####
    # 2#X#X#
    # 3#X#O#
    # 4##X##

    def setUp(self) -> None:
        self.provider = TicTacToeVectorProviderStub().provider

    def test_resolve(self):
        wr = TicTacToeOpponentWinMove(self.provider, OItem.id)
        self.assertIsNone(wr.resolve())
