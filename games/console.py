# IDE: PyCharm
# Project: games
# Path: 
# File: console.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-09 (y-m-d) 10:40 AM

from typing import Optional, Callable, Any, Type

from .board.axis import IntAxis
from .board.board import IBoard
from .items.items import BoardItem

RETURN_COMMAND = '-ret'


def get_default_input(msg: str, factory: Callable[[Any], Any] = str,
                      default: Any = None, return_command: str = RETURN_COMMAND, required: bool = False):
    while True:
        res = input('%s [%s]:' % (msg, default))
        if res == return_command:
            return factory(default)

        if default is None and res == '' and required:
            print('Value is required')
            continue

        if res:
            try:
                res = factory(res)
            except (ValueError, IndexError) as err:
                print(err)
            else:
                return res
        else:
            return factory(default)


def board_item_factory(
        board: IBoard,
        *args,
        item_class: Type[BoardItem] = BoardItem,
        **kwargs) -> Callable[[str], BoardItem]:

    def detect_axis(s: str) -> BoardItem:
        x, y = map(lambda v: v.strip(), s.split(':'))
        if isinstance(board.axis_x, IntAxis):
            x = int(x)
        if isinstance(board.axis_y, IntAxis):
            y = int(y)
        return item_class(board, x, y, *args, **kwargs)

    return detect_axis
