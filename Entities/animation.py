import time

import pygame

import loader

BASE_FRAME_DUR = 2

class Animation:
    loop:bool
    offset:tuple
    frame_dur:int
    color:tuple
    alterable:bool

    sprite:pygame.Surface
    sprite_original:pygame.Surface
    sprite_list:list[pygame.Surface]

    frame_count:int = 0
    curr_frame:int = 0
    static:bool = False
    finished:bool = False

    def __init__(self, name:str, loop:bool = True, offset:tuple = (0,0), frame_dur:int = BASE_FRAME_DUR,
                 color:tuple = (), alterable:bool = False, sprite_list:list[pygame.Surface] = None):
        self.loop = loop
        self.offset = offset
        self.frame_dur = frame_dur
        self.color = color
        self.alterable = alterable

        if name == '':
            self.sprite_list = sprite_list
        else:
            self.sprite_list = loader.load_sprites(name)

        if not self.color == ():
            self._color_sprites()

        if len(self.sprite_list) == 0:
            raise Exception("Cannot load animation with no sprites")
        if len(self.sprite_list) == 1:
            self.static = True

        # print(name, self.static)

        if self.alterable:
            self.sprite_original = self.sprite_list[0]
            self.sprite = self.sprite_original.copy()
        else:
            self.sprite = self.sprite_list[0]

    def copy(self):
        return Animation('', self.loop, self.offset, self.frame_dur, (), self.alterable, self.sprite_list)

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
            if self.alterable:
                self.sprite_original = self.sprite_list[self.curr_frame]
                self.sprite = self.sprite_original.copy()
            else:
                self.sprite = self.sprite_list[self.curr_frame]

    def restore_unaltered(self):
        if self.alterable:
            self.sprite = self.sprite_original.copy()


    def reset(self):
        self.frame_count = 0
        self.curr_frame = 0
        self.finished: bool = False

        if self.alterable:
            self.sprite_original = self.sprite_list[self.curr_frame]
            self.sprite = self.sprite_original.copy()
        else:
            self.sprite = self.sprite_list[0]
        return self

import pygame