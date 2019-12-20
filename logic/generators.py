import json

from .components.renderable import RenderableComponent
from .components.combat_stats import StatsComponent
from .components.name_component import NameComponent

# usable items
from .components.meditem_component import MedItemComponent
from .components.ranged_component import RangedComponent
from .components.area_of_effect import AreaOfEffectComponent
from .components.wearable import WearableComponent
from .components.melee_bonus_component import MeleeBonusComponent
from .components.weapon import WeaponComponent

def generate_npc(m_id):
    if m_id == 'None' or m_id == None:
        print("Wanted id of None, aborting")
        return

    print("Generating monster with id " + str(m_id))

    # paranoia
    if m_id not in npc_data:
        print("Don't know how to generate " + str(m_id) + "!")
        return

    comps = []
    # Components we want
    comps.append(RenderableComponent(char=npc_data[m_id]['renderable']['glyph'], color=tuple(npc_data[m_id]['renderable']['fg'])))
    comps.append(NameComponent(npc_data[m_id]['name']))
    comps.append(StatsComponent(hp=npc_data[m_id]['stats']['hp'], power=npc_data[m_id]['stats']['power']))

    return comps

def generate_item(_id):
    if _id == 'None' or _id == None:
        print("Wanted id of None, aborting")
        return

    print("Generating item with id " + str(_id))

    # paranoia
    if _id not in items_data:
        print("Don't know how to generate " + str(_id) + "!")
        return

    comps = []
    # Components we want
    comps.append(RenderableComponent(char=items_data[_id]['renderable']['glyph'], color=tuple(items_data[_id]['renderable']['fg'])))
    comps.append(NameComponent(items_data[_id]['name']))
    # optional components
    if 'consumable' in items_data[_id]:
        if 'effects' in items_data[_id]['consumable']:
            #print("Eff: " + str(items_data[_id]['consumable']['effects']))
            if 'med_item' in items_data[_id]['consumable']['effects']:
                comps.append(MedItemComponent(int(items_data[_id]['consumable']['effects']['med_item'])))
            if 'ranged' in items_data[_id]['consumable']['effects']:
                comps.append(RangedComponent(int(items_data[_id]['consumable']['effects']['ranged'])))
            if 'area_of_effect' in items_data[_id]['consumable']['effects']:
                comps.append(AreaOfEffectComponent(int(items_data[_id]['consumable']['effects']['area_of_effect'])))

    if 'wearable' in items_data[_id]:
        comps.append(WearableComponent(items_data[_id]['wearable']['slot'].upper()))
    if 'melee_bonus' in items_data[_id]:
        comps.append(MeleeBonusComponent(int(items_data[_id]['melee_bonus'])))
    if 'weapon' in items_data[_id]:
        num = None
        dam = None
        if 'damage_number_dice' in items_data[_id]['weapon']:
            num = int(items_data[_id]['weapon']['damage_number_dice'])
        if 'damage_dice' in items_data[_id]['weapon']:
            dam = int(items_data[_id]['weapon']['damage_dice'])
        
        comps.append(WeaponComponent(num_dice=num, dam_dice=dam))

    return comps

# Load JSON
# this is triggered by merely importing this module
with open("npcs.json") as json_data:
        npc_data = json.load(json_data)
        print(npc_data)

with open("items.json") as json_data:
    items_data = json.load(json_data)
    print(items_data)