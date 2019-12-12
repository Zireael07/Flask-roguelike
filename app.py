from flask import Flask, render_template, jsonify
app = Flask(__name__)

# generic
from logic import game
from logic import game_vars
from logic import constants

# more specific stuff we need
from logic.player import Player
from logic.position import Position
from logic.renderable import RenderableComponent
from logic.in_backpack import InBackpackComponent
from logic.name_component import NameComponent
from logic.dead_component import DeadComponent
from logic import arenamap

# helpers
'''
Collects all the info that is needed for Flask internal API to redraw the game
'''
def data_to_redraw():
    # redraw
    ##data = game.represent_world(game_vars.world, Player)
    position = game.get_position(game_vars.world)
    #console = arenamap.get_map_glyphs(game_vars.mapa)
    console = arenamap.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)

    # draw other entities
    for ent, (pos, visual) in game_vars.world.get_components(Position, RenderableComponent):
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        if game_vars.world.has_component(ent, DeadComponent):
            # skip
            continue
        if game_vars.world.has_component(ent, InBackpackComponent):
            # skip
            continue
        # draw
        console[pos.x][pos.y] = visual.char

    # draw player at his position
    console[position.x][position.y] = '@'

    # messages
    if len(game_vars.messages) <= constants.NUM_MESSAGES:
        messages = game_vars.messages
    else:
        # slicing
        messages = game_vars.messages[-constants.NUM_MESSAGES:]

    # HUD
    fighter = game.get_stats(game_vars.world)

    # inventory
    inventory = []
    letter_index = ord('a')
    for ent, (name, inbackpack) in game_vars.world.get_components(NameComponent, InBackpackComponent):
        inventory.append((chr(letter_index), name.name))
        letter_index += 1

    return { "position" : position, "console": console, "messages" : messages, "fighter" : fighter, "inventory" : inventory}



@app.route('/')
def hello_world():
    # Init game
    game.main()

    # Initial page draw
    ##data = game.represent_world(game_vars.world, Player)
    position = game.get_position(game_vars.world)
    #mapa = arenamap.get_map_HTML(game_vars.mapa)
    #console = arenamap.get_map_glyphs(game_vars.mapa)
    console = arenamap.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)
    # draw player at his position
    console[position.x][position.y] = '@'
    # draw other entities
    for ent, (pos, visual) in game_vars.world.get_components(Position, RenderableComponent):
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        # draw
        console[pos.x][pos.y] = visual.char

    return render_template('index.html', position = position, console=console, style=arenamap.map_style)
    #return game.represent_world(game_vars.world, Position)
    # dict is converted to JSON automatically
    #return {
    #    "location": (1,1)
    #}
    #return 'Hello, World!'


# Thanks to https://repl.it/@EthanGoldman/Python-Flask-Website-with-Ajax-and-Jquery for figuring this out!
#When HTML button is clicked, execute the function
@app.route('/move/<x>/<y>', methods = ['GET'])
def move(x=None, y=None):
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return
    print("Move: " + str(x) + " " + str(y)) 

    action = {'move': (int(x), int(y))}

    game.act_and_update(game_vars.world, action)
    data = data_to_redraw()

    return jsonify({'data': render_template('response.html', 
    position=data['position'], console=data['console'], style=arenamap.map_style, messages=data['messages'], stats=data['fighter'])})



@app.route('/get', methods = ["GET"])
def get():
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return
    print("Get action!") 

    action = {'pick_up': True}

    game.act_and_update(game_vars.world, action)
    data = data_to_redraw()

    return jsonify({'data': render_template('inventory.html', inventory=data['inventory'])})
    #position=data['position'], console=data['console'], style=arenamap.map_style, messages=data['messages'], stats=data['fighter'], inventory=data['inventory'])})
