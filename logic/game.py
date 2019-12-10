import jsonpickle  # because we're lazy and don't want to manually serialize everything

from . import esper # the one Python3 library we're using

from .position import Position
from .velocity import Velocity
from .player import Player
from .turn_component import TurnComponent
from .renderable import RenderableComponent
from .NPC_component import NPC_Component
from .blocks_tile import TileBlocker

from .movement_processor import MovementProcessor
from .action_processor import ActionProcessor
from .fov_processor import FovProcessor
##from .AI_processor import AIProcessor

from . import arenamap
from . import constants
from . import ppfov
from .tile_lookups import get_block_path

from . import game_vars

def main():
    # Prepare world
    world = esper.World()

    # Initial FOV setup
    fov_map = [[0 for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]
    explored = [[0 for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]
    game_vars.fov = fov_map
    game_vars.explored = explored

    # Instantiate processors
    movement_processor = MovementProcessor()
    action_processor = ActionProcessor()
    fov_processor = FovProcessor()

    world.add_processor(action_processor, 100)
    world.add_processor(movement_processor, 50)
    world.add_processor(fov_processor, 45)

    # Create entities and assign components
    player = world.create_entity()
    world.add_component(player, Player())
    world.add_component(player, TurnComponent())
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())

    # Create some npcs
    world.create_entity(
        Position(x=4, y=4),
        RenderableComponent(char='h', color=(255, 255, 255)),
        Velocity(),
        TileBlocker(),
        NPC_Component()
    ) 
    world.create_entity(
        Position(x=12, y=6),
        RenderableComponent(char='h', color=(255, 255, 255)),
        Velocity(),
        TileBlocker(),
        NPC_Component()
    ) 

    # Generate map
    mapa = arenamap.map_create([(10,10), (15,15)])
    #arenamap.print_map_string(mapa)
    game_vars.mapa = mapa

    # Initial FOV
    ppfov.fieldOfView(1,1, constants.MAP_WIDTH, constants.MAP_HEIGHT, 6, explore, block_sight)

    # Save state 
    game_vars.world = world
    game_vars.fov = fov_map

    print("Initialized game...")

    # traditional loop is not necessary in Flask
    #try:
    #    while True:
    #        world.process()
    #        time.sleep(1)

# FOV interface
def explore(x,y):
    game_vars.fov[x][y] = 1
    game_vars.explored[x][y] = 1

def block_sight(x,y):
    return get_block_path(game_vars.mapa[x][y])

# Functions called by the Flask API
def move_and_update(world, action):
    world.get_processor(ActionProcessor).action = action
    world.process()

def get_position(world):
    # we can get it straight from the world
    for ent, (player, pos) in world.get_components(Player, Position):
        return pos


# debugging
def json_info(comp):
    return jsonpickle.encode(comp)
    #return str(comp)
    #return str(type(comp))


def represent_world(world, *with_components):
    data = {} 

    for ent, _ in world.get_components(*with_components):

        components = world.components_for_entity(ent)

        data.update({"ent": ent})
        list = []
        for c in components:
            list.append(json_info(c))
 
        data.update({"list" : list})

    return data
#    print(tabulate.tabulate(data))

