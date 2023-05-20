from Entities import animation, entity, ui_entity
from States import game_state
import instance as inst
from States import join, lobby
import network


class MainMenu(game_state.GameState):
    def __init__(self):
        self.init_layers()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)

        self.layers['ui'].add_entity(HostButton((407, 728)))
        self.layers['ui'].add_entity(JoinButton((991, 728)))

        self.name_input = NameInput((589, 540), active=True)
        self.layers['ui'].add_entity(self.name_input)

    def frame_logic(self):
        self.update_all()

class HostButton(ui_entity.Button):
    idle_anim = animation.Animation('host_button', loop = True)
    hover_anim = animation.Animation('host_button_hover', loop = True)
    click_anim = hover_anim

    def on_mouse_up(self):
        inst.name = inst.state.name_input.text
        network.init()
        inst.change_state(lobby.Lobby())

class JoinButton(ui_entity.Button):
    idle_anim = animation.Animation('join_button', loop = True)
    hover_anim = animation.Animation('join_button_hover', loop = True)
    click_anim = hover_anim

    def on_mouse_up(self):
        inst.name = inst.state.name_input.text
        inst.change_state(join.Join())

class NameInput(ui_entity.TextInput):
    text_offset = (33, 0)
    font_size = 52
    idle_anim = animation.Animation('name_input', loop=True, alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim