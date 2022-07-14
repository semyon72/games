# IDE: PyCharm
# Project: games
# Path: web_games
# File: utils.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-07-02 (y-m-d) 6:30 PM

import sys
from importlib import import_module
from typing import Optional


def get_module_attr(attr_path: str) -> type:
    mn, _, attr_name = attr_path.rpartition('.')
    m = sys.modules.get(mn)
    if not m:
        m = import_module(mn)
    if m:
        res = getattr(m, attr_name, None)
        if res:
            return res

    raise ValueError(f'Module {mn} has not {attr_name}')


def get_game_site_manager(game_manager: str = 'web_games.game_manager.site_games') -> Optional['GameSiteManager']:
    return get_module_attr(game_manager)


def get_site_games():
    game_manager = get_game_site_manager()
    return tuple((uuid, game.verbose_name) for uuid, game in game_manager.items())



