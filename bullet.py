import json

class Bullet:
    def init(self, username, pos_x, pos_y):
        self.username = username
        self.pos_x = pos_x
        self.pos_y = pos_y

    def toJson(self):
        bullet_to_json = {'username': self.username, 'pos_x': self.pos_x, 'pos_y': self.pos_y}
        return json.dumps(bullet_to_json)

    def fromJson(bulletInfoJson):
        bulletInfo = Bullet()
        bulletInfoJson = json.loads(bulletInfoJson)
        bulletInfo.username = bulletInfoJson['username']
        bulletInfo.pos_x = bulletInfoJson['pos_x']
        bulletInfo.pos_y = bulletInfoJson['pos_y']
        return bulletInfo