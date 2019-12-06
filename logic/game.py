from . import esper

from .position import Position
from .velocity import Velocity

from . import game_vars

def main():
    # Prepare world
    world = esper.World()
    # Instantiate processors
    
    # Create entities and assign components
    player = world.create_entity()
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())

    # Save state 
    game_vars.world = world

    print("Main logic")
    # traditional loop
    #try:
    #    while True:
    #        world.process()
    #        time.sleep(1)
  
def json_info(comp):
    return str(comp)
    #return str(type(comp))


def represent_world(world, *with_components):
    data = {} 

    for ent, _ in world.get_components(*with_components):

        components = world.components_for_entity(ent)

        data.update({"ent": ent})
        list = []
        for c in components:
            list.append(json_info(c))
 
        data.update({"list" : list})

    return data
    print(tabulate.tabulate(data))

