from . import esper

from .want_to_use_med import WantToUseMed
from .combat_stats import StatsComponent
from .name_component import NameComponent
from .meditem_component import MedItemComponent
from .skip_component import SkipComponent

from . import game_vars

class UseItemProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Use item processor...")
        for ent, (use) in self.world.get_component(WantToUseMed):
            item_ID = self.world.component_for_entity(ent, WantToUseMed).item_ID 
            print("Item id to use: " + str(item_ID))

            # if item is a med item
            if self.world.has_component(item_ID, MedItemComponent):
                print("Item is a med item")
                value = self.world.component_for_entity(item_ID, MedItemComponent).heal
                user_stats = self.world.component_for_entity(ent, StatsComponent)
                # heal
                user_stats.hp += value
                if user_stats.hp > user_stats.hp_max:
                    user_stats.hp = user_stats.hp_max

                # message
                name = self.world.component_for_entity(ent, NameComponent)
                item_name = self.world.component_for_entity(item_ID, NameComponent)
                game_vars.messages.append(name.name + " uses " + item_name.name + ", healing " + str(value) + " hp!")
            
            # generic message
            #game_vars.messages.append(name.name + " uses " + item_name.name + "!")
            
            # cleanup
            self.world.remove_component(ent, WantToUseMed)
            self.world.add_component(item_ID, SkipComponent()) # using it to mark it as being removed
            self.world.delete_entity(item_ID)

