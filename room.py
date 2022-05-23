import json
from data import Data
import constants

class Room:
    def __init__(self, room_id, name, creator, players):
        self.room_id = room_id
        self.creator = creator
        self.name = name
        self.players = players
    
    def toJson(self):
        room_to_json = {'room_id': self.room_id, 'name': self.name, 'creator': self.creator, 'players': self.players}
        return json.dumps(room_to_json)

    def toDict(self):
        room_to_dict = {'room_id': self.room_id, 'name': self.name, 'creator': self.creator, 'players': self.players}
        return room_to_dict

    def fromJson(roomJson):
        roomJson = json.loads(roomJson)
        room_id = roomJson['room_id']
        name = roomJson['name']
        creator = roomJson['creator']
        players = roomJson['players']
        room = Room(room_id, name, creator, players)
        return room

    def getAllRooms(rooms):
        rooms_json = [obj.toDict() for obj in rooms]
        data = Data(constants.ACTIVE_ROOMS, rooms_json, "")
        return data
    