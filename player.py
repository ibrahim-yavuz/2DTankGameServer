import json
from constants import PLAYERS_CONNECTED
from data import Data

class Player:
    def __init__(self, username, address):
        self.username = username
        self.host = address[0]
        self.port = address[1]
        self.address = address

    def toJson(self):
        player_to_json = {'username': self.username, 'host': self.host, 'port': self.port}
        return json.dumps(player_to_json)

    def fromJson(playerJson):
        playerJson = json.loads(playerJson)
        username = playerJson['username']
        host = playerJson['host']
        port = playerJson['port']
        player = Player(username, (host, port))
        return player

    def getAllPlayers(players):
        players_json = "["
        players_json = players_json + ','.join(players)
        players_json = players_json + "]"
        data = Data(PLAYERS_CONNECTED, json.loads(players_json))
        return data
