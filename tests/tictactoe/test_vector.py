# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-17 (y-m-d) 7:37 PM
from unittest import TestCase

from games.tictactoe.vector import (
    TicTacToeRowVectorProvider, TicTacToeColumnVectorProvider, TicTacToeBackDiagonalVectorProvider,
    TicTacToeForwardDiagonalVectorProvider
)
from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board
from tests.tictactoe.board_stubs import TicTacToeVectorProviderStub1


class TestTicTacToeRowVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = TicTacToeRowVectorProvider(Board(AsciiAxis(5), Int1Axis(4)), 'X', 4)

    def test_provide(self):
        tres = [
            {('a', 1): None, ('b', 1): None, ('c', 1): None, ('d', 1): None, ('e', 1): None},
            {('a', 2): None, ('b', 2): None, ('c', 2): None, ('d', 2): None, ('e', 2): None},
            {('a', 3): None, ('b', 3): None, ('c', 3): None, ('d', 3): None, ('e', 3): None},
            {('a', 4): None, ('b', 4): None, ('c', 4): None, ('d', 4): None, ('e', 4): None}
        ]
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 5
        self.assertListEqual(tres, self.provider.provide())

        self.provider.cnt_in_row = 6
        self.assertListEqual([], self.provider.provide())


class TestTicTacToeColumnVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = TicTacToeColumnVectorProvider(Board(AsciiAxis(5), Int1Axis(4)), 'X', 4)

    def test_provide(self):
        tres = [
            {('a', 1): None, ('a', 2): None, ('a', 3): None, ('a', 4): None},
            {('b', 1): None, ('b', 2): None, ('b', 3): None, ('b', 4): None},
            {('c', 1): None, ('c', 2): None, ('c', 3): None, ('c', 4): None},
            {('d', 1): None, ('d', 2): None, ('d', 3): None, ('d', 4): None},
            {('e', 1): None, ('e', 2): None, ('e', 3): None, ('e', 4): None}
        ]
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 5
        self.assertListEqual([], self.provider.provide())


class TestTicTacToeBackDiagonalVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = TicTacToeBackDiagonalVectorProvider(Board(AsciiAxis(5), Int1Axis(4)), 'X', -1)

    def test_provide(self):
        tres = [
            # backward diagonal vectors
            {('a', 1): None, ('b', 2): None, ('c', 3): None, ('d', 4): None},
            {('b', 1): None, ('c', 2): None, ('d', 3): None, ('e', 4): None},
            {('c', 1): None, ('d', 2): None, ('e', 3): None},
            {('d', 1): None, ('e', 2): None},
            {('e', 1): None},
            {('a', 2): None, ('b', 3): None, ('c', 4): None},
            {('a', 3): None, ('b', 4): None},
            {('a', 4): None},
        ]
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 0
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 1
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        for cnt in range(1, max(len(self.provider.board.axis_x), len(self.provider.board.axis_x)) + 2):
            self.provider.cnt_in_row = cnt
            ttres = [*filter(lambda points: len(points) >= self.provider.cnt_in_row, tres)]
            for i, v in enumerate(self.provider):
                self.assertDictEqual(ttres[i], v)

        self.provider.cnt_in_row = 5
        self.assertListEqual([], self.provider.provide())


class TestTicTacToeForwardDiagonalVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = TicTacToeForwardDiagonalVectorProvider(Board(AsciiAxis(5), Int1Axis(4)), 'X', -1)

    def test_provide(self):

        tres = [
            # forward diagonal vectors
            {('e', 1): None, ('d', 2): None, ('c', 3): None, ('b', 4): None},
            {('d', 1): None, ('c', 2): None, ('b', 3): None, ('a', 4): None},
            {('c', 1): None, ('b', 2): None, ('a', 3): None},
            {('b', 1): None, ('a', 2): None},
            {('a', 1): None},
            {('e', 2): None, ('d', 3): None, ('c', 4): None},
            {('e', 3): None, ('d', 4): None},
            {('e', 4): None},
        ]

        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 0
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        self.provider.cnt_in_row = 1
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)

        for cnt in range(1, max(len(self.provider.board.axis_x), len(self.provider.board.axis_x)) + 2):
            self.provider.cnt_in_row = cnt
            ttres = [*filter(lambda points: len(points) >= self.provider.cnt_in_row, tres)]
            for i, v in enumerate(self.provider):
                self.assertDictEqual(ttres[i], v)

        self.provider.cnt_in_row = 5
        self.assertListEqual([], self.provider.provide())


class TestTicTacToeVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider_stub = TicTacToeVectorProviderStub1()

    def test_provide(self):
        ttres = (*self.provider_stub.row_list, *self.provider_stub.col_list,
                 *self.provider_stub.diag_list, *self.provider_stub.diag_list_fwd)
        for v in self.provider_stub.provider:
            self.assertIn(v, ttres)
