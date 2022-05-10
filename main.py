from http import server
import config
from socket_operations import *

server_socket = SocketOperations(config.host['port'])
print(server_socket.get_connected_clients())
server_socket.start_the_game()