import random

from .components.position import Position
from .components.velocity import Velocity
from .components.player import Player
from .components.turn_component import TurnComponent
from .components.renderable import RenderableComponent
from .components.NPC_component import NPC_Component
from .components.blocks_tile import TileBlocker
from .components.combat_stats import StatsComponent
from .components.name_component import NameComponent
from .components.equipment_component import EquipmentComponent
from .components.item_component import ItemComponent


from . import constants
from . import random_utils
from . import generators

def spawn_player(world):
    player = world.create_entity()
    world.add_component(player, Player())
    world.add_component(player, TurnComponent())
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())
    world.add_component(player, StatsComponent(hp=20, power=4))
    world.add_component(player, NameComponent("Player"))
    world.add_component(player, EquipmentComponent())


def spawn_npc(world):
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

def spawn_item(world):
    # random location
    pos = (random.randint(1, constants.MAP_WIDTH-2), random.randint(1, constants.MAP_HEIGHT-2))

    choice = random_utils.generate_random_item()
    # things that all items share
    it = world.create_entity(Position(x=pos[0], y=pos[1]), ItemComponent())

    # fill in the rest
    add = generators.generate_item(choice.lower())

    # add them
    for a in add:
        world.add_component(it, a)