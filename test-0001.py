a = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e'}
b = {1:'a', 2:'b', 3:'c', 6:'f', 7:'g', 8:'h'}
c = {}

for i in a.keys():
    found = False

    for j in b.keys():
        if a.get(i) == b.get(j):
            found = True
            break

    if not found:
        print(a.get(i), "to be deleted.")
    else:
        c[i] = a[i]
        print(a.get(i), "to be remained.")

for j in b.keys():
    found = False

    for i in a.keys():
        if b.get(j) == a.get(i):
            found = True
            break
    
    if not found:
        print(b.get(j), "to be added.")
        c[j] = b[j]

print("after update:", c)