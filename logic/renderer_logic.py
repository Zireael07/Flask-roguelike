"""
The backend things that are ultimately used by the frontend to render the game
"""

from . import constants
from .tile_lookups import TileTypes, get_map_str, get_index, get_color
from .map_common import drawn_wall_glyph

# for styling function
from . import game_vars
from .components.player import Player
from .components.cursor_component import CursorComponent

from logic import game
from logic.components.position import Position
from logic.components.renderable import RenderableComponent
from logic.components.in_backpack import InBackpackComponent
from logic.components.equipped import EquippedComponent
from logic.components.name_component import NameComponent
from logic.components.dead_component import DeadComponent
from logic.components.skip_component import SkipComponent
from logic.components.faction_component import FactionComponent

def redraw_console(position):
    # cam
    game_vars.camera.update(position)

    console = map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)

    player_ent = None
    for ent, (player) in game_vars.world.get_component(Player):
        player_ent = ent

    # camera
    cam = game_vars.camera
    width_start = cam.get_width_start()
    width_end = cam.get_width_end(game_vars.mapa)
    height_start = cam.get_height_start()
    height_end = cam.get_height_end(game_vars.mapa)

    # draw other entities
    matches = game_vars.world.get_components(Position, RenderableComponent)
    # sort by render order
    matches.sort(key=lambda item: item[1][1].render_order.value)

    for ent, (pos, visual) in matches:
        # if not in camera view
        if pos.x < width_start or pos.x > width_end or pos.y < height_start or pos.y > height_end:
            # skip
            continue
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        if game_vars.world.has_component(ent, DeadComponent):
            # skip
            continue
        if game_vars.world.has_component(ent, InBackpackComponent):
            # skip
            continue
        if game_vars.world.has_component(ent, EquippedComponent):
            # skip
            continue

        ret = None
        # check faction
        if game_vars.world.has_component(ent, FactionComponent):
            player_f = game_vars.world.component_for_entity(player_ent, FactionComponent).faction
            fact = game_vars.world.component_for_entity(ent, FactionComponent)
            react = game.get_faction_reaction(player_f, fact.faction)
            #print("react: " + str(react))
        
            if react < -50:
                ret = "hostile"
            elif react < 0:
                ret = "unfriendly"
            elif react == 0:
                ret = "neutral"
            elif react > 50:
                ret = "helpful"
            elif react > 0:
                ret = "friendly"

        # draw (subtracting camera start to draw in screen space)
        console[pos.x-width_start][pos.y-height_start] = (visual.char, visual.color, ret)

    # draw player at his position
    console[position.x-width_start][position.y-height_start] = ('@', (255, 255, 255), "friendly")

    return console

def map_to_draw(inc_map, fov, explored):
    #mapa = map_common.get_map_glyphs(inc_map)

    # dummy
    mapa = [[("&nbsp;", (255, 255, 255), None) for _ in range(constants.MAP_HEIGHT+1)] for _ in range(constants.MAP_WIDTH+1)]

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
                    # special case for walls
                    if inc_map[tx][ty] == get_index(TileTypes.WALL):
                        mapa[x][y] = (drawn_wall_glyph(inc_map, tx,ty), get_color(inc_map[tx][ty]), None)
                    else:
                        mapa[x][y] = (get_map_str(inc_map[tx][ty]), get_color(inc_map[tx][ty]), None)
                else:
                    mapa[x][y] = ("&nbsp;", (255, 255, 255), None)
                    # blank span later escaped by |safe Jinja template markup
            else:
                mapa[x][y] = ("&nbsp;", (255, 255, 255), None)
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