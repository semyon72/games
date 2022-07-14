# IDE: PyCharm
# Project: games
# Path: ${DIR_PATH}
# File: ${FILE_NAME}
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-10 (y-m-d) 5:18 AM
from unittest import TestCase

from games.tictactoe.player import TicTacToePlayerX, TicTacToePlayerY

from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board, ConsoleRenderer
from tests.tictactoe.board_stubs import TicTacToeVectorProviderStub


class TestTicTacToeVectorProvider(TestCase):

    def setUp(self) -> None:
        self.provider_stub = TicTacToeVectorProviderStub()

    def test_provide(self):
        ttres = (*self.provider_stub.row_list, *self.provider_stub.col_list,
                 *self.provider_stub.diag_list, *self.provider_stub.diag_list_fwd)
        for v in self.provider_stub.provider.provide():
            self.assertIn(v, ttres)

    def test_iterable(self):
        ttres = (*self.provider_stub.row_list, *self.provider_stub.col_list,
                 *self.provider_stub.diag_list, *self.provider_stub.diag_list_fwd)
        for v in self.provider_stub.provider:
            self.assertIn(v, ttres)


class TestTicTacToePlayerX(TestCase):
    # 3 in row
    #  abcde
    # 1#####
    # 2#X#X#
    # 3#X#O#
    # 4##X##

    def setUp(self) -> None:
        tobj = TestTicTacToeVectorProvider()
        tobj._callSetUp()
        self.board = tobj.provider_stub.board
        self.player = TicTacToePlayerX(self.board)

    def test_board(self):
        self.assertIs(self.player.board, self.board)

    def test_cnt_in_row(self):
        self.assertEqual(3, self.player.cnt_in_row)

    def test_dynamical(self):
        axl, ayl, cntinrow = 3, 3, 3
        board = Board(AsciiAxis(axl), Int1Axis(ayl))
        player_x = TicTacToePlayerX(board, cntinrow)
        player_y = TicTacToePlayerY(board, cntinrow)
        renderer = ConsoleRenderer(board)

        for i in range(axl * ayl // 2):
            point = player_x.move_suggestion()
            player_x.play(*point)
            point = player_y.move_suggestion()
            player_y.play(*point)
            print('-----------')
            # resstr = _catch_stdout(renderer.render())
            renderer.render()

        point = player_x.move_suggestion()
        if point is not None:
            player_x.play(*point)
            print('-----------')
            renderer.render()
