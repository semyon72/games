# IDE: PyCharm
# Project: games
# Path: algo
# File: vector.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-15 (y-m-d) 9:18 AM

from typing import Iterable, Type, Optional

from ..board.board import IBoard
from ..items.items import TPoint
from ..vector.vector import (IVectorProvider, TVector, RowVectorProvider,
                             ColumnVectorProvider, BackDiagonalVectorProvider, ForwardDiagonalVectorProvider)


class TicTacToeVectorProviderMixin:

    def __init__(self: IVectorProvider, board: IBoard, item_id: str, cnt_in_row: int = 3) -> None:
        super().__init__(board)
        self.item_id = item_id
        self.cnt_in_row = cnt_in_row


class ITicTacToeVectorProvider(TicTacToeVectorProviderMixin, IVectorProvider):

    def extract_vectors(self, vector_points: Iterable[TPoint]) -> list[TVector]:
        """Returns list of vectors from vector passed as parameter and values that contains.
           Each Item in list is dict where values is integer weights of this vector point.
           Implements - 'business logic' """

        result = []
        vector_points = tuple(vector_points)
        if len(vector_points) < self.cnt_in_row:
            return result

        res = {}
        for x, y in vector_points:
            item = self.board[x, y]
            if item is None or item.id == self.item_id:
                res[x, y] = item
            else:
                if len(res) >= self.cnt_in_row:
                    result.append(res)
                res = {}
        if len(res) >= self.cnt_in_row:
            result.append(res)
        return result


class TicTacToeRowVectorProvider(ITicTacToeVectorProvider, RowVectorProvider):

    def provide_start_points(self) -> Iterable[TPoint]:
        if self.cnt_in_row <= len(self.board.axis_x):
            yield from super().provide_start_points()


class TicTacToeColumnVectorProvider(ITicTacToeVectorProvider, ColumnVectorProvider):

    def provide_start_points(self) -> Iterable[TPoint]:
        if self.cnt_in_row <= len(self.board.axis_y):
            yield from super().provide_start_points()


class TicTacToeBackDiagonalVectorProvider(ITicTacToeVectorProvider, BackDiagonalVectorProvider):

    def provide_start_points(self) -> Iterable[TPoint]:
        for x, y in super().provide_start_points():
            ix, iy = self.vector_points_class.get_point_idx(self, x, y)
            if len(self.board.axis_y) - iy >= self.cnt_in_row <= len(self.board.axis_x) - ix:
                yield x, y


class TicTacToeForwardDiagonalVectorProvider(ITicTacToeVectorProvider, ForwardDiagonalVectorProvider):

    def provide_start_points(self) -> Iterable[TPoint]:
        for x, y in super().provide_start_points():
            ix, iy = self.vector_points_class.get_point_idx(self, x, y)
            if ix+1 >= self.cnt_in_row <= len(self.board.axis_y) - iy:
                yield x, y


class TicTacToeVectorProvider(TicTacToeVectorProviderMixin, IVectorProvider):

    partial_vector_provider_classes: Iterable[Type[ITicTacToeVectorProvider]] = (
        TicTacToeRowVectorProvider, TicTacToeColumnVectorProvider,
        TicTacToeBackDiagonalVectorProvider, TicTacToeForwardDiagonalVectorProvider
    )

    def __init__(self: IVectorProvider, board: IBoard, item_id: str, cnt_in_row: int = 3) -> None:
        super().__init__(board, item_id, cnt_in_row)
        self.__cache: Optional[list[TVector]] = None

    def clear_cache(self):
        self.__cache = None

    def filter_vectors(self, vectors: list[TVector]) -> list[TVector]:
        """Returns list of vectors from vectors passed as parameter.
           Each Item in list is dict where values is PItem itself and key is TPoint.
           Implements - 'business logic' """
        return vectors

    def provide(self) -> list[TVector]:
        if self.__cache is None:
            self.__cache = []
            for provider_class in self.partial_vector_provider_classes:  # walk by rows
                self.__cache.extend(self.filter_vectors(provider_class(self.board, self.item_id, self.cnt_in_row).provide()))
        return self.__cache
