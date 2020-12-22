partition1 = "SOLc p Zc SOLn LAn SOLn DOn Zc SIb"
partition = partition1.split(' ')
Note = []
Duree = []

def transformation(L, N, D: list):
    dico_n = {"DO": 0, "RE": 2, "MI": 4, "FA": 5, "SOL": 7, "LA": 9, "SI": 11, "Z": -1, "": -2}
    dico_d = {"c": 2, "n": 4, "b": 8, "r": 16}
    for x in L:
        note = ""
        duree = ""
        for y in x:
            if 'A' <= y <= 'Z':
                note = note + y
            else:
                duree = duree + y
        N.append(note)
        D.append(duree)
    nc = []
    for s in N:
        if dico_n[s] > -2:
            nc.append(dico_n[s])
    print("nc=", nc)
    dc = []
    for s in D:
        if s == "p":
            dc[-1] += dc[-1]//2
        else:
            dc.append(dico_d[s])
    print("dc=", dc)
    return (nc, dc)



print(transformation(partition, Note, Duree))