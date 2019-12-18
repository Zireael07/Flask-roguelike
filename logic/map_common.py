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
    #mapa = get_map_glyphs(inc_map)

    # dummy
    mapa = [[("&nbsp;", (255, 255, 255)) for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]

    # camera
    cam = game_vars.camera
    width_start = cam.get_width_start()
    width_end = cam.get_width_end(game_vars.mapa)
    height_start = cam.get_height_start()
    height_end = cam.get_height_end(game_vars.mapa)

    # based on https://bfnightly.bracketproductions.com/rustbook/chapter_41.html
    # x,y are screen coordinates, tx, ty are map (tile) coordinates
    y = 0
    for ty in range(height_start, height_end+1):
    #for ty in range(len(inc_map[0])):
        x = 0
        #for tx in range(len(inc_map)):
        for tx in range(width_start, width_end+1):
            # if on map
            if tx >= 0 and tx < len(inc_map) and ty >= 0 and ty < len(inc_map[0]):
            #if tx >= width_start and tx <= width_end and ty >= height_start and ty <= height_end:
                # visible or explored
                if fov[tx][ty] == 1 or explored[tx][ty]: 
                    mapa[x][y] = (get_map_str(inc_map[tx][ty]), (255,255,255))
                else:
                    mapa[x][y] = ("&nbsp;", (255, 255, 255))
                    # blank span later escaped by |safe Jinja template markup
            else:
                mapa[x][y] = ("&nbsp;", (255, 255, 255))
                # blank span later escaped by |safe Jinja template markup
            
            x += 1
        y += 1

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