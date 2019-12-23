from .. import constants
from ..tile_lookups import TileTypes, get_index

from .. import bsp



def room_func(room, mapa):
    # set all tiles within a rectangle to wall
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1+1, room.y2):
            # paranoia
            if y < len(mapa[0]) and x < len(mapa):
                mapa[x][y] = get_index(TileTypes.WALL)

    # Build Interior
    for x in range(room.x1+2,room.x2-1):
        for y in range(room.y1+2,room.y2-1):
            # paranoia
            if y < len(mapa[0]) and x < len(mapa):
                mapa[x][y] = get_index(TileTypes.FLOOR)

# kwargs are there for chaining to work (see game.py 75 and 125)
def map_create(level, **kwargs):

    start_x = 0
    start_y = 0
    end_y = constants.MAP_HEIGHT
    end_x = constants.MAP_WIDTH

    width = end_x - start_x
    height = end_y - start_y

    # if level has submap, we only act within submap borders
    if len(level.submaps) > 0:
        start_x = level.submaps[0].x1
        end_x = level.submaps[0].x2+1
        start_y = level.submaps[0].y1
        end_y = level.submaps[0].y2+1

    #level.mapa = [[ get_index(TileTypes.FLOOR) for _ in range(start_y, end_y)] for _ in range(start_x, end_x)]
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            level.mapa[x][y] = get_index(TileTypes.FLOOR)

    # BSP
    bsp_t = bsp.BSPTree(width/2)
    bsp_t.generateLevel(width, height, room_func, level.mapa)


    return level # for chaining


