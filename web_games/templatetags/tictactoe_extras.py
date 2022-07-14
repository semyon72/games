# IDE: PyCharm
# Project: games
# Path: web_games/templatetags
# File: tictactoe_extras.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-07-08 (y-m-d) 4:57 PM
import html
import json
from typing import Union

from django import template
from django.utils.safestring import mark_safe

from games.renderer.renderer import HTMLRender
from games.tictactoe.player import ITicTacToePlayer
from ..models import GameBoard, ActiveGame
from games.board.board import HTMLRenderer, IBoard
from games.board.serializer import JSONBoardSerializer
from ..utils import get_module_attr

register = template.Library()


class GameBoardHTMLRenderer(HTMLRenderer):

    board_id_str = 'tictactoe_board_%s'

    def __init__(self, game_board: Union[GameBoard, IBoard], board_id='id') -> None:
        self.board_id = self.board_id_str % board_id
        board = game_board
        if isinstance(game_board, GameBoard):
            self.board_id = self.board_id_str % game_board.pk
            self.game_board = game_board
            board = JSONBoardSerializer(None).loads(game_board.data).board
        super().__init__(board)

    def get_board_renderer(self, rows: list[HTMLRender]):
        result = super().get_board_renderer(rows)
        result.attrs['id'] = self.board_id
        return result


@register.filter(name='render_board', is_safe=True)
def render_board(board, board_id=None):
    if isinstance(board, (IBoard, GameBoard)):
        kwargs = {'game_board': board}
        if board_id is not None:
            kwargs['board_id'] = html.escape(str(board_id))
        return mark_safe(GameBoardHTMLRenderer(**kwargs).render())

    raise ValueError(f'Expected GameBoard or IBoard instances. Got an instance of {board.__class__.__name__}')


@register.inclusion_tag('web_games/tictactoe_activegame_info.html', takes_context=True)
def render_activegame(context, activegame: ActiveGame,
                      player: ITicTacToePlayer = None, opponent_player: ITicTacToePlayer = None):
    template_context = {'active_game_object': activegame}

    if player is None:
        # reconstruct board
        board = JSONBoardSerializer(None).loads(activegame.board.data).board

        # reconstruct the current player
        player_class = globals().get(activegame.player_class)
        if player_class is None:
            player_class = get_module_attr(activegame.player_class)

        pkwargs = json.loads(activegame.player_kwargs)
        player = player_class(board, **pkwargs)

    player_item_id = player.item_class.id

    if opponent_player is None:
        # Get the opponent player
        site = context['view'].get_site()
        opponent_player_class = [cls for cls in site.player_classes if cls is not type(player)][0]
        opponent_player = opponent_player_class(player.board, player.cnt_in_row)

    opponent_player_item_id = opponent_player.item_class.id

    template_context.update(
        {'player': player,
         'player_item_id': player_item_id,
         'opponent_player': opponent_player,
         'opponent_player_item_id': opponent_player_item_id,
         'view': context.get('view'),
         'request': context.get('request'),
         }
    )

    return template_context
