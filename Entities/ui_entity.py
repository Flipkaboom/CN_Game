import random
from abc import ABC, abstractmethod

import pygame

from Entities import entity, animation
import user_input


class UiEntity(entity.Entity, ABC):
    uses_mouse = True
    hovering:bool = False

    def __init__(self, pos:tuple, uses_mouse:bool = False):
        super().__init__(pos)
        self.uses_mouse = uses_mouse

    def update(self):
        if self.bbox.collidepoint(user_input.mouse_canvas_pos()):
            if not self.hovering:
                self.hovering = True
                self.on_hover_start()
        else:
            if self.hovering:
                self.hovering = False
                self.on_hover_end()

        super().update()

    def mouse_event(self, pos:tuple, down:bool):
        if self.bbox.collidepoint(pos):
            if down:
                self.on_mouse_down()
            else:
                self.on_mouse_up()

    def on_hover_start(self):
        pass

    def on_hover_end(self):
        pass

    def on_mouse_down(self):
        pass

    def on_mouse_up(self):
        pass

class Button(UiEntity, ABC):
    idle_anim:animation.Animation
    hover_anim:animation.Animation = None
    click_anim:animation.Animation = None

    def __init__(self, pos: tuple):
        super().__init__(pos, uses_mouse=True)

    def on_hover_start(self):
        if self.hover_anim:
            self.change_anim(self.hover_anim)

    def on_hover_end(self):
        if self.hover_anim:
            self.change_anim(self.idle_anim)

    def on_mouse_down(self):
        if self.click_anim:
            self.change_anim(self.click_anim)

    def on_mouse_up(self):
        if self.click_anim:
            self.change_anim(self.hover_anim)

class TextDisplay(Button, ABC):
    text:str
    text_surface:pygame.Surface
    text_offset:tuple = (0,0)
    font_size = 50
    font:pygame.font

    def __init__(self, pos: tuple, font_size: int = 0, text_offset: tuple = ()):
        super().__init__(pos)

        self.text = ''
        if text_offset != ():
            self.text_offset = text_offset
        if font_size > 0:
            self.font_size = font_size

        self.font = pygame.font.Font('fonts/comic.ttf', self.font_size)

    def update(self):
        super().update()
        self.text_surface = self.font.render(self.text, True, (0,0,0))
        self.curr_anim.restore_unaltered()
        self.curr_anim.sprite.blit(self.text_surface, self.text_offset)


class TextInput(TextDisplay):
    active:bool
    disabled:bool = False

    def __init__(self, pos: tuple, font_size: int = 0, text_offset: tuple = (), active=False):
        super().__init__(pos, font_size, text_offset)

        self.active = active
        if active:
            #FIXME before release
            user_input.text_input = 'red'

    def update(self):
        if self.active and not self.disabled:
            self.text = user_input.text_input

        super().update()

    def mouse_event(self, pos:tuple, down:bool):
        if not self.bbox.collidepoint(pos):
            if down:
                self.active = False

        super().mouse_event(pos, down)

    def on_mouse_down(self):
        self.active = True
        user_input.text_input = self.text
        super().on_mouse_down()