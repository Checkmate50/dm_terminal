"""
Simple script which generates the types of potions created from a list of ingredients
Input is simply a txt file.  Alternatively, change the definition of item_list (~line 135)
Written by Dietrich Geisler
"""
import sys

RANGES = [[0, 2], [2, 6], [6, 10], [10, 12]]


class Type:
    def __init__(self, name, value):
        self.name = name.strip()
        self.value = value
        self.count = 1

    def active(self):
        if self.value == 4:
            return self.count >= 2
        return self.count >= self.value

    def increment(self):
        self.count += 1

    def compare(self, name, value):
        return self.name == name and self.value == value

    def __str__(self):
        val = "I" * self.value
        if self.value == 4:
            val = "IV"
        return self.name + " " + val

    def __repr__(self):
        return self.__str__()


class Ingredient:
    # types should be an array of 12 strings
    def __init__(self, name, types):
        self.name = name
        self.types = []
        for i in range(len(RANGES)):
            for t in types[RANGES[i][0]: RANGES[i][1]]:
                self.types.append(Type(t, i + 1))

    # ingredients should be a (possibly empty) array of ingredients
    def combine(self, ingredients):
        for i in self.types:
            found = False
            n = i.name
            if n.lower() == "n":
                continue
            v = i.value
            for j in ingredients:
                if j.compare(n, v):
                    j.increment()
                    found = True
                    break
            if found == False:
                ingredients.append(i)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Potion:
    # ingredients should be a nx12 string matrix
    def __init__(self, ingredients):
        self.types = []
        self.type_codes = []
        for i in ingredients:
            i.combine(self.types)
        self.gen_active_array()
        t = open("Types.txt", 'r')
        for line in t:
            self.type_codes.append(line.strip().split("\t"))

    def gen_active_array(self):
        self.active = []
        for i in self.types:
            max = True
            if not i.active():
                continue
            for j in self.types:
                if j.active() and j.name == i.name and j.value > i.value:
                    max = False
                    break
            if max:
                self.active.append(i)

    def code(self):
        to_return = ""
        for i in self.active:
            for j in self.type_codes:
                if i.name.lower() == j[1].lower():
                    to_return += str(int(j[0]) + i.value - 1) + "-"
                    break
        return to_return[:-1]

    def __str__(self):
        if len(self.active) == 0:
            return "nothing"
        to_return = ""
        for i in self.active:
            to_return += str(i) + "\n"
        to_return += self.code()
        return to_return


# Parses the 'items' from the given chemistry table
def parse_table(items):
    table = open("Ingredients.txt", 'r')
    to_return = []
    found = []
    for item in table:
        temp = item.split("\t")
        found.append(temp[0].lower().strip())
        if temp[0].lower() in items:
            to_return.append(Ingredient(temp[0], temp[1:14]))

    for ingr in items:
        if ingr not in found:
            print("Warning: the ingredient " + ingr + " was not found.")
    return to_return


def main():
    item_list = ["pheonix juniper", "fieldcress"]

    if len(sys.argv) > 1:
        item_list = []
        list = open(sys.argv[1], 'r')
        for item in list:
            item_list.append(item.strip().lower())

    print(Potion(parse_table(item_list)))


if __name__ == "__main__":
    main()
