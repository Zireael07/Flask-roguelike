from . import esper

from .position import Position
from .velocity import Velocity
from .blocks_tile import TileBlocker
from .turn_component import TurnComponent

from .combat_component import CombatComponent

from .tile_lookups import get_block_path
from . import game_vars

class MovementProcessor(esper.Processor):

    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            #print("Ent: " + str(ent) + " vel " + str(vel))
            if vel.dx == 0 and vel.dy == 0:
                # skip entity
                continue 
            
            tx = pos.x + vel.dx 
            ty = pos.y + vel.dy

            vel.dx = 0
            vel.dy = 0

            # don't walk out of map
            if tx < 0 or tx > 19 or ty < 0 or tx > 19:
                continue
            # check for unwalkable tiles
            if get_block_path(game_vars.mapa[tx][ty]):
                continue

            # Check for entities
            for ent_target, (blocker, pos_tg) in self.world.get_components(TileBlocker, Position):
                if pos_tg.x == tx and pos_tg.y ==ty:
                    # Trigger a bump-attack here.
                    print("Attacking " + str(ent_target) + " @ " + str(pos_tg))
                    self.world.add_component(ent, CombatComponent(target_ID=ent_target))

            # move (if no combat going on)
            if not self.world.has_component(ent, CombatComponent):
                pos.x = tx
                pos.y = ty
                #print("Pos after move process: " + str(pos.x) + " " + str(pos.y))
