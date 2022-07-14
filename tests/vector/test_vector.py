# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-15 (y-m-d) 9:24 PM
from unittest import TestCase

from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board
from games.vector.vector import (HorizontalVectorPoints, VerticalVectorPoints, BackDiagonalVectorPoints,
                                 ForwardDiagonalVectorPoints, RowVectorProvider, ColumnVectorProvider,
                                 DiagonalsVectorProvider, ForwardDiagonalVectorProvider, BackDiagonalVectorProvider)
from games.vector.intersection import IntersectionPoint


class TestHorizontalVectorPoints(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(5), Int1Axis(4))

    def test_get_points(self):
        # test itself point -> deep = 0
        points = HorizontalVectorPoints(self.board, 'a', 1, 0)
        self.assertListEqual(points.get_points(), [('a', 1)])

        # test itself point + one point on right side -> deep = 1 by default
        points = HorizontalVectorPoints(self.board, 'a', 1)
        self.assertListEqual(points.get_points(), [('a', 1), ('b', 1)])

        # test start point out of axis range
        points = HorizontalVectorPoints(self.board, 'f', 1)
        with self.assertRaises(ValueError) as vr:
            points.get_points()
        self.assertEqual(
            vr.exception.args[0],
            'The vector point is outside the range of the axis. Char should be in range [a..e]: f'
        )

        # test last point in board row -> deep = 0
        points = HorizontalVectorPoints(self.board, 'e', 1, 0)
        self.assertListEqual(points.get_points(), [('e', 1)])

        # test attempt to out of range start from last point in board row -> deep = 1 by default
        points = HorizontalVectorPoints(self.board, 'e', 1)
        self.assertListEqual(points.get_points(), [])

        # test all points in row -> deep = -1
        points = HorizontalVectorPoints(self.board, 'a', 1, -1)
        self.assertListEqual(points.get_points(), [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1)])

        # test all points in row -> deep = 3
        points = HorizontalVectorPoints(self.board, 'a', 1, 3)
        self.assertListEqual(points.get_points(), [('a', 1), ('b', 1), ('c', 1), ('d', 1)])


class TestVerticalVectorPoints(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(5), Int1Axis(4))

    def test_get_points(self):
        """ Vertical testing """

        # test itself point -> deep = 0
        points = VerticalVectorPoints(self.board, 'a', 1, 0)
        self.assertListEqual(points.get_points(), [('a', 1)])

        # test itself point + one point on right side -> deep = 1 by default
        points = VerticalVectorPoints(self.board, 'a', 1)
        self.assertListEqual(points.get_points(), [('a', 1), ('a', 2)])

        # test start point out of axis range
        points = VerticalVectorPoints(self.board, 'e', 5)
        with self.assertRaises(ValueError) as vr:
            points.get_points()
        self.assertEqual(
            vr.exception.args[0],
            'The vector point is outside the range of the axis. 5 is not in range'
        )

        # test last point in board row -> deep = 0
        points = VerticalVectorPoints(self.board, 'e', 4, 0)
        self.assertListEqual(points.get_points(), [('e', 4)])

        # test attempt to out of range start from last point in board row -> deep = 1 by default
        points = VerticalVectorPoints(self.board, 'e', 3, 2)
        self.assertListEqual(points.get_points(), [])

        # test all points in row -> deep = -1
        points = VerticalVectorPoints(self.board, 'a', 1, -1)
        self.assertListEqual(points.get_points(), [('a', 1), ('a', 2), ('a', 3), ('a', 4)])


class TestBackDiagonalVectorPoints(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(5), Int1Axis(4))

    def test_get_points(self):
        """Back diagonal testing"""

        # test itself point -> deep = 0
        points = BackDiagonalVectorPoints(self.board, 'a', 1, 0)
        self.assertListEqual(points.get_points(), [('a', 1)])

        # test itself point + one point on right side -> deep = 1 by default
        points = BackDiagonalVectorPoints(self.board, 'a', 1)
        self.assertListEqual(points.get_points(), [('a', 1), ('b', 2)])

        # test start point out of axis range
        points = BackDiagonalVectorPoints(self.board, 'e', 5)
        with self.assertRaises(ValueError) as vr:
            points.get_points()
        self.assertEqual(
            vr.exception.args[0],
            'The vector point is outside the range of the axis. 5 is not in range'
        )

        # test last point in board row -> deep = 0
        points = BackDiagonalVectorPoints(self.board, 'e', 4, 0)
        self.assertListEqual(points.get_points(), [('e', 4)])

        # test attempt to out of range start from last point in board row -> deep = 1 by default
        points = BackDiagonalVectorPoints(self.board, 'e', 3, 2)
        self.assertListEqual(points.get_points(), [])

        # test all points in row -> deep = -1
        points = BackDiagonalVectorPoints(self.board, 'a', 1, -1)
        self.assertListEqual(points.get_points(), [('a', 1), ('b', 2), ('c', 3), ('d', 4)])

        # test all points in row -> deep = -1
        points = BackDiagonalVectorPoints(self.board, 'b', 1, -1)
        self.assertListEqual(points.get_points(), [('b', 1), ('c', 2), ('d', 3), ('e', 4)])


class TestForwardDiagonalVectorPoints(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(5), Int1Axis(4))

    def test_get_points(self):
        """Forward giagonal testing"""

        # test itself point -> deep = 0
        point = ForwardDiagonalVectorPoints(self.board, 'a', 1, 0)
        self.assertListEqual(point.get_points(), [('a', 1)])

        # test itself point + one point on left side -> deep = 1 by default
        point = ForwardDiagonalVectorPoints(self.board, 'e', 3)
        self.assertListEqual(point.get_points(), [('e', 3), ('d', 4)])

        # test start point out of axis range
        point = ForwardDiagonalVectorPoints(self.board, 'f', 3)
        with self.assertRaises(ValueError) as vr:
            point.get_points()
        self.assertEqual(
            vr.exception.args[0],
            'The vector point is outside the range of the axis. Char should be in range [a..e]: f'
        )

        # test last point in board row -> deep = 0
        point = ForwardDiagonalVectorPoints(self.board, 'a', 4, 0)
        self.assertListEqual(point.get_points(), [('a', 4)])

        # test attempt to out of range start from last point in board row -> deep = 1 by default
        point = ForwardDiagonalVectorPoints(self.board, 'e', 3, 2)
        self.assertListEqual(point.get_points(), [])

        # test all points in row -> deep = -1
        point = ForwardDiagonalVectorPoints(self.board, 'e', 1, -1)
        self.assertListEqual(point.get_points(), [('e', 1), ('d', 2), ('c', 3), ('b', 4)])

        # test all points in row -> deep = -1
        point = ForwardDiagonalVectorPoints(self.board, 'c', 2, -1)
        self.assertListEqual(point.get_points(), [('c', 2), ('b', 3), ('a', 4)])


class TestRowVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = RowVectorProvider(Board(AsciiAxis(5), Int1Axis(4)))

    def test_provide(self):
        tres = [
            {('a', 1): None, ('b', 1): None, ('c', 1): None, ('d', 1): None, ('e', 1): None},
            {('a', 2): None, ('b', 2): None, ('c', 2): None, ('d', 2): None, ('e', 2): None},
            {('a', 3): None, ('b', 3): None, ('c', 3): None, ('d', 3): None, ('e', 3): None},
            {('a', 4): None, ('b', 4): None, ('c', 4): None, ('d', 4): None, ('e', 4): None}
        ]
        for i, v in enumerate(self.provider):
            self.assertDictEqual(tres[i], v)


class TestColumnVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = ColumnVectorProvider(Board(AsciiAxis(5), Int1Axis(4)))

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


class TestBackDiagonalVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = BackDiagonalVectorProvider(Board(AsciiAxis(5), Int1Axis(4)))

    def test_provide_start_points(self):
        tres = [('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1), ('a', 2), ('a', 3), ('a', 4)]
        self.assertListEqual(tres, list(self.provider.provide_start_points()))


class TestForwardDiagonalVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = ForwardDiagonalVectorProvider(Board(AsciiAxis(5), Int1Axis(4)))

    def test_provide_start_points(self):
        tres = [('e', 1), ('d', 1), ('c', 1), ('b', 1), ('a', 1), ('e', 2), ('e', 3), ('e', 4)]
        self.assertListEqual(tres, list(self.provider.provide_start_points()))


class TestDiagonalsVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider = DiagonalsVectorProvider(Board(AsciiAxis(5), Int1Axis(4)))

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
        self.assertListEqual(tres, self.provider.provide())


class TestIntersectionPoint(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(5), Int1Axis(4))
        self.provider = (
            *RowVectorProvider(self.board),
            *ColumnVectorProvider(self.board),
            *DiagonalsVectorProvider(self.board)
        )
        self._init_intersection_point()

    def _init_intersection_point(self):
        self.intersection_point = IntersectionPoint(('a', 1))
        for v in self.provider:
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
        for v in self.provider:
            ip.add(v)
            if p in v:
                tres.append(v)
        self.assertListEqual(tres, ip.vectors)

    def test_count(self):
        self._init_intersection_point()
        self.assertEqual(4, len(self.intersection_point))
