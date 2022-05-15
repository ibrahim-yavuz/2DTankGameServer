import json
import socket
import constants
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
            self.UDPServerSocket.sendto(data, player.address)


    def get_data(self):
        bytesAddressPair = self.UDPServerSocket.recvfrom(buffer_size)
        message = bytesAddressPair[0].decode('utf-8')

        print("{} from {}".format(message, bytesAddressPair[1]))

        return message

    def send_player_data(self):
        new_json = "["
        for player in self.players:
            if player == self.players[len(self.players) - 1]:
                new_json = new_json + player.toJson()
            else:
                new_json = new_json + player.toJson() + ","
        new_json = json.loads(new_json + "]")
        self.send_data(json.dumps(new_json))
        return new_json    


    def start_the_game(self):
        while True:
            data = self.get_data()
            self.send_data(data)
            
    
    def close_socket(self):
        self.UDPServerSocket.close()

