import queue

import pygame.key

import network
from States.Playing import playing
from GameNetworkProtocol import connection
from Entities import physics, animation
from Entities.ui_entity import TextDisplay
from . import ops
from .direction import Direction
import instance as inst


class NameTag(TextDisplay):
    idle_anim = animation.Animation('player_name_tag', alterable=True)


class Player(physics.PhysicsEntity):
    name:str
    remote:bool
    ready:bool = False
    color:tuple[int, int, int]

    name_tag:NameTag

    damage:int = 0
    stun_dur:int = 0

    controls_up:bool = False
    controls_left:bool = False
    controls_down:bool = False
    controls_right:bool = False
    controls_shift:bool = False

    controls_disabled:bool = False

    can_double_jump:bool = True
    jump_remaining:int = 0
    blocking:bool = False
    dead:bool = False

    attack_dir:Direction= Direction.NONE
    #num of frames to skip before attacking
    attack_countdown:int = 0

    target_pos:tuple[int,int] = None
    received_network:bool = False

    def __init__(self, pos:tuple[int, int], name:str, color:tuple[int, int, int], remote:bool = True):
        self.name = name
        self.color = color
        self.remote = remote

        self.name_tag = NameTag((0,0), 25, (5,-5), (255, 255, 255))
        self.name_tag.text = self.name

        self.load_animations()

        super().__init__(pos)

    def update_color(self, color:tuple[int, int, int]):
        self.color = color
        self.load_animations()
        self.change_anim(self.idle_anim)

    def load_animations(self):
        self.idle_anim = animation.Animation('player_idle', frame_dur=7, color=self.color)
        self.stun_anim = animation.Animation('player_stunned', frame_dur=5, color=self.color)
        self.block_anim = animation.Animation('player_block', color=self.color)
        self.attack_right_anim = animation.Animation('player_attack_r', offset=(-50, -50), frame_dur=5,
                                                     color=self.color, loop=False)
        self.attack_left_anim = animation.Animation('player_attack_l', offset=(-50, -50), frame_dur=5,
                                                     color=self.color, loop=False)
        self.attack_up_anim = animation.Animation('player_attack_u', offset=(-50, -50), frame_dur=5,
                                                    color=self.color, loop=False)


    @classmethod
    def from_connection(cls, c:connection.Connection):
        return cls((960,200), c.player_name, (0,0,0))

    def update(self):
        if self.dead:
            return

        if self.remote:
            #remote update
            self.move_to_target_smooth()
            self.update_remote()
        else:
            #local update
            self.update_local_input()

            if self.blocking and not self.controls_shift:
                self.stop_block()

            if self.bbox.y > 1080:
                self.die()

        #dead reckoning
        if not self.received_network:
            if self.remote:
                print('Predicted movement of ', self.name)
            self.update_shared_controls()

        #shared update
        if self.stun_dur > 0:
            self.disable_controls()
            self.stun_dur -= 1
        elif self.stun_dur == 0:
            self.change_anim(self.idle_anim)
            self.enable_controls()
            self.stun_dur -= 1

        if self.jump_remaining > 0:
            self.jump_remaining -= 1

        if self.attack_countdown == 0 and self.attack_dir != Direction.NONE:
            self.attack(self.attack_dir)
            self.attack_dir = Direction.NONE

        if self.attack_countdown > 0:
            self.attack_countdown -= 1

        if not self.received_network:
            #update physics
            super().update()
        else:
            self.update_animation()

        self.name_tag.set_pos((self.bbox.x - 25, self.bbox.bottom + 10))

        #pos op
        if not self.remote:
            network.queue_op(ops.Pos((self.bbox.x, self.bbox.y), self.speed,
                                     self.controls_up, self.controls_left, self.controls_down, self.controls_right))

    def update_remote(self):
        pass

    def update_local_input(self):
        keys = pygame.key.get_pressed()

        #controls that should stay active
        self.controls_shift = keys[pygame.K_LSHIFT]

        if self.controls_disabled:
            self.disable_controls()
            return

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
                self.jump()
            elif key == pygame.K_UP or key == pygame.K_KP8:
                self.attack_start(Direction.UP)
            elif key == pygame.K_LEFT or key == pygame.K_KP4:
                self.attack_start(Direction.LEFT)
            elif key == pygame.K_DOWN or key == pygame.K_KP5:
                pass
                # self.attack_start(Direction.DOWN)
            elif key == pygame.K_RIGHT or key == pygame.K_KP6:
                self.attack_start(Direction.RIGHT)
            elif key == pygame.K_LSHIFT:
                self.start_block()

    def update_shared_controls(self):
        if self.controls_left:
            if self.colliding_down:
                self.accelerate((-15, 0), max_x=30)
            else:
                self.accelerate((-4, 0), max_x=30)

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
                self.accelerate((0, -200), max_y=25)

    def attack_start(self, direction:Direction):
        if self.attack_dir != Direction.NONE:
            return

        if not self.remote:
            network.queue_op(ops.Attack(direction))

        self.disable_controls()

        if direction == Direction.RIGHT:
            self.change_anim(self.attack_right_anim)
            self.attack_countdown = 10
        elif direction == Direction.LEFT:
            self.change_anim(self.attack_left_anim)
            self.attack_countdown = 10
        elif direction == Direction.UP:
            self.change_anim(self.attack_up_anim)
            self.attack_countdown = 10
        elif direction == Direction.DOWN:
            raise Exception("attack down doesn't exist")
            # self.change_anim(self.attack_right_anim)
            # self.attack_countdown = 7
        self.attack_dir = direction

    def attack(self, attack_dir:Direction):
        if attack_dir == Direction.NONE:
            return
        elif attack_dir == Direction.RIGHT:
            attack_bbox = pygame.Rect((self.bbox.x + 70, self.bbox.y - 50), (80, 150))
        elif attack_dir == Direction.LEFT:
            attack_bbox = pygame.Rect((self.bbox.x - 50, self.bbox.y - 50), (80, 150))
        elif attack_dir == Direction.UP:
            attack_bbox = pygame.Rect((self.bbox.x - 35, self.bbox.y - 50), (170, 80))
        else:
            return

        state:playing.Playing = inst.state
        if self.remote:
            if attack_bbox.colliderect(state.player_me.bbox):
                state.player_me.hit(attack_dir)
        # else:
        #     #dead-reckoning but it has too many issues because of getting stunned
        #     for e in state.players.values():
        #         if attack_bbox.colliderect(e.bbox):
        #             # e:Player = e
        #             e.hit(attack_dir)

    def anim_done(self):
        if 'player_attack' in self.curr_anim.name:
            self.enable_controls()

        super().anim_done()

    def hit(self, hit_dir:Direction = Direction.NONE):
        if not self.blocking:
            self.stun(15)
            self.damage += 5

        self.hit_local_portion(hit_dir)

    def hit_local_portion(self, hit_dir:Direction):
        if not self.remote:
            network.queue_op(ops.Hit(self.damage))

            hit_strength = self.damage
            if self.blocking:
                hit_strength = int(hit_strength / 2)
            hit_strength_secondary:int = int(hit_strength / 2)

            if hit_dir == Direction.UP:
                self.accelerate((0, -hit_strength))
            elif hit_dir == Direction.LEFT:
                self.accelerate((-hit_strength, -hit_strength_secondary))
            elif hit_dir == Direction.DOWN:
                self.accelerate((0, hit_strength))
            elif hit_dir == Direction.RIGHT:
                self.accelerate((hit_strength, -hit_strength_secondary))

    def stun(self, dur:int):
        self.stun_dur = dur
        self.attack_countdown = 0
        self.attack_dir = Direction.NONE
        self.change_anim(self.stun_anim)

    def jump(self):
        if self.colliding_down:
            self.accelerate((0, -200), max_y=25)
            self.jump_remaining = 10
        elif self.can_double_jump:
            self.accelerate((0, -200), max_y=25)
            self.can_double_jump = False
            self.jump_remaining = 5

    def start_block(self):
        self.blocking = True
        self.disable_controls()
        self.change_anim(self.block_anim)
        if not self.remote:
            network.queue_op(ops.BlockStart())

    def stop_block(self):
        self.blocking = False
        self.enable_controls()
        self.change_anim(self.idle_anim)
        if not self.remote:
            network.queue_op(ops.BlockStop())

    def enable_controls(self):
        self.controls_disabled = False

    def disable_controls(self):
        self.controls_disabled = True

        self.controls_left = False
        self.controls_right = False
        self.controls_down = False
        self.controls_up = False
        while 1:
            try:
                inst.state.key_events.get(block=False)
            except queue.Empty:
                break
        return

    def move_to_target_smooth(self):
        if not self.target_pos:
            return

        pos = self.target_pos
        delta_pos = (pos[0] - self.bbox.x, pos[1] - self.bbox.y)
        speed_limit = 100

        if delta_pos[0] >= 0:
            speed_x = min(delta_pos[0], speed_limit)
            speed_x = max(speed_x, self.speed[0])
        else:
            speed_x = max(delta_pos[0], -speed_limit)
            speed_x = min(speed_x, self.speed[0])

        if delta_pos[1] >= 0:
            speed_y = min(delta_pos[1], speed_limit)
            speed_y = max(speed_y, self.speed[1])
        else:
            speed_y = max(delta_pos[1], -speed_limit)
            speed_y = min(speed_y, self.speed[1])

        new_pos = (self.bbox.x + speed_x, self.bbox.y + speed_y)
        self.set_pos(new_pos)
        if new_pos == self.target_pos:
            self.target_pos = None
        else:
            print('Interpolated movement of ', self.name)

    def on_collide_down(self):
        self.can_double_jump = True

    def on_collide_up(self):
        self.jump_remaining = 0

    def die(self):
        self.set_pos((0, 1100))
        self.name_tag.set_pos((0, 1100))
        self.dead = True
        if not self.remote:
            network.queue_op(ops.Death())