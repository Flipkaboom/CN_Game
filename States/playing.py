from States import game_state
from Entities import player
import network

curr_state:game_state.GameState

class Playing(game_state.GameState):
    player_me:player.Player
    players: dict[tuple[str, int], player.Player] = dict[tuple[str, int], player.Player]()

    def __init__(self, player_me:player.Player, players:dict[tuple[str, int], player.Player]):
        global curr_state
        curr_state = self

        self.player_me = player_me
        self.players = players

        self.init_layers()

        self.add_layer('background')
        self.add_layer('players')
        self.add_layer('terrain', collision=True)
        self.add_layer('ui')

    def frame_logic(self):
        network.handle_all()

        self.update_all()

        network.send_all()