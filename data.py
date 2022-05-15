import json

class Data:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def toJson(self):
        data_to_json = {'type': self.type, 'data': self.data}
        return json.dumps(data_to_json)

    def fromJson(dataJson):
        dataJson = json.loads(dataJson)
        data = Data(dataJson['type'], dataJson['data'])
        return data