import math
from .. import esper

from ..components.combat_component import CombatComponent
from ..components.combat_stats import StatsComponent
from ..components.name_component import NameComponent
from ..components.dead_component import DeadComponent
from ..components.player import Player

from ..components.faction_component import FactionComponent
from ..components.equipped import EquippedComponent
from ..components.weapon import WeaponComponent
from ..components.melee_bonus_component import MeleeBonusComponent
from ..components.attributes_component import AttributesComponent
from ..components.skills_component import SkillsComponent

from .. import game_vars
from .. import random_utils

def get_faction_reaction(faction, target_faction):
    #print("Faction reaction check: " + faction + " " + target_faction)
    for fact in game_vars.factions:
        #print(fact)
        if fact[0] == faction and fact[1] == target_faction:
            print("Faction reaction of " + fact[0] + " to " + fact[1] + " is " + str(fact[2]))
            return fact[2]


'''
Makes a skill test for "skill", where "skill" is a string
'''
def skill_test(skill, ent, world):
    sk = getattr(world.component_for_entity(ent, SkillsComponent), skill)
    game_vars.messages.append(("Making a test for " + skill + " " + str(sk), (0, 255, 0)))
    result = random_utils.roll(1, 100)
    player = world.has_component(ent, Player)
    if result < sk:
        if player:
            # check how much we gain in the skill
            tick = random_utils.roll(1, 100)

            # roll OVER the current skill
            if tick > getattr(world.component_for_entity(ent, SkillsComponent), skill):

                # +1d4 if we succeeded
                gain = random_utils.roll(1, 4)
                setattr(world.component_for_entity(ent, SkillsComponent), skill, getattr(world.component_for_entity(ent, SkillsComponent), skill) + gain)

                game_vars.messages.append(("You gain " + str(gain) + " skill points!", (115, 255, 115))) # libtcod light green

            else:
                # +1 if we didn't
                setattr(world.component_for_entity(ent, SkillsComponent), skill, getattr(world.component_for_entity(ent, SkillsComponent), skill) + 1)
                game_vars.messages.append(("You gain 1 skill point", (115, 255, 115)))
        return True
    else:
        if player:
            # if we failed, the check for gain is different
            tick = random_utils.roll(1,100)

            # roll OVER the current skill
            if tick > sk:
                # +1 if we succeeded, else nothing
                setattr(world.component_for_entity(ent, SkillsComponent), skill, getattr(world.component_for_entity(ent, SkillsComponent), skill) + 1)
                game_vars.messages.append(("You learn from your failure and gain 1 skill point", (115, 255, 115))) # libtcod light green

        return False


class CombatProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        #print("Combat processor...")
        for ent, (com) in self.world.get_component(CombatComponent):
            attacker_ID = ent
            # if dead, you don't get a last swing
            if self.world.has_component(ent, DeadComponent):
                return

            target_ID = self.world.component_for_entity(attacker_ID, CombatComponent).target_ID

            attacker_faction = self.world.component_for_entity(attacker_ID, FactionComponent).faction
            target_faction = self.world.component_for_entity(target_ID, FactionComponent).faction

            if attacker_faction == target_faction:
                # same faction, don't attack
                return

            # are we enemies?
            is_enemy_faction = get_faction_reaction(attacker_faction, target_faction) < 0
            if is_enemy_faction:
                print ("Target faction " + target_faction + " is enemy!")

                # message
                attacker_name = self.world.component_for_entity(attacker_ID, NameComponent)
                target_name = self.world.component_for_entity(target_ID, NameComponent)

                # roll attack
                attack_roll = random_utils.roll(1, 100)
                attack_skill = self.world.component_for_entity(attacker_ID, SkillsComponent).melee

                # d100 roll under
                if skill_test("melee", attacker_ID, self.world):
                #if attack_roll < attack_skill:
                    # target hit!
                    # assume target can try to dodge
                    if skill_test("dodge", target_ID, self.world):
                        game_vars.messages.append((target_name.name + " dodges!", (0, 191, 0))) # libtcod dark green
                    else:
                        # no dodge
                        attacker_stats = self.world.component_for_entity(attacker_ID, StatsComponent)
                        target_stats = self.world.component_for_entity(target_ID, StatsComponent)
                        # deal damage!
                        
                        # if no weapon, deal 1d6
                        roll = (1,6)
                        # use equipped weapon's data
                        for item_ent, (equip, weapon) in self.world.get_components(EquippedComponent, WeaponComponent):
                            #print(str(equip.slot))
                            if equip.owner == attacker_ID and equip.slot == "MAIN_HAND":
                                print("Use weapon dice")
                                roll = (weapon.num_dice, weapon.dam_dice)

                        # deal damage!
                        damage = random_utils.roll(roll[0], roll[1])

                        # Strength bonus
                        attacker_attributes = self.world.component_for_entity(attacker_ID, AttributesComponent)
                        str_bonus = int(math.floor(((attacker_attributes.strength - 10) / 2)))

                        damage = damage + str_bonus
                        # prevent negative damage
                        damage = max(0, damage)
                        
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

                        # color
                        player_hit = self.world.has_component(target_ID, Player)
                        if player_hit:
                            color = (255, 0, 0)
                        else:
                            color = (127, 127, 127) # libtcod light gray
                            

                        game_vars.messages.append((attacker_name.name + " attacks " + target_name.name + " for " + str(damage) + " (" + str(str_bonus) + " STR) damage!", color))
                else:
                    # miss
                    game_vars.messages.append((attacker_name.name + " attacks " + target_name.name + " but misses!", (115, 115, 255))) # libtcod light blue