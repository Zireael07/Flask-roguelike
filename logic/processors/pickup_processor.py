from .. import esper

from ..components.equipment_component import EquipmentComponent
from ..components.in_backpack import InBackpackComponent

from ..components.item_component import ItemComponent
from ..components.position import Position
from ..components.name_component import NameComponent

from ..components.want_to_pickup import WantToPickupComponent

from .. import game_vars

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Pickup processor...")
        for ent, (pick, equip, pos) in self.world.get_components(WantToPickupComponent, EquipmentComponent, Position):
            for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, Position):
                if pos.x == item_pos.x and pos.y == item_pos.y:
                    if not self.world.has_component(item_ent, InBackpackComponent):
                        equip.equipment.append(item_ent)
                        self.world.add_component(item_ent, InBackpackComponent())
                        # message
                        ent_name = self.world.component_for_entity(item_ent, NameComponent)
                        game_vars.messages.append(("Player picked up " + ent_name.name + "!", (255,255, 255)))
                        break # only pick up one item
            
            self.world.remove_component(ent, WantToPickupComponent)