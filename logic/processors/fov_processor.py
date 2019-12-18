from .. import esper

from ..components.player import Player
from ..components.position import Position

from .. import ppfov
from .. import constants
from ..tile_lookups import get_block_path

from .. import game_vars

 # FOV interface
def explore(x,y):
    game_vars.fov[x][y] = 1
    game_vars.explored[x][y] = 1

def block_sight(x,y):
    return get_block_path(game_vars.mapa[x][y])

def update_FOV(src_x, src_y):
    # Generate FOV
    game_vars.fov = [[0 for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]
    ppfov.fieldOfView(src_x,src_y, constants.MAP_WIDTH, constants.MAP_HEIGHT, 6, explore, block_sight)


class FovProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self):
        for ent, (player, pos) in self.world.get_components(Player, Position):
            #print("FOV process pos " + str(pos.x) + " " + str(pos.y))
            update_FOV(pos.x, pos.y)