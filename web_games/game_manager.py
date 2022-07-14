# IDE: PyCharm
# Project: games
# Path: web_games
# File: game_manager.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-25 (y-m-d) 12:06 PM

from abc import abstractmethod
from typing import Protocol, Type, Callable, Union, Optional, NamedTuple, Mapping, Iterator

from django.urls import path, re_path, include
from django.views import View

from games.tictactoe.player import IPlayer, TicTacToePlayerX

from .utils import get_module_attr
from .views.tictactoe import TicTacToeView, TicTacToeCreateView, TicTacToePlayView, TicTacToeDeleteView

"""
Usage in urls.py

urlpatterns = [
    .....
    path('tictactoe_games/', TicTacToeGameSite('games').urls),
    path('tictactoe_web_games/', TicTacToeGameSite('web_games').urls),
    *sites.get_root_path(),  # defaults are root_route='games/' and app_namespace='games' 
    *GameSiteManager(TicTacToeGameSite, root_route='web_games/', app_namespace='weeb_games').get_root_path(),
    .....
]
"""

TAppNameSpace = TAppName = str
TPathList = list[Union[path, re_path]]


class UrlsResult(NamedTuple):
    paths: TPathList
    app_name: Optional[TAppName] = None
    app_namespace: Optional[TAppNameSpace] = None


class GameSiteAction(NamedTuple):
    route: str
    view: Callable
    kwargs: dict


class IGameSite(Protocol):

    @abstractmethod
    def get_paths(self) -> TPathList:
        raise NotImplementedError

    @property
    @abstractmethod
    def urls(self) -> UrlsResult:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_viewname(cls, view: Union[Callable, Type[View]]) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def player_classes(self) -> list[Type[IPlayer]]:
        raise NotImplementedError


class BaseGameSite(NamedTuple):
    namespace: str = None  # also mentioned as app_namespace (synonym of app_namespace)
    uuid: str = ''
    name: Optional[str] = None  # also mentioned as app_name (synonym of app_name)
    verbose_name: str = ''
    actions: dict[str, Optional[GameSiteAction]] = {}

    def get_route(self, action_name):
        return self.actions[action_name].route

    def get_paths(self) -> TPathList:
        result = []
        for action_name, action in self.actions.items():
            if action:
                view = action.view
                if type(view) is type and issubclass(view, View):
                    view = view.as_view()
                _path = path(action.route, view, name=action_name, kwargs=action.kwargs)
                result.append(_path)
        return result

    @property
    def urls(self) -> UrlsResult:
        return UrlsResult(self.get_paths(), self.name, self.namespace)

    @classmethod
    def get_viewname(cls, view: Union[Callable, View, Type[View]]) -> str:
        res_list = []
        for action_name, action in cls.actions.items():
            if isinstance(view, View):
                view = type(view)

            if hasattr(action.view, 'view_class') and type(view) is type and view is action.view.view_class:
                res_list.append(action_name)
            elif callable(view) and callable(action.view) and view is action.view:
                res_list.append(action_name)

        if res_list:
            # returning a last viewname is questionable
            # return ':'.join((cls.name, res_list[-1] if len(res_list) > 1 else res_list[0]))
            if len(res_list) > 1:
                raise ValueError(f'Name of URL can\'t be unambiguously resolved for {view!r}')
            return ':'.join((cls.name, res_list[0]))
        return ''

    @property
    def player_classes(self) -> list[Type[IPlayer]]:
        default_player_cls_attr_name = 'default_player_classes'
        res = []
        player_classes = getattr(self, default_player_cls_attr_name, tuple())
        for pcls in player_classes:
            if isinstance(pcls, str):
                pcls = get_module_attr(pcls)

            if issubclass(pcls, IPlayer):
                res.append(pcls)
            else:
                raise TypeError(
                    f'Attribute {default_player_cls_attr_name} should be a string or class that implements IPlayer.'
                )
        return res


class TicTacToeGameSite(BaseGameSite):
    uuid: str = 'f84e0df2-8316-4346-913c-a3c52c233ace'
    name: str = 'tictactoe'
    verbose_name: str = 'Tic Tac Toe'
    default_player_classes = (TicTacToePlayerX, 'games.tictactoe.player.TicTacToePlayerY')

    actions: dict[str, GameSiteAction] = {
        'list': GameSiteAction(
            '/'.join((name, '')),
            TicTacToeView.as_view(),
            {'guid': uuid}
        ),
        'create': GameSiteAction(
            '/'.join((name, 'create', '')),
            TicTacToeCreateView.as_view(),
            {'guid': uuid}
        ),
        'delete': GameSiteAction(
            '/'.join((name, 'delete', '<int:pk>', '')),
            TicTacToeDeleteView.as_view(),
            {'guid': uuid}
        ),
        'play': GameSiteAction(
            '/'.join((name, 'play', '<int:pk>', '')),
            TicTacToePlayView.as_view(),
            {'guid': uuid})
    }


class GameSiteManager(Mapping):

    def __init__(self, site: Type[BaseGameSite], *sites: tuple[Type[BaseGameSite]],
                 root_route: str = '', app_namespace: str = None) -> None:
        self.root_route = root_route
        self.namespace = app_namespace
        self._games: dict[str, IGameSite] = {
            site_cls.uuid: site_cls(app_namespace) for site_cls in (site, *sites)
        }

    def __iter__(self) -> Iterator[str]:
        for uuid in self._games:
            yield uuid

    def __len__(self) -> int:
        return len(self._games)

    def __getitem__(self, uuid) -> IGameSite:
        return self._games[uuid]

    def get_root_path(self) -> list[Union[path, re_path]]:
        return [path(self.root_route, site.urls) for site in self.values()]

    def get_game_site(self, view: Union[Type[View], View, Callable]) -> Optional[BaseGameSite]:
        for uuid, game_site in self.items():  # type tuple[str, BaseGameSite]
            for action in game_site.actions.values():
                if isinstance(view, View):
                    view = type(view)

                view_class = getattr(action.view, 'view_class', action.view)
                if view_class and view_class is view:
                    return game_site

    def get_viewname(self, view: Union[Callable, View, Type[View]]) -> str:
        res_list = []
        for site in self.values():
            vn = site.get_viewname(view)
            if vn:
                res_list.append(vn)

        if res_list:
            if len(res_list) > 1:
                raise ValueError(f'Name of URL can\'t be unambiguously resolved for {view!r}')
            return res_list[0]
        return ''


site_games = GameSiteManager(TicTacToeGameSite, root_route='games/', app_namespace='games')
