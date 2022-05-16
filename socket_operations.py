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

    def get_host(self):
        return self.UDPServerSocket.getsockname()[0]


    def get_port_number(self):
        return self.UDPServerSocket.getsockname()[1]


    def send_data(self, data):
        data = str.encode(data)
        for player in self.players:
            self.UDPServerSocket.sendto(data, Player.fromJson(player).address)


    def get_data(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]

        data = Data.fromJson(message)

        if(data.type == constants.PLAYERS_CONNECTED):
            player_data = Player(data.data['user'], address)
            
            if(player_data.toJson() not in self.players):
                self.players.append(player_data.toJson())
            return Player.getAllPlayers(self.players).toJson()
        elif(data.type == constants.DISCONNECTED):
            if self.find_player_with_address(address) != False:
                print("Player {} disconnected from the server".format(self.find_player_with_address(address)))
                self.players.remove(self.find_player_with_address(address))
                print("Current Players: {}".format(Player.getAllPlayers(self.players).toJson()))
                return Player.getAllPlayers(self.players).toJson()            
        
        return message
          

    def start_the_game(self):
        while True:
            data = self.get_data()
            print(data)
            self.send_data(data)

    
    def find_player_with_address(self, player_address):
        for player in self.players:
            player_data = Player.fromJson(player)
            print("{} - player data: {}".format(player_address, player_data.address))
            if player_data.address == player_address:
                return player_data.toJson()
        return False

    
    def close_socket(self):
        self.UDPServerSocket.close()

