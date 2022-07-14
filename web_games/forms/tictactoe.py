# IDE: PyCharm
# Project: games
# Path: web_games/forms
# File: tictactoe.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-24 (y-m-d) 12:54 PM
from django.core.exceptions import ValidationError
from django.forms import Form, IntegerField, ChoiceField
from django.utils.translation import gettext as _

from games.board.axis import AsciiAxis, Int1Axis, IntAxis
from games.board.board import Board
from games.items.items import TPoint
from games.tictactoe.player import TicTacToePlayerX, TicTacToePlayerY, ITicTacToePlayer
from .base import PlayersNextMoveForm
from ..utils import get_game_site_manager


class TicTacToePlayersNextMoveForm(PlayersNextMoveForm):

    def __init__(self, *args, **kwargs):

        # Just the stubs
        self._player: ITicTacToePlayer = None

        id = object()
        for attr_name in ('player', ):
            msg_attr_name = ' '.join([(_.capitalize() if i == 0 else _) for i, _ in enumerate(attr_name.split('_'))])
            attr_val = kwargs.pop(attr_name, id)
            if attr_val is id:
                raise ValueError(
                    f'{msg_attr_name} object is required and should be passed as "{attr_name}" key value argument'
                )
            elif not isinstance(attr_val, ITicTacToePlayer):
                raise ValueError(f'{msg_attr_name} object should be instance of IPlayer')

            setattr(self, f'_{attr_name}', attr_val)
        super().__init__(*args, **kwargs)

    def validate_move_str(self, s: str) -> TPoint:
        x, y = map(lambda v: v.strip(), s.split(':'))
        if isinstance(self._player.board.axis_x, IntAxis):
            x = int(x)
        if isinstance(self._player.board.axis_y, IntAxis):
            y = int(y)

        _ = self._player.board[x, y]
        if _ is not None:
            try:
                self._player.item_class(self._player.board, x, y)
            finally:
                self._player.board[x, y] = _

        return x, y

    def clean_move_to(self) -> TPoint:
        move_str = self.cleaned_data['move_to']
        try:
            x, y = self.validate_move_str(move_str)
        except Exception as err:
            raise ValidationError(err)
        return x, y


def get_player_choices():
    res = []
    gsm = get_game_site_manager()
    if gsm:
        gs = gsm['f84e0df2-8316-4346-913c-a3c52c233ace']
        res = [(player_cls.__name__, f'{_("is")} {player_cls.item_class.id}') for player_cls in gs.player_classes]

    return res


class TicTacToeCreateForm(Form):

    axis_choices = (
        (AsciiAxis.__name__, _('letters a..Z (max size is 26)')),
        (Int1Axis.__name__, _('numbers 1..50')),
        (IntAxis.__name__, _('numbers 0..49')),
    )
    player_choices = get_player_choices

    axis_x_size = IntegerField(label=_('Axis X size'), min_value=3, max_value=50, initial=3)
    axis_x_type = ChoiceField(label=_('Type axis X'), choices=axis_choices, initial=AsciiAxis.__name__)
    axis_y_size = IntegerField(label=_('Axis Y size'), min_value=3, max_value=50, initial=3)
    axis_y_type = ChoiceField(label=_('Type axis Y'), choices=axis_choices, initial=Int1Axis.__name__)
    cnt_in_row = IntegerField(label=_('Number in a row for win'), min_value=3, max_value=50, initial=3)
    player = ChoiceField(label=_('Player Type'), choices=player_choices, initial=TicTacToePlayerX.__name__)

    def __init__(self, *args, **kwargs):
        self._player = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        try:
            axis_x_type = globals()[cleaned_data['axis_x_type']]
            axis_y_type = globals()[cleaned_data['axis_y_type']]
            board = Board(axis_x_type(cleaned_data['axis_x_size']), axis_y_type(cleaned_data['axis_y_size']))
            player_type = globals()[cleaned_data['player']]
            self._player = player_type(board, cleaned_data['cnt_in_row'])
        except Exception as err:
            ValidationError(f'Can\'t create Player due to: {err}')
        else:
            cleaned_data['player'] = self._player

        return cleaned_data
