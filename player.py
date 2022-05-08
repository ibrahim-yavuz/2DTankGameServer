import json

class Player:
    def __init__(self, username, host, port):
        self.username = username
        self.host = host
        self.port = port
        self.address = (host, port)

    def toJson(self):
        player_to_json = {'username': self.username, 'host': self.host, 'port': self.port}
        return json.dumps(player_to_json)

    def fromJson(playerJson):
        player = Player()
        playerJson = json.loads(playerJson)
        player.username = playerJson['username']
        player.host = playerJson['host']
        player.port = playerJson['port']
        return player