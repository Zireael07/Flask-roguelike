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