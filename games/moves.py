# IDE: PyCharm
# Project: games
# Path: algo
# File: moves.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-15 (y-m-d) 12:33 PM
from abc import abstractmethod, ABC
from typing import Optional, Type, Union

from .items.items import TPoint
from .vector.vector import IVectorProvider


class IMoveResolver(ABC):

    def __init__(self, vector_provider: IVectorProvider) -> None:
        self.vector_provider: IVectorProvider = vector_provider

    @abstractmethod
    def resolve(self) -> Optional[TPoint]:
        raise NotImplementedError


class MoveResolved(Exception):

    def __init__(self, key: TPoint, vector: dict, *args, **kwargs) -> None:
        self.key = key
        self.vector = vector
        super().__init__(f'Decision found: {key} in {vector}', *args, **kwargs)


class MoveDispatcher(IMoveResolver):

    def __init__(self,
                 vector_provider: IVectorProvider,
                 resolver: Union[IMoveResolver, Type[IMoveResolver]],
                 *resolvers: Union[IMoveResolver, Type[IMoveResolver]]) -> None:
        super().__init__(vector_provider)
        self.resolvers: list[IMoveResolver] = [self._instantiate_resolver(resolver),
                                               *(self._instantiate_resolver(r) for r in resolvers)]

    def _instantiate_resolver(self, resolver: Union[IMoveResolver, Type[IMoveResolver]]):
        if issubclass(type(resolver), type):
            return resolver(self.vector_provider)
        else:
            return resolver

    def resolve(self) -> Optional[TPoint]:
        for r in self.resolvers:
            res = r.resolve()
            if res is not None:
                return res
        return None
