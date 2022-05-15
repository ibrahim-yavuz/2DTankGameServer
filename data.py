import json

class Data:
    def __init__(self, dataType, incomingData):
        self.dataType = dataType
        self.incomingData = incomingData

    def toJson(self):
        data_to_json = {'dataType': self.dataType, 'incomingData': self.incomingData}
        return json.dumps(data_to_json)

    def fromJson(dataJson):
        data = Data(dataJson['dataType'], dataJson['incomingData'])
        return data