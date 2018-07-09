from math import *
from functools import partial
import random


def sp(d):
    print("%e" % d)


def ln(x):
    return log(x)


def quad(a, b, c):
    val = sqrt(b ** 2 - 4 * a * c)
    return (-b - val) / (2 * a), (-b + val) / (2 * a)


def roll(count, sides, verbose=False):
    rolls = [random.randint(1, sides) for _ in range(count)]
    if verbose:
        return rolls
    return sum(rolls)


def gen_roll(count, sides):
    return partial(roll, count, sides, False)


def str_to_data(s):
    try:
        return int(s)
    except e:
        pass
    try:
        return float(s)
    except e:
        pass
    return s


def read_csv(filename):
    with open(filename) as f:
        return [str_to_data(line.strip().split(",")) for line in f]
