import bisect
import random

# create actual random tables
def generate_NPC_rarity():
    chances = []

    chances.append(("Human", 80))
    chances.append(("Cop", 20))

    return get_chance_roll_table(chances)

def generate_item_rarity():
    chances = []

    chances.append(("Pistol", 25))
    chances.append(("Medkit", 50))
    chances.append(("Grenade", 15))

    return get_chance_roll_table(chances)


# ... and use them
def generate_random_NPC():
    NPC_chances = generate_NPC_rarity()
    d100 = roll(1, 100)

    #print "Rolled " + str(d100) + " on random monster gen table"
    res = get_result(d100, NPC_chances)
    print("Random NPC is " + res)

    return res

def generate_random_item():
    item_chances = generate_item_rarity()

    d100 = roll(1, 100)

    #print "Rolled " + str(d100) + " on random monster gen table"
    res = get_result(d100, item_chances)
    print("Random item is " + res)

    return res

# helpers
def roll(dice, sides):
    result = 0

    for _ in range(0, dice, 1):
        # a <= N <= b
        roll = random.randint(1, sides)
        result += roll

    print('Rolling ' + str(dice) + "d" + str(sides) + " result: " + str(result))

    return result

def get_chance_roll_table(chances, pad=True):
    num = 0
    chance_roll = []

    for chance in chances:
        old_num = num + 1
        num += 1 + chance[1]

        # clip top number to 100
        if num > 100:
            num = 100

        chance_roll.append((chance[0], old_num, num))

    if pad:
        # pad out to 100
        print("Last number is " + str(num))
        chance_roll.append(("None", num, 100))

    return chance_roll

def get_result(roll, table):
    breakpoints = [k[2] for k in table if k[2] < 100]
    breakpoints.sort()

    print(breakpoints)

    i = bisect.bisect(breakpoints, roll)
    res = table[i][0]

    return res