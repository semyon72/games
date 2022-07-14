# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-08 (y-m-d) 6:20 PM

from tests.utils import _catch_stdout

from unittest import TestCase

from games.board.axis import AsciiAxis, Int1Axis, IntAxis, FixedAxis
from games.board.board import Board, ConsoleRenderer, HTMLRenderer
from games.items.items import BoardItem


class TestBoard(TestCase):

    def setUp(self) -> None:
        self.std_board = Board(AsciiAxis(5), Int1Axis(3))
        self.item_c2 = BoardItem(self.std_board, 'c', 2)

    def test_axis_x(self):
        self.assertSequenceEqual('abcde', self.std_board.axis_x)

    def test_axis_y(self):
        self.assertSequenceEqual((1, 2, 3), self.std_board.axis_y)

    def test__validate_index(self):
        self.assertIsNone(self.std_board._validate_index('b', 3))
        with self.assertRaises(IndexError):
            self.std_board._validate_index('t', 3)

    def test_index(self):
        c2 = self.std_board.index(self.item_c2)
        self.assertEqual(('c', 2), c2)
        with self.assertRaises(ValueError):
            self.std_board.index(object())

    def test_get_column(self):
        self.assertEqual((None, self.item_c2, None), self.std_board.get_column('c'))

    def test_get_row(self):
        self.assertEqual((None, None,self.item_c2, None, None), self.std_board.get_row(2))


class TestConsoleRenderer(TestCase):

    def setUp(self) -> None:
        self.std_board = Board(AsciiAxis(5), Int1Axis(3))
        self.item_c2 = BoardItem(self.std_board, 'c', 2)
        self.renderer = ConsoleRenderer(self.std_board)

    def test__render_header(self):
        rstr = _catch_stdout(self.renderer._render_header)
        self.assertEqual(' abcde', rstr)

    def test_render(self):
        rstr = _catch_stdout(self.renderer.render)
        self.assertEqual(' abcde\n1#####\n2##?##\n3#####\n', rstr)

    def test_misc(self):
        b = Board(AsciiAxis(5), Int1Axis(3))
        bi = BoardItem(b, 'c', 2)
        bi = BoardItem(b, 'a', 1)
        bi = BoardItem(b, 'e', 3)
        # Should be
        rstr = ' abcde\n1?####\n2##?##\n3####?\n'
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(b).render))

        b = Board(AsciiAxis(5), IntAxis(3))
        bi = BoardItem(b, 'c', 1)
        bi = BoardItem(b, 'a', 0)
        bi = BoardItem(b, 'e', 2)
        # Should be
        rstr = ' abcde\n0?####\n1##?##\n2####?\n'
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(b).render))

        b = Board(Int1Axis(3), FixedAxis(('aa', 'bb', 'cc')))
        bi = BoardItem(b, 2, 'bb')
        bi = BoardItem(b, 1, 'aa')
        bi = BoardItem(b, 3, 'cc')
        # Should be
        rstr = ' 123\naa?##\nbb#?#\ncc##?\n'
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(b).render))

        b = Board(IntAxis(3), FixedAxis(('aa', 'bb', 'cc')))
        bi = BoardItem(b, 1, 'bb')
        bi = BoardItem(b, 0, 'aa')
        bi = BoardItem(b, 2, 'aa')
        # Should be
        rstr = ' 012\naa?#?\nbb#?#\ncc###\n'
        self.assertEqual(rstr, _catch_stdout(ConsoleRenderer(b).render))


class TestHTMLRenderer(TestCase):

    def setUp(self) -> None:
        self.std_board = Board(AsciiAxis(5), Int1Axis(3))
        self.item_c2 = BoardItem(self.std_board, 'c', 2)
        self.renderer = HTMLRenderer(self.std_board)

    def test__render_header(self):
        rstr = str(self.renderer._render_header())
        self.assertEqual('<tr><th>&nbsp;</th><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr>', rstr)

    def test_render(self):
        rstr = self.renderer.render()
        tstr = '<table><tr><th>&nbsp;</th><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr><tr><th>1</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>2</th><td>&nbsp;</td><td>&nbsp;</td><td>?</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>3</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>'
        self.assertEqual(tstr, rstr)

    def test_misc(self):
        b = Board(AsciiAxis(5), Int1Axis(3))
        bi = BoardItem(b, 'c', 2)
        bi = BoardItem(b, 'a', 1)
        bi = BoardItem(b, 'e', 3)
        # Should be
        rstr = '<table><tr><th>&nbsp;</th><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr><tr><th>1</th><td>?</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>2</th><td>&nbsp;</td><td>&nbsp;</td><td>?</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>3</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>?</td></tr></table>'
        self.assertEqual(rstr, HTMLRenderer(b).render())

        b = Board(AsciiAxis(5), IntAxis(3))
        bi = BoardItem(b, 'c', 1)
        bi = BoardItem(b, 'a', 0)
        bi = BoardItem(b, 'e', 2)
        # Should be
        rstr = '<table><tr><th>&nbsp;</th><th>a</th><th>b</th><th>c</th><th>d</th><th>e</th></tr><tr><th>0</th><td>?</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>1</th><td>&nbsp;</td><td>&nbsp;</td><td>?</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>2</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>?</td></tr></table>'
        self.assertEqual(rstr, HTMLRenderer(b).render())

        b = Board(Int1Axis(3), FixedAxis(('aa', 'bb', 'cc')))
        bi = BoardItem(b, 2, 'bb')
        bi = BoardItem(b, 1, 'aa')
        bi = BoardItem(b, 3, 'cc')
        # Should be
        rstr = '<table><tr><th>&nbsp;</th><th>1</th><th>2</th><th>3</th></tr><tr><th>aa</th><td>?</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><th>bb</th><td>&nbsp;</td><td>?</td><td>&nbsp;</td></tr><tr><th>cc</th><td>&nbsp;</td><td>&nbsp;</td><td>?</td></tr></table>'
        self.assertEqual(rstr, HTMLRenderer(b).render())

        b = Board(IntAxis(3), FixedAxis(('aa', 'bb', 'cc')))
        bi = BoardItem(b, 1, 'bb')
        bi = BoardItem(b, 0, 'aa')
        bi = BoardItem(b, 2, 'aa')
        # Should be
        rstr = '<table><tr><th>&nbsp;</th><th>0</th><th>1</th><th>2</th></tr><tr><th>aa</th><td>?</td><td>&nbsp;</td><td>?</td></tr><tr><th>bb</th><td>&nbsp;</td><td>?</td><td>&nbsp;</td></tr><tr><th>cc</th><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>'
        self.assertEqual(rstr, HTMLRenderer(b).render())
