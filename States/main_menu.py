import pygame

from Entities import animation
import loader
from Entities import entity
from States import game_state
import instance


class MainMenu(game_state.GameState):
    game_instance:instance.Instance

    def __init__(self, inst:instance.Instance):
        self.game_instance = inst

        self.init_layers()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)

        self.layers['ui'].add_entity(HostButton((407, 728)))
        self.layers['ui'].add_entity(JoinButton((991, 728)))

    def frame_logic(self):
        self.update_all()

class HostButton(entity.Button):
    idle_anim = animation.Animation('host_button', loop = True)
    hover_anim = animation.Animation('host_button_hover', loop = True)
    click_anim = hover_anim

    def on_mouse_up(self):
        instance.global_instance.change_state()#FIXME

class JoinButton(entity.Button):
    idle_anim = animation.Animation('join_button', loop = True)
    hover_anim = animation.Animation('join_button_hover', loop = True)
    click_anim = hover_anim


    def on_mouse_up(self):
        instance.global_instance.change_state()#FIXME