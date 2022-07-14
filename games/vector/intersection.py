# IDE: PyCharm
# Project: games
# Path: games/vector
# File: intersection.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-20 (y-m-d) 9:30 AM
import functools
import random
from dataclasses import dataclass, field
from typing import Collection, Iterator, Optional, Type, Callable, Iterable

from .vector import TVector
from ..items.items import TPoint


@dataclass
class IIntersectionPoint(Collection):
    point: TPoint
    vectors: list[TVector] = field(default_factory=list, init=False, repr=False, )

    def __len__(self) -> int:
        return len(self.vectors)

    def __iter__(self) -> Iterator[TVector]:
        for v in self.vectors:
            yield v

    def __contains__(self, __vector: TVector) -> bool:
        return __vector in self.vectors


class IntersectionPoint(IIntersectionPoint):

    def clear(self) -> 'IntersectionPoint':
        self.vectors = []
        return self

    def add(self, vector: TVector) -> 'IntersectionPoint':
        if vector not in self and self.point in vector:
            self.vectors.append(vector)
        return self


class IntersectionPoints:

    intersection_point_class: Type[IntersectionPoint] = IntersectionPoint

    def __init__(self) -> None:
        self.points: dict[TPoint, IIntersectionPoint] = {}

    def clear(self) -> 'IntersectionPoints':
        self.points = {}
        return self

    def add(self, point: TPoint, vector: TVector) -> 'IntersectionPoints':
        ip = self.points.get(point)
        if ip is None:
            ip = self.intersection_point_class(point)
            self.points[point] = ip

        ip.add(vector)
        return self

    def get_largest_list(self) -> list[Optional[IIntersectionPoint]]:
        """ tests max count (number) intersections of vectors """

        def red_func(ips: list[IntersectionPoint], ip: IntersectionPoint):
            if not len(ips):
                ips.append(ip)
            else:
                ipc, ipfc = (sum(1 for v in ip.vectors for _ in v), sum(1 for v in ips[0].vectors for _ in v))
                if ipc > ipfc:
                    ips = [ip]
                elif ipc == ipfc:
                    ips.append(ip)

            return ips

        return functools.reduce(red_func, self.points.values(), [])

    def get_largest(self, func: Callable[[list[Optional[IIntersectionPoint]]],
                                         Optional[IIntersectionPoint]] = random.choice
                    ) -> Optional[IIntersectionPoint]:
        bests = self.get_largest_list()
        if not bests:
            return
        return func(bests)

    @classmethod
    def create(cls, vector_provider: Iterable[TVector]) -> 'IntersectionPoints':
        self = cls()
        for vector in vector_provider:
            for point, item in vector.items():
                self.add(point, vector)

        return self
