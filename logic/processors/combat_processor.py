from .. import esper

from ..components.combat_component import CombatComponent
from ..components.combat_stats import StatsComponent
from ..components.name_component import NameComponent
from ..components.dead_component import DeadComponent
from ..components.player import Player

from ..components.equipped import EquippedComponent
from ..components.weapon import WeaponComponent
from ..components.melee_bonus_component import MeleeBonusComponent

from .. import game_vars
from .. import random_utils

class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Combat processor...")
        for ent, (com) in self.world.get_component(CombatComponent):
            attacker_ID = ent
            target_ID = self.world.component_for_entity(attacker_ID, CombatComponent).target_ID

            attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
            target_stats = self.world.component_for_entity(target_ID, StatsComponent)
            # deal damage!
            #damage = attacker_stats.power
            
            # if no weapon, deal 1d6
            roll = (1,6)
            # use equipped weapon's data
            for item_ent, (equip, weapon) in self.world.get_components(EquippedComponent, WeaponComponent):
                print(str(equip.slot))
                if equip.owner == attacker_ID and equip.slot == "MAIN_HAND":
                    print("Use weapon dice")
                    roll = (weapon.num_dice, weapon.dam_dice)

            # deal damage!
            damage = random_utils.roll(roll[0], roll[1])

            
            # any bonuses?
            for item_ent, (equip, bonus) in self.world.get_components(EquippedComponent, MeleeBonusComponent):
                # only add bonuses for items actually equipped by attacker
                if equip.owner == attacker_ID:
                    damage += bonus.bonus

            target_stats.hp -= damage

            # dead!
            if target_stats.hp <= 0:
                self.world.add_component(target_ID, DeadComponent())
                self.world.remove_component(ent, CombatComponent)

            # message
            attacker_name = self.world.component_for_entity(attacker_ID, NameComponent)
            target_name = self.world.component_for_entity(target_ID, NameComponent)

            # color
            player_hit = self.world.has_component(target_ID, Player)
            if player_hit:
                color = (255, 0, 0)
            else:
                color = (127, 127, 127) # libtcod light gray
                

            game_vars.messages.append((attacker_name.name + " attacks " + target_name.name + " for " + str(damage) + " damage!", color))