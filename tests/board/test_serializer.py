# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-22 (y-m-d) 11:30 AM
from unittest import TestCase

from games.board.axis import AsciiAxis, Int1Axis
from games.board.serializer import Board, JSONBoardSerializer
from games.items.items import XItem, OItem, BoardItem


class TestJSONBoardSerializer(TestCase):

    def setUp(self) -> None:
        self.board = Board(AsciiAxis(3), Int1Axis(2))
        self.x_item = XItem(self.board, 'a', 1)
        self.o_item = OItem(self.board, 'c', 2)
        self.board_item = BoardItem(self.board, 'b', 2)
        self.serializer: JSONBoardSerializer = JSONBoardSerializer(self.board)

    def test__dumps_axis(self):
        res = self.serializer._dumps_axis(self.board.axis_x)
        self.assertEqual('{"class": "games.board.axis.AsciiAxis", "args": [3], "kwargs": {}}', res)
        res = self.serializer._dumps_axis(self.board.axis_y)
        self.assertEqual('{"class": "games.board.axis.Int1Axis", "args": [2], "kwargs": {}}', res)

    def test__loads_axis(self):
        res = self.serializer._loads_axis('{"class": "games.board.axis.AsciiAxis", "args": [3], "kwargs": {}}')
        self.assertEqual(3, len(res))
        self.assertIs(AsciiAxis, type(res))

        res = self.serializer._loads_axis('{"class": "games.board.axis.Int1Axis", "args": [2], "kwargs": {}}')
        self.assertEqual(2, len(res))
        self.assertIs(Int1Axis, type(res))

    def test__dumps_board(self):
        res = self.serializer._dumps_board()
        tstr = '{"class": "games.board.board.Board", ' \
               '"args": [' \
               '"{\\"class\\": \\"games.board.axis.AsciiAxis\\", \\"args\\": [3], \\"kwargs\\": {}}", ' \
               '"{\\"class\\": \\"games.board.axis.Int1Axis\\", \\"args\\": [2], \\"kwargs\\": {}}"' \
               '], "kwargs": {}}'
        self.assertEqual(tstr, res)

    def test__loads_board(self):
        tstr = '{"class": "games.board.board.Board", ' \
               '"args": [' \
               '"{\\"class\\": \\"games.board.axis.AsciiAxis\\", \\"args\\": [3], \\"kwargs\\": {}}", ' \
               '"{\\"class\\": \\"games.board.axis.Int1Axis\\", \\"args\\": [2], \\"kwargs\\": {}}"' \
               '], "kwargs": {}}'
        res = self.serializer._loads_board(tstr)
        self.assertIs(Board, type(res))
        self.assertIs(AsciiAxis, type(res.axis_x))
        self.assertEqual(3, len(res.axis_x))
        self.assertIs(Int1Axis, type(res.axis_y))
        self.assertEqual(2, len(res.axis_y))

    def test__dumps_item(self):
        res = self.serializer._dumps_item(self.o_item)
        self.assertEqual(f'{{"class": "games.items.items.OItem", '
                         f'"args": [], '
                         f'"kwargs": {{"x": "{self.o_item.x}", "y": {self.o_item.y}}}}}', res)
        res = self.serializer._dumps_item(self.x_item)
        self.assertEqual('{"class": "games.items.items.XItem", "args": [], "kwargs": {"x": "a", "y": 1}}', res)
        res = self.serializer._dumps_item(self.board_item)
        self.assertEqual('{"class": "games.items.items.BoardItem", "args": [], "kwargs": {"x": "b", "y": 2}}', res)

    def test__loads_item(self):
        board = Board(AsciiAxis(3), Int1Axis(2))
        res = self.serializer._loads_item(
            board,
            '{"class": "games.items.items.XItem", "args": [], "kwargs": {"x": "a", "y": 1}}'
        )
        self.assertIs(XItem, type(res))
        self.assertIs(board['a', 1], res)

    def test_dumps(self):
        res = self.serializer.dumps()
        tstr = '{"class": "games.board.board.Board", ' \
               '"args": ["{\\"class\\": \\"games.board.axis.AsciiAxis\\", \\"args\\": [3], \\"kwargs\\": {}}", ' \
               '"{\\"class\\": \\"games.board.axis.Int1Axis\\", \\"args\\": [2], \\"kwargs\\": {}}"], ' \
               '"kwargs": {}}\n' \
               '{"class": "games.items.items.XItem", "args": [], "kwargs": {"x": "a", "y": 1}}\n' \
               '{"class": "games.items.items.OItem", "args": [], "kwargs": {"x": "c", "y": 2}}\n' \
               '{"class": "games.items.items.BoardItem", "args": [], "kwargs": {"x": "b", "y": 2}}'
        self.assertEqual(tstr, res)

    def test_loads(self):
        tstr = '{"class": "games.board.board.Board", ' \
               '"args": ["{\\"class\\": \\"games.board.axis.AsciiAxis\\", \\"args\\": [3], \\"kwargs\\": {}}", ' \
               '"{\\"class\\": \\"games.board.axis.Int1Axis\\", \\"args\\": [2], \\"kwargs\\": {}}"], ' \
               '"kwargs": {}}\n' \
               '{"class": "games.items.items.XItem", "args": [], "kwargs": {"x": "a", "y": 1}}\n' \
               '{"class": "games.items.items.OItem", "args": [], "kwargs": {"x": "c", "y": 2}}\n' \
               '{"class": "games.items.items.BoardItem", "args": [], "kwargs": {"x": "b", "y": 2}}'

        board = self.serializer.loads(tstr).board
        self.assertIs(Board, type(board))
        self.assertIs(type(board['a', 1]), XItem)
        self.assertIs(type(board['c', 2]), OItem)
        self.assertIs(type(board['b', 2]), BoardItem)
