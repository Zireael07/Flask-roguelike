from .. import esper

from ..components.player import Player
from ..components.name_component import NameComponent
from ..components.dead_component import DeadComponent
from ..components.combat_stats import StatsComponent


from .. import game_vars

class DeathProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (name, dead) in self.world.get_components(NameComponent, DeadComponent):
            if self.world.has_component(ent, Player):
                #print("Player is dead!!!")
                game_vars.messages.append(("YOU DIED!!", (255, 0, 0)))
                # skip
                continue

            # if fighter.hp > 0:
            #     # skip
            #     continue

            game_vars.messages.append((name.name + " is dead!", (127, 127, 127)))
            # delete from ECS
            self.world.delete_entity(ent)
