# IDE: PyCharm
# Project: games
# Path: games/board
# File: serializer.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-22 (y-m-d) 9:05 PM
import json
import sys

from .axis import IAxis
from .board import Board
from ..items.items import BoardItem


class JSONBoardSerializer:

    class_name_key = 'class'
    class_args_key = 'args'
    class_kwargs_key = 'kwargs'

    def __init__(self, board: Board = None) -> None:
        self.board = board

    def __str2class(self, cls: str):
        res = globals().get(cls)
        if res is None:
            mod_str, _, cls = cls.rpartition('.')
            mod = sys.modules.get(mod_str)
            if mod is None:
                raise ModuleNotFoundError(f'Can\'t find module: {mod_str}')
            try:
                res = getattr(mod, cls)
            except AttributeError:
                raise ModuleNotFoundError(f'Can\'t find class: {cls} in module {mod.__name__}')
        return res

    def __class2str(self, obj):
        cls = type(obj)
        return '.'.join((*cls.__module__.split('.'), cls.__name__))

    def _dumps_axis(self, axis: IAxis) -> str:
        result = {self.class_name_key: self.__class2str(axis),
                  self.class_args_key: [len(axis)],
                  self.class_kwargs_key: {}}
        return json.dumps(result)

    def _loads_axis(self, json_axis: str) -> IAxis:
        info = json.loads(json_axis)
        cls = self.__str2class(info[self.class_name_key])
        result = cls(*info[self.class_args_key], **info[self.class_kwargs_key])

        return result

    def _dumps_board(self) -> str:
        ax = self._dumps_axis(self.board.axis_x)
        ay = self._dumps_axis(self.board.axis_y)
        result = {
            self.class_name_key: self.__class2str(self.board),
            self.class_args_key: [ax, ay],
            self.class_kwargs_key: {}
        }
        return json.dumps(result)

    def _loads_board(self, json_board: str) -> Board:
        info = json.loads(json_board)
        cls = self.__str2class(info[self.class_name_key])
        args = [self._loads_axis(axis) for axis in info[self.class_args_key]]
        result = cls(*args, **info[self.class_kwargs_key])
        return result

    def _dumps_item(self, item: BoardItem) -> str:
        result = {
            self.class_name_key: self.__class2str(item),
            self.class_args_key: [],
            self.class_kwargs_key: {'x': item.x, 'y': item.y}
        }
        return json.dumps(result)

    def _loads_item(self, board: Board, json_item: str) -> BoardItem:
        info = json.loads(json_item)
        cls = self.__str2class(info[self.class_name_key])
        result = cls(board, **info[self.class_kwargs_key])
        return result

    def dumps(self) -> str:
        result = [self._dumps_board()]

        items = self.board.__dict__.get('_Board__items')
        for point, item in items.items():
            if point != (item.x, item.y):
                AssertionError('The x, y positions of the Item does not correlate to index in board items.')
            result.append(self._dumps_item(item))

        return "\n".join(result)

    def loads(self, json_board: str) -> 'JSONBoardSerializer':
        json_board, *json_items = json_board.split('\n')
        res_board = self._loads_board(json_board)
        for item in json_items:
            self._loads_item(res_board, item)
        self.board = res_board
        return self
