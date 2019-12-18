"""
The backend things that are ultimately used by the frontend to render the game
"""

from . import constants
from .tile_lookups import get_map_str

# for styling function
from . import game_vars
from .components.player import Player
from .components.cursor_component import CursorComponent

def map_to_draw(inc_map, fov, explored):
    #mapa = map_common.get_map_glyphs(inc_map)

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
        # camera
        cam = game_vars.camera
        width_start = cam.get_width_start()
        width_end = cam.get_width_end(game_vars.mapa)
        height_start = cam.get_height_start()
        height_end = cam.get_height_end(game_vars.mapa)
        # draw in screen/tile coords
        if x == cursor.x-width_start and y == cursor.y-height_start:
            return "cursor"

    if game_vars.explored[x][y] == 1 and game_vars.fov[x][y] == 0:
        return "explored"
    else:
        return "normal"