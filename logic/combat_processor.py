from . import esper

from .combat_component import CombatComponent
from .combat_stats import StatsComponent


class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (com) in self.world.get_component(CombatComponent):
            attacker_ID = ent
            target_ID = self.world.component_for_entity(attacker_ID, CombatComponent).target_ID

            attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
            target_stats = self.world.component_for_entity(target_ID, StatsComponent)
            # deal damage!
            target_stats.hp -= attacker_stats.power

            # message