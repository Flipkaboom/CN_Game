from Entities import animation, entity, ui_entity
from States import game_state
import instance as inst
from States import join, lobby
import network


class MainMenu(game_state.GameState):
    def __init__(self):
        super().__init__()

        self.add_layer('decoration')
        self.add_layer('ui', uses_mouse=True)

        self.layers['ui'].add_entity(HostButton((407, 703)))
        self.layers['ui'].add_entity(JoinButton((991, 703)))

        self.name_input = NameInput((589, 573), active=True)
        self.layers['ui'].add_entity(self.name_input)

        self.layers['decoration'].add_entity(Title((95, 70)))
        self.layers['decoration'].add_entity(Ghost((47, 40)))
        self.layers['decoration'].add_entity(Ghost((45, 937)))
        self.layers['decoration'].add_entity(Ghost((1770, 40)))
        self.layers['decoration'].add_entity(Ghost((1770, 937)))


    def frame_logic(self):
        self.update_all()

class HostButton(ui_entity.Button):
    idle_anim = animation.Animation('host_button')
    hover_anim = animation.Animation('host_button_hover')
    click_anim = hover_anim

    def on_mouse_up(self):
        inst.name = inst.state.name_input.text
        network.init()
        inst.change_state(lobby.Lobby())

class JoinButton(ui_entity.Button):
    idle_anim = animation.Animation('join_button')
    hover_anim = animation.Animation('join_button_hover')
    click_anim = hover_anim

    def on_mouse_up(self):
        inst.name = inst.state.name_input.text
        inst.change_state(join.Join())

class NameInput(ui_entity.TextInput):
    text_offset = (33, 0)
    font_size = 52
    idle_anim = animation.Animation('name_input', alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim

class Title(ui_entity.UiEntity):
    idle_anim = animation.Animation('title')

class Ghost(ui_entity.UiEntity):
    idle_anim = animation.Animation('player_idle', frame_dur=7)