from States import game_state

class Playing(game_state.GameState):
    def __init__(self):
        self.init_layers()

        self.add_layer('background')
        self.add_layer('players')
        self.add_layer('terrain')
        self.add_layer('ui')

    def frame_logic(self):
        pass