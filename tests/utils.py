# IDE: PyCharm
# Project: games
# Path: tests
# File: utils.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-08 (y-m-d) 6:58 PM

import sys
from io import StringIO
from typing import Callable


def _catch_stdout(callback: Callable, *args, **kwargs):
    stdout = sys.stdout
    _stdout = None
    try:
        _stdout = StringIO(newline=None)
        sys.stdout = _stdout
        callback(*args, **kwargs)
        _stdout.seek(0)
        result = _stdout.read()
    finally:
        sys.stdout = stdout
        if _stdout is not None:
            _stdout.close()

    return result
