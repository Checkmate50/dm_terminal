from src.util import roll
from src.battle_help import gen_attack


class Creature:
    def __init__(self, name, level, hp_base, s, d, con, w, i, cha, base_ac=10):
        self.name = name
        self.level = level
        self.hp_base = hp_base
        self.str = s
        self.dex = d
        self.con = con
        self.wis = w
        self.int = i
        self.cha = cha
        self.base_ac = base_ac
        self.ac = base_ac + modifier(self.dex)
        self.prof_bonus = self.level // 4 + 1
        self.attacks = []

        hp_rolls = sum([roll(1, self.hp_base) for _ in range(self.level - 1)])
        con_modifier = modifier(self.con) * self.level
        self.max_health = self.hp_base + hp_rolls + con_modifier
        self.health = self.max_health
        self.initiative = -1

    def roll_initiative(self):
        self.initiative = roll(1, 20) + self.dex

    def attack(self, ac, index=1):
        return self.attacks[index](ac)

    def attribute_roll(self, attribute):
        return roll(1, 20) + modifier(self.get_attribute(attribute))

    def saving_throw(self, attribute):
        return self.attribute_roll(attribute) + self.prof_bonus

    def add_attack(self, damage, attribute="str", count=1):
        self.attacks.append(self.__def_attack(attribute, damage, count))

    def set_attack(self, index, damage, attribute="str", count=1):
        self.attacks[index] = self.__def_attack(attribute, damage, count)

    def modify_attack(self, index, damage, attribute="str", count=1):
        self.attacks[index] = self.__def_attack(attribute, damage, count)

    def __def_attack(self, attribute, damage, count):
        att = self.get_attribute(attribute)
        att_mod = att + self.prof_bonus
        return gen_attack(att_mod, damage, att, count)

    def get_attribute(self, attribute):
        if attribute == "strength" or attribute == "str" or attribute == "s":
            return self.str
        if attribute == "dexterity" or attribute == "dex" or attribute == "d":
            return self.str
        if attribute == "constitution" or attribute == "con":
            return self.str
        if attribute == "wisdom" or attribute == "wis" or attribute == "w":
            return self.str
        if attribute == "intelligence" or attribute == "int" or attribute == "i":
            return self.str
        if attribute == "charisma" or attribute == "cha":
            return self.str
        raise ValueError("Unknown attribute " + attribute)


def modifier(score):
    if score < 0 or score > 30:
        raise ValueError("Cannot have an attribute score of " + str(score))
    return score // 2 - 5
