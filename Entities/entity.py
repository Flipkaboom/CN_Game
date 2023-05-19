from abc import ABC, abstractmethod

import pygame

import game_input
from Entities import animation


class Entity(ABC):
    visible:bool = True
    uses_mouse:bool = False

    idle_anim:animation.Animation

    bbox:pygame.Rect
    curr_anim:animation.Animation


    def __init__(self):
        self.change_anim(self.idle_anim)
        self.bbox = self.curr_anim.sprite.get_rect()

    @abstractmethod
    def update(self):
        self.update_animation()

    def update_animation(self):
        self.curr_anim.update()
        if self.curr_anim.finished:
            self.anim_done()

    def anim_done(self):
        #FIXME anim_done method on animation?
        self.change_anim(self.idle_anim)

    def change_anim(self, anim:animation.Animation):
        self.curr_anim = anim.reset()

    def mouse_event(self, pos:tuple, down:bool):
        pass

    def move(self, pos:tuple):
        self.bbox = self.bbox.move(pos)


class PhysicsEntity(Entity, ABC):
    gravity:bool

    speed:tuple[int, int]

    @abstractmethod
    def update(self):
        #apply gravity

        #move

        #check collision

        super().update()

class UiEntity(Entity, ABC):
    uses_mouse = True
    hovering:bool = False

    def update(self):
        if self.bbox.collidepoint(game_input.mouse_canvas_pos()):
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
    hover_anim:animation.Animation
    click_anim:animation.Animation

    def __init__(self, pos: tuple):
        super().__init__()
        self.move(pos)

    def on_hover_start(self):
        self.change_anim(self.hover_anim)

    def on_hover_end(self):
        self.change_anim(self.idle_anim)

    def on_mouse_down(self):
        self.change_anim(self.click_anim)

    def on_mouse_up(self):
        self.change_anim(self.hover_anim)