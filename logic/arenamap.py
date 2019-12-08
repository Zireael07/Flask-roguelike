import sys

from . import constants
from .tile_lookups import TileTypes, get_index, get_map_str

def map_create(pillars):
    #new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]
    new_map = [[ get_index(TileTypes.FLOOR) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]

    for coords in pillars:
        new_map[coords[0]][coords[1]] = get_index(TileTypes.WALL) #.block_path = True
        #new_map[12][12] = 0 #.block_path = True

    # walls around the map
    for x in range(constants.MAP_WIDTH):
        new_map[x][0] = get_index(TileTypes.WALL) #.block_path = True
        new_map[x][constants.MAP_WIDTH-1] = get_index(TileTypes.WALL) #.block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y] = get_index(TileTypes.WALL) #.block_path = True
        new_map[constants.MAP_HEIGHT-1][y] = get_index(TileTypes.WALL) #.block_path = True

    return new_map

if __name__ == '__main__':

    #test map generation
    test_attempts = 3
    for i in range(test_attempts):
        current_map = map_create([(10,10), (15,15)])

        print_map_string(current_map)


# helpers
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


def map_to_draw(inc_map, fov):
    mapa = get_map_glyphs(inc_map)

    # dummy
    mapa = [[get_map_str(get_index(TileTypes.FLOOR)) for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            if fov[x][y] == 1: # visible
                mapa[x][y] = get_map_str(inc_map[x][y])
            else:
                mapa[x][y] = "&nbsp;"
                # blank span later escaped by |safe Jinja template markup

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