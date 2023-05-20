import pygame

import network
from Entities import animation, entity, ui_entity
from States import game_state
import instance as inst


class Lobby(game_state.GameState):
    def __init__(self):
        self.init_layers()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)
        self.add_layer('players')

        self.layers['ui'].add_entity(Header((36,0)))

        self.layers['ui'].add_entity(ReadyButton((1538, 829)))

        self.color_input = ColorInput((1159, 734), active=True)
        self.layers['ui'].add_entity(self.color_input)
        self.color_preview = ColorPreview((1160, 836))
        self.layers['ui'].add_entity(self.color_preview)

        x = 400
        y = 18
        for i in range(0, 6):
            self.layers['players'].add_entity(Player((x,y)))
            y += 30 + 149
        x = 1160
        y = 18
        for i in range(0, 3):
            self.layers['players'].add_entity(Player((x, y)))
            y += 30 + 149

        conn = Connection((x, y))
        conn.text = network.address[0] + ':' + str(network.address[1])
        self.layers['ui'].add_entity(conn)

    def frame_logic(self):
        i = 0
        conns = network.active_conns()
        for player in self.layers['players'].entities:
            if i < len(conns):
                player.text = conns[i].player_name
            else:
                player.text = ''
            i += 1

        self.update_all()


class Header(ui_entity.UiEntity):
    idle_anim = animation.Animation('lobby_header', loop=True)

class ReadyButton(ui_entity.Button):
    idle_anim = animation.Animation('lobby_ready', loop = True)
    hover_anim = animation.Animation('lobby_ready_hover', loop = True)
    click_anim = hover_anim

    locked_anim = animation.Animation('lobby_ready_locked', loop = True)

    locked:bool = False

    def on_mouse_up(self):
        if not self.locked:
            if inst.state.color_preview.valid_color:
                self.locked = True
                self.idle_anim = self.locked_anim
                self.hover_anim = self.locked_anim
                self.change_anim(self.locked_anim)
                inst.state.color_input.disabled = True
                #do ready


class Player(ui_entity.TextDisplay):
    text_offset = (50,50)
    font_size = 50
    idle_anim = animation.Animation('lobby_player', loop=True, alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim

class Connection(Player):
    idle_anim = animation.Animation('lobby_conn', loop=True, alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim

class ColorInput(ui_entity.TextInput):
    text_offset = (33, 0)
    font_size = 52
    idle_anim = animation.Animation('lobby_color_input', loop=True, alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim

class ColorPreview(ui_entity.UiEntity):
    idle_anim = animation.Animation('lobby_preview_unknown', loop=True)

    curr_color:str = ''
    valid_color:bool = False

    def update(self):
        super().update()

        new_color = inst.state.color_input.text
        if self.curr_color != new_color:
            self.curr_color = new_color
            try:
                tmp = pygame.Color(new_color)
                rgb = tmp.r, tmp.g, tmp.b
                self.change_anim(animation.Animation('lobby_preview', loop=True, color=rgb))
                self.valid_color = True
            except ValueError:
                self.change_anim(self.idle_anim)
                self.valid_color = False
