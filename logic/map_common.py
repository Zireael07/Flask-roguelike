import sys

from . import constants
from .tile_lookups import TileTypes, get_index, get_map_str

# for styling function
from . import game_vars
from .player import Player
from .cursor_component import CursorComponent

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


def map_to_draw(inc_map, fov, explored):
    mapa = get_map_glyphs(inc_map)

    # dummy
    mapa = [[get_map_str(get_index(TileTypes.FLOOR)) for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]

    for y in range(len(inc_map[0])):
        for x in range(len(inc_map)):
            # visible or explored
            if fov[x][y] == 1 or explored[x][y]: 
                mapa[x][y] = get_map_str(inc_map[x][y])
            else:
                mapa[x][y] = "&nbsp;"
                # blank span later escaped by |safe Jinja template markup

    return mapa

"""
Returns CSS classes
Kudos to https://teamtreehouse.com/community/how-do-you-add-classes-and-ids-to-template-blocks-in-flask for figuring that out
"""
def map_style(x, y):
    cursor = None
    for ent, (player, cur) in game_vars.world.get_components(Player, CursorComponent):
        cursor = cur
    
    if cursor is not None:
        if x == cursor.x and y == cursor.y:
            return "cursor"

    if game_vars.explored[x][y] == 1 and game_vars.fov[x][y] == 0:
        return "explored"
    else:
        return "normal"

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