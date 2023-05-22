import network
from Entities import animation, entity, ui_entity
from States import game_state, lobby
import instance as inst


class Join(game_state.GameState):
    def __init__(self):
        super().__init__()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)

        self.layers['ui'].add_entity(Header((0, 58)))

        #FIXME before release
        self.ip_input = IpInput((165, 434))#, active=True)
        self.port_input = PortInput((1182, 431))
        self.layers['ui'].add_entity(self.ip_input)
        self.layers['ui'].add_entity(self.port_input)

        self.layers['ui'].add_entity(ConnectButton((698, 753)))

    def frame_logic(self):
        self.update_all()

class ConnectButton(ui_entity.Button):
    idle_anim = animation.Animation('join_button')
    hover_anim = animation.Animation('join_button_hover')
    click_anim = hover_anim

    def on_mouse_up(self):
        if not inst.state.port_input.text.isdigit():
            return
        network.init()
        network.join(inst.state.ip_input.text, int(inst.state.port_input.text))
        inst.change_state(lobby.Lobby())

class Header(ui_entity.UiEntity):
    idle_anim = animation.Animation('connect_header')

class IpInput(ui_entity.TextInput):
    text_offset = (50, 42)
    font_size = 122
    idle_anim = animation.Animation('ip_input', alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim

class PortInput(ui_entity.TextInput):
    text_offset = (125, 42)
    font_size = 122
    idle_anim = animation.Animation('port_input', alterable=True)
    hover_anim = idle_anim
    click_anim = hover_anim