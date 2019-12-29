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
from .components.faction_component import FactionComponent
from .components.attributes_component import AttributesComponent
from .components.skills_component import SkillsComponent
# for equippable items
from .components.wearable import WearableComponent
from .components.equipped import EquippedComponent

from . import constants
from . import random_utils
from . import map_common
from . import generators

def spawn_player(world, loc):
    player = world.create_entity(Position(x=loc[0], y=loc[1]), Velocity(), SkillsComponent(), NameComponent("Player") )
    add = [ Player(), TurnComponent(), StatsComponent(hp=20, power=4), AttributesComponent(15, 14, 13, 12, 8, 10),
    EquipmentComponent(), FactionComponent("player") ]

    for a in add:
        world.add_component(player, a)

    equip_list = ["T-shirt", "Jeans", "Boots"]
    for e in equip_list:
        spawn_named_item(world, loc, e.lower(), player)

def spawn_npc(world, pos):
    # random location
    #pos = (random.randint(1, constants.MAP_WIDTH-2), random.randint(1, constants.MAP_HEIGHT-2))

    choice = random_utils.generate_random_NPC()

    # the things that all NPCs share
    npc = world.create_entity(Position(x=pos[0], y=pos[1]), Velocity(), TileBlocker(), NPC_Component(), AttributesComponent(), SkillsComponent())

    # fill in the rest
    add, equip_list = generators.generate_npc(choice.lower())
    # add them
    for a in add:
        world.add_component(npc, a)

    for e in equip_list:
        spawn_named_item(world, pos, e, npc)

def spawn_item(world, pos):
    # random location
    #pos = (random.randint(1, constants.MAP_WIDTH-2), random.randint(1, constants.MAP_HEIGHT-2))

    choice = random_utils.generate_random_item()
    # things that all items share
    it = world.create_entity(Position(x=pos[0], y=pos[1]), ItemComponent())

    # fill in the rest
    add = generators.generate_item(choice.lower())

    # add them
    for a in add:
        world.add_component(it, a)

def spawn_named_item(world, pos, _id, ent_equipped=None):
    # things that all items share
    it = world.create_entity(Position(x=pos[0], y=pos[1]), ItemComponent())

    # fill in the rest
    add = generators.generate_item(_id)

    # add them
    for a in add:
        world.add_component(it, a)

    if ent_equipped:
        world.add_component(it, EquippedComponent(slot=world.component_for_entity(it, WearableComponent).slot, owner=ent_equipped))
        print("Spawned an equipped item... " + str(world.component_for_entity(it, NameComponent).name))


        