from flask import Flask, render_template, jsonify
app = Flask(__name__)

# generic
from logic import game
from logic import game_vars
from logic import constants
from logic import game_loaders

# more specific stuff we need
from logic.components.player import Player
from logic.components.cursor_component import CursorComponent
from logic.components.position import Position
from logic.components.renderable import RenderableComponent
from logic.components.in_backpack import InBackpackComponent
from logic.components.equipped import EquippedComponent
from logic.components.name_component import NameComponent
from logic.components.dead_component import DeadComponent
from logic.components.skip_component import SkipComponent


from logic import renderer_logic

# helpers
'''
Collects all the info that is needed for Flask internal API to redraw the game
'''
def data_to_redraw():
    # redraw
    position = game.get_position(game_vars.world)

    # cam
    game_vars.camera.update(position)

    console = renderer_logic.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)

    # camera
    cam = game_vars.camera
    width_start = cam.get_width_start()
    width_end = cam.get_width_end(game_vars.mapa)
    height_start = cam.get_height_start()
    height_end = cam.get_height_end(game_vars.mapa)

    # draw other entities
    matches = game_vars.world.get_components(Position, RenderableComponent)
    # sort by render order
    matches.sort(key=lambda item: item[1][1].render_order.value)

    for ent, (pos, visual) in matches:
        # if not in camera view
        if pos.x < width_start or pos.x > width_end or pos.y < height_start or pos.y > height_end:
            # skip
            continue
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        if game_vars.world.has_component(ent, DeadComponent):
            # skip
            continue
        if game_vars.world.has_component(ent, InBackpackComponent):
            # skip
            continue
        if game_vars.world.has_component(ent, EquippedComponent):
            # skip
            continue
        # draw (subtracting camera start to draw in screen space)
        console[pos.x-width_start][pos.y-height_start] = (visual.char, visual.color)

    # draw player at his position
    console[position.x-width_start][position.y-height_start] = ('@', (255, 255, 255))

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
        # skips entities that are being removed
        if game_vars.world.has_component(ent, SkipComponent):
            continue

        inventory.append((chr(letter_index), name.name, ent))
        letter_index += 1

    for ent, (name, equip) in game_vars.world.get_components(NameComponent, EquippedComponent):
        # skips entities that are being removed
        if game_vars.world.has_component(ent, SkipComponent):
            continue

        inventory.append((chr(letter_index), name.name + " (equipped)", ent))
        letter_index += 1


    return { "position" : position, "console": console, "messages" : messages, "fighter" : fighter, "inventory" : inventory}



@app.route('/')
def hello_world():
    # Init game
    game.main()

    # Initial page draw
    position = game.get_position(game_vars.world)

    console = renderer_logic.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)

    # camera
    cam = game_vars.camera
    width_start = cam.get_width_start()
    width_end = cam.get_width_end(game_vars.mapa)
    height_start = cam.get_height_start()
    height_end = cam.get_height_end(game_vars.mapa)

    # draw other entities
    for ent, (pos, visual) in game_vars.world.get_components(Position, RenderableComponent):
        # if not in camera view
        if pos.x < width_start or pos.x > width_end or pos.y < height_start or pos.y > height_end:
            # skip
            continue
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        # draw
        console[pos.x-width_start][pos.y-height_start] = (visual.char, visual.color)

    # draw player at his position
    console[position.x-width_start][position.y-height_start] = ('@', (255, 255, 255))

    return render_template('index.html', position = position, console=console, style=renderer_logic.map_style)
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
    position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])})



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

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })


@app.route('/use/<id>', methods = ["GET"])
def use_item(id=None):
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return
    print("Use action! - " + str(id))

    action = {'use_item': int(id)}

    game.act_and_update(game_vars.world, action)
    data = data_to_redraw()

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })

# this is an additional route because it shows a special screen
@app.route('/drop_view', methods = ["GET"])
def drop_view():
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return

    # inventory data
    inventory = []
    letter_index = ord('a')
    for ent, (name, inbackpack) in game_vars.world.get_components(NameComponent, InBackpackComponent):
        # skips entities that are being removed
        if game_vars.world.has_component(ent, SkipComponent):
            continue

        inventory.append((chr(letter_index), name.name, ent))
        letter_index += 1

    return jsonify({'inven': render_template('drop_inventory.html', inventory=inventory)})

@app.route('/drop/<id>', methods = ["GET"])
def drop_item(id=None):
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return
    print("Drop action! - " + str(id))

    action = {'drop_item': int(id)}

    game.act_and_update(game_vars.world, action)
    data = data_to_redraw()

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })

@app.route('/target_confirm', methods = ["GET"])
def target_confirm(x=None, y=None):
    if not game.is_player_alive(game_vars.world):
        print("Abort early, player dead")
        # This is a crash in Flask code, but it doesn't matter as we're dead either way
        return

    cursor = None
    for ent, (player, cur) in game_vars.world.get_components(Player, CursorComponent):
        cursor = cur
    
    # if no cursor, we clicked it by mistake = ignore
    if cursor is not None:
        # get x,y from cursor
        x = cursor.x
        y = cursor.y
        print("Confirmed target: " + str(x) + " " + str(y))

        action = {'target': (int(x), int(y))}

        game.act_and_update(game_vars.world, action)
        data = data_to_redraw()

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })

@app.route('/save', methods = ["GET"])
def save():
    game_loaders.save_game()

    data = data_to_redraw()

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })

@app.route('/load', methods = ["GET"])
def load():
    game_loaders.load_game()

    game.force_update(game_vars.world)

    data = data_to_redraw()

    return jsonify({'inven': render_template('inventory.html', inventory=data['inventory']),
    'data' : render_template('response.html', position=data['position'], console=data['console'], style=renderer_logic.map_style, messages=data['messages'], stats=data['fighter'])
    })