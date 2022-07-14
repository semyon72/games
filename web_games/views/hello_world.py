# IDE: PyCharm
# Project: games
# Path: web_games/views
# File: hello_world.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-06-23 (y-m-d) 11:41 AM

from django.views.generic import TemplateView


class HelloWorld(TemplateView):
    template_name = 'web_games/hello_world.html'
