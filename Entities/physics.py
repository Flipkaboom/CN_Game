from abc import ABC, abstractmethod

import pygame.draw

from . import entity
import instance as inst

class PhysicsEntity(entity.Entity):
    gravity:bool

    speed:tuple[int, int] = (0,0)

    colliding_up:bool = False
    colliding_left:bool = False
    colliding_down:bool = False
    colliding_right:bool = False

    def __init__(self, pos:tuple[int, int], gravity:bool = True):
        self.gravity = gravity
        super().__init__(pos)

    # @abstractmethod
    def update(self):
        if self.gravity:
            self.accelerate((0, 2), max_y=30)

        self.move_collision(self.speed)

        super().update()

    def accelerate(self, acceleration:tuple[int, int], max_x:int = 100, max_y:int = 100):
        if acceleration[0] >= 0:
            speed_x = min(acceleration[0] + self.speed[0], max_x)
            speed_x = max(speed_x, self.speed[0])
        else:
            speed_x = max(acceleration[0] + self.speed[0], -max_x)
            speed_x = min(speed_x, self.speed[0])

        if acceleration[1] >= 0:
            speed_y = min(acceleration[1] + self.speed[1], max_y)
            speed_y = max(speed_y, self.speed[1])
        else:
            speed_y = max(acceleration[1] + self.speed[1], -max_y)
            speed_y = min(speed_y, self.speed[1])


        self.speed = (speed_x, speed_y)

    def dampen_x(self, dampen_acc:int):
        if self.speed[0] == 0:
            return

        if self.speed[0] > 0:
            self.speed = (max(self.speed[0] - dampen_acc, 0), self.speed[1])
        else:
            self.speed = (min(self.speed[0] + dampen_acc, 0), self.speed[1])

    def on_collide_up(self):
        pass

    def on_collide_left(self):
        pass

    def on_collide_down(self):
        pass

    def on_collide_right(self):
        pass


    def move_collision(self, vect:tuple[int, int]):
        self.colliding_up = False
        self.colliding_left = False
        self.colliding_down = False
        self.colliding_right = False

        self.bbox, self.speed = self.move_collision_recursive(vect)


    def move_collision_recursive(self, vect:tuple[int, int], bbox:pygame.Rect = None) -> (pygame.Rect, tuple[int, int]):
        if vect == (0,0):
            if not bbox:
                return self.bbox, (0,0)
            return bbox, (0,0)

        if not bbox:
            bbox = self.bbox

        new_bbox = bbox.move(vect)

        for _, layer in inst.state.layers.items():
            if layer.collision:
                for e in layer.entities:
                    clip = new_bbox.clip(e.bbox)
                    if clip.size != (0,0):
                        if vect[0] > 0:
                            inv_vect_pos_x = clip.right - 1
                        elif vect[0] < 0:
                            inv_vect_pos_x = clip.x
                        else:
                            inv_vect_pos_x = clip.centerx

                        if vect[1] > 0:
                            inv_vect_pos_y = clip.bottom - 1
                        elif vect[1] < 0:
                            inv_vect_pos_y = clip.y
                        else:
                            inv_vect_pos_y = clip.centery

                        inv_vect = (inv_vect_pos_x, inv_vect_pos_y,
                                    inv_vect_pos_x - vect[0], inv_vect_pos_y - vect[1])
                        inv_vect_clip = e.bbox.inflate(2,2).clipline(inv_vect)
                        backwards_movement = (inv_vect_clip[1][0] - inv_vect_clip[0][0],
                                              inv_vect_clip[1][1] - inv_vect_clip[0][1])
                        new_bbox = new_bbox.move(backwards_movement)

                        # if new_bbox.colliderect(e.bbox):
                        #     print(type(e))
                        #     print(vect, inv_vect, inv_vect_clip, backwards_movement, e.bbox.x, new_bbox.right)
                        #     print(vect, inv_vect, inv_vect_clip, backwards_movement, e.bbox.y, new_bbox.bottom)
                        #     raise Exception('Box still colliding after moving along inverted vector')

                        if inv_vect_clip[1][0] == e.bbox.x - 1:
                            remaining_vect = (0, self.speed[1])
                            if not self.colliding_left:
                                self.colliding_left = True
                                self.on_collide_left()
                        elif inv_vect_clip[1][0] == e.bbox.right:
                            remaining_vect = (0, self.speed[1])
                            if not self.colliding_right:
                                self.colliding_right = True
                                self.on_collide_right()
                        elif inv_vect_clip[1][1] == e.bbox.y - 1:
                            remaining_vect = (self.speed[0], 0)
                            if not self.colliding_down:
                                self.colliding_down = True
                                self.on_collide_down()
                        elif inv_vect_clip[1][1] == e.bbox.bottom:
                            remaining_vect = (self.speed[0], 0)
                            if not self.colliding_up:
                                self.colliding_up = True
                                self.on_collide_up()
                        else:
                            remaining_vect = (0,0)
                        #     raise Exception('Inverted vector clip with collision box did not line up with any bbox edge')

                        return self.move_collision_recursive(remaining_vect, new_bbox)

        return new_bbox, vect