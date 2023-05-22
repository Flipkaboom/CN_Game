import queue
from enum import Enum

import pygame.key

import network
from States.Playing import playing
from GameNetworkProtocol import connection
from Entities import physics, animation
from . import ops
import instance as inst


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    NONE = 4


class Player(physics.PhysicsEntity):
    name:str
    remote:bool
    ready:bool = False
    color:tuple[int, int, int]

    controls_up:bool = False
    controls_left:bool = False
    controls_down:bool = False
    controls_right:bool = False

    can_double_jump:bool = True
    jump_remaining:int = 0

    attack_dir:Direction= Direction.NONE
    #num of frames to skip before attacking
    attack_countdown:int = 0

    received_network:bool = False

    def __init__(self, pos:tuple[int, int], name:str, color:tuple[int, int, int], remote:bool = True):
        self.name = name
        self.color = color
        self.remote = remote

        self.load_animations()

        super().__init__(pos)

    def update_color(self, color:tuple[int, int, int]):
        self.color = color
        self.load_animations()
        self.change_anim(self.idle_anim)

    def load_animations(self):
        self.idle_anim = animation.Animation('player_idle', frame_dur=15, color=self.color)
        self.attack_right_anim = animation.Animation('player_attack_r', offset=(-50, -50), frame_dur=3,
                                                     color=self.color, loop=False)

    @classmethod
    def from_connection(cls, c:connection.Connection):
        return cls((960,200), c.player_name, (0,0,0))

    def update(self):
        if self.remote:
            self.update_remote()
        else:
            self.update_local_input()

        if not self.received_network:
            if self.remote:
                print('Performed dead reckoning on ', self.name)
            self.update_shared_controls()

        #shared update
        if self.jump_remaining > 0:
            self.jump_remaining -= 1

        if self.attack_countdown == 0 and self.attack_dir != Direction.NONE:
            self.attack(self.attack_dir)
            self.attack_dir = Direction.NONE

        if self.attack_countdown > 0:
            self.attack_countdown -= 1

        #update physics
        super().update()

        if not self.remote:
            network.queue_op(ops.Pos((self.bbox.x, self.bbox.y), self.speed,
                                     self.controls_up, self.controls_left, self.controls_down, self.controls_right))

    def update_remote(self):
        pass

    def update_local_input(self):
        keys = pygame.key.get_pressed()

        self.controls_left = keys[pygame.K_a]
        self.controls_right = keys[pygame.K_d]
        self.controls_down = keys[pygame.K_s]
        self.controls_up = keys[pygame.K_w] or keys[pygame.K_SPACE]

        while 1:
            try:
                key = inst.state.key_events.get(block=False).key
            except queue.Empty:
                break
            if key == pygame.K_w or key == pygame.K_SPACE:
                self.jump_local()
            if key == pygame.K_UP or key == pygame.K_KP8:
                self.attack_start(Direction.UP)
            if key == pygame.K_LEFT or key == pygame.K_KP4:
                self.attack_start(Direction.LEFT)
            if key == pygame.K_DOWN or key == pygame.K_KP5:
                self.attack_start(Direction.DOWN)
            if key == pygame.K_RIGHT or key == pygame.K_KP6:
                self.attack_start(Direction.RIGHT)

    def update_shared_controls(self):
        if self.controls_left:
            if self.colliding_down:
                self.accelerate((-15, 0), max_x=-30)
            else:
                self.accelerate((-4, 0), max_x=-30)

        if self.controls_right:
            if self.colliding_down:
                self.accelerate((15, 0), max_x=30)
            else:
                self.accelerate((4, 0), max_x=30)

        if not (self.controls_left or self.controls_right):
            if self.colliding_down:
                self.dampen_x(5)
            else:
                self.dampen_x(1)

        if self.controls_down:
            pass#FIXME go down faster?

        if self.controls_up:
            if self.jump_remaining > 0:
                self.accelerate((0, -200), max_y=-25)

    def attack_start(self, direction:Direction):
        if self.attack_dir != Direction.NONE:
            return

        if direction == Direction.RIGHT:
            self.change_anim(self.attack_right_anim)
            self.attack_countdown = 7
            self.attack_dir = Direction.RIGHT
            # self.accelerate((200,0))

    def attack(self, attack_dir:Direction):
        if attack_dir == Direction.NONE:
            return
        if attack_dir == Direction.RIGHT:
            attack_bbox = pygame.Rect((self.bbox.x + 85, self.bbox.y - 28), (65, 120))
        else:
            return

        state:playing.Playing = inst.state
        for e in state.layers['players'].entities:
            if attack_bbox.colliderect(e.bbox):
                # e:Player = e
                e.accelerate((100, 0))

    def jump_local(self):
        if self.colliding_down:
            self.accelerate((0, -200), max_y=-25)
            self.jump_remaining = 10
        elif self.can_double_jump:
            self.accelerate((0, -200), max_y=-25)
            self.can_double_jump = False
            self.jump_remaining = 5

    def jump_remote(self):
        pass

    def on_collide_down(self):
        self.can_double_jump = True