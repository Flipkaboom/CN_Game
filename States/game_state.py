from abc import ABC, abstractmethod

from collections import OrderedDict

from Entities import entity

class Layer:
    entities:list[entity.Entity]
    collision:bool
    uses_mouse:bool

    def __init__(self, collision:bool = False, uses_mouse:bool = False):
        self.entities = list[entity.Entity]()
        self.collision = collision
        self.uses_mouse = uses_mouse

    def add_entity(self, e:entity.Entity):
        self.entities.append(e)

class GameState(ABC):
    layers:OrderedDict[str, Layer] #FIXME add list type

    @abstractmethod
    def frame_logic(self):
        pass

    def init_layers(self):
        self.layers = OrderedDict[str, Layer]()

    def add_layer(self, name:str, collision:bool = False, uses_mouse:bool = False):
        self.layers[name] = Layer(collision, uses_mouse)

    def mouse_event(self, pos:tuple, down:bool):
        for l in self.layers.values():
            for e in l.entities:
                if e.uses_mouse:
                    e.mouse_event(pos, down)

    def update_all(self):
        for l in self.layers.values():
            for e in l.entities:
                e.update()

    def stop(self):
        pass

""""
class Template(game_state.GameState):
    def __init__(self):
        self.init_layers()

        self.add_layer('background')
        self.add_layer('ui', uses_mouse=True)

        self.layers['ui'].add_entity(HostButton((407, 728)))
        self.layers['ui'].add_entity(JoinButton((991, 728)))

        self.name_input = NameInput((501, 548), (224, 0), 52, True)
        self.layers['ui'].add_entity(self.name_input)

    def frame_logic(self):
        self.update_all()
"""