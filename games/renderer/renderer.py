# IDE: PyCharm
# Project: games
# Path: 
# File: renderer.py
# Contact: Semyon Mamonov <semyon.mamonov@gmail.com>
# Created by ox23 at 2022-05-31 (y-m-d) 5:44 PM


from abc import ABC, abstractmethod
from typing import Optional, Union
import html


class IRender(ABC):

    @abstractmethod
    def render(self) -> Optional[str]:
        raise NotImplementedError


class CharRender(IRender):
    char = '#'

    def __init__(self, char: Optional[str] = None):
        self.char = char or self.char

    def render(self):
        print(self.char, end='')


class NewLineCharRender(CharRender):
    char = "\n"


class HTMLRender(IRender):

    void_tags = ('area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img', 'input',
                 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr')

    content: Union[str, int] = '#'
    tag: str = ''
    attrs: dict = {}

    def __init__(self,
                 content: Union[int, str, 'HTMLRender', list['HTMLRender'], tuple['HTMLRender'], None] = None,
                 tag: str = None,
                 attrs: dict = None):
        self.content = content or self.content
        self.tag = tag or self.tag
        self.attrs = attrs if attrs is not None else dict(self.attrs)

    def _compose_attrs(self):
        result = []
        for k, v in self.attrs.items():
            result.append(f'{html.escape(str(k))}="{html.escape(str(v))}"')  # like <... class="fff ggg"  etc...>
        return ' '.join(result)

    @staticmethod
    def _compose_content_value(value):
        if isinstance(value, int):
            entity_name = html.entities.codepoint2name.get(value)
            if entity_name is None:
                raise ValueError('Content is not valid an entity integer value')
            return f'&{entity_name};'

        if isinstance(value, HTMLRender):
            return value.render()

        return html.escape(value)

    def _compose_content(self):
        if isinstance(self.content, (list, tuple)):
            res = [self._compose_content_value(v) for v in self.content]
        else:
            res = [self._compose_content_value(self.content)]
        return ''.join(res)

    def _compose(self):
        if self.tag:
            tag_e = f'</{html.escape(self.tag)}>'
            tag_fmt = '<%s%s>'
            tag_attrs = " ".join((html.escape(self.tag), self._compose_attrs())).strip()
            if self.tag in self.void_tags:
                if self.content:
                    raise Exception(f'Tag {self.tag} has content {self.content} but it is a void element')
                tag_b = tag_fmt % (tag_attrs, ' /')
                tag_e = ''
            else:
                tag_b = tag_fmt % (tag_attrs, '')
            return ''.join((tag_b, self._compose_content(), tag_e))
        else:
            return self._compose_content()

    def __str__(self) -> str:
        return self._compose()

    def render(self):
        return self._compose()
