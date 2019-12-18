import jsonpickle  # because we're lazy and don't want to manually serialize everything
import random

from . import esper # the one Python3 library we're using
from . import esper_ext # ease of use extensions

from .components.position import Position
from .components.velocity import Velocity
from .components.player import Player
from .components.turn_component import TurnComponent
from .components.renderable import RenderableComponent
from .components.NPC_component import NPC_Component
from .components.blocks_tile import TileBlocker
from .components.combat_stats import StatsComponent
from .components.name_component import NameComponent
from .components.dead_component import DeadComponent
from .components.equipment_component import EquipmentComponent
from .components.item_component import ItemComponent
from .components.meditem_component import MedItemComponent
from .components.ranged_component import RangedComponent
from .components.area_of_effect import AreaOfEffectComponent
from .components.wearable import WearableComponent
from .components.melee_bonus_component import MeleeBonusComponent

from .processors.movement_processor import MovementProcessor
from .processors.action_processor import ActionProcessor
from .processors.fov_processor import FovProcessor
from .processors.combat_processor import CombatProcessor
from .processors.death_processor import DeathProcessor
from .processors.AI_processor import AIProcessor
from .processors.pickup_processor import PickupProcessor
from .processors.use_item_processor import UseItemProcessor
from .processors.drop_processor import DropProcessor

from . import arenamap
from . import constants
from . import ppfov
from . import camera
from .tile_lookups import get_block_path

from . import random_utils
from . import generators

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
    player = world.create_entity()
    world.add_component(player, Player())
    world.add_component(player, TurnComponent())
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())
    world.add_component(player, StatsComponent(hp=20, power=4))
    world.add_component(player, NameComponent("Player"))
    world.add_component(player, EquipmentComponent())

    # Create some npcs
    for i in range(constants.NUM_NPC):
        # random location
        pos = (random.randint(1, constants.MAP_WIDTH-2), random.randint(1, constants.MAP_HEIGHT-2))

        choice = random_utils.generate_random_NPC()

        # the things that all NPCs share
        npc = world.create_entity(Position(x=pos[0], y=pos[1]), Velocity(), TileBlocker(), NPC_Component())

        # fill in the rest
        add = generators.generate_npc(choice.lower())
        # add them
        for a in add:
            world.add_component(npc, a)

        # if choice == "Thug":
        #     world.add_components(npc, RenderableComponent(char='h', color=(255, 255, 255)), NameComponent("Thug"), StatsComponent(hp=6, power=2))
        # elif choice == "Cop":
        #     world.add_components(npc, RenderableComponent(char='c', color=(0, 255, 0)), NameComponent("Cop"), StatsComponent(hp=11, power=3))

    # Some items
    for i in range(constants.NUM_ITEMS):
        # random location
        pos = (random.randint(1, constants.MAP_WIDTH-2), random.randint(1, constants.MAP_HEIGHT-2))

        choice = random_utils.generate_random_item()
        # things that all items share
        it = world.create_entity(Position(x=pos[0], y=pos[1]), ItemComponent())

        if choice == "Medkit":
            world.add_components(it, RenderableComponent(char='!', color=(255, 0, 0)), NameComponent("Medkit"),
            MedItemComponent(6)
        )
        elif choice == "Pistol":
            world.add_components(it, RenderableComponent(char=")", color=(0, 255, 0)), NameComponent("Pistol"),
            RangedComponent(6)
        )
        elif choice == "Grenade":
            world.add_components(it, RenderableComponent(char="*", color=(255,255,0)),  NameComponent("Grenade"),
            RangedComponent(6), AreaOfEffectComponent(3),
        )
        elif choice == "Combat Knife":
            world.add_components(it, RenderableComponent(char="/", color=(150, 255, 0)), NameComponent("Combat Knife"),
            WearableComponent("MAIN_HAND"), MeleeBonusComponent(2),
        )

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

