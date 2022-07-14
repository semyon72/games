# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-02 (y-m-d) 8:42 AM
import string
from functools import partial
from typing import Iterable, Callable, Optional
from unittest import TestCase

from games.board.board1 import Board, ConsoleBoard, ConsoleRenderer, StandardBoard, IBoard, StandardConsoleBoard
from games.items.items import BoardItem
from tests.utils import _catch_stdout


class TestBoard(TestCase):

    def setUp(self) -> None:
        self.x = 7
        self.y = 5
        self.board: Board = Board(self.x, self.y)

    def test__relative_to_absolute_index(self):
        self.assertEqual(9, self.board._relative_to_absolute_index(3, 2))
        self.assertEqual(0, self.board._relative_to_absolute_index(1, 1))
        self.assertEqual(48, self.board._relative_to_absolute_index(7, 7))

    def test__validate_index(self):
        self.assertRaises(IndexError, self.board._validate_index, 7, 9)
        self.assertRaises(IndexError, self.board._validate_index, 7, -3)
        self.assertIs(None, self.board._validate_index(7, 1))

    def test_get_x_label(self):
        self.assertEqual('-7', self.board.get_x_label(-7))
        self.assertEqual('None', self.board.get_x_label(None))
        self.assertEqual('100', self.board.get_x_label(100))

    def test_get_y_label(self):
        self.assertEqual('-7', self.board.get_x_label(-7))
        self.assertEqual('None', self.board.get_x_label(None))
        self.assertEqual('100', self.board.get_x_label(100))

    def test__col_generator(self):
        col = self.board._col_generator(3)
        self.assertIsInstance(col, Iterable)
        tcol = tuple(col)
        self.assertEqual(self.board.y_size, len(tcol))

        with self.assertRaises(IndexError):
            tuple(self.board._col_generator(9))
        with self.assertRaises(IndexError):
            tuple(self.board._col_generator(-1))
        tcol = tuple(self.board._col_generator(7))
        self.assertEqual(self.board.y_size, len(tcol))

    def test__row_generator(self):
        row = self.board._row_generator(3)
        self.assertIsInstance(row, Iterable)
        trow = tuple(row)
        self.assertEqual(self.board.x_size, len(trow))

        with self.assertRaises(IndexError):
            tuple(self.board._row_generator(9))
        with self.assertRaises(IndexError):
            tuple(self.board._row_generator(-1))
        tcol = tuple(self.board._row_generator(5))
        self.assertEqual(self.board.x_size, len(trow))

    def _get_test_board(x, y, cls: IBoard = Board, renderer: Optional[Callable] = None):

        def _renderer(x: int, y: int) -> str:
            return TestBoard._get_test_board.render_format.format('[{x}:{y}]', x=x, y=y)

        b = cls(x, y)
        if renderer is None:
            renderer = _renderer

        for iy in range(1, y + 1):
            for ix in range(1, x + 1):
                bi = BoardItem(b, ix, iy)
                bi.render = partial(renderer, ix, iy)
                b[ix, iy] = bi
        return b

    _get_test_board.render_format = '[{x}:{y}]'
    _get_test_board = staticmethod(_get_test_board)

    def test_get_column(self):
        x, y = (7, 3)
        tb = self._get_test_board(x, y)
        col = 5
        items = tb.get_column(col)
        self.assertEqual(y, len(items))
        for iy, item in enumerate(items, 1):
            self.assertEqual(col, item.x)
            self.assertEqual(iy, item.y)
            self.assertEqual(str(col), item.x_label)
            self.assertEqual(str(iy), item.y_label)
            self.assertEqual(self._get_test_board.render_format.format(x=col, y=item.y), item.item.render())

    def test_get_row(self):
        x, y = (7, 3)
        tb = self._get_test_board(x, y)
        row = 3
        items = tb.get_row(row)
        self.assertEqual(x, len(items))
        for ix, item in enumerate(items, 1):
            self.assertEqual(row, item.y)
            self.assertEqual(ix, item.x)
            self.assertEqual(str(row), item.y_label)
            self.assertEqual(str(ix), item.x_label)
            self.assertEqual(self._get_test_board.render_format.format(x=item.x, y=row), item.item.render())

    def test_render(self):
        ...

    def test_getitem(self):
        self.assertIs(None, self.board[self.x, self.y])
        with self.assertRaises(IndexError):
            t = self.board[self.x, self.y + 1]

        x, y = (7, 3)
        tb = self._get_test_board(x, y)
        x, y = (3, 2)
        self.assertEqual(self._get_test_board.render_format.format(x=x, y=y), tb[x, y].render())

    def test_setitem(self):
        x, y, fmt_str = (7, 5, '[{x}:{y}]')

        bi = BoardItem(self.board, x, y)
        bi.render = partial(lambda slf: fmt_str.format(x=slf.x, y=slf.y), bi)
        self.assertEqual(fmt_str.format(x=x, y=y), bi.render())

        self.assertIs(bi, self.board[x, y])
        self.assertEqual(fmt_str.format(x=x, y=y), self.board[x, y].render())

        self.assertEqual(None, self.board[7, 3])

    def test_delitem(self):
        x, y = (2, 4)
        obi = self.board[x, y]
        self.assertIsNone(obi)
        bi = BoardItem(self.board, x, y)
        obi = self.board[x, y]
        self.assertIs(bi, obi)
        del self.board[x, y]
        self.assertIsNone(bi.board)
        self.assertIsNone(self.board[x, y])


class TestConsoleRenderer(TestCase):

    def setUp(self) -> None:
        self.x = 5
        self.y = 7
        self.board = TestBoard._get_test_board(
            self.x,
            self.y,
            renderer=lambda x, y: print(TestBoard._get_test_board.render_format.format('[{x}:{y}]', x=x, y=y), end='')
        )
        self.renderer = ConsoleRenderer(self.board)

    def test__render_header(self):
        rstr = _catch_stdout(self.renderer._render_header, self.board.get_row(1))
        self.assertEqual(" 12345", rstr)

    def test__render_row(self):
        rstr = _catch_stdout(self.renderer._render_row, self.board.get_row(7))
        self.assertEqual('7[1:7][2:7][3:7][4:7][5:7]', rstr)

    def test_render(self):
        board = Board(1, 0)
        renderer = ConsoleRenderer(board)
        rstr = _catch_stdout(renderer.render)
        self.assertEqual("", rstr)

        board = Board(self.x, self.y)
        renderer = ConsoleRenderer(board)
        rstr = _catch_stdout(renderer.render)
        self.assertEqual(
            " 12345\n1#####\n2#####\n3#####\n4#####\n5#####\n6#####\n7#####\n",
            rstr
        )

        rstr = _catch_stdout(self.renderer.render)
        self.assertEqual(
            " 12345\n"
            "1[1:1][2:1][3:1][4:1][5:1]\n"
            "2[1:2][2:2][3:2][4:2][5:2]\n"
            "3[1:3][2:3][3:3][4:3][5:3]\n"
            "4[1:4][2:4][3:4][4:4][5:4]\n"
            "5[1:5][2:5][3:5][4:5][5:5]\n"
            "6[1:6][2:6][3:6][4:6][5:6]\n"
            "7[1:7][2:7][3:7][4:7][5:7]\n",
            rstr
        )


class TestConsoleBoard(TestCase):

    def setUp(self) -> None:
        self.x = 4
        self.y = 3
        self.board = TestBoard._get_test_board(
            self.x,
            self.y,
            cls=ConsoleBoard,
            renderer=lambda x, y: print(TestBoard._get_test_board.render_format.format('[{x}:{y}]', x=x, y=y), end='')
        )

    def test_render(self):
        rstr = _catch_stdout(self.board.render)
        self.assertEqual(" 1234\n1[1:1][2:1][3:1][4:1]\n2[1:2][2:2][3:2][4:2]\n3[1:3][2:3][3:3][4:3]\n", rstr)


class TestStandardBoard(TestCase):
    render_fmt_str = '[{x}:{y}]'

    def setUp(self) -> None:
        self.board = StandardBoard(3, 5)

    def test_get_x_label(self):
        self.assertEqual('a', self.board.get_x_label(1))
        self.assertEqual('c', self.board.get_x_label(3))
        self.assertEqual('z', self.board.get_x_label(26))
        with self.assertRaises(IndexError):
            self.board.get_x_label(30)

    def test__char_to_index(self):
        self.assertEqual(1, self.board._char_to_index('a'))
        self.assertEqual(3, self.board._char_to_index('c'))
        with self.assertRaises(IndexError):
            self.assertEqual(26, self.board._char_to_index('z'))
        with self.assertRaises(ValueError):
            self.board._char_to_index('A')

    def test_getitem(self):
        self.assertIsNone(self.board['a', 1])

    def test_setitem(self):
        point = ('b', 4)
        self.assertIsNone(self.board[point])
        bi = BoardItem(self.board, *point)
        self.assertIs(bi, self.board[point])

    def test_delitem(self):
        point = ('c', 5)
        self.assertIsNone(self.board[point])
        bi = BoardItem(self.board, *point)
        self.assertIs(bi, self.board[point])
        del self.board[point]
        self.assertIsNone(self.board[point])
        self.assertIsNone(bi.board)

    def _get_test_board(self, x: int, y: int, cls: IBoard = StandardBoard):
        tb = cls(x, y)
        for iy in range(1, y + 1):
            for ix in StandardBoard.allow_chars[:x]:
                bi = BoardItem(tb, ix, iy)
                bi.render = partial(lambda x, y: print(self.render_fmt_str.format(x=x, y=y), end=''), ix, iy)
        return tb

    def test_get_column(self):
        x, y = (7, 3)
        tb = self._get_test_board(x, y)

        col = 'e'
        items = tb.get_column(col)
        self.assertEqual(y, len(items))
        for iy, item in enumerate(items, 1):
            self.assertEqual(tb._char_to_index(col), item.x)
            self.assertEqual(iy, item.y)
            self.assertEqual(col, item.x_label)
            self.assertEqual(str(iy), item.y_label)
            rstr = _catch_stdout(item.item.render)
            self.assertEqual(self.render_fmt_str.format(x=col, y=item.y), rstr)

    def test_get_row(self):
        x, y = (7, 3)
        tb = self._get_test_board(x, y)

        row = 3
        items = tb.get_row(row)
        self.assertEqual(x, len(items))
        for ix, item in enumerate(items):
            self.assertEqual(ix + 1, item.x)
            self.assertEqual(row, item.y)
            xchr = string.ascii_letters[ix]
            self.assertEqual(xchr, item.x_label)
            self.assertEqual(str(row), item.y_label)
            rstr = _catch_stdout(item.item.render)
            self.assertEqual(self.render_fmt_str.format(x=xchr, y=row), rstr)

    def test_render(self):
        x, y = (5, 3)

        b = StandardBoard(x, y)
        renderer = ConsoleRenderer(b)
        rstr = _catch_stdout(renderer.render)
        self.assertEqual(
            " abcde\n1#####\n2#####\n3#####\n",
            rstr
        )

        tb = self._get_test_board(x, y)
        renderer = ConsoleRenderer(tb)
        rstr = _catch_stdout(renderer.render)
        self.assertEqual(
            " abcde\n"
            "1[a:1][b:1][c:1][d:1][e:1]\n"
            "2[a:2][b:2][c:2][d:2][e:2]\n"
            "3[a:3][b:3][c:3][d:3][e:3]\n",
            rstr
        )


class TestStandardConsoleBoard(TestCase):

    render_fmt_str: str = TestStandardBoard.render_fmt_str

    def test_render(self):
        x, y = (5, 3)

        b = StandardConsoleBoard(x, y)
        rstr = _catch_stdout(b.render)
        self.assertEqual(
            " abcde\n1#####\n2#####\n3#####\n",
            rstr
        )

        tb = TestStandardBoard._get_test_board(self, x, y, cls=StandardConsoleBoard)
        rstr = _catch_stdout(tb.render)
        self.assertEqual(
            " abcde\n"
            "1[a:1][b:1][c:1][d:1][e:1]\n"
            "2[a:2][b:2][c:2][d:2][e:2]\n"
            "3[a:3][b:3][c:3][d:3][e:3]\n",
            rstr
        )
