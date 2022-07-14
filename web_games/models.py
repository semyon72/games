from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class GameBoard(models.Model):
    data = models.TextField(verbose_name=_('Serialized last state of game\'s board.'))
    created = models.DateTimeField(verbose_name=_('Created'), blank=True, auto_now_add=True)
    modified = models.DateTimeField(verbose_name=_('Modified'), blank=True, auto_now=True)
    completed = models.DateTimeField(verbose_name=_('Completed'), blank=True, null=True, default=None)


class ActiveGame(models.Model):
    gsid = models.CharField(max_length=255, verbose_name=_('Game session id'))
    game_uuid = models.CharField(max_length=255, verbose_name=_('Game unique id'))
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE)
    player_class = models.CharField(max_length=255, verbose_name=_('Player class for this game'))
    player_kwargs = models.CharField(max_length=255, verbose_name=_('Keyword arguments for player class'))

    def __str__(self):
        return f'{self.game_uuid}:session[{self.gsid}]:{self._meta.pk.name}[{self.pk}]'
