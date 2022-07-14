# IDE: PyCharm
# Project: games
# Path: tests/tictactoe
# File: test_intersection.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-20 (y-m-d) 10:26 AM
from unittest import TestCase

from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board, ConsoleRenderer
from games.items.items import XItem
from games.tictactoe.vector import TicTacToeVectorProvider
from games.vector.intersection import IntersectionPoints
from tests.tictactoe.board_stubs import TicTacToeVectorProviderStub
from tests.utils import _catch_stdout


class TestIntersectionPoints(TestCase):

    def setUp(self) -> None:
        # 3 in row
        #  abcde
        # 1#####
        # 2#X#X#
        # 3#X#O#
        # 4##X##
        self.provider = TicTacToeVectorProviderStub().provider

    def _provider_to_get_largest(self):
        # 3 in row
        #  abcd
        # 1####
        # 2#X##
        # 3####
        # 4X###
        board = Board(AsciiAxis(4), Int1Axis(4))
        XItem(board, 'b', 2)
        XItem(board, 'a', 4)
        rstr = " abcd\n1####\n2#X##\n3####\n4X###\n"
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(board).render))
        return TicTacToeVectorProvider(board, XItem.id, 3)

    def test_get_largest_list(self):
        ips = IntersectionPoints.create(self.provider)
        self.assertTupleEqual((('b', 2), ), tuple(ip.point for ip in ips.get_largest_list()))

        tprov = self._provider_to_get_largest()
        ips = IntersectionPoints.create(tprov)
        self.assertTupleEqual(
            (('b', 2), ('c', 2), ('b', 3), ('c', 3)),
            tuple(ip.point for ip in ips.get_largest_list()))

    def test_get_largest(self):
        ips = IntersectionPoints.create(self.provider)
        self.assertEqual(('b', 2), ips.get_largest().point)

        tprov = self._provider_to_get_largest()
        ips = IntersectionPoints.create(tprov)
        self.assertIn(ips.get_largest().point, (('b', 2), ('c', 2), ('b', 3), ('c', 3)))

    def test_parse_vectors(self):
        # 3 in row
        #  abcde
        # 1#####
        # 2#X#X#
        # 3#X#O#
        # 4##X##

        ips = IntersectionPoints.create(self.provider)
        self.assertEqual(19, len(ips.points))
        self.assertEqual(3, len(ips.points['c', 2]))
        self.assertEqual(4, len(ips.points['b', 2]))
        self.assertEqual(4, len(ips.points['b', 3]))
        self.assertEqual(3, len(ips.points['a', 1]))
        self.assertEqual(2, len(ips.points['d', 4]))
