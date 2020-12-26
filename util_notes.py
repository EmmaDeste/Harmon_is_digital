import random
partition1 = "SOLc p Zc SOLn LAn SOLn DOn Zc SIb"


def partition_to_noteduree(partition):
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


def noteduree_to_partition(note_c: list, duree_c: list ) -> list:
    partition_l = ""
    dico_n = {0: "DO", 2: "RE", 4: "MI", 5: "FA", 7: "SOL", 9: "LA", 11: "SI", -1: "Z"}
    dico_d = {2: "c ", 3: "c p ", 4: "n ", 6: "n p ", 8: "b ", 12: "b p ", 16: "r ", 24: "r p "}
    for i in range(len(note_c)):
        nc = note_c[i]
        dc = duree_c[i]
        partition_l += dico_n[nc] + dico_d[dc]
    return partition_l[:-1] #-1 pour enlever l'espace final



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


def creation_partition(l: list):
    occurs_DO = 0
    occurs_RE = 0
    occurs_MI = 0
    occurs_FA = 0
    occurs_SOL = 0
    occurs_LA = 0
    occurs_SI = 0
    occurs_Z = 0
    succ_do = []
    succ_re = []
    succ_mi = []
    succ_fa = []
    succ_sol = []
    succ_la = []
    succ_si = []
    succ_z = []
    duree = []
    for t in l:
        print(t)
        """
        for i in range(len(l)):
            if l[i] == 0:
                occurs_DO += 1
                succ_do.append(l[i + 1])
            if l[i] == 2:
                occurs_RE += 1
                succ_re.append(l[i + 1])
            if l[i] == 4:
                occurs_MI += 1
                succ_mi.append(l[i + 1])
            if l[i] == 5:
                occurs_FA += 1
                succ_fa.append(l[i + 1])
            if l[i] == 7:
                occurs_SOL += 1
                succ_sol.append(l[i + 1])
            if l[i] == 9:
                occurs_LA += 1
                succ_la.append(l[i + 1])
            if l[i] == 11:
                occurs_SI += 1
                succ_si.append(l[i + 1])
            if l[i] == -1:
                occurs_Z += 1
                succ_z.append(l[i + 1])"""
    dico_no = {occurs_DO: succ_do, occurs_RE: succ_re, occurs_MI: succ_mi, occurs_FA: succ_fa, occurs_SOL: succ_sol, occurs_LA: succ_la, occurs_SI: succ_si, occurs_Z: succ_z}
    first_note = max([occurs_DO, occurs_RE, occurs_MI, occurs_FA, occurs_SOL, occurs_LA, occurs_SI, occurs_Z])
    partition = []
    y = 0
    m = dico_no[first_note]
    while y < 25:
        m += random.choice([m])
        partition.append(m)
        y += 1
    return partition




b = 5
l = [0, 9, 2, 11, 7, 9, 5, 4]
#print(transposition(l,b))
#print(inversion(l))
(n,d) = partition_to_noteduree(partition1)
#print(n, d)
#print(frequences(n))
#print(creation_partition(l))
#p = creation_partition(l)
#print(p)
s = noteduree_to_partition(n, d)
print(s)
print(partition_to_noteduree(s))
