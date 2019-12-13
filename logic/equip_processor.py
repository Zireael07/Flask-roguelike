from . import esper

from .equipment_component import EquipmentComponent
from .in_backpack import InBackpackComponent

from .item_component import ItemComponent
from .position import Position

from .want_to_pickup import WantToPickupComponent

from . import game_vars

class EquipProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Equip processor...")
        for ent, (pick, equip, pos) in self.world.get_components(WantToPickupComponent, EquipmentComponent, Position):
            for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, Position):
                if pos.x == item_pos.x and pos.y == item_pos.y:
                    if not self.world.has_component(item_ent, InBackpackComponent):
                        equip.equipment.append(item_ent)
                        self.world.add_component(item_ent, InBackpackComponent())
                        game_vars.messages.append("Player picked up item!")
            
            self.world.remove_component(ent, WantToPickupComponent)