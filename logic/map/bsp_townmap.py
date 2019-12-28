import random

from .. import constants
from ..map_common import print_map_string
from ..tile_lookups import TileTypes, get_index

from .. import bsp



def room_func(room, mapa):
    # set all tiles within a rectangle to wall
    for x in range(room.x1, room.x2):
        for y in range(room.y1, room.y2):
            # paranoia
            if y < len(mapa[0]) and x < len(mapa):
                mapa[x][y] = get_index(TileTypes.WALL)

    # Build Interior
    for x in range(room.x1+1,room.x2-1):
        for y in range(room.y1+1,room.y2-1):
            # paranoia
            if y < len(mapa[0]) and x < len(mapa):
                mapa[x][y] = get_index(TileTypes.FLOOR_INDOOR)

# kwargs are there for chaining to work (see game.py 75 and 125)
def map_create(level, **kwargs):

    start_x = 0
    start_y = 0
    end_y = constants.MAP_HEIGHT
    end_x = constants.MAP_WIDTH

    # if level has submap, we only act within submap borders
    if len(level.submaps) > 0:
        start_x = level.submaps[0].x1
        end_x = level.submaps[0].x2+1
        start_y = level.submaps[0].y1
        end_y = level.submaps[0].y2+1


    width = end_x - start_x
    height = end_y - start_y
    print("Map width: " + str(width) + " map height" + str(height))

    #level.mapa = [[ get_index(TileTypes.FLOOR) for _ in range(start_y, end_y)] for _ in range(start_x, end_x)]
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            level.mapa[x][y] = get_index(TileTypes.FLOOR)

    # BSP
    bsp_leaf = int(width/2) if width > 8 else width
    bsp_t = bsp.BSPTree(bsp_leaf)
    bsp_t.generateLevel(start_x, start_y, width, height, room_func, level.mapa)

    create_doors(bsp_t, level.mapa)

    # debug
    print_map_string(level.mapa)

    return level # for chaining


def create_doors(bsp, mapa):
    for room in bsp.rooms:
        (x, y) = room.center()
        #print("Creating door for " + str(x) + " " + str(y))

        choices = ["north", "south", "east", "west"]

        # copy the list so that we don't modify it while iterating (caused some directions to be missed)
        sel_choices = list(choices)

        # check if the door leads anywhere
        for choice in choices:
            #print(str(choice)+"...")
            if choice == "north":
                checkX = x
                checkY = room.y1-1

            if choice == "south":
                checkX = x
                checkY = room.y2

            if choice == "east":
                checkX = room.x2
                checkY = y

            if choice == "west":
                checkX = room.x1-1
                checkY = y

            
            #print("Checking dir " + str(choice) + ": x:" + str(checkX) + " y:" + str(checkY) + " " + str(self._map[checkX][checkY]))
            
            # if going out of map, not an option
            if checkX > len(mapa)-1 or checkY > len(mapa[0])-1:
                sel_choices.remove(choice)
            else:
                # if it leads to a wall, remove it from list of choices
                if mapa[checkX][checkY] in [get_index(TileTypes.WALL), get_index(TileTypes.TREE)]: #0:
                    #print("Removing direction from list" + str(choice))
                    sel_choices.remove(choice)

        #print("Choices: " + str(sel_choices))
        if len(sel_choices) > 0:
            wall = random.choice(sel_choices)

            #print(str(wall))
            if wall == "north":
                wallX = x
                wallY = room.y1

            elif wall == "south":
                wallX = x
                wallY = room.y2 - 1

            elif wall == "east":
                wallX = room.x2 - 1
                wallY = y

            elif wall == "west":
                wallX = room.x1
                wallY = y

            mapa[wallX][wallY] = get_index(TileTypes.FLOOR)