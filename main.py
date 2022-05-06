from player_info import PlayerInfo
import socket
import config

buffer_size = config.host['buffer_size']

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((config.host['ip'], config.host['port']))

client_addresses = []

def get_connected_clients() -> str:
    bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
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
    bytesAddressPair = UDPServerSocket.recvfrom(buffer_size)
    message = bytesAddressPair[0].decode('utf-8')
    playerInfo = PlayerInfo.fromJson(message)
    return playerInfo


command = ""

while command != 'start':
    command = get_connected_clients()

print("CREATED SERVER")

while True:
    try:
        player_info = get_player_info()
        send_player_info(player_info)
    except:
        print("An error occured!")