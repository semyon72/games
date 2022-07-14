# IDE: PyCharm
# Project: games
# Path: 
# File: board.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-05-31 (y-m-d) 5:26 PM

import string
from abc import abstractmethod
from collections import namedtuple
from typing import Optional, Iterable, Sequence

from ..items.items import BoardItem
from ..renderer.renderer import IRender, CharRender, NewLineCharRender


BoardItemInfo = namedtuple('BoardItemInfo', ('x', 'x_label', 'y', 'y_label', 'item'))


class IBoard(Sequence):

    @property
    @abstractmethod
    def x_size(self) -> int:
        ...

    @property
    @abstractmethod
    def y_size(self) -> int:
        ...

    @abstractmethod
    def get_x_label(self, x) -> str:
        ...

    @abstractmethod
    def get_y_label(self, y) -> str:
        ...

    @abstractmethod
    def get_column(self, x: int) -> tuple[Optional[BoardItemInfo]]:
        ...

    @abstractmethod
    def get_row(self, y: int) -> tuple[Optional[BoardItemInfo]]:
        ...


class Board(IBoard):
    """
        All of index x and y is friendly and starts from 1
        ------1-------2-3-------------------> x
        1 x=1; y=1
        |
        |
        \/
        y

    """
    header_info_class = BoardItemInfo

    def __init__(self, x_size: int, y_size: int):
        self.__x_size, self.__y_size = (x_size, y_size)
        self.__items: list[Optional[BoardItem]] = [None for _ in range(x_size * y_size)]

    def __len__(self) -> int:
        return self.x_size * self.y_size

    @property
    def x_size(self):
        return self.__x_size

    @property
    def y_size(self):
        return self.__y_size

    @property
    def items(self):
        return self.__items

    def _validate_index(self, x: int, y: int) -> None:
        min_idx = 1
        for xy, size, axis in ((x, self.x_size, 'x'), (y, self.y_size, 'y')):
            if xy > size:
                raise IndexError(f"index of '{axis}' exceeds max available '{size}': {xy}")
            if min_idx > xy:
                raise IndexError(f"index of '{axis}' less than '{min_idx}': {xy}")

    def _relative_to_absolute_index(self, x: int, y: int) -> int:
        """convert the human-readable index (starts from 1 for sake) to absolute index in side self.items"""
        return self.x_size*(y-1)+x-1

    def __getitem__(self, key: tuple[int, int]) -> Optional[BoardItem]:
        """
            Index starts from 1 for sake.
            Also, it does index range checking and throw IndexError if result of checking was negative.
        """
        x, y = key
        self._validate_index(x, y)
        return self.items[self._relative_to_absolute_index(x, y)]

    def __delitem__(self, key: tuple[int, int]):
        x, y = key
        old = self[x, y]
        if old is not None:
            old.board = None
        idx = self._relative_to_absolute_index(x, y)
        self.items[idx] = None

    def __setitem__(self, key: tuple[int, int], item: BoardItem):
        x, y = key
        del self[x, y]
        idx = self._relative_to_absolute_index(x, y)
        item.board = self
        item.x = x
        item.y = y
        self.items[idx] = item

    def get_x_label(self, x) -> str:
        return str(x)

    def get_y_label(self, y) -> str:
        return str(y)

    def _col_generator(self, x: int) -> Iterable[Optional[BoardItemInfo]]:
        self._validate_index(x, 1)
        start_abs_idx = self._relative_to_absolute_index(x, 1)
        r = range(start_abs_idx, len(self.items), self.x_size)  # for column
        x_label = self.get_x_label(x)
        for y0, abs_idx in enumerate(r):
            yield self.header_info_class(
                y=y0+1,
                y_label=self.get_y_label(y0+1),
                x=x,
                x_label=x_label,
                item=self.items[abs_idx]
            )

    def _row_generator(self, y: int) -> Iterable[Optional[BoardItemInfo]]:
        self._validate_index(1, y)
        start_abs_idx = self._relative_to_absolute_index(1, y)
        r = range(start_abs_idx, start_abs_idx + self.x_size)  # for row when xory is y
        y_label = self.get_y_label(y)
        for x0, abs_idx in enumerate(r):
            yield self.header_info_class(
                x=x0+1,
                x_label=self.get_x_label(x0+1),
                y=y,
                y_label=y_label,
                item=self.items[abs_idx]
            )

    def get_column(self, x: int) -> tuple[Optional[BoardItemInfo]]:
        return tuple(self._col_generator(x))

    def get_row(self, y: int) -> tuple[Optional[BoardItemInfo]]:
        return tuple(self._row_generator(y))


class ConsoleRenderer(IRender):

    empty_item_renderer = CharRender('#')

    def __init__(self, board: IBoard):
        self.board = board

    def _render_header(self, row: Iterable[BoardItemInfo]):
        # render x header
        for i, info in enumerate(row):
            if i == 0:
                CharRender(' ').render()
            CharRender(info.x_label).render()

    def _render_row(self, row: Iterable[BoardItemInfo]):
        # render rows, row header is included
        for i, info in enumerate(row):
            if i == 0:
                CharRender(info.y_label).render()
            if info.item is None:
                self.empty_item_renderer.render()
            else:
                info.item.render()

    def render(self):
        for y in range(self.board.y_size):
            row = self.board.get_row(y+1)
            if y == 0:
                self._render_header(row)
                NewLineCharRender().render()
            self._render_row(row)
            NewLineCharRender().render()


class ConsoleBoard(Board, IRender):

    def render(self):
        ConsoleRenderer(self).render()


class StandardBoard(IBoard):

    allow_chars: tuple[str] = tuple(chr for chr in string.ascii_lowercase)

    def __init__(self, x_size: int, y_size: int):
        self.board: IBoard = Board(x_size, y_size)
        self.board.get_x_label = self.get_x_label

    @property
    def x_size(self):
        return self.board.y_size

    @property
    def y_size(self):
        return self.board.y_size

    def _char_to_index(self, cx: str) -> int:
        idx = self.allow_chars.index(cx) + 1
        if idx > self.board.x_size:
            raise IndexError(f'character "{cx}" out of allowed by size "{self.board.x_size}" for this board')
        return idx

    def get_x_label(self, x) -> str:
        return self.allow_chars[x-1]

    def get_y_label(self, y) -> str:
        return self.board.get_y_label(y)

    def __len__(self) -> int:
        return len(self.board)

    def __getitem__(self, key: tuple[str, int]):
        x, y = (self._char_to_index(key[0]), key[1])
        return self.board[x, y]

    def __setitem__(self, key: tuple[str, int], item: BoardItem):
        x, y = (self._char_to_index(key[0]), key[1])
        self.board[x, y] = item

    def __delitem__(self, key: tuple[str, int]):
        x, y = (self._char_to_index(key[0]), key[1])
        del self.board[x, y]

    def get_column(self, cx: str) -> tuple[Optional[BoardItemInfo]]:
        return self.board.get_column(self._char_to_index(cx))

    def get_row(self, y: int) -> tuple[Optional[BoardItemInfo]]:
        return self.board.get_row(y)

    def render(self):
        pass


class StandardConsoleBoard(StandardBoard, IRender):

    def render(self):
        ConsoleRenderer(self).render()
