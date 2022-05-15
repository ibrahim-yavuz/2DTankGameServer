import json
from constants import PLAYERS_CONNECTED
from data import Data

class Player:
    def __init__(self, user, address):
        self.user = user
        self.ip = address[0]
        self.port = address[1]
        self.address = address

    def toJson(self):
        player_to_json = {'user': self.user, 'ip': self.ip, 'port': self.port}
        return json.dumps(player_to_json)

    def fromJson(playerJson):
        playerJson = json.loads(playerJson)
        user = playerJson['user']
        ip = playerJson['ip']
        port = playerJson['port']
        player = Player(user, (ip, port))
        return player

    def getAllPlayers(players):
        players_json = "["
        players_json = players_json + ','.join(players)
        players_json = players_json + "]"
        data = Data(PLAYERS_CONNECTED, json.loads(players_json))
        return data
