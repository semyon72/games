# IDE: PyCharm
# Project: games
# Path: web_games/forms
# File: base.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-24 (y-m-d) 12:20 PM
from django.core.exceptions import ValidationError
from django.forms import Form, CharField


class PlayersNextMoveForm(Form):

    move_to = CharField(
        max_length=12,
        required=True,
        help_text='Use ":" as axis divider. For example, first cell can be referenced as a:1'
    )

    def clean_move_to(self):
        raise ValidationError('move is not valid')