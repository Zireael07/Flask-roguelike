from . import esper

from .position import Position
from .velocity import Velocity
from .turn_component import TurnComponent

class MovementProcessor(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            print("Ent: " + str(ent) + " vel " + str(vel))
            if vel.dx == 0 and vel.dy == 0:
                # skip entity
                continue 
            
            tx = pos.x + vel.dx 
            ty = pos.y + vel.dy

            vel.dx = 0
            vel.dy = 0

            # don't walk out of map
            if tx < 0 or tx > 19 or ty < 0 or tx > 19:
                return

            pos.x = tx
            pos.y = ty
            #print("Pos after move process: " + str(pos.x) + " " + str(pos.y))
