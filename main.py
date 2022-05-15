from socket_operations import *

main_server_socket = SocketOperations(5555)
print("Started the server at - {}:{}".format(main_server_socket.get_host(), main_server_socket.get_port_number()))
main_server_socket.start_the_game()