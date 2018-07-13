"""
Outputs the number of ingrediants with each property
Written by Dietrich Geisler
"""
import sys


def parse_types():
    table = open("Types.txt")
    to_return = [["Type", "I", "II", "III", "IV", "Total"]]
    for item in table:
        item = item.strip()
        to_return.append([item.split("\t")[1].strip(), 0, 0, 0, 0, 0])  # organization is [name, I, II, III, IV]
    table.close()
    return to_return


def find_type(table, type):
    for i in range(len(table)):
        if table[i][0] == type:
            return i
    print(type + " not found")


def parse_ingredients(types):
    table = open("Ingredients.txt", 'r')
    for item in table:
        temp = item.split("\t")
        while len(temp) > 13:
            temp.pop()
        temp.pop(0)  # remove name
        level = 1
        for i in range(len(temp)):
            temp[i] = temp[i].strip()
            if temp[i] != "N":
                j = find_type(types, temp[i])
                types[j][level] += 1
                types[j][-1] += 1
            if i == 1 or i == 5 or i == 9:
                level += 1
    table.close()
    return types


def print_counts(counts):
    s = ""
    for row in counts:
        for item in row:
            s += str(item) + "\t"
        s = s.strip()
        s += "\n"
    s = s.strip()
    f = open("Counts.txt", 'w')
    f.write(s)
    f.close()


def main():
    print_counts(parse_ingredients(parse_types()))


if __name__ == "__main__":
    main()
