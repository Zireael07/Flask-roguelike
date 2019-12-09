from . import esper

from .NPC_component import NPC_Component
from .turn_component import TurnComponent
from .player import Player


class AIProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (brain) in self.world.get_components(NPC_Component):
            if not self.world.has_component(ent, Player):
                self.take_turn()

        # player takes the next turn
        player_id = None
        for ent, (player) in self.world.get_components(Player):
            player_id = ent

        self.world.add_component(player_id, TurnComponent())
        self.world.remove_processor(AIProcessor)


    def take_turn(self):
        print('AI thinks.')