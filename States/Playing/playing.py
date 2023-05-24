from States import game_state, lobby
from . import player, terrain
import network
import instance as inst


class Playing(game_state.GameState):
    player_me: player.Player
    players: dict[tuple[str, int], player.Player] = dict[tuple[str, int], player.Player]()

    uses_key_events = True
    background_color = (159, 207, 229)
    border_color = (255, 255, 255)

    def __init__(self, player_me: player.Player, players:dict[tuple[str, int], player.Player]):
        # global curr_state
        # curr_state = self
        super().__init__()

        self.player_me = player_me
        self.players = players

        self.add_layer('background')
        self.layers['background'].add_entity(terrain.CloudRight((1332,57)))
        self.layers['background'].add_entity(terrain.CloudLeft((0, 57)))
        self.layers['background'].add_entity(terrain.CloudUp((0,0)))
        self.layers['background'].add_entity(terrain.CloudDown((300,948)))

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
        for e in network.get_events():
            if e[0] == 'CONNECT':
                try:
                    self.players[e[1]] = player.Player.from_connection(network.Gnp.gl.connections[e[1]])
                    self.players[e[1]].die()
                except KeyError:
                    print('Got CONNECT event but connection is not available')
            if e[0] == 'DISCONNECT':
                try:
                    self.players[e[1]].die()
                    del self.players[e[1]]
                except KeyError:
                    print('Got DISCONNECT event but connection was not in player list')

        alive_count = 0
        for p in self.layers['players'].entities:
            p:player.Player = p
            if not p.dead:
                alive_count += 1
            p.received_network = False

        if not self.player_me.dead:
            alive_count += 1

        if (alive_count <= 1 and len(self.layers['players'].entities) > 0) or alive_count == 0:
            inst.change_state(lobby.Lobby(list(self.players.keys()), win=not self.player_me.dead,
                                          lost=self.player_me.dead, color=self.player_me.color))
            return

        network.handle_all()

        self.update_all()

        network.send_all()