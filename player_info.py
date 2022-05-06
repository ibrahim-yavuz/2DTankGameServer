import json

class PlayerInfo:
    def init(self, name, pos_x, pos_y, rot_z):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rot_z = rot_z

    def toJson(self):
        player_to_json = {'name': self.name, 'pos_x': self.pos_x, 'pos_y': self.pos_y, 'rot_z': self.rot_z}
        return json.dumps(player_to_json)

    def fromJson(playerInfoJson):
        playerInfo = PlayerInfo()
        playerInfoJson = json.loads(playerInfoJson)
        playerInfo.name = playerInfoJson['name']
        playerInfo.pos_x = playerInfoJson['pos_x']
        playerInfo.pos_y = playerInfoJson['pos_y']
        playerInfo.rot_z = playerInfoJson['rot_z']
        return playerInfo