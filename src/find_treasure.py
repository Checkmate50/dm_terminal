"""
Generates the treasure found by a DnD 5e group
Takes 2-3 arguments: [party_level, type_of_hoard, specific_type]
Where party_level is the converted level of the party (0 < party_level < 20)
type_of_hoard of hoard is between 0 and 5 (see help dialog for details)
and specific_type is an optional string indicating the kind of item you want to generate

Written by Dietrich Geisler
"""

# from potion import *
import sys
import random

random.seed()


# level > 0
def gen_rarity(level):
    unchecked = []
    to_return = []
    for i in range(1, min(4, level) + 1):
        temp = rarity_recursive(level, i, i)
        for j in temp:
            j.append(i)
            unchecked.append(j)
    if level < 6:
        unchecked.append([level])
    for i in unchecked:
        if len(i) <= 4:
            to_return.append(i)
    return to_return


def rarity_recursive(level, m, u):
    to_return = []
    i = 1
    for i in range(1, min(u, level - m) + 1):
        temp = rarity_recursive(level, i + m, i)
        for j in temp:
            j.append(i)
            to_return.append(j)
    if i + m == level:
        to_return.append([i])
    return to_return


def gen_potion(level):
    f = open("types.txt", 'r')
    types = []
    for i in f:
        item = i.strip().split("\t")
        types.append(item[1])
    f.close()
    ing = []
    rares = gen_rarity(level + 1)
    rarities = rares[random.randint(0, len(rares) - 1)]
    s = ""
    for i in rarities:
        s += types.pop(random.randint(1, len(types) - 1))
        s += " " + ("IV" if i == 4 else "I" * int(i)) + "\n"
    return s.strip()


def spell_level(level):
    l = level.lower().strip()
    if l == "c":
        return "Cantrip"
    if l == "1":
        return "1st Level"
    if l == "2":
        return "2nd Level"
    if l == "3":
        return "3rd Level"
    return l + "th Level"


def gen_scroll(level):
    if random.random() < .5:
        level -= 1
    if level > 9:
        level = 9
    dc = str([13, 13, 13, 15, 15, 17, 17, 18, 18, 19][level])
    att = ["+5", "+5", "+5", "+7", "+7", "+9", "+9", "+10", "+10", "+11"][level]
    level = str(level)
    if level == "0":
        level = "c"
    f = open("spells.txt")
    spells = []
    for s in f:
        l = s.split()
        if l[1].lower().strip() == level:
            spells.append(l[0] + "\t" + spell_level(l[1]))
    if level == "c":
        level = 1
    level = 2 * int(level) - 1
    return "Scroll of " + spells[random.randint(0, len(spells) - 1)] + "\nLevel: " + str(
        level) + "\tSave DC " + dc + "\tAttack Bonus " + att


def gen_treasure(level, gp_mult):
    level = int(((level + 1) / 2))
    treasure = []
    r = level ** 4 * (random.random() * .2 + 1)
    treasure.append(str(int(r * gp_mult)) + " gp")
    return treasure


def gen_magic(level, artifacts, hoard, item):
    level = int(((level + 1) / 2)) - 2
    arts = []
    for i in range(4):
        for j in range(hoard[i]):
            if item == "potion" or (item == "" and random.random() < (.01) * (9 - level + i)):
                # Add a potion of appropriate level to the list
                arts.append("Potion:\n" + gen_potion(level + i))
            elif item == "scroll" or (
                    item == "" and random.random() < .25):  # Note that this is a separate random number!!!
                # Add a scroll of appropriate level to the list
                arts.append("Scroll:\n" + gen_scroll(level + i))
                if level + i > 1:
                    arts.append("Scroll:\n" + gen_scroll(level + i - 1))
            else:
                if len(artifacts[i]) == 0:
                    arts.append("Nothing")
                    continue
                artifact = artifacts[i][random.randint(0, len(artifacts[i]) - 1)]
                att = "\n(Requires Attunement)" if artifact[3] == "y" else ""
                arts.append(
                    "Artifact:\n" + artifact[0] + "\n" + "Level: " + str(2 * (level + i) - 1) + "\tValue: " + artifact[
                        1] + "\tDMG: " + artifact[-1] + att)
    return arts


def print_treasure(treasure, artifacts):
    print("\n\033[4mTreasure\033[0m\n")
    for t in treasure:
        print(t)
    print("\n\033[4mMagic Items\033[0m\n")
    if len(artifacts) == 0:
        print("None")
        return
    i = 1
    for a in artifacts:
        print(str(i) + ". " + a + "\n")
        i += 1


# Parses the artifacts of appropriate levels from the artifact table
# Assumes that the artifact table is sorted by level
def parse_artifacts(table, level, item):
    if item == "potion" or item == "scroll":
        return []
    to_return = []
    temp_level = level - 4
    for i in range(4):
        temp = []
        to_return.append(temp)
    i = 0
    for art in table:
        artifact = art.split("\t")
        if int(artifact[2]) < temp_level:
            continue
        while int(artifact[2]) > temp_level:
            i += 1
            temp_level += 2
        if i == 4:
            break
        if item != "" and artifact[-2].lower().strip() != item:
            continue
        artifact[-1] = artifact[-1].lower().strip()  # Remove newline char
        to_return[i].append(artifact)

    return to_return


def parse_hoard(table, level):
    to_return = []
    for item in table:
        items = item.split("\t")
        items[-1] = items[-1].strip()
        items[0] = float(items[0])
        for i in range(1, len(items)):
            items[i] = int(items[i])
        if level == 1 and items[2] > 0:
            continue
        if level <= 3 and items[1] > 0:
            continue
        if level == 19 and items[4] > 0:
            continue
        to_return.append(items)
    return to_return[random.randint(0, len(to_return) - 1)]


def help():
    print("Give the party level and hoard type")
    print("The party level must be between 1 and 20")
    print("The hoard level must be between 0 and 5, each of which correspond to the following")
    print("0- single item of appropriate level")
    print("1- minor loot drop")
    print("2- small treasure chest")
    print("3- large treasure chest")
    print("4- small hoard / major loot drop")
    print("5- large/epic hoard")
    print("Optional: request a specific type of artifact (including scroll or potion")
    exit()


def main():
    # Read in command line arguments
    if len(sys.argv) < 3:
        help()
    level = int(sys.argv[1])
    hoard = int(sys.argv[2])
    if level < 0 or level > 20:
        print("0 < party_level < 21")
        exit(0)
    if not hoard in [*range(6)]:
        print("type_of_hoard must be 1, 2, 3, 4, or 5")
        exit(0)
    item = ""
    if len(sys.argv) == 4:
        item = sys.argv[3].lower().strip()

    level += (level % 2) - 1
    artifacts = parse_artifacts(open("artifacts.txt"), level, item)

    f = open("hoard_table_" + str(hoard) + ".txt")
    hoard = parse_hoard(f, level)
    print_treasure(gen_treasure(level, hoard[0]), gen_magic(level, artifacts, hoard[1:], item))


if __name__ == "__main__":
    main()
