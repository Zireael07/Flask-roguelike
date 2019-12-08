from flask import Flask, render_template, jsonify
app = Flask(__name__)

# generic
from logic import game
from logic import game_vars

# more specific stuff we need
from logic.player import Player
from logic.position import Position
from logic.renderable import RenderableComponent
from logic import arenamap

@app.route('/')
def hello_world():
    # Init game
    game.main()

    # Initial page draw
    data = game.represent_world(game_vars.world, Player)
    pos = game.get_position(data)
    #mapa = arenamap.get_map_HTML(game_vars.mapa)
    #console = arenamap.get_map_glyphs(game_vars.mapa)
    console = arenamap.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)
    # draw player at his position
    console[pos.x][pos.y] = '@'
    # draw other entities
    for ent, (pos, visual) in game_vars.world.get_components(Position, RenderableComponent):
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        # draw
        console[pos.x][pos.y] = visual.char

    return render_template('index.html', position = pos, console=console, style=arenamap.map_style)
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
    print("Move: " + str(x) + " " + str(y)) 

    action = {'move': (int(x), int(y))}

    game.move_and_update(game_vars.world, action)
    # redraw
    data = game.represent_world(game_vars.world, Player)
    pos = game.get_position(data)
    #console = arenamap.get_map_glyphs(game_vars.mapa)
    console = arenamap.map_to_draw(game_vars.mapa, game_vars.fov, game_vars.explored)
    # draw player at his position
    console[pos.x][pos.y] = '@'
    # draw other entities
    for ent, (pos, visual) in game_vars.world.get_components(Position, RenderableComponent):
        if not game_vars.fov[pos.x][pos.y]:
            # skip
            continue
        # draw
        console[pos.x][pos.y] = visual.char

    return jsonify({'data': render_template('response.html', position=pos, console=console, style=arenamap.map_style)})

