import json
from player import Player
from player_info import PlayerInfo
import socket
import config

buffer_size = config.host['buffer_size']
host_ip = config.host['ip']
port = config.host['port']

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((host_ip, port))

players = []

def get_connected_clients() -> str:
    bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
    message = bytesAddressPair[0].decode('utf-8')
    address = bytesAddressPair[1]


    if message != config.commands['start']:
        player = Player(message, address[0], address[1])
        if player not in players:
            players.append(player)
        print(send_player_data())

    return message


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


def send_command(command):
    bytesToSend = str.encode(command)
    for player in players:
        UDPServerSocket.sendto(bytesToSend, player.address)


while True:
    command = get_connected_clients()
    if command == config.commands['start']:
        send_command(command=command)
        break

while True:
    try:
        player_info = get_player_info()
        send_player_info(player_info)
    except:
        print("An error has occured")