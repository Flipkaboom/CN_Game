from GameNetworkProtocol import connection

class Player:
    name:str
    ready:bool = False
    color:tuple[int, int, int]

    def __init__(self, name:str, color:tuple[int, int, int]):
        self.name = name
        self.color = color

    @classmethod
    def from_connection(cls, c:connection.Connection):
        #FIXME add all relevant info from connection
        return cls(c.player_name, (0,0,0))
