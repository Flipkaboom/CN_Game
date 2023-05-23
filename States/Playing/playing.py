from States import game_state, lobby
from . import player, terrain
import network
import instance as inst


class Playing(game_state.GameState):
    player_me: player.Player
    players: dict[tuple[str, int], player.Player] = dict[tuple[str, int], player.Player]()

    uses_key_events = True

    def __init__(self, player_me: player.Player, players:dict[tuple[str, int], player.Player]):
        # global curr_state
        # curr_state = self
        super().__init__()

        self.player_me = player_me
        self.players = players

        self.add_layer('background')

        self.add_layer('terrain', collision=True)
        self.layers['terrain'].add_entity(terrain.LargePlatform((346, 764)))
        self.layers['terrain'].add_entity(terrain.SmallPlatform((1138, 521)))
        self.layers['terrain'].add_entity(terrain.SmallPlatform((543, 359)))

        self.add_layer('players')
        for p in players.values():
            p.ready = False
            self.layers['players'].add_entity(p)

        self.add_layer('player_me')
        self.layers['player_me'].add_entity(self.player_me)
        self.player_me.ready = False

        self.add_layer('name_tags')
        self.layers['name_tags'].add_entity(self.player_me.name_tag)
        for p in players.values():
            self.layers['name_tags'].add_entity(p.name_tag)


        self.add_layer('ui')

    def frame_logic(self):
        all_dead_remote = True
        for p in self.layers['players'].entities:
            p:player.Player = p
            if not p.dead:
                all_dead_remote = False
            p.received_network = False

        if all_dead_remote and self.player_me.dead:
            inst.change_state(lobby.Lobby(list(self.players.keys())))

        network.handle_all()

        self.update_all()

        network.send_all()