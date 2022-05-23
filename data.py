import json

class Data:
    def __init__(self, type, data, room_id):
        self.type = type
        self.data = data
        self.room_id = room_id

    def toJson(self):
        data_to_json = {'type': self.type, 'data': self.data, 'room_id': self.room_id}
        return json.dumps(data_to_json)

    def fromJson(dataJson):
        dataJson = json.loads(dataJson)
        data = Data(dataJson['type'], dataJson['data'], dataJson['room_id'])
        return data