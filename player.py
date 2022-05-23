import json
from constants import PLAYERS_CONNECTED
from data import Data

class Player:
    def __init__(self, id, user, address):
        self.user = user
        self.id = id
        self.ip = address[0]
        self.port = address[1]
        self.address = address

    def toDict(self):
        player_to_dict = {'user': self.user, 'id': self.id,'ip': self.ip, 'port': self.port}
        return player_to_dict

    def toJson(self):
        player_to_json = {'user': self.user, 'id': self.id,'ip': self.ip, 'port': self.port}
        return json.dumps(player_to_json)


    def fromJson(playerJson):
        playerJson = json.loads(playerJson)
        user = playerJson['user']
        id = playerJson['id']
        ip = playerJson['ip']
        port = playerJson['port']
        player = Player(id, user, (ip, port))
        return player
        

    def getAllPlayers(players):
        players_json = [obj.toDict() for obj in players]
        data = Data(PLAYERS_CONNECTED, players_json, "")
        return data.toJson()
