# IDE: PyCharm
# Project: games
# Path: tests/vector
# File: test_intersection.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-20 (y-m-d) 9:34 AM
from unittest import TestCase

from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board, ConsoleRenderer
from games.items.items import XItem
from games.tictactoe.vector import TicTacToeVectorProvider
from games.vector.intersection import IntersectionPoint, IntersectionPoints
from tests.utils import _catch_stdout


class TestIntersectionPoint(TestCase):

    def setUp(self) -> None:
        #  abcde
        # 1#####
        # 2#####
        # 3#####
        # 4#####
        self.board = Board(AsciiAxis(5), Int1Axis(4))
        rstr = " abcde\n1#####\n2#####\n3#####\n4#####\n"
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(self.board).render))
        self.provider = TicTacToeVectorProvider(self.board, XItem.id, 1)

    def _init_intersection_point(self):
        self.intersection_point = IntersectionPoint(('a', 1))
        for v in self.provider.provide():
            self.intersection_point.add(v)

    def test_clear(self):
        self._init_intersection_point()
        self.assertEqual(4, len(self.intersection_point))
        self.intersection_point.clear()
        self.assertEqual(0, len(self.intersection_point))

    def test_add(self):
        p = ('c', 2)
        ip = IntersectionPoint(p)
        tres = []
        for v in self.provider.provide():
            ip.add(v)
            if p in v:
                tres.append(v)
        self.assertListEqual(tres, ip.vectors)

    def test_length(self):
        self._init_intersection_point()
        self.assertEqual(4, len(self.intersection_point))


class TestIntersectionPoints(TestCase):

    def setUp(self) -> None:
        tobj = TestIntersectionPoint()
        tobj._callSetUp()
        self.provider = tobj.provider

    def test_get_largest_list(self):
        ips = IntersectionPoints.create(self.provider)
        self.assertTupleEqual((('c', 2), ('c', 3)), tuple(ip.point for ip in ips.get_largest_list()))

    def test_get_largest(self):
        ips = IntersectionPoints.create(self.provider)
        self.assertIn(ips.get_largest().point, (('c', 2), ('c', 3)))

    def test_parse_vectors(self):
        #  abcde
        # 1#####
        # 2#####
        # 3#####
        # 4#####

        ips = IntersectionPoints.create(self.provider)
        self.assertEqual(20, len(ips.points))
        self.assertEqual(4, len(ips.points['a', 1]))
        self.assertEqual(4, len(ips.points['a', 4]))
        self.assertEqual(4, len(ips.points['e', 1]))
        self.assertEqual(4, len(ips.points['e', 4]))
        self.assertEqual(4, len(ips.points['b', 2]))
        self.assertEqual(4, len(ips.points['c', 2]))
