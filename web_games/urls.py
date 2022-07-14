# IDE: PyCharm
# Project: games
# Path: web_games
# File: urls.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-23 (y-m-d) 11:38 AM

"""
Usage in root urls.py

urlpatterns = [
    .....
    path('tictactoe_games/', TicTacToeGameSite('games').urls),
    path('tictactoe_web_games/', TicTacToeGameSite('web_games').urls),

    *sites.get_root_path(),  # defaults are root_route='games/' and app_namespace='games'
    *GameSiteManager(TicTacToeGameSite, root_route='web_games/', app_namespace='weeb_games').get_root_path(),
    .....
]
"""
