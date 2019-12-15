from . import esper

from .combat_component import CombatComponent
from .combat_stats import StatsComponent
from .name_component import NameComponent
from .dead_component import DeadComponent

from .equipped import EquippedComponent
from .melee_bonus_component import MeleeBonusComponent

from . import game_vars

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Combat processor...")
        for ent, (com) in self.world.get_component(CombatComponent):
            attacker_ID = ent
            target_ID = self.world.component_for_entity(attacker_ID, CombatComponent).target_ID

            attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
            target_stats = self.world.component_for_entity(target_ID, StatsComponent)
            # deal damage!
            damage = attacker_stats.power
            # any bonuses?
            for item_ent, (equip, bonus) in self.world.get_components(EquippedComponent, MeleeBonusComponent):
                damage += bonus.bonus

            target_stats.hp -= damage

            # dead!
            if target_stats.hp <= 0:
                self.world.add_component(target_ID, DeadComponent())
                self.world.remove_component(ent, CombatComponent)

            # message
            attacker_name = self.world.component_for_entity(attacker_ID, NameComponent)
            target_name = self.world.component_for_entity(target_ID, NameComponent)
            game_vars.messages.append(attacker_name.name + " attacks " + target_name.name + " for " + str(damage) + " damage!")