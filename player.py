import json

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
        player = Player()
        playerJson = json.loads(playerJson)
        player.username = playerJson['username']
        player.host = playerJson['host']
        player.port = playerJson['port']
        return player