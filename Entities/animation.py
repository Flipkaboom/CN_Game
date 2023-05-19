import time

import pygame

import loader

BASE_FRAME_DUR = 2

class Animation:
    loop:bool
    offset:tuple
    frame_dur:int
    color:tuple

    sprite:pygame.Surface
    sprite_list:list[pygame.Surface]

    frame_count:int = 0
    curr_frame = 0
    static:bool = False
    finished:bool = False

    def __init__(self, name:str, loop:bool = False, offset:tuple = (0,0), frame_dur:int = BASE_FRAME_DUR, color:tuple = ()):
        self.loop = loop
        self.offset = offset
        self.frame_dur = frame_dur
        self.color = color

        self.sprite_list = loader.load_sprites(name)

        if not self.color == ():
            self._color_sprites()

        if len(self.sprite_list) == 0:
            raise Exception("Cannot load animation with no sprites")
        if len(self.sprite_list) == 1:
            self.static = True
        self.sprite = self.sprite_list[0]

    def _color_sprites(self):
        for greyscale_img in self.sprite_list:
            greyscale_img.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)

    def update(self):
        if self.static:
            return

        self.frame_count += 1

        if self.frame_count % self.frame_dur == 0:
            self.curr_frame += 1
            if self.curr_frame >= len(self.sprite_list):
                if self.loop:
                    self.curr_frame = 0
                else:
                    self.finished = True
                    return
            self.sprite = self.sprite_list[self.curr_frame]

    def reset(self):
        self.frame_count = 0
        self.curr_frame = 0
        self.static: bool = False
        self.finished: bool = False
        self.sprite = self.sprite_list[0]
        return self

import pygame