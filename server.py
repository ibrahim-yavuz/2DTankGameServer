import socket
import json

localIP = '192.168.1.111'
localPort = 65413
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

client_addresses = []

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
        playerInfo.name = playerInfoJson['name']
        playerInfo.pos_x = playerInfoJson['pos_x']
        playerInfo.pos_y = playerInfoJson['pos_y']
        playerInfo.rot_z = playerInfoJson['rot_z']
        return playerInfo


def get_connected_clients():
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('utf-8')
    address = bytesAddressPair[1]

    if address not in client_addresses and message == "connected":
        client_addresses.append(address)

    return message

def send_player_info(playerInfo):
    bytesToSend = str.encode(playerInfo.toJson())
    for address in client_addresses:
        UDPServerSocket.sendto(bytesToSend, address)


def get_player_info() -> PlayerInfo:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode('utf-8')
    playerInfo = PlayerInfo.fromJson(message)
    return playerInfo


"""
command = ""

while command != 'start':
    command = get_connected_clients()

while True:
    player_info = get_player_info()
    print(data)
    send_player_info(data)"""