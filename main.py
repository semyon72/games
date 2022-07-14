# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from games.board.axis import AsciiAxis, Int1Axis
from games.board.board import Board, ConsoleRenderer
from games.console import get_default_input, board_item_factory
from games.tictactoe.player import TicTacToePlayerX, TicTacToePlayerY


def main():
    # Some examples of use
    #
    # size_x = get_default_input('Enter "X-columns on board"', int, default=3)
    # size_y = get_default_input('Enter "Y-columns on board"', int, default=3)
    # board = Board(AsciiAxis(size_x), Int1Axis(size_y))
    # bi = BoardItem(board, 'a', 3, 'X')
    # board_item_factory(board, '&')(get_default_input('Enter "point on board"', default='b:2'))
    # ConsoleRenderer(board).render()
    # get_default_input('Enter "point on board"', board_item_factory(board, '@'), required=True)
    # ConsoleRenderer(board).render()
    # get_default_input('Enter "point on board"', board_item_factory(board, item_class=XItem), required=True)
    # ConsoleRenderer(board).render()

    size_x = get_default_input('Enter "X-columns on board"', int, default=3)
    size_y = get_default_input('Enter "Y-columns on board"', int, default=3)
    board = Board(AsciiAxis(size_x), Int1Axis(size_y))
    cnt_in_row = get_default_input('Enter "number of X or O in row for win"', int, default=3)
    player_x = TicTacToePlayerX(board, cnt_in_row)
    player_y = TicTacToePlayerY(board, cnt_in_row)
    renderer = ConsoleRenderer(board)
    while next_x := player_x.move_suggestion():
        renderer.render()
        next_x = get_default_input(
            'Next move ',
            board_item_factory(player_x.board, item_class=player_x.item_class),
            default=f'{next_x[0]}:{next_x[1]}'
        )
        player_x.play(next_x)
        next_y = player_y.move_suggestion()
        if next_y:
            player_y.play(*next_y)

    get_default_input('Game over.', str, default="Enter")


if __name__ == '__main__':
    main()
