import jsonpickle  # because we're lazy and don't want to manually serialize everything

from . import esper # the one Python3 library we're using

from .position import Position
from .velocity import Velocity
from .movement_processor import MovementProcessor
from .action_processor import ActionProcessor

from . import arenamap

from . import game_vars

def main():
    # Prepare world
    world = esper.World()

    # Instantiate processors
    movement_processor = MovementProcessor()
    action_processor = ActionProcessor()

    world.add_processor(action_processor, 100)
    world.add_processor(movement_processor, 50)    

    # Create entities and assign components
    player = world.create_entity()
    world.add_component(player, Position(x=1, y=1))
    world.add_component(player, Velocity())

    # Generate map
    mapa = arenamap.map_create([(10,10), (15,15)])
    #arenamap.print_map_string(mapa)

    # Save state 
    game_vars.world = world
    game_vars.mapa = mapa

    print("Main logic")
    # traditional loop is not necessary in Flask
    #try:
    #    while True:
    #        world.process()
    #        time.sleep(1)
  
# Functions called by the Flask API
def move_and_update(world, action):
    world.get_processor(ActionProcessor).action = action
    world.process()

def get_position(data):
    # raw JSON
    #return data['list'][0]
    return jsonpickle.decode(data['list'][0])

def json_info(comp):
    return jsonpickle.encode(comp)
    #return str(comp)
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
#    print(tabulate.tabulate(data))

