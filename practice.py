




budget = 60
keys = [10, 20, 30, 40, 50]
drives = [1, 2, 3, 4, 5]



def getMoneySpent(keyboards, drives, budget):
    max_spent = -1
    for keyboard in keys:
        for drive in drives:
            if keyboard + drive <= budget:
                max_spent = max(max_spent, keyboard + drive)
    return max_spent

print(getMoneySpent(keys, drives, budget))




def kangaroo(x1, v1, x2, v2):
    if x1 == x2:
        return "YES"
    if x1 < x2 and v1 < v2:
        return "NO"
    if x1 > x2 and v1 > v2:
        return "NO"
    return kangaroo(x1 + v1, v1, x2 + v2, v2)

print(kangaroo(0, 3, 4, 2))




def gridSearch(G, P):
    for i in range(len(G) - len(P) + 1):
        for j in range(len(G[0]) - len(P[0]) + 1):
            if G[i][j:j+len(P[0])] == P[0]:
                return "YES"
    return "NO"


