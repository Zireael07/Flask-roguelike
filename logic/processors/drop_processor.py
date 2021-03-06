from .. import esper

from ..components.want_to_drop import WantToDrop
from ..components.in_backpack import InBackpackComponent
from ..components.position import Position
from ..components.name_component import NameComponent
from ..components.equipped import EquippedComponent

from .. import game_vars

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Drop item processor...")
        for ent, (use, pos) in self.world.get_components(WantToDrop, Position):
            item_ID = self.world.component_for_entity(ent, WantToDrop).item_ID 
            print("Item id to drop: " + str(item_ID))

            # message
            name = self.world.component_for_entity(ent, NameComponent)
            item_name = self.world.component_for_entity(item_ID, NameComponent)

            if self.world.has_component(item_ID, InBackpackComponent):
                self.world.remove_component(item_ID, InBackpackComponent)
            # if equipped, unequip
            if self.world.has_component(item_ID, EquippedComponent):
                game_vars.messages.append((name.name + " unequips " + item_name.name, (255, 255, 255)))
                self.world.remove_component(item_ID, EquippedComponent)
            
            pos_item = self.world.component_for_entity(item_ID, Position)
            pos_item.x, pos_item.y = pos.x, pos.y
            


            
            # generic message
            game_vars.messages.append((name.name + " drops " + item_name.name + "!", (255, 255, 255)))
            
            # cleanup
            self.world.remove_component(ent, WantToDrop)

