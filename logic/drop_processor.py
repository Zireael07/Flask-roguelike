from . import esper

from .want_to_drop import WantToDrop
from .in_backpack import InBackpackComponent
from .position import Position
from .name_component import NameComponent

from . import game_vars

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Drop item processor...")
        for ent, (use, pos) in self.world.get_components(WantToDrop, Position):
            item_ID = self.world.component_for_entity(ent, WantToDrop).item_ID 
            print("Item id to drop: " + str(item_ID))

            self.world.remove_component(item_ID, InBackpackComponent)
            
            pos_item = self.world.component_for_entity(item_ID, Position)
            pos_item.x, pos_item.y = pos.x, pos.y
            

            # message
            name = self.world.component_for_entity(ent, NameComponent)
            item_name = self.world.component_for_entity(item_ID, NameComponent)
            
            # generic message
            game_vars.messages.append(name.name + " drops " + item_name.name + "!")
            
            # cleanup
            self.world.remove_component(ent, WantToDrop)

