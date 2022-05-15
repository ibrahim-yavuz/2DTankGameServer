import json

class Server:
    def __init__(self, address):
        self.host = address[0]
        self.port = address[1]
        self.address = (self.host, self.port)

    def toJson(self):
        server_to_json = {'host': self.host, 'port': self.port}
        return json.dumps(server_to_json)

    def fromJson(serverJson):
        server = Server()
        serverJson = json.loads(serverJson)
        server.username = serverJson['username']
        server.host = serverJson['host']
        server.port = serverJson['port']
        return server