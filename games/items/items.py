# IDE: PyCharm
# Project: games
# Path: 
# File: items.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-05-31 (y-m-d) 5:26 PM

from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Protocol

TPointX = TypeVar('TPointX', str, int)
TPointY = TypeVar('TPointY', str, int)
TPoint = tuple[TPointX, TPointY]


class PItem(Protocol):
    id: str
    x: TPointX
    y: TPointY

    @abstractmethod
    def render(self):
        raise NotImplementedError


@dataclass
class BoardItem(PItem):
    board: 'IBoard'
    x: TPointX
    y: TPointY
    id: str = '?'

    def __post_init__(self):
        self.board[self.x, self.y] = self

    def render(self):
        print(str(self.id), end='')


class ItemTriesToOccupyOccupiedPointError(Exception):

    def __init__(self, item: BoardItem, *args: object) -> None:
        self.item: BoardItem = item
        super().__init__(f'Item \'{self.item.id}\' tries to occupy an occupied point [{self.item.x}:{self.item.y}]')


@dataclass
class XItem(BoardItem):
    id: str = 'X'

    def __post_init__(self):
        if self.board[self.x, self.y] is None:
            super(XItem, self).__post_init__()
        else:
            raise ItemTriesToOccupyOccupiedPointError(self)


@dataclass
class OItem(XItem):
    id: str = 'O'


class ShipItem(BoardItem):
    state_char = {'live': '\u2610', 'dead': '', 'shoot': ''}


class ShipItemGroup:
    pass
