from abc import ABC, abstractmethod

import pygame

from Entities import animation


class Entity(ABC):
    visible:bool = True
    uses_mouse:bool = False

    idle_anim:animation.Animation

    bbox:pygame.Rect
    curr_anim:animation.Animation


    def __init__(self, pos:[int, int]):
        self.change_anim(self.idle_anim)
        self.bbox = self.curr_anim.sprite.get_rect()
        self.move(pos)

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
        if anim.alterable:
            self.curr_anim = anim.copy()
        else:
            self.curr_anim = anim.reset()

    def mouse_event(self, pos:tuple, down:bool):
        pass

    def move(self, pos:tuple):
        self.bbox = self.bbox.move(pos)

    def set_pos(self, pos:[int, int]):
        self.bbox = pygame.Rect(pos[0], pos[1], self.bbox.width, self.bbox.height)