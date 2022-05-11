import json
import socket
import constants
from player import Player
from player_info import PlayerInfo

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


    def send_command(self, command):
        bytesToSend = str.encode(command)
        for player in self.players:
            self.UDPServerSocket.sendto(bytesToSend, player.address)
        
    def get_connected_clients(self) -> str:
        while True:
            bytesAddressPair = SocketOperations.UDPServerSocket.recvfrom(buffer_size)
            message = bytesAddressPair[0].decode('utf-8')
            address = bytesAddressPair[1]

            if message != constants.START:
                player = Player(message, address)
                if player not in self.players:
                    self.players.append(player)
                self.send_player_data()
            else:
                self.send_command(command=message)
                break
        return self.players


    def send_player_data(self):
        new_json = "["
        for player in self.players:
            if player == self.players[len(self.players) - 1]:
                new_json = new_json + player.toJson()
            else:
                new_json = new_json + player.toJson() + ","
        new_json = json.loads(new_json + "]")
        self.send_command(json.dumps(new_json))
        return new_json

    def send_player_info(self, playerInfo):
        bytesToSend = str.encode(playerInfo.toJson())
        for player in self.players:
            self.UDPServerSocket.sendto(bytesToSend, player.address)


    def get_player_info(self) -> PlayerInfo:
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')
        playerInfo = PlayerInfo.fromJson(message)
        return playerInfo

    def start_the_game(self):
        while True:
            try:
                player_info = self.get_player_info()
                self.send_player_info(player_info)
            except:
                print("An error has occured")
                self.UDPServerSocket.close()
                break
    
    def close_socket(self):
        self.UDPServerSocket.close()

