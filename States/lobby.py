import pygame

import network
from Entities import animation, entity, ui_entity, player
from States import game_state, playing
import instance as inst


class Lobby(game_state.GameState):
    def __init__(self):
        self.players:dict[tuple[str, int], player.Player] = dict[tuple[str, int], player.Player]()

        self.init_layers()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)
        self.add_layer('players')

        self.layers['ui'].add_entity(Header((36,0)))

        self.ready = False
        self.layers['ui'].add_entity(ReadyButton((1538, 829)))

        self.color_input = ColorInput((1159, 734), active=True)
        self.layers['ui'].add_entity(self.color_input)
        self.color_preview = ColorPreview((1160, 836))
        self.layers['ui'].add_entity(self.color_preview)

        x = 400
        y = 18
        for i in range(0, 6):
            self.layers['players'].add_entity(PlayerUi((x, y)))
            y += 30 + 149
        x = 1160
        y = 18
        for i in range(0, 3):
            self.layers['players'].add_entity(PlayerUi((x, y)))
            y += 30 + 149

        conn_ui = ConnectionUi((x, y))
        conn_ui.text = network.address[0] + ':' + str(network.address[1])
        self.layers['ui'].add_entity(conn_ui)

    def frame_logic(self):

        for e in network.get_events():
            if e[0] == 'CONNECT':
                try:
                    self.players[e[1]] = player.Player.from_connection(network.Gnp.gl.connections[e[1]])
                    if self.ready:
                        network.queue_op(MatchReady(self.color_preview.rgb))
                except KeyError:
                    print('Got CONNECT event but connection is not available')
            if e[0] == 'DISCONNECT':
                try:
                    del self.players[e[1]]
                except KeyError:
                    print('Got DISCONNECT event but connection was not in player list')

        i = 0
        player_uis = self.layers['players'].entities
        for player_ui, player_conn in zip(player_uis, self.players.values()):
            player_ui.text = player_conn.name
            if  player_conn.ready:
                player_ui.change_anim(player_ui.ready_anim)
            else:
                player_ui.change_anim(player_ui.conn_anim)
            i += 1

        while i < 9:
            player_uis[i].text = ''
            player_uis[i].change_anim(player_uis[i].idle_anim)
            i += 1

        all_ready = True
        if not self.ready:
            all_ready = False
        for p in self.players.values():
            if not p.ready:
                all_ready = False
                break
        if all_ready:
            player_me = player.Player(inst.name, self.color_preview.rgb)
            inst.change_state(playing.Playing(player_me, self.players))
            return

        network.handle_all()

        self.update_all()

        network.send_all()


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
                inst.state.ready = True
                network.queue_op(MatchReady(inst.state.color_preview.rgb))
                #do ready


class PlayerUi(ui_entity.TextDisplay):
    text_offset = (50,50)
    font_size = 50

    idle_anim = animation.Animation('lobby_player_empty', loop=True, alterable=True)
    # hover_anim = idle_anim
    # click_anim = hover_anim
    ready_anim = animation.Animation('lobby_player_ready', loop=True, alterable=True)
    conn_anim = animation.Animation('lobby_player', loop=True, alterable=True)

class ConnectionUi(PlayerUi):
    idle_anim = animation.Animation('lobby_conn', loop=True, alterable=True)
    # hover_anim = idle_anim
    # click_anim = hover_anim

class ColorInput(ui_entity.TextInput):
    text_offset = (33, 0)
    font_size = 52
    idle_anim = animation.Animation('lobby_color_input', loop=True, alterable=True)
    # hover_anim = idle_anim
    # click_anim = hover_anim

class ColorPreview(ui_entity.UiEntity):
    idle_anim = animation.Animation('lobby_preview_unknown', loop=True)

    rgb:tuple[int, int, int] = (0, 0, 0)
    curr_color:str = ''
    valid_color:bool = False

    def update(self):
        super().update()

        new_color = inst.state.color_input.text
        if self.curr_color != new_color:
            self.curr_color = new_color
            try:
                tmp = pygame.Color(new_color)
                self.rgb = tmp.r, tmp.g, tmp.b
                self.change_anim(animation.Animation('lobby_preview', loop=True, color=self.rgb))
                self.valid_color = True
            except ValueError:
                self.change_anim(self.idle_anim)
                self.valid_color = False


from GameNetworkProtocol import connection as conn
from GameNetworkProtocol.operations import Operation

class MatchReady(Operation):
    length = 4

    color:tuple[int, int, int]

    def handle(self, parent_conn:conn.Connection):
        # print('Got ready from ', parent_conn.player_name)
        inst.state.players[parent_conn.address].ready = True
        inst.state.players[parent_conn.address].color = self.color

    def __init__(self, color:tuple[int, int, int]):
        self.color = color

    def encode(self) -> bytes:
        return self._encode_values(chars=(self.color[0], self.color[1], self.color[2]))


    @classmethod
    def from_data(cls, data:bytes):
        r, g, b = Operation._decode_values(data, num_chars=3)
        return cls((r, g, b))