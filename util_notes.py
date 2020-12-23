partition1 = "SOLc p Zc SOLn LAn SOLn DOn Zc SIb"



def transformation(partition):
    L = partition.split(' ')
    N = []
    D = []
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

def transposition(p, k):
    """
    :param p: partition
    :param k: nombre de demi-ton duquel transposé
    :return: partition transposée
    """
    t = []
    for i in range(len(p)):
        if p[i]<0 :
            a = p[i]
        else:
            a = (p[i] + k) % 12
        t.append(a)
    return t


def inversion(p):
    i = []
    for y in range(len(p)):
        if p[y]<0 :
            a = p[y]
        else:
            a = (12 - p[y]) %12
        i.append(a)
    return i


def frequences(l):
    f = []
    dico_f={-1: -1, 0: 264, 1: 281.6,2: 297,3: 316.8,4: 330,5:352 ,6: 375.5,7: 396,8: 422.4,9: 440,10: 469.33,11: 495}
    for s in l:
        f.append(dico_f[s])
    return f


b = 5
l = [0, 1, 3, 9, 2, 11, 4, 10, 7, 8, 5, 6]
print(transposition(l,b))
print(inversion(l))
(n,d)=transformation(partition1)
print(n, d)
print(frequences(n))
