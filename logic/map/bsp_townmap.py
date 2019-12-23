from .. import constants
from ..tile_lookups import TileTypes, get_index

from .. import bsp



def room_func(room, mapa):
    # set all tiles within a rectangle to wall
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1+1, room.y2):
            mapa[x][y] = get_index(TileTypes.WALL)

    # Build Interior
    for x in range(room.x1+2,room.x2-1):
        for y in range(room.y1+2,room.y2-1):
            mapa[x][y] = get_index(TileTypes.FLOOR)

def map_create():
    new_map = [[ get_index(TileTypes.FLOOR) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

    # BSP
    bsp_t = bsp.BSPTree(constants.MAP_WIDTH/2)
    bsp_t.generateLevel(constants.MAP_WIDTH, constants.MAP_HEIGHT, room_func, new_map)


    return new_map


