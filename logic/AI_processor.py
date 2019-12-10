from . import esper

from .NPC_component import NPC_Component
from .turn_component import TurnComponent
from .position import Position
from .player import Player
from .blocks_tile import TileBlocker

from . import game_vars
from .tile_lookups import TileTypes, get_index
from . import astar

class AIProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        player_id = None
        for ent, (player) in self.world.get_components(Player):
            player_id = ent

        for ent, (brain) in self.world.get_components(NPC_Component):
            if not self.world.has_component(ent, Player):
                self.take_turn(ent, player_id)

        # player takes the next turn
        self.world.add_component(player_id, TurnComponent())
        self.world.remove_processor(AIProcessor)


    def take_turn(self, ent, player_id):
        print('AI thinks.')
        position = self.world.component_for_entity(ent, Position)
        player_pos = self.world.component_for_entity(player_id, Position)
        # FOV is symmetric: if we're in FOV, player is in NPC's sights too
        if game_vars.fov[position.x][position.y]:
            print("We can see player")
            # pathfinding
            # avoid changing the real map
            import copy
            path_map = copy.deepcopy(game_vars.mapa)
            # mark spots with blocking entities as "walls"
            for entity, (block, pos) in self.world.get_components(TileBlocker, Position):
                path_map[pos.x][pos.y] = get_index(TileTypes.WALL)

            path = astar.astar(path_map, (position.x, position.y), (player_pos.x, player_pos.y))
            print("Path: " + str(path))
            # #0 is our current position
            if len(path) > 1:
                if path[1] != (player_pos.x, player_pos.y):
                    # just move (the path only works on walkable tiles anyway)
                    position.x, position.y = path[1]
                else:
                    print("AI kicks at your shins")