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
    rooms = []
    roomCounter = 0
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


    def send_data_to_single_address(self, data, address):
        data = str.encode(data)
        self.UDPServerSocket.sendto(data, address)


    def find_room_by_id(self, id):
        for room in self.rooms:
            if id == room.id:
                return room
        return None

    
    def get_players_from_room(self, room):
        return room.players


    def create_room(self, room_id, name, creator):
        players = [creator]
        room = Room(room_id, name, creator, players)
        self.roomCounter = self.roomCounter + 1
        self.rooms.append(room)


    def get_rooms(self):
        return self.rooms


    def send_rooms(self):
        data = Data(constants.ACTIVE_ROOMS, self.rooms)
        self.send_data(data.toJson())


    def join_room(self, player, room):
        room.players.append(player)

    
    def disconnect_from_room(self, player, room):
        room.players.remove(player)
    

    def create_player(self, user, id, ip, port):
        player = Player(id, user, (ip, port))
        self.players.add(player)

    
    def send_players_of_the_room(self, room):
        data = Data(constants.PLAYERS_CONNECTED, room.players)
        self.send_data(data.toJson())

    
    def get_data_from_client(self) -> dict:
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')
        address = bytesAddressPair[1]
        return (message, address)


    def get_data(self):
        while True:
            data = Data.fromJson(self.get_data_from_client().message)

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

            elif(data.data == constants.CREATE_ROOM):
                id = "Room{}".format(self.roomCounter)
                print(json.dumps({'id': id}))
                self.send_data_to_single_address(json.dumps({'id': id}), address)

            elif(data.type == constants.CREATE_ROOM):
                room_data = data.data
                room = Room(room_data['room_id'], room_data['name'], room_data['creator'], room_data['players'])
                self.rooms.append(room.toJson())
                print(Room.getAllRooms(self.rooms).toJson())
                self.send_data_to_single_address(Room.getAllRooms(self.rooms).toJson(), address)
                self.roomCounter = self.roomCounter + 1
                self.playerCounter = self.playerCounter + 1
                print(self.get_players_from_room(room))


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

