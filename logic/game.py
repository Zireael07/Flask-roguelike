import jsonpickle  # because we're lazy and don't want to manually serialize everything

from . import esper # the one Python3 library we're using

from .position import Position
from .velocity import Velocity
from .player import Player
from .turn_component import TurnComponent
from .renderable import RenderableComponent
from .NPC_component import NPC_Component
from .blocks_tile import TileBlocker
from .combat_stats import StatsComponent
from .name_component import NameComponent
from .dead_component import DeadComponent
from .equipment_component import EquipmentComponent
from .item_component import ItemComponent

from .movement_processor import MovementProcessor
from .action_processor import ActionProcessor
from .fov_processor import FovProcessor
from .combat_processor import CombatProcessor
from .death_processor import DeathProcessor
from .AI_processor import AIProcessor
from .equip_processor import EquipProcessor

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
    combat_processor = CombatProcessor()
    death_processor = DeathProcessor()
    equip_processor = EquipProcessor()

    world.add_processor(action_processor, 100)
    world.add_processor(equip_processor, 52)
    world.add_processor(movement_processor, 50)
    world.add_processor(AIProcessor(), 48)
    world.add_processor(combat_processor, 45)
    world.add_processor(death_processor, 20)
    world.add_processor(fov_processor, 15)

    # Create entities and assign components
    player = world.create_entity()
    world.add_component(player, Player())
    world.add_component(player, TurnComponent())
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())
    world.add_component(player, StatsComponent(hp=20, power=4))
    world.add_component(player, NameComponent("Player"))
    world.add_component(player, EquipmentComponent())

    # Create some npcs
    world.create_entity(
        Position(x=4, y=4),
        RenderableComponent(char='h', color=(255, 255, 255)),
        Velocity(),
        TileBlocker(),
        NPC_Component(),
        StatsComponent(hp=11, power=2),
        NameComponent("Human")
    ) 
    world.create_entity(
        Position(x=12, y=6),
        RenderableComponent(char='h', color=(255, 255, 255)),
        Velocity(),
        TileBlocker(),
        NPC_Component(),
        StatsComponent(hp=11, power=2),
        NameComponent("Human")
    ) 

    # Some items
    world.create_entity(
        ItemComponent(),
        Position(x=6, y=5),
        RenderableComponent(char='/', color=(0, 255, 255)),
        NameComponent("Combat Knife")
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

