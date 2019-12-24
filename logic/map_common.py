import sys
import random

from . import constants
from .tile_lookups import TileTypes, get_index, get_map_str, get_block_path
from .enum_constants import Constants

Directions = Constants(
    NORTH = (0, -1),
    SOUTH = (0, 1),
    EAST = (1, 0),
    WEST = (-1, 0),
    NORTHEAST = (1, -1),
    NORTHWEST = (-1, -1),
    SOUTHEAST = (1, 1),
    SOUTHWEST = (-1, 1),
    CENTER = (0,0),
)

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x+w
        self.y2 = y+h

    def center(self):
        centerX = (self.x1 + self.x2)//2 #integer division
        centerY = (self.y1 + self.y2)//2
        return (centerX, centerY)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
            self.y1 <= other.y2 and self.y2 >= other.y1)

    # readable representation
    def __str__(self):
        return 'Rect(x='+str(self.x1)+', y='+str(self.y1)+ ' , w=' + str(self.x2-self.x1) + ' , h=' + str(self.y2-self.y1) + ')'

def get_free_tiles(inc_map):
    free_tiles = []
    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            if not get_block_path(inc_map[x][y]):
                free_tiles.append((x,y))
    return free_tiles

def random_free_tile(inc_map):
    free_tiles = get_free_tiles(inc_map)

    index = random.randint(0, len(free_tiles)-1)

    #print("Index is " + str(index))

    x = free_tiles[index][0]
    y = free_tiles[index][1]

    print("Coordinates are " + str(x) + " " + str(y))

    return x, y


def tiles_distance_to(start, target):
    x_diff = start[0] - target[0]
    y_diff = start[1] - target[1]

    ##ensure always positive values
    if x_diff < 0:
        x_diff = x_diff * -1

    if y_diff < 0:
        y_diff = y_diff * -1

    return max(x_diff, y_diff)

# based on RLTK-rs tutorial
def drawn_wall_glyph(inc_map, x,y):
    # don't check if we would go past map borders
    if x < 1 or y < 1 or x > len(inc_map)-1 or y > len(inc_map[0])-1:
        return "#" #get_index(TileTypes.WALL) # '#'

    # bitmask
    mask = 0
    if is_wall(inc_map, x, y-1):
        mask += 1
    if is_wall(inc_map, x, y + 1):
        mask += 2
    if is_wall(inc_map, x-1, y):
        mask += 4
    if is_wall(inc_map, x+1, y):
        mask += 8

    # assign tiles
    if mask == 0:
        return "○" #get_index(TileTypes.WALL_PILLAR) # pillar
    elif mask == 1:
        return "║" #get_index(TileTypes.WALL_V) # wall only to the north
    elif mask == 2:
        return "║" #get_index(TileTypes.WALL_V) # wall only to the south
    elif mask == 3:
        return "║" #get_index(TileTypes.WALL_V) # wall only to the north and south
    elif mask == 4:
        return "═" #get_index(TileTypes.WALL_H) # wall only to the west
    elif mask == 5:
        return "╝" #get_index(TileTypes.WALL_SE_C) # wall to north and west
    elif mask == 6:
        return "╗" #get_index(TileTypes.WALL_NE_C) # wall to south and west
    elif mask == 7:
        return "╣" #get_index(TileTypes.WALL_TE) # wall to the north, south and west
    elif mask == 8:
        return "═" #get_index(TileTypes.WALL_H) # wall only to the east
    elif mask == 9:
        return "╚" #get_index(TileTypes.WALL_SW_C) # wall to the north and east
    elif mask == 10:
        return "╔" #get_index(TileTypes.WALL_NW_C) # wall to the south and east
    elif mask == 11:
        return "╠" #get_index(TileTypes.WALL_TW) # wall to the south, north and east
    elif mask == 12:
        return "═" #get_index(TileTypes.WALL_H) # wall to the east and west
    elif mask == 13:
        return "╩" #get_index(TileTypes.WALL_TS) # wall to the east, west and south
    elif mask == 14:
        return "╦" #get_index(TileTypes.WALL_TN) # wall to the east, west and north
    else:
        return "#" #get_index(TileTypes.WALL) # "#"


def is_wall(inc_map, x,y):
    return inc_map[x][y] == get_index(TileTypes.WALL)

# this is for debugging
def print_map_string(inc_map):
    # write columns
    for x in range(len(inc_map)):
        sys.stdout.write(str(x%10)) #just the units digit to save space

    # line break
    sys.stdout.write("\n")

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            #sys.stdout.write(tile_types[inc_map[x][y]].map_str)
            sys.stdout.write(get_map_str(inc_map[x][y]))
        
        #our row ended, print line number and add a line break
        sys.stdout.write(str(y) + "\n")

# this is for map overview
def get_map_string(inc_map):
    list_str = []

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            #list.append(tile_types[inc_map[x][y]].map_str)
            list_str.append(get_map_str(inc_map[x][y]))

        # our row ended, add a line break
        list_str.append("\n")

    string = ''.join(list_str)

    #print string
    return string

# this is for map display
# just store map glyphs
def get_map_glyphs(inc_map):
    mapa = []

    # dummy
    mapa = [[get_map_str(get_index(TileTypes.FLOOR)) for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            mapa[x][y] = get_map_str(inc_map[x][y])

    return mapa


def get_map_HTML(inc_map):
    list_str = []

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            #list.append(tile_types[inc_map[x][y]].map_str)
            list_str.append(get_map_str(inc_map[x][y]))

        # our row ended, add a line break
        list_str.append("<br />")

    string = ''.join(list_str)

    #print(string)
    return string