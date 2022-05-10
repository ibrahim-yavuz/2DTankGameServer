import config
from socket_operations import *

get_connected_clients()

while True:
    try:
        player_info = get_player_info()
        send_player_info(player_info)
    except:
        print("An error has occured")