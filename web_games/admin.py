from django.contrib import admin

# Register your models here.

from .models import ActiveGame, GameBoard


class GameBoardAdmin(admin.ModelAdmin):
    pass

admin.site.register(GameBoard, GameBoardAdmin)


class ActiveGameAdmin(admin.ModelAdmin):
    pass

admin.site.register(ActiveGame, ActiveGameAdmin)

