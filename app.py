from flask import Flask
app = Flask(__name__)

from logic import game
from logic import game_vars
from logic.position import Position

@app.route('/')
def hello_world():
    game.main()

    return game.represent_world(game_vars.world, Position)
    # dict is converted to JSON automatically
    #return {
    #    "location": (1,1)
    #}
    #return 'Hello, World!'

