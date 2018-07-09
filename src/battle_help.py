from math import *
from functools import partial
from src.util import roll


def attack(att_mod, dmg, dmg_mod, ac, resist=False, count=1, adv=0):
    """
    int att_mod is the attack roll modifier
    <partial> dmg is the set of rolls for damage
    int dmg_mod is the damage modifier
    returns (damage, hit_count, crit_fail_count)
    """
    to_return = []
    for _ in range(count):
        att = roll(1, 20)
        if adv == 1:
            att = max(att, roll(1, 20))
        elif adv == 2:
            att = min(att, roll(1, 20))
        ar = att + att_mod
        damage = 0
        if att == 1:
            pass
        elif att == 20:
            damage = dmg() + dmg() + dmg_mod
        elif ar > ac:
            damage = dmg() + dmg_mod
        elif ar in (ac, ac - 1):
            damage = (dmg() + dmg_mod) / 2
        damage = ceil(damage / (2 if resist else 1))
        to_return.append((att, damage))
    return to_return


def gen_damage(rolls):
    return lambda: sum(map(lambda x: x(), rolls))


def gen_attack(att_mod, dmg, dmg_mod, c=1):
    return partial(attack, att_mod, dmg, dmg_mod, count=c)
