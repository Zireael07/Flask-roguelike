from . import esper

from .player import Player
from .name_component import NameComponent
from .dead_component import DeadComponent
from .combat_stats import StatsComponent


from . import game_vars

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (name, dead) in self.world.get_components(NameComponent, DeadComponent):
            if self.world.has_component(ent, Player):
                print("Player is dead!!!")
                # skip
                continue

            # if fighter.hp > 0:
            #     # skip
            #     continue

            game_vars.messages.append(name.name + " is dead!")
            # delete from ECS
            self.world.delete_entity(ent)
