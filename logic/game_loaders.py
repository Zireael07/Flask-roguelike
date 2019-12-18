#import jsonpickle
#import json
import shelve
import os

from . import game_vars

from .components.player import Player

# save/load
def save_game():

    # jsonpickle by default can't handle the way esper stores components/entities/processors

    # Veins of the Earth used jsonpickle because a) it's human readable and b) it's more secure than pickle (by virtue of being human readable, mostly)
    # data = {
    #     # 'serialized_world': jsonpickle.encode(game_vars.world),
    #     'serialized_map': jsonpickle.encode(game_vars.mapa),
    #     'serialized_fov': jsonpickle.encode(game_vars.fov),
    #     'serialized_explored': jsonpickle.encode(game_vars.explored),
    #     'serialized_messages': jsonpickle.encode(game_vars.messages),

    # }

    # # write to file
    # with open('savegame.json', 'w') as save_file:
    #     json.dump(data, save_file, indent=4)

    # shelve is backed by pickle
    # however, if it's secure enough for my day job, it's also secure enough for my hobby project xDDD
     with shelve.open('savegame', 'n') as data_file:
        # serialize the world
        data_file['next_entity_id'] = game_vars.world._next_entity_id
        data_file['components'] = game_vars.world._components
        data_file['entities'] = game_vars.world._entities
        # the rest
        data_file['map'] = game_vars.mapa
        data_file['fov'] = game_vars.fov
        data_file['camera'] = game_vars.camera
        data_file['explored'] = game_vars.explored
        data_file['messages'] = game_vars.messages

def load_game():
    print("Loading game...")

    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        # load the world
        game_vars.world._next_entity_id = data_file['next_entity_id']
        game_vars.world._components = data_file['components']
        game_vars.world._entities = data_file['entities']
        # the rest
        game_vars.mapa = data_file['map']
        game_vars.camera = data_file['camera']
        game_vars.fov = data_file['fov']
        game_vars.explored = data_file['explored']
        game_vars.messages = data_file['messages']


    # see comments in save_game()
    # with open('savegame.json', 'r') as save_file:
    #     data = json.load(save_file)

    #game_vars.world = world_tmp
    # game_vars.mapa = jsonpickle.decode(data['serialized_map'])
    # game_vars.fov = jsonpickle.decode(data['serialized_explored'])
    # game_vars.explored = jsonpickle.decode(data['serialized_explored'])
    # game_vars.messages = jsonpickle.decode(data['serialized_messages'])

    # test
    #print(game_vars.world.get_component(Player))
