# IDE: PyCharm
# Project: games
# Path: web_games/views
# File: tictactoe.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-23 (y-m-d) 12:13 PM

import uuid
import json
from datetime import datetime
from typing import Type

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, ListView, DeleteView

from games.board.serializer import JSONBoardSerializer
from games.tictactoe.player import ITicTacToePlayer, PlayerWon

from ..utils import get_module_attr, get_game_site_manager
from ..forms.tictactoe import TicTacToePlayersNextMoveForm, TicTacToeCreateForm
from ..models import ActiveGame, GameBoard

GAME_SESSION_COOKIE_NAME = 'game_sessionid'


class GameViewMixin(View):

    def get(self, request: HttpRequest, *args, **kwargs):
        request.session.setdefault(GAME_SESSION_COOKIE_NAME, str(uuid.uuid4()))
        return super().get(request, *args, **kwargs)

    @classmethod
    def get_site(cls) -> Type['IGameSite']:
        gm = get_game_site_manager()
        return gm.get_game_site(cls)


class TicTacToePlayView(GameViewMixin, FormView):

    template_name = 'web_games/tictactoe_play.html'
    form_class = TicTacToePlayersNextMoveForm
    active_game_object: ActiveGame = None
    _player: ITicTacToePlayer = None
    _opponent_player: ITicTacToePlayer = None

    def get_player(self) -> ITicTacToePlayer:
        pk = self.kwargs['pk']
        game_uuid = self.kwargs.get('guid')
        gsid = self.request.session.session_key
        ag = get_object_or_404(ActiveGame.objects.filter(pk=pk, game_uuid=game_uuid, gsid=gsid))
        self.active_game_object = ag
        board = JSONBoardSerializer(None).loads(ag.board.data).board

        pcls = globals().get(ag.player_class)
        if pcls is None:
            pcls = get_module_attr(ag.player_class)

        pkwargs = json.loads(ag.player_kwargs)
        player = pcls(board, **pkwargs)
        return player

    def get_opponent_player(self) -> ITicTacToePlayer:
        site = self.get_site()
        pcls = [cls for cls in site.player_classes if cls is not type(self._player)][0]
        res = pcls(self._player.board, self._player.cnt_in_row)
        return res

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._player = self.get_player()
        self._opponent_player = self.get_opponent_player()

    def get_success_url(self):
        site = self.get_site()
        return reverse(
            site.get_viewname(self),
            current_app=self.request.resolver_match.namespace,
            args=(self.active_game_object.pk, )
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['player'] = self._player
        return kwargs

    def form_valid(self, form):
        game_is_complete = False

        try:
            self._player.play(*form.cleaned_data['move_to'])
        except PlayerWon:
            game_is_complete = True

        # bot
        if not self._opponent_player.is_board_full() and not game_is_complete:
            opponent_move = self._opponent_player.move_suggestion()
            try:
                self._opponent_player.play(*opponent_move)
            except PlayerWon:
                game_is_complete = True
        # end-bot

        # store all changes
        self.active_game_object.board.data = JSONBoardSerializer(self._player.board).dumps()
        if game_is_complete or self._player.is_board_full():
            self.active_game_object.board.completed = datetime.now()

        self.active_game_object.board.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_won = self._player.is_won()
        context['player'] = self._player

        is_opponent_won = self._opponent_player.is_won()
        context['opponent_player'] = self._opponent_player

        is_board_full = self._player.is_board_full()
        if is_opponent_won or is_won or is_board_full:
            context['form'] = ''

        return context


class TicTacToeCreateView(GameViewMixin, FormView):

    template_name = 'web_games/tictactoe_create.html'
    form_class = TicTacToeCreateForm
    active_game_object: ActiveGame = None

    def get_success_url(self):
        site = self.get_site()
        return reverse(
            site.get_viewname(TicTacToePlayView),
            current_app=self.request.resolver_match.namespace,
            args=(self.active_game_object.pk, )
        )

    def form_valid(self, form):
        player = form.cleaned_data['player']

        gb = GameBoard()
        gb.data = JSONBoardSerializer(player.board).dumps()
        gb.save()

        ag = ActiveGame()
        ag.gsid = self.request.session.session_key
        ag.game_uuid = self.kwargs.get('guid')
        ag.player_class = f'{player.__module__}.{player.__class__.__name__}'
        ag.player_kwargs = json.dumps({'cnt_in_row': player.cnt_in_row})
        ag.board = gb
        ag.save()

        self.active_game_object = ag
        return super().form_valid(form)


class TicTacToeView(GameViewMixin, ListView):
    template_name = 'web_games/tictactoe_list.html'
    paginate_by = 12

    def get_queryset(self) -> list[ActiveGame]:
        res = ActiveGame.objects.filter(
            game_uuid=self.kwargs.get('guid'),
            gsid=self.request.session.session_key,
        ).order_by('-pk')
        return res


class TicTacToeDeleteView(GameViewMixin, DeleteView):
    template_name = 'web_games/tictactoe_delete.html'

    def get_success_url(self):
        site = self.get_site()
        return reverse(
            site.get_viewname(TicTacToeView),
            current_app=self.request.resolver_match.namespace,
        )

    def form_valid(self, form):
        self.object.board.delete()
        return super().form_valid(form)

    def get_queryset(self) -> list[ActiveGame]:
        res = ActiveGame.objects.filter(
            game_uuid=self.kwargs.get('guid'),
            gsid=self.request.session.session_key,
        )
        return res
