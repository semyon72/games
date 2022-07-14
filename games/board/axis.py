# IDE: PyCharm
# Project: games
# Path: board
# File: axis.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-05 (y-m-d) 11:12 AM

from abc import abstractmethod
from typing import Sequence, Any


class AxisIndexNotInRangeError(IndexError):

    msg = 'Index should be in range [{min}..{max}]: {idx}'

    def __init__(self, min: int, max: int, idx: int, *args: object) -> None:
        self.min = min
        self.max = max
        self.idx = idx
        super().__init__(self.msg.format(**locals()))


class IAxis(Sequence):

    __size = None

    @abstractmethod
    def get_max_size(self) -> int:
        ...

    def set_size(self, size: int) -> None:
        size = int(size)
        max_size = self.get_max_size()
        if size < 1 or size > max_size:
            raise ValueError(f'Size should be in range [1..{max_size}]: {size}')
        self.__size = size

    def __len__(self) -> int:
        return self.__size


class IntAxis(IAxis):

    max_size: int = 1000000

    def __init__(self, size: int):
        self._range = None
        self.set_size(size)

    def set_size(self, size: int) -> None:
        super().set_size(size)
        self._range = range(size)

    def get_max_size(self) -> int:
        return self.max_size

    def __contains__(self, value: int) -> bool:
        return bool(value in self._range)

    def __getitem__(self, i: int) -> int:
        if 0 > i or i > len(self)-1:
            raise AxisIndexNotInRangeError(0, len(self)-1, i)
        return self._range[i]

    def index(self, value: int) -> int:
        return self._range.index(value)


class Int1Axis(IntAxis):

    def set_size(self, size: int) -> None:
        super().set_size(size)
        self._range = range(1, size+1)


class AsciiAxis(IAxis):

    ord_range: tuple[tuple[int, int]] = ((ord('a'), ord('z')), (ord('A'), ord('Z')))

    def __init__(self, size: int):
        self.set_size(size)

    def get_max_size(self) -> int:
        return sum(ecode-bcode+1 for bcode, ecode in self.ord_range)

    def index(self, ch: str) -> int:
        chcode = ord(ch)
        tcnt = 0
        for bcode, ecode in self.ord_range:
            if bcode <= chcode <= ecode:
                tcnt += chcode - bcode
                if tcnt >= len(self):
                    raise ValueError(f'Char should be in range [{self[0]}..{self[len(self)-1]}]: {ch}')
                else:
                    return tcnt
            tcnt += ecode - bcode + 1
        raise ValueError

    def __contains__(self, ch: str) -> bool:
        try:
            self.index(ch)
        except ValueError:
            return False
        return True

    def index_to_char(self, i: int) -> str:
        if 0 > i or i >= len(self):
            raise AxisIndexNotInRangeError(0, len(self)-1, i)

        idx1 = i + 1
        for bcode, ecode in self.ord_range:
            idx1 -= ecode - bcode + 1
            if idx1 <= 0:
                return chr(ecode + idx1)

    def __getitem__(self, i: int) -> str:
        return self.index_to_char(i)


class FixedAxis(IAxis):

    def __init__(self, keys: Sequence):
        self.__keys = keys
        self.set_size(len(keys))

    def get_max_size(self) -> int:
        return len(self.__keys)

    def __getitem__(self, i: int) -> Any:
        if i >= len(self) or i < 0:
            raise AxisIndexNotInRangeError(0, len(self)-1, i)
        return self.__keys[i]
