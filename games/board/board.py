# IDE: PyCharm
# Project: games
# Path: 
# File: board.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-05-31 (y-m-d) 5:26 PM

from abc import abstractmethod
from typing import Optional, Sequence, Iterator

from .axis import IAxis
from ..items.items import BoardItem, PItem, TPointY, TPointX, TPoint
from ..renderer.renderer import IRender, CharRender, NewLineCharRender, HTMLRender

"""
    b = Board(AsciiAxis(5), Int1Axis(3))
    bi = BoardItem(b, 'c', 2)
    bi = BoardItem(b, 'a', 1)
    bi = BoardItem(b, 'e', 3)
    ConsoleRenderer(b).render()

# Should be
#  abcde
# 1?####
# 2##?##
# 3####?

    b = Board(AsciiAxis(5), IntAxis(3))
    bi = BoardItem(b, 'c', 1)
    bi = BoardItem(b, 'a', 0)
    bi = BoardItem(b, 'e', 2)
    ConsoleRenderer(b).render()

# Should be
#  abcde
# 0?####
# 1##?##
# 2####?

    b = Board(Int1Axis(3), FixedAxis(('aa', 'bb', 'cc')))
    bi = BoardItem(b, 2, 'bb')
    bi = BoardItem(b, 1, 'aa')
    bi = BoardItem(b, 3, 'cc')
    ConsoleRenderer(b).render()

# Should be
#  123
# aa?##
# bb#?#
# cc##?

    b = Board(IntAxis(3), FixedAxis(('aa', 'bb', 'cc')))
    bi = BoardItem(b, 1, 'bb')
    bi = BoardItem(b, 0, 'aa')
    bi = BoardItem(b, 2, 'aa')
    ConsoleRenderer(b).render()

# Should be
#  012
# aa?#?
# bb#?#
# cc###

"""


class IBoard(Sequence):

    @property
    @abstractmethod
    def axis_x(self) -> IAxis:
        ...

    @property
    @abstractmethod
    def axis_y(self) -> IAxis:
        ...

    @abstractmethod
    def get_column(self, x: int) -> tuple[Optional[BoardItem]]:
        ...

    @abstractmethod
    def get_row(self, y: int) -> tuple[Optional[BoardItem]]:
        ...


class Board(IBoard):
    """
        All of indexes the x and y axis depends on IAxis that is used as parameters of __init__
        ------1-------2-3-------------------> x
        1 x=1; y=1
        |
        |
        \/
        y

    """

    def __init__(self, axis_x: IAxis, axis_y: IAxis):
        self.__axis_x = axis_x
        self.__axis_y = axis_y
        self.__items = {}

    @property
    def axis_x(self) -> IAxis:
        return self.__axis_x

    @property
    def axis_y(self) -> IAxis:
        return self.__axis_y

    def __len__(self) -> int:
        return len(self.axis_x) * len(self.axis_y)

    def _validate_index(self, x: TPointX, y: TPointY) -> None:
        msg = 'Index "{valname}" should be in range [{start}..{end}]: {value}'
        for valname, value, axis in (('x', x, self.axis_x), ('y', y, self.axis_y)):
            if value not in axis:
                raise IndexError(msg.format(valname=valname, start=axis[0], end=axis[len(axis)-1], value=value))

    def __getitem__(self, key: TPoint) -> Optional[PItem]:
        self._validate_index(*key)
        return self.__items.get(key, None)

    def __setitem__(self, key: TPoint, value: PItem):
        self._validate_index(*key)
        self.__items[key] = value

    def __delitem__(self, key: TPoint):
        self._validate_index(*key)
        del self.__items[key]

    def index(self, value: PItem) -> TPoint:
        for k, v in self.__items.items():
            if value is v:
                return k
        raise ValueError

    def __iter__(self) -> Iterator[Optional[PItem]]:
        for y in self.axis_y:
            for x in self.axis_x:
                yield x, y

    def get_column(self, x: TPointX) -> tuple[Optional[PItem]]:
        return tuple(self[x, y] for y in self.axis_y)

    def get_row(self, y: TPointY) -> tuple[Optional[PItem]]:
        return tuple(self[x, y] for x in self.axis_x)


class ConsoleRenderer(IRender):

    empty_item_renderer = CharRender('#')
    zero_item_renderer = CharRender(' ')

    def __init__(self, board: IBoard):
        self.board: IBoard = board

    def _render_header(self):
        # render x header
        for i, header in enumerate(self.board.axis_x):
            if i == 0:
                self.zero_item_renderer.render()
            CharRender(str(header)).render()

    def render(self):
        for i, y in enumerate(self.board.axis_y):
            if i == 0:
                self._render_header()
                NewLineCharRender().render()
            for j, x in enumerate(self.board.axis_x):
                if j == 0:
                    CharRender(str(y)).render()
                item = self.board[x, y]
                if item is None:
                    self.empty_item_renderer.render()
                else:
                    item.render()
            NewLineCharRender().render()


class HTMLRenderer(IRender):

    default_tag_attrs = {'td': {}, 'th': {}, 'tr': {}, 'table': {'border': '1'}}

    def __init__(self, board: IBoard):
        self.board: IBoard = board

    def get_zero_item_renderer(self):
        return HTMLRender(0xa0, 'th', attrs=dict(self.default_tag_attrs.get('th')))

    def get_empty_item_renderer(self):
        return HTMLRender(0xa0, 'td', attrs=dict(self.default_tag_attrs.get('td')))

    def get_x_header_renderer(self, val):
        return HTMLRender(str(val), 'th', attrs=dict(self.default_tag_attrs.get('th')))

    def get_y_header_renderer(self, val):
        return self.get_x_header_renderer(val)

    def get_item_renderer(self, item: BoardItem):
        return HTMLRender(str(item.id), 'td', attrs=dict(self.default_tag_attrs.get('td')))

    def get_row_renderer(self, row: list[HTMLRender]):
        return HTMLRender(row, 'tr', attrs=dict(self.default_tag_attrs.get('tr')))

    def get_board_renderer(self, rows: list[HTMLRender]):
        return HTMLRender(rows, 'table', attrs=dict(self.default_tag_attrs.get('table')))

    def on_render(self, render_obj: HTMLRender, x: Optional[TPointX] = None, y: Optional[TPointY] = None):
        if render_obj.tag == 'td':
            render_obj.attrs.update({'data-x': str(x), 'data-y': str(y)})
        return render_obj

    def _render_header(self):
        # render x header
        row = []
        for i, header in enumerate(self.board.axis_x):
            if i == 0:
                row.append(self.on_render(self.get_zero_item_renderer()))
            row.append(self.on_render(self.get_x_header_renderer(str(header)), x=header))
        return self.on_render(self.get_row_renderer(row))

    def render(self):
        rows = []
        for i, y in enumerate(self.board.axis_y):
            if i == 0:
                rows.append(self._render_header())

            row = []
            for j, x in enumerate(self.board.axis_x):
                if j == 0:
                    row.append(self.on_render(self.get_y_header_renderer(str(y)), y=y))
                item = self.board[x, y]
                if item is not None:
                    irender = self.get_item_renderer(item)
                else:
                    irender = self.get_empty_item_renderer()
                row.append(self.on_render(irender, x=x, y=y))

            rows.append(self.on_render(self.get_row_renderer(row)))
        return self.on_render(self.get_board_renderer(rows)).render()

