from flask import Flask, render_template, jsonify
app = Flask(__name__)

from logic import game
from logic import game_vars
from logic.position import Position
from logic import arenamap

@app.route('/')
def hello_world():
    # Init game
    game.main()

    # Initial page draw
    data = game.represent_world(game_vars.world, Position)
    pos = game.get_position(data)
    mapa = arenamap.get_map_HTML(game_vars.mapa)

    return render_template('index.html', position = pos, mapa=mapa)
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
    data = game.represent_world(game_vars.world, Position)
    pos = game.get_position(data)

    return jsonify({'data': render_template('response.html', position=pos)})

