# IDE: PyCharm
# Project: games
# Path: 
# File: vector.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-15 (y-m-d) 4:56 PM
from abc import ABC, abstractmethod
from typing import Optional, Iterable, Iterator, Type

from ..board.board import IBoard
from ..items.items import PItem, TPoint, TPointY, TPointX


TVectorPoints = list[TPoint]
TVector = dict[TPoint, Optional[PItem]]


class IVectorPoints(Iterable):

    @abstractmethod
    def get_points(self) -> TVectorPoints:
        raise NotImplementedError

    def __iter__(self) -> Iterator[TPoint]:
        for p in self.get_points():
            yield p


class VectorPoints(IVectorPoints):

    def __init__(self, board: IBoard, x: TPointX, y: TPointY, deep: Optional[int] = 1) -> None:
        self.board = board
        self.x = x
        self.y = y
        self.deep = deep
        self.__points: TVectorPoints = []

    @property
    def points(self):
        return self.__points

    def get_point_idx(self, x: TPointX, y: TPointY) -> Optional[tuple[int, int]]:
        try:
            iy = self.board.axis_y.index(y)  # only index validation - will raise ValueError if 'y' out of range
            ix = self.board.axis_x.index(x)
        except ValueError as err:
            raise ValueError('The vector point is outside the range of the axis. ' + err.args[0])
        else:
            result = (ix, iy)
        return result

    def get_point_xy(self, ix: int, iy: int) -> Optional[TPoint]:
        try:
            y = self.board.axis_y[iy]  # only index validation - will raise IndexError if 'iy' out of range
            x = self.board.axis_x[ix]
        except IndexError as err:
            raise IndexError('Axis indices that are out of range are used. ' + err.args[0])
        else:
            result = (x, y)
        return result

    def is_sense_go_further(self, ix: int, iy: int, deep: int) -> bool:
        """default behaviour - not more than deep value and all if self.deep < 0."""
        return self.deep < 0 or self.deep - deep > 0

    @abstractmethod
    def get_next_ixy(self, ix: int, iy: int) -> tuple[int, int]:
        raise NotImplementedError

    def _process_points(self, ix: int, iy: int, deep: int = 0) -> TVectorPoints:
        self.__points.append(self.get_point_xy(ix, iy))
        if self.is_sense_go_further(ix, iy, deep):
            ix, iy = self.get_next_ixy(ix, iy)
            if 0 <= ix < len(self.board.axis_x) and 0 <= iy < len(self.board.axis_y):
                self._process_points(ix, iy, deep+1)
        if deep == 0:
            return self.points

    def get_points(self) -> TVectorPoints:
        if self.__points and self.__points[0] == (self.x, self.y):
            return self.points

        self.__points.clear()
        result = self._process_points(*self.get_point_idx(self.x, self.y), 0)

        if len(result)-1 == self.deep or self.deep < 0:
            return result

        self.__points.clear()
        return []


class HorizontalVectorPoints(VectorPoints):

    def get_next_ixy(self, ix: int, iy: int) -> tuple[int, int]:
        return ix+1, iy


class VerticalVectorPoints(VectorPoints):

    def get_next_ixy(self, ix: int, iy: int) -> tuple[int, int]:
        return ix, iy+1


class BackDiagonalVectorPoints(VectorPoints):

    def get_next_ixy(self, ix: int, iy: int) -> tuple[int, int]:
        return ix+1, iy+1


class ForwardDiagonalVectorPoints(VectorPoints):

    def get_next_ixy(self, ix: int, iy: int) -> tuple[int, int]:
        return ix-1, iy+1


class IVectorProvider(Iterable):

    def __init__(self, board: IBoard) -> None:
        self.board = board

    @abstractmethod
    def provide(self) -> list[TVector]:
        raise NotImplementedError

    def __iter__(self) -> Iterator[TVector]:
        for v in self.provide():
            yield v


class VectorProvider(IVectorProvider):

    vector_points_class: Optional[Type[VectorPoints]] = None

    def get_vector_points_class(self) -> Type[VectorPoints]:
        if not issubclass(self.vector_points_class, VectorPoints):
            raise ValueError(
                'Must be reimplemented in descendants or pointed as class attribute vector_points_class'
            )
        return self.vector_points_class

    def provide_start_points(self) -> Iterable[TPoint]:
        raise NotImplementedError

    def extract_vectors(self, vector_points: Iterable[TPoint]) -> list[TVector]:
        result = [{(x, y): self.board[x, y] for x, y in vector_points}]
        return result

    def provide(self) -> list[TVector]:
        vectors = []
        for x, y in self.provide_start_points():  # walk by rows
            vectors.extend(self.extract_vectors(self.get_vector_points_class()(self.board, x, y, -1)))
        return vectors


class RowVectorProvider(VectorProvider):

    vector_points_class = HorizontalVectorPoints

    def provide_start_points(self) -> Iterable[TPoint]:
        return ((self.board.axis_x[0], y) for y in self.board.axis_y)  # walk by rows


class ColumnVectorProvider(VectorProvider):

    vector_points_class = VerticalVectorPoints

    def provide_start_points(self) -> Iterable[TPoint]:
        return ((x, self.board.axis_y[0]) for x in self.board.axis_x)  # walk by columns


class BackDiagonalVectorProvider(VectorProvider):

    vector_points_class = BackDiagonalVectorPoints

    def provide_start_points(self) -> Iterable[TPoint]:
        """ It should return points x1:y1, x2:y1, .... Xn:y1 and x1:y2, x1:y3, ... x1:Yn """
        for iy, y in enumerate(self.board.axis_y):
            for ix, x in enumerate(self.board.axis_x):
                if ix > 0 and iy > 0:
                    break
                yield x, y


class ForwardDiagonalVectorProvider(VectorProvider):

    vector_points_class = ForwardDiagonalVectorPoints

    def provide_start_points(self) -> Iterable[TPoint]:
        """ It should return points Xn:y1, Xn-1:y1, .... x1:y1 and Xn:y2, Xn:y3, ... Xn:Yn """
        for iy, y in enumerate(self.board.axis_y):
            for ix, x in enumerate(reversed(self.board.axis_x)):
                if ix > 0 and iy > 0:
                    break
                yield x, y


class DiagonalsVectorProvider(IVectorProvider):

    def provide(self) -> list[TVector]:
        return [
            *BackDiagonalVectorProvider(self.board).provide(),
            *ForwardDiagonalVectorProvider(self.board).provide()
        ]


class IRated(ABC):

    @abstractmethod
    def rate(self):
        ...


class RatedVector(IRated):

    def __init__(self, vector: TVector) -> None:
        self.vector: TVector = vector

    def get_item_rate(self, item: Optional[PItem]) -> int:
        if item is None:
            return 1
        elif isinstance(item, IRated):
            return item.rate()
        else:
            raise NotImplementedError('Rated item has not rate.')

    def rate(self):
        rate = 0
        for item in self.vector.values():
            rate += self.get_item_rate(item)
        return rate
