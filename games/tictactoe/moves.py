# IDE: PyCharm
# Project: games
# Path: tictactoe
# File: moves.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-19 (y-m-d) 9:44 PM
import functools
import random
from typing import Optional

from ..items.items import TPoint
from ..moves import IMoveResolver, MoveResolved
from ..tictactoe.vector import ITicTacToeVectorProvider
from ..vector.vector import TVector
from ..vector.intersection import IntersectionPoints, IIntersectionPoint, IntersectionPoint


class TicTacToeWinMove(IMoveResolver):

    def test_win_case(self, vector: TVector) -> Optional[TPoint]:

        if len(tuple(val for val in vector.values() if val is not None)) >= self.vector_provider.cnt_in_row - 1:
            # tests X..X..X on 3X in row worse than ..XX...

            def reduce_func(items, item_next):
                if len(items) < self.vector_provider.cnt_in_row - 1:
                    items.append(item_next)
                    return items
                items.append(item_next)

                empties = tuple((k, v) for k, v in items if v is None)
                if len(empties) == 1:
                    raise MoveResolved(empties[0][0], items)

                return items[1:]

            try:
                functools.reduce(reduce_func, vector.items(), [])
            except MoveResolved as res:
                return res.key
        return

    def resolve(self) -> Optional[TPoint]:
        for v in self.vector_provider.provide():
            res = self.test_win_case(v)
            if res:
                return res


class TicTacToeOpponentWinMove(IMoveResolver):

    def __init__(self, vector_provider: ITicTacToeVectorProvider, opponent_id: str) -> None:
        super().__init__(vector_provider)
        self.opponent_id = opponent_id

    def resolve(self) -> Optional[TPoint]:
        ovprovider = type(self.vector_provider)(
            self.vector_provider.board,
            self.opponent_id,
            self.vector_provider.cnt_in_row
        )
        return TicTacToeWinMove(ovprovider).resolve()


class TicTacToeIntersectionPoints(IntersectionPoints):

    def add(self, point: TPoint, vector: TVector) -> 'IntersectionPoints':
        if point in vector and vector[point] is not None:
            return self

        return super(TicTacToeIntersectionPoints, self).add(point, vector)

    def calc_vector_rate(self, vector: TVector) -> int:
        return len(vector) + sum(20 for point, val in vector if val is not None)

    def calc_intersection_point_rate(self, ip: IntersectionPoint):
        res = 0
        if ip is not None:
            for v in ip.vectors:
                res += self.calc_vector_rate(v)
        return res

    def get_most_rated(self) -> list[Optional[IIntersectionPoint]]:
        # will search empty point with most rated intersection
        res = []
        for (x, y), ip in self.points.items():
            if ip.point != (x, y):
                raise AssertionError(f'Integrity violation: IntersectionPoint.point{ip.point} must be ({x}, {y})')

            rate = self.calc_intersection_point_rate(ip)
            if len(res):
                if res[0][0] > rate:
                    continue
                elif res[0][0] < rate:
                    res.clear()

            res.append((rate, ip))

        return [ip for rate, ip in res]


class TicTacToeIntersectionMove(IMoveResolver):

    def resolve(self) -> Optional[TPoint]:
        best = TicTacToeIntersectionPoints.create(self.vector_provider).get_most_rated()
        return None if not best else random.choice(best).point


class TicTacToeRandomMove(IMoveResolver):

    def resolve(self) -> Optional[TPoint]:
        b = self.vector_provider.board
        empties = [(x, y) for x, y in b if b[x, y] is None]
        if empties:
            return random.choice(empties)
        return None
