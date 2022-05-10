import json
import socket
import config
from player import Player
from player_info import PlayerInfo

buffer_size = config.host['buffer_size']
host_ip = config.host['ip']
port = config.host['port']

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((host_ip, port))

players = []

def send_command(command):
    bytesToSend = str.encode(command)
    for player in players:
        UDPServerSocket.sendto(bytesToSend, player.address)
        
def get_connected_clients() -> str:
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        if message != config.commands['start']:
            player = Player(message, address)
            if player not in players:
                players.append(player)
            print(send_player_data())
        else:
            send_command(command=message)
            break


def send_player_data():
    new_json = "["
    for player in players:
        if player == players[len(players) - 1]:
            new_json = new_json + player.toJson()
        else:
            new_json = new_json + player.toJson() + ","
    new_json = json.loads(new_json + "]")
    send_command(json.dumps(new_json))
    return new_json

def send_player_info(playerInfo):
    bytesToSend = str.encode(playerInfo.toJson())
    for player in players:
        UDPServerSocket.sendto(bytesToSend, player.address)


def get_player_info() -> PlayerInfo:
    bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
    message = bytesAddressPair[0].decode('utf-8')
    playerInfo = PlayerInfo.fromJson(message)
    return playerInfo
