import json
import socket
import constants
from data import Data
from player import Player
from _thread import *

from room import Room

buffer_size = constants.BUFFER_SIZE
host_ip = constants.HOST_IP

class SocketOperations:
    playerCounter = 0
    players = []
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self, port):
        self.UDPServerSocket.bind((host_ip, port))

    #Socket Information
    def get_socket(self):
        return self.UDPServerSocket

    def get_host(self):
        return self.UDPServerSocket.getsockname()[0]


    def get_port_number(self):
        return self.UDPServerSocket.getsockname()[1]

    
    #Server-Client Communication
    def send_data(self, data):
        data = str.encode(data)
        for player in self.players:
            self.UDPServerSocket.sendto(data, Player.fromJson(player).address)


    def get_data(self):
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
            message = bytesAddressPair[0].decode('utf-8')
            address = bytesAddressPair[1]

            data = Data.fromJson(message)

            if(data.type == constants.PLAYERS_CONNECTED):
                player_data = Player("Player{}".format(self.playerCounter), data.data['user'], address)

                if(player_data.toJson() not in self.players):
                    self.players.append(player_data.toJson())
                    self.playerCounter = self.playerCounter + 1
                self.send_data(Player.getAllPlayers(self.players).toJson())

            elif(data.type == constants.DISCONNECTED):
                if self.find_player_with_address(address) != False:
                    print("Player {} disconnected from the server".format(self.find_player_with_address(address)))
                    self.players.remove(self.find_player_with_address(address))
                    print("Current Players: {}".format(Player.getAllPlayers(self.players).toJson()))
                    self.send_data(Player.getAllPlayers(self.players).toJson())

            self.send_data(message)
          

    def start_the_game(self):
        self.get_data()

    
    def find_player_with_address(self, player_address):
        for player in self.players:
            player_data = Player.fromJson(player)
            if player_data.address == player_address:
                return player_data.toJson()
        return False

    
    def close_socket(self):
        self.UDPServerSocket.close()

