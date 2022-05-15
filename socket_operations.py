import json
import socket
import constants
from data import Data
from player import Player

buffer_size = constants.BUFFER_SIZE
host_ip = constants.HOST_IP

class SocketOperations:
    players = []
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self, port):
        self.UDPServerSocket.bind((host_ip, port))

    def get_socket(self):
        return self.UDPServerSocket

    def get_host(self) -> str:
        return self.UDPServerSocket.getsockname()[0]


    def get_port_number(self) -> int:
        return self.UDPServerSocket.getsockname()[1]


    def send_data(self, data):
        data = str.encode(data)
        for player in self.players:
            print(player.address)
            self.UDPServerSocket.sendto(data, player.address)


    def get_data(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        print(message)

        data = Data.fromJson(message)

        if(data.dataType == "PlayerConnected"):
            player_data = Player(data.incomingData['username'], address)
            
            if(player_data not in self.players):
                print(player_data.toJson())
                self.players.append(player_data)
                return Data(data.dataType, player_data.toJson())

        return message  


    def start_the_game(self):
        while True:
            data = self.get_data()
            self.send_data(data)

    
    def close_socket(self):
        self.UDPServerSocket.close()

