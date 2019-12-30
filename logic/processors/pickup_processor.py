from .. import esper

from ..components.equipment_component import EquipmentComponent
from ..components.in_backpack import InBackpackComponent
from ..components.equipped import EquippedComponent

from ..components.item_component import ItemComponent
from ..components.position import Position
from ..components.name_component import NameComponent

from ..components.want_to_pickup import WantToPickupComponent

from .. import game_vars

def pick_up(options, ent, equip, world):
    if len(options) == 0:
        # message
        game_vars.messages.append(("Nothing to pick up here!", (255, 255, 255)))

    elif len(options) == 1:
        item_ent = options[0]
        equip.equipment.append(item_ent)
        world.add_component(item_ent, InBackpackComponent())
        # message
        ent_name = world.component_for_entity(item_ent, NameComponent)
        game_vars.messages.append(("Player picked up " + ent_name.name + "!", (255,255, 255)))
    else:
        # because we render topmost item in stack, we also need to pick up topmost item in stack
        # to make it visually clear what happened
        options.reverse()

        item_ent = options[0]
        equip.equipment.append(item_ent)
        world.add_component(item_ent, InBackpackComponent())
        # message
        ent_name = world.component_for_entity(item_ent, NameComponent)
        game_vars.messages.append(("Player picked up " + ent_name.name + "!", (255,255, 255)))

    world.remove_component(ent, WantToPickupComponent)

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Pickup processor...")
        options = []
        for ent, (pick, equip, pos) in self.world.get_components(WantToPickupComponent, EquipmentComponent, Position):
            for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, Position):
                if pos.x == item_pos.x and pos.y == item_pos.y:
                    if self.world.has_component(item_ent, InBackpackComponent):
                        # skip
                        continue
                    if self.world.has_component(item_ent, EquippedComponent):
                        # skip
                        continue
                    
                    options.append(item_ent)

            pick_up(options, ent, equip, self.world)
