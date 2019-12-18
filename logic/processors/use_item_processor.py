from .. import esper

from ..components.want_to_use_med import WantToUseMed
from ..components.combat_stats import StatsComponent
from ..components.name_component import NameComponent
from ..components.meditem_component import MedItemComponent
from ..components.skip_component import SkipComponent

from ..components.want_to_use_item import WantToUseItem
from ..components.position import Position
from ..components.ranged_component import RangedComponent
from ..components.cursor_component import CursorComponent
from ..components.area_of_effect import AreaOfEffectComponent

from ..components.in_backpack import InBackpackComponent
from ..components.equipped import EquippedComponent
from ..components.wearable import WearableComponent

from .. import game_vars
from .. import map_common

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
                game_vars.messages.append((name.name + " uses " + item_name.name + ", healing " + str(value) + " hp!", (0, 255, 0)))
            
            # generic message
            #game_vars.messages.append(name.name + " uses " + item_name.name + "!")
            
            # cleanup
            self.world.remove_component(ent, WantToUseMed)
            self.world.add_component(item_ID, SkipComponent()) # using it to mark it as being removed
            self.world.delete_entity(item_ID)

        for ent, (use) in self.world.get_component(WantToUseItem):
            item_ID = self.world.component_for_entity(ent, WantToUseItem).item_ID
            print("Item id to use: " + str(item_ID))

            # equip/unequip
            if self.world.has_component(item_ID, WearableComponent):
                # if not equipped already
                if not self.world.has_component(item_ID, EquippedComponent):
                    slot = self.world.component_for_entity(item_ID, WearableComponent)

                    # unequip anything we might have in the slot
                    for item_ent, (equip, name) in self.world.get_components(EquippedComponent, NameComponent):
                        if equip.slot == slot:
                            ent_name = self.world.component_for_entity(ent, NameComponent)
                            game_vars.messages.append((ent_name.name + " unequips " + name.name, (255,255,255)))
                            self.world.remove_component(item_ent, EquippedComponent)
                            self.world.add_component(item_ent, InBackpackComponent)

                    # equip
                    self.world.add_component(item_ID, EquippedComponent(slot=slot))
                    self.world.remove_component(item_ID, InBackpackComponent)
                    name = self.world.component_for_entity(ent, NameComponent)
                    item_name = self.world.component_for_entity(item_ID, NameComponent)
                    game_vars.messages.append((name.name + " equips " + item_name.name,  (255,255,255)))
                else:
                    # unequip
                    ent_name = self.world.component_for_entity(ent, NameComponent)
                    game_vars.messages.append((ent_name.name + " unequips " + name.name,  (255,255,255)))
                    self.world.remove_component(item_ent, EquippedComponent)
                    self.world.add_component(item_ent, InBackpackComponent)

                # cleanup
                self.world.remove_component(ent, WantToUseItem)

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
                        # single target
                        if not self.world.has_component(item_ID, AreaOfEffectComponent):
                            # is there an entity?
                            targeted = None
                            for tg_ent, (pos, fighter) in self.world.get_components(Position, StatsComponent):
                                if pos.x == tg_x and pos.y == tg_y:
                                    targeted = tg_ent
                                    fighter.hp -= 6 # dummy

                                    # message
                                    name = self.world.component_for_entity(ent, NameComponent)
                                    tg_name = self.world.component_for_entity(tg_ent, NameComponent)
                                    game_vars.messages.append((name.name + " shoots " + tg_name.name + " for 6 damage!",  (255,255,255)))

                            if targeted is None:
                                game_vars.messages.append("No target selected")
                            else:
                                # be nice, only take the item away if we selected a target
                                self.world.add_component(item_ID, SkipComponent()) # using it to mark it as being removed
                                self.world.delete_entity(item_ID)
                        else:
                            radius = self.world.component_for_entity(item_ID, AreaOfEffectComponent).radius
                            for tg_ent, (pos, fighter) in self.world.get_components(Position, StatsComponent):
                                if map_common.tiles_distance_to((tg_x, tg_y), (pos.x, pos.y)) <= radius:
                                    fighter.hp -= 6 # dummy

                                    # message
                                    name = self.world.component_for_entity(ent, NameComponent)
                                    tg_name = self.world.component_for_entity(tg_ent, NameComponent)
                                    game_vars.messages.append((name.name + " blasts " + tg_name.name + " for 6 damage!",  (255,255,255)))

                            # remove item
                            self.world.add_component(item_ID, SkipComponent()) # using it to mark it as being removed
                            self.world.delete_entity(item_ID)

                        # cleanup
                        self.world.remove_component(ent, WantToUseItem)
                        # remove cursor
                        self.world.remove_component(ent, CursorComponent)