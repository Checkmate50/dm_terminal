"""
Reads the given potion code
Written by Dietrich Geisler
"""
import sys

code = "61-17-24"
p = code.split("-")
if len(sys.argv) > 1:
	p = sys.argv
	p.pop(0)
	for i in range(len(p)):
		p[i] = int(p[i])

type_codes = []
t = open("Types.txt", 'r')
for line in t:
	type_codes.append(line.split())
	
comp = []
for i in p:
	mod = (int(i)%4)+1
	value = "I"*mod
	if mod == 4:
		value = "IV"
	i = str(int(i)-mod+1)
	name = ""
	for j in type_codes:
		if i == j[0]:
			name = j[1]
	comp.append(name + " " + value)
	
for i in comp:
	print(i)