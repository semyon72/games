# IDE: PyCharm
# Project: games
# Path: algo
# File: tictactoe.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-08 (y-m-d) 8:23 PM
import functools
from abc import ABC, abstractmethod
from typing import Type, Optional, Union

from ..moves import MoveDispatcher
from .moves import TicTacToeWinMove, TicTacToeOpponentWinMove, TicTacToeIntersectionMove, TicTacToeRandomMove
from .vector import TicTacToeVectorProvider
from ..board.board import IBoard
from ..items.items import XItem, PItem, TPointX, TPointY, OItem, BoardItem, TPoint


class PlayerException(Exception):
    pass


class PlayerWon(PlayerException):
    msg = 'Player {id} is won: [{info}]'

    def __init__(self, points_info: list[tuple[TPoint, Optional[BoardItem]]], *args: object) -> None:
        self.points_info = points_info
        msg = self.msg.format(
            id=self.points_info[0][1].id,
            info=', '.join(f'{x}:{y}' for (x, y), item in self.points_info)
        )

        super().__init__(msg)


class PlayerBoardFull(PlayerException):
    msg = 'Board is full'

    def __init__(self, *args: object) -> None:
        super().__init__(self.msg)


class IPlayer(ABC):

    item_class: Type[PItem]

    @property
    @abstractmethod
    def board(self):
        raise NotImplementedError

    @abstractmethod
    def move_suggestion(self) -> TPoint:
        raise NotImplementedError

    @abstractmethod
    def play(self, x: Union[TPointX, BoardItem], y: Optional[TPointY] = None):
        raise NotImplementedError


class ITicTacToePlayer(IPlayer):

    @property
    @abstractmethod
    def cnt_in_row(self):
        raise NotImplementedError

    @abstractmethod
    def is_board_full(self, throw_exc=False):
        raise NotImplementedError

    @abstractmethod
    def is_won(self, last_move: Optional[BoardItem] = None, throw_exc=False) -> Optional[bool]:
        raise NotImplementedError


class TicTacToePlayerX(ITicTacToePlayer):

    item_class: Type[PItem] = XItem
    opponent_item_class: Type[PItem] = OItem
    vector_provider_class = TicTacToeVectorProvider

    def __init__(self, board: IBoard, cnt_in_row=3) -> None:
        self._vector_provider = self.vector_provider_class(board, self.item_class.id, cnt_in_row)
        self.move_dispatcher = self.get_move_dispatcher()

    def get_move_dispatcher(self) -> MoveDispatcher:
        mr = [TicTacToeWinMove,
              TicTacToeOpponentWinMove(self._vector_provider, self.opponent_item_class.id),
              TicTacToeIntersectionMove, TicTacToeRandomMove]

        return MoveDispatcher(self._vector_provider, *mr)

    @property
    def board(self):
        return self._vector_provider.board

    @property
    def cnt_in_row(self):
        return self._vector_provider.cnt_in_row

    def move_suggestion(self):
        self._vector_provider.clear_cache()
        return self.move_dispatcher.resolve()

    def is_board_full(self, throw_exc=False) -> Optional[bool]:
        res = len([pitem for pitem in self.board if self.board[pitem] is None]) == 0
        if throw_exc:
            raise PlayerBoardFull()
        return res

    def is_won(self,
               last_move: Optional[BoardItem] = None,
               throw_exc=False) -> Union[bool, list[tuple[TPoint, Optional[BoardItem]]], None]:

        def red_func(pis: list[tuple[TPoint, Optional[BoardItem]]], pi: tuple[TPoint, Optional[BoardItem]]):
            if len(pis) < self.cnt_in_row:
                if type(pi[1]) is self.item_class:
                    pis.append(pi)
                else:
                    pis.clear()
            if len(pis) == self.cnt_in_row:
                raise PlayerWon(pis)
            return pis

        try:
            if last_move:
                vectors = (v for v in self._vector_provider.provide() if (last_move.x, last_move.y) in v)
            else:
                vectors = (v for v in self._vector_provider.provide())

            for v in vectors:
                functools.reduce(red_func, v.items(), [])

        except PlayerWon as err:
            if throw_exc:
                raise
            else:
                return err.points_info

        return False

    def play(self, x: Union[TPointX, BoardItem], y: Optional[TPointY] = None):
        if isinstance(x, BoardItem):
            if self.board is not x.board:
                raise ValueError('BoardItem does not belong to the current player\'s board')
            bi = x
        else:
            bi = self.item_class(self.board, x, y)
        self._vector_provider.clear_cache()
        self.is_won(bi, True)


class TicTacToePlayerY(TicTacToePlayerX):
    item_class: Type[PItem] = OItem
    opponent_item_class: Type[PItem] = XItem
