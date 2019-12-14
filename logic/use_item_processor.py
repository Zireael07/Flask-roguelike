from . import esper

from .want_to_use_med import WantToUseMed
from .combat_stats import StatsComponent
from .name_component import NameComponent
from .meditem_component import MedItemComponent
from .skip_component import SkipComponent

from .want_to_use_item import WantToUseItem
from .position import Position
from .ranged_component import RangedComponent
from .cursor_component import CursorComponent

from . import game_vars
from . import map_common

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

        for ent, (use) in self.world.get_component(WantToUseItem):
            item_ID = self.world.component_for_entity(ent, WantToUseItem).item_ID
            print("Item id to use: " + str(item_ID))

            # if item is a ranged item and we have a cursor
            if self.world.has_component(item_ID, RangedComponent):
                ranged = self.world.component_for_entity(item_ID, RangedComponent)
                player_pos = self.world.component_for_entity(ent, Position)
                if self.world.has_component(ent, CursorComponent):
                    tg_x = self.world.component_for_entity(ent, CursorComponent).x
                    tg_y = self.world.component_for_entity(ent, CursorComponent).y
                    if map_common.tiles_distance_to((player_pos.x, player_pos.y), (tg_x, tg_y)) > ranged.radius:
                        print("Distance exceeded")
                        # remove cursor
                        self.world.remove_component(ent, CursorComponent)
                        self.world.remove_component(ent, WantToUseItem)

                    else:
                        # is there an entity?
                        targeted = None
                        for tg_ent, (pos, fighter) in self.world.get_components(Position, StatsComponent):
                            if pos.x == tg_x and pos.y == tg_y:
                                targeted = tg_ent
                                fighter.hp -= 6 # dummy

                                # message
                                name = self.world.component_for_entity(ent, NameComponent)
                                tg_name = self.world.component_for_entity(tg_ent, NameComponent)
                                game_vars.messages.append(name.name + " shoots " + tg_name.name + " for 6 damage!")

                        if targeted is None:
                            game_vars.messages.append("No target selected")
                        else:
                            # be nice, only take the item away if we selected a target
                            self.world.add_component(item_ID, SkipComponent()) # using it to mark it as being removed
                            self.world.delete_entity(item_ID)

                        # cleanup
                        self.world.remove_component(ent, WantToUseItem)
                        # remove cursor
                        self.world.remove_component(ent, CursorComponent)