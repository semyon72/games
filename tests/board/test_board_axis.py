# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-05 (y-m-d) 1:43 PM
from typing import Any
from unittest import TestCase

from games.board.axis import IAxis, IntAxis, Int1Axis, AsciiAxis, FixedAxis


class TestIAxis(TestCase):

    class _Axis(IAxis):

        def __init__(self, size: int):
            self.set_size(size)

        def get_max_size(self) -> int:
            return 15

        def __getitem__(self, i: int) -> Any:
            return True

    def test_misc(self):
        with self.assertRaises(ValueError):
            self._Axis(0)
        with self.assertRaises(ValueError):
            self._Axis(16)
        with self.assertRaises(ValueError):
            self._Axis('fgsf')

    def test_get_max_size(self):
        axis = self._Axis(3)
        self.assertEqual(15, axis.get_max_size())

    def test_set_size(self):
        axis = self._Axis(3)
        self.assertEqual(3, len(axis))
        axis.set_size(5)
        self.assertEqual(5, len(axis))
        with self.assertRaises(ValueError):
            axis.set_size(0)
        with self.assertRaises(ValueError):
            axis.set_size(16)


class TestIntAxis(TestCase):

    def setUp(self) -> None:
        self.axis = IntAxis(7)

    def test_all(self):
        with self.assertRaises(ValueError):
            IntAxis(1000000000)
        axis = IntAxis(1000000)
        self.assertEqual(999999, axis[999999])
        self.assertEqual(0, axis[0])
        with self.assertRaises(IndexError):
            axis[-1]
        with self.assertRaises(IndexError):
            axis[1000000]
        self.assertEqual(999999, axis.index(999999))
        self.assertIn(999999, axis)

    def test_get_max_size(self):
        self.assertEqual(self.axis.max_size, self.axis.get_max_size())
        self.axis.max_size = 1000
        self.assertEqual(self.axis.max_size, self.axis.get_max_size())

    def test_index(self):
        self.assertEqual(3, self.axis.index(3))
        with self.assertRaises(ValueError):
            self.axis.index(10)


class TestInt1Axis(TestCase):

    def test_all(self):
        with self.assertRaises(ValueError):
            Int1Axis(1000000000)
        axis = Int1Axis(1000000)
        self.assertEqual(1000000, axis[999999])
        self.assertEqual(999999, axis.index(1000000))
        with self.assertRaises(IndexError):
            axis[-1]
        with self.assertRaises(IndexError):
            axis[1000000]
        self.assertNotIn(1000001, axis)
        self.assertNotIn(0, axis)
        self.assertIn(45, axis)
        self.assertEqual(0, axis.index(1))
        self.assertEqual(1, axis[0])


class TestAsciiAxis(TestCase):

    def test_all(self):
        with self.assertRaises(ValueError):
            AsciiAxis(53)
        axis = AsciiAxis(52)
        self.assertEqual('Z', axis[51])
        self.assertEqual(51, axis.index('Z'))
        self.assertEqual('a', axis[0])
        self.assertEqual(3, axis.index('d'))
        self.assertEqual(27, axis.index('B'))
        with self.assertRaises(IndexError):
            axis[-1]
        with self.assertRaises(IndexError):
            axis[1000000]
        self.assertNotIn('$', axis)
        self.assertIn('f', axis)
        self.assertEqual(0, axis.index('a'))
        self.assertEqual('a', axis[0])

    def test_get_max_size(self):
        axis = AsciiAxis(5)
        self.assertEqual(52, axis.get_max_size())

    def test_index_to_char(self):
        axis = AsciiAxis(52)
        self.assertEqual('a', axis.index_to_char(0))
        self.assertEqual('Z', axis.index_to_char(51))
        self.assertEqual('C', axis.index_to_char(28))
        axis.set_size(7)
        with self.assertRaises(IndexError):
            axis.index_to_char(7)

    def test_index(self):
        axis = AsciiAxis(52)
        self.assertEqual(0, axis.index('a'))
        self.assertEqual(51, axis.index('Z'))
        self.assertEqual(28, axis.index('C'))
        with self.assertRaises(ValueError):
            axis.index('#')
        axis.set_size(7)
        with self.assertRaises(ValueError):
            axis.index('h')
        self.assertEqual(len(axis)-1, axis.index('g'))


class TestFixedAxis(TestCase):

    def setUp(self) -> None:
        self.test_sequence = (1, '2345', 3)

    def test_all(self):
        axis = FixedAxis(self.test_sequence)
        with self.assertRaises(ValueError):
            axis.set_size(5)
        self.assertEqual(3, len(axis))
        self.assertSequenceEqual(self.test_sequence, axis)

        self.assertEqual(3, axis[2])
        self.assertEqual(1, axis.index('2345'))
        self.assertEqual(1, axis[0])
        self.assertEqual(2, axis.index(3))
        with self.assertRaises(IndexError):
            axis[7]
        self.assertNotIn('$', axis)
        self.assertIn('2345', axis)
        self.assertEqual(0, axis.index(1))
        self.assertEqual(1, axis[0])

        axis.set_size(2)
        self.assertEqual(2, len(axis))
        with self.assertRaises(IndexError):
            axis[2]
        self.assertNotIn(3, axis)
        self.assertIn('2345', axis)
        with self.assertRaises(ValueError):
            axis.index(3)
        self.assertEqual(3, axis.get_max_size())

    def test_get_max_size(self):
        axis = FixedAxis(self.test_sequence)
        self.assertEqual(3, axis.get_max_size())
