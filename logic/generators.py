import json

from .components.renderable import RenderableComponent
from .components.combat_stats import StatsComponent
from .components.name_component import NameComponent


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

# Load JSON
# this is triggered by merely importing this module
with open("npcs.json") as json_data:
        npc_data = json.load(json_data)
        print(npc_data)
