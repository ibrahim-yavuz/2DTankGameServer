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
    UDPServerSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __init__(self, port):
        self.UDPServerSocket.bind((host_ip, port))

    # Socket Information
    def get_socket(self):
        return self.UDPServerSocket


    def get_host(self):
        return self.UDPServerSocket.getsockname()[0]


    def get_port_number(self):
        return self.UDPServerSocket.getsockname()[1]


    # Server-Client Communication
    def send_data(self, data):
        data = str.encode(data)
        for player in self.players:
            self.UDPServerSocket.sendto(data, player.address)


    def send_data_to_single_room(self, data, room):
        data = str.encode(data)
        for player in room.players:
            self.UDPServerSocket.sendto(data, player['address'])


    def send_data_to_single_address(self, data, address):
        data = str.encode(data)
        self.UDPServerSocket.sendto(data, address)


    def find_room_by_id(self, id):
        for room in self.rooms:
            if id == room.room_id:
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
        data = Data(constants.ACTIVE_ROOMS, self.rooms, "")
        self.send_data(data.toJson())


    def join_room(self, player, room):
        if player not in room.players:
            room.players.append(player)


    def disconnect_from_room(self, player, room):
        room.players.remove(player)


    def create_player(self, user, address, room):
        id = "Player{}".format(self.playerCounter)
        player = Player(id, user, address)
        self.players.append(player)
        if room:
            room.players.append(player)
        return player

    def create_player_without_room(self, user, address):
        id = "Player{}".format(self.playerCounter)
        player = Player(id, user, address)
        print(player.toJson())
        if player not in self.players:
            self.players.append(player)
        return player


    def send_players_of_the_room(self, room):
        if room:
            data = Data(constants.PLAYERS_CONNECTED, room.players, room.room_id)
            self.send_data_to_single_room(data.toJson(), room)


    def get_address_from_client(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        address = bytesAddressPair[1]
        return address


    def get_data(self):
        while True:
            bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
            message = bytesAddressPair[0].decode('utf-8')
            address = bytesAddressPair[1]
            data = Data.fromJson(message)
            current_room = self.find_room_by_id(data.room_id)

            if(data.type == constants.PLAYERS_CONNECTED):
                self.players_connected(data, address, current_room)

            elif(data.type == constants.DISCONNECTED):
                self.players_disconnected(address, current_room)
                
            elif(data.data == constants.CREATE_ROOM):
                self.send_id_to_room(address)

            elif(data.type == constants.CREATE_ROOM):
                self.create_room_command(data, address)

            if current_room:
                self.send_data_to_single_room(message, current_room)


    def create_room_command(self, data, address):
        room_data = data.data
        room = Room(room_data['room_id'], room_data['name'], room_data['creator'], room_data['players'])
        self.create_room(room.room_id, room.name, room.creator)
        self.send_data_to_single_address(Room.getAllRooms(self.rooms).toJson(), address)
        self.roomCounter = self.roomCounter + 1
        self.playerCounter = self.playerCounter + 1


    def send_id_to_room(self, address):
        id = "Room{}".format(self.roomCounter)
        self.send_data_to_single_address(
                    json.dumps({'id': id}), address)

    
    def players_connected(self, data, address, current_room):
        if current_room:
            self.create_player(data.data['user'], address, current_room)
            self.send_players_of_the_room(current_room)
        else:
            self.create_player_without_room(data.data['user'], address)
            self.send_data(Player.getAllPlayers(self.players))


    def players_disconnected(self, address, current_room):
        player = self.find_player_with_address(address)
        if player != False:
            self.disconnect_from_room(player, current_room)
            self.send_players_of_the_room(current_room)


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
