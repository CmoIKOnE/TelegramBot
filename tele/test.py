import re

a = [['петя',10,130,35], ['вася',11,135,39],['женя',9,140,33],['дима',10,128,30]]
 
n = input('Сортировать по имени (1), возрасту (2), росту (3), весу (4): ')
n = int(n)-1
t = input('По возрастанию (0), по убыванию (1): ')
t = int(t)
 
a.sort(key=lambda i: i[n], reverse=t)
 
for i in a:
    print("%7s %3d %4d %3d" % (i[0],i[1],i[2],i[3]))


"""L = []
a1 = []
with open("test.txt", "r") as f:
    for line in f:
    	if re.match(r'VISUAL')
        L.append(line)
for i in sorted(L):
    print(i.strip())"""