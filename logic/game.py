import jsonpickle  # because we're lazy and don't want to manually serialize everything

from . import esper # the one Python3 library we're using
from . import esper_ext # ease of use extensions

from .processors.movement_processor import MovementProcessor
from .processors.action_processor import ActionProcessor
from .processors.fov_processor import FovProcessor
from .processors.combat_processor import CombatProcessor
from .processors.death_processor import DeathProcessor
from .processors.AI_processor import AIProcessor
from .processors.pickup_processor import PickupProcessor
from .processors.use_item_processor import UseItemProcessor
from .processors.drop_processor import DropProcessor

from .components.player import Player
from .components.position import Position
from .components.dead_component import DeadComponent
from .components.combat_stats import StatsComponent

from . import arenamap
from . import constants
from . import ppfov
from . import camera
from .tile_lookups import get_block_path

from . import spawner

from . import game_vars

def main():
    # Prepare world
    # We're using some QoL extensions
    world = esper_ext.WorldExt()

    # Initial FOV setup
    fov_map = [[0 for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]
    explored = [[0 for _ in range(constants.MAP_HEIGHT)] for _ in range(constants.MAP_WIDTH)]
    game_vars.fov = fov_map
    game_vars.explored = explored

    # Instantiate processors
    movement_processor = MovementProcessor()
    action_processor = ActionProcessor()
    fov_processor = FovProcessor()
    combat_processor = CombatProcessor()
    death_processor = DeathProcessor()
    pickup_processor = PickupProcessor()
    useitem_processor = UseItemProcessor()
    drop_processor = DropProcessor()

    world.add_processor(action_processor, 100)
    world.add_processor(pickup_processor, 52)
    world.add_processor(useitem_processor, 52)
    world.add_processor(drop_processor, 52)
    world.add_processor(movement_processor, 50)
    world.add_processor(AIProcessor(), 48)
    world.add_processor(combat_processor, 45)
    world.add_processor(death_processor, 20)
    world.add_processor(fov_processor, 15)

    # Create entities and assign components
    spawner.spawn_player(world)

    # Create some npcs
    for i in range(constants.NUM_NPC):
        spawner.spawn_npc(world)


    # Some items
    for i in range(constants.NUM_ITEMS):
        spawner.spawn_item(world)
        
    # Generate map
    mapa = arenamap.map_create([(10,10), (15,15)])
    #arenamap.print_map_string(mapa)
    game_vars.mapa = mapa

    # Initial FOV
    ppfov.fieldOfView(1,1, constants.MAP_WIDTH, constants.MAP_HEIGHT, 6, explore, block_sight)

    # Camera
    cam = camera.obj_Camera()
    cam.start_update()

    # Save state 
    game_vars.world = world
    game_vars.fov = fov_map
    game_vars.camera = cam
    # Init messages
    game_vars.messages = []

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
def act_and_update(world, action):
    world.get_processor(ActionProcessor).action = action
    world.process()

def force_update(world):
    world.process()

def get_position(world):
    # we can get it straight from the world
    for ent, (player, pos) in world.get_components(Player, Position):
        return pos

def get_stats(world):
    for ent, (player, fighter) in world.get_components(Player, StatsComponent):
        return fighter

def is_player_alive(world):
    for ent, (player) in world.get_components(Player, Position):
        alive = not world.has_component(ent, DeadComponent)
        #print("Alive? " + str(alive))
        return alive

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

