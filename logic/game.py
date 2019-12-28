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

from . import map_common
from .map import level
from .map import arenamap
from .map import noisemap
from .map import bsp_townmap
from .map import rectangle_detect

from . import constants
from . import ppfov
from . import camera
from .tile_lookups import TileTypes, get_block_path, get_index

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


    # Generate map

    # this doesn't work (sad face)
    #mapa = noisemap.map_create().apply_rectangle_detection()
    
    # trick from http://hack.limbicmedia.ca/signal-chaining-in-python/
    mapgen_chain = [
        {'function': noisemap.map_create},
        {'function': rectangle_detect.apply_rectangle_detection},
        {'function': bsp_townmap.map_create}
     ]

    init_mapa = [[ get_index(TileTypes.WALL) for _ in range(0, constants.MAP_HEIGHT)] for _ in range(0, constants.MAP_WIDTH)]
    init_lvl = level.obj_Level(init_mapa) 
   
    lvl = chain(init_lvl, mapgen_chain)
    mapa = lvl.mapa

    #mapa = bsp_townmap.map_create()
    #mapa = noisemap.map_create()
    #mapa = arenamap.map_create([(10,10), (15,15)])
    #arenamap.print_map_string(mapa)
    game_vars.mapa = mapa


    # Factions
    game_vars.factions = []
    add_faction(("player", "enemy", -100))
    add_faction(("player", "neutral", 0))
    add_faction(("player", "cop", 0))
    add_faction(("cop", "enemy", -100))

    # Create some npcs
    for i in range(constants.NUM_NPC):
        loc = map_common.random_free_tile(mapa)
        spawner.spawn_npc(world, loc)

    # Some items
    for i in range(constants.NUM_ITEMS):
        loc = map_common.random_free_tile(mapa)
        spawner.spawn_item(world, loc)

    # Player start location
    loc = map_common.random_free_tile(mapa)

    # Create entities and assign components
    spawner.spawn_player(world, loc)        

    # Initial FOV
    ppfov.fieldOfView(loc[0],loc[1], constants.MAP_WIDTH, constants.MAP_HEIGHT, 6, explore, block_sight)

    # Camera
    cam = camera.obj_Camera()
    cam.start_update(loc)

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


# Chaining functions
def chain(input_, operations):  
    for operation in operations:
        input_ = operation['function'](input_, **operation)

    return input_

# Factions
def add_faction(faction_data):
    game_vars.factions.append(faction_data)
    print ("Added faction " + str(faction_data))

    # add the reverse mapping, too
    game_vars.factions.append((faction_data[1], faction_data[0], faction_data[2]))
    print ("Added reverse faction " + str((faction_data[1], faction_data[0], faction_data[2])))

def get_faction_reaction(faction, target_faction):
    if faction == target_faction:
        return 100

    for fact in game_vars.factions:
        if fact[0] == faction and fact[1] == target_faction:
            #print("Faction reaction of " + fact[0] + " to " + fact[1] + " is " + str(fact[2]))
            return fact[2]

# FOV interface
def explore(x,y):
    game_vars.fov[x][y] = 1
    game_vars.explored[x][y] = 1

def block_sight(x,y):
    # paranoia
    if x < 0 or y < 0 or y > len(game_vars.mapa[0]) or x > len(game_vars.mapa):
        return False
    else:
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
        return pos, ent

def get_stats(world):
    for ent, (player, fighter) in world.get_components(Player, StatsComponent):
        return fighter

def is_player_alive(world):
    for ent, (player) in world.get_components(Player, Position):
        alive = not world.has_component(ent, DeadComponent)
        #print("Alive? " + str(alive))
        return alive
