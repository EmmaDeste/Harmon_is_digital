#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

partition1 = "SOLc p Zc SOLn LAn SOLn DOn Zc SIb"


def partition_to_noteduree(partition):
    """

    :param partition: partition en toutes lettres à transformer
    :return: les notes et les durées sous forme de chiffres et séparées
    """
    l = partition.split(' ')
    n = []
    d = []
    dico_n = {"DO": 0, "DOD":1, "RE": 2, "RED":3, "MI": 4,
              "FA": 5, "FAD": 6, "SOL": 7, "SOLD": 8, "LA": 9, "LAD": 10, "SI": 11, "Z": -1, "": -2}
    dico_d = {"c": 2, "n": 4, "b": 8, "r": 16}
    for x in l:
        note = ""
        duree = ""
        for y in x:
            if 'A' <= y <= 'Z':
                note = note + y
            else:
                duree = duree + y
        n.append(note)
        d.append(duree)
    nc = []
    for s in n:
        if dico_n[s] > -2:
            nc.append(dico_n[s])
    print("nc=", nc)
    dc = []
    for s in d:
        if s == "p":
            dc[-1] += dc[-1] // 2
        else:
            dc.append(dico_d[s])
    print("dc=", dc)
    return (nc, dc)


def noteduree_to_partition(note_c: list, duree_c: list) -> list:
    """

    :param note_c: liste des notes chiffrées
    :param duree_c: liste des durées chiffrées
    :return: partition lettrée
    """
    partition_l = ""
    dico_n = {0: "DO", 1: "DOD", 2: "RE", 3: "RED", 4: "MI",
              5: "FA", 6: "FAD", 7: "SOL", 8: "SOLD", 9: "LA", 10: "LAD", 11: "SI", -1: "Z"}  #D for dièse
    dico_d = {2: "c ", 3: "c p ", 4: "n ", 6: "n p ", 8: "b ", 12: "b p ", 16: "r ", 24: "r p "}
    for i in range(len(note_c)):
        nc = note_c[i]
        dc = duree_c[i]
        print("nc= ",nc, " dc= ",dc)
        partition_l += dico_n[nc] + dico_d[dc]
    return partition_l[:-1]  # -1 pour enlever l'espace final


def transposition(p, k):
    """
    :param p: partition
    :param k: nombre de demi-ton duquel transposé
    :return: partition transposée
    """
    t = []
    for i in range(len(p)):
        if p[i] < 0:
            a = p[i]
        else:
            a = (p[i] + k) % 12
        t.append(a)
    return t


def inversion(p):
    """

    :param p: partition à inverser
    :return: partition inversée
    """
    i = []
    for y in range(len(p)):
        if p[y] < 0:
            a = p[y]
        else:
            a = (12 - p[y]) % 12
        i.append(a)
    return i


def frequences(l):
    """

    :param l: list des notes chiffrées
    :return: listes des fraquences à jouer
    """
    f = []
    dico_f = {-1: -1, 0: 264, 1: 281.6, 2: 297, 3: 316.8, 4: 330, 5: 352, 6: 375.5, 7: 396, 8: 422.4, 9: 440,
              10: 469.33, 11: 495}
    for s in l:
        f.append(dico_f[s])
    return f


def creation_duree_v2(l : list):
    """

    :param l: collection of song (tuples: title/partition)
    :return: new partition of time
    """
    occurs_c = 0
    occurs_cp = 0
    occurs_n = 0
    occurs_np = 0
    occurs_b = 0
    occurs_bp = 0
    occurs_r = 0
    occurs_rd = 0
    succ_c = []
    succ_cp = []
    succ_n = []
    succ_np = []
    succ_b = []
    succ_bp = []
    succ_r = []
    succ_rp = []
    occur = [0] * 25  # https://stackoverflow.com/questions/8528178/list-of-zeros-in-python
    succ = []
    for i in range(25):
        succ.append([])
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(dc)):
            duree = dc[i]
            if duree >= 0:
                occur[duree] += 1
        for i in range(len(dc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            duree = dc[i]
            suiv = dc[i + 1]
            if duree >= 0 and suiv >= 0:
                succ[duree].append(suiv)
    print("occur =", occur)
    print("succ = ", succ)
    y = 0
    max_occurence = max(occur)
    index = 0
    found = False
    while index < len(occur) and found == False:
        if occur[index] == max_occurence:
            found = True
            i = index
        else:
            index += 1
    print("max_occurence = ", max_occurence)  # trouver indice de la note qui apparait le plus
    m = i
    partition = [m]
    while y < 25:
        m = random.choice(succ[m])
        partition.append(m)
        y += 1
    return partition


def creation_partition_v2(l: list):
    """

    :param l: collection of song (tuples : title/partition
    :return: new partition of note
    """
    global i
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
    occur = [0] * 12  # https://stackoverflow.com/questions/8528178/list-of-zeros-in-python
    succ = []
    for i in range(12):
        succ.append([])
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(nc)):
            note = nc[i]
            if note >= 0:
                occur[note] += 1
        for i in range(len(nc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            note = nc[i]
            suiv = nc[i + 1]
            if note >= 0 and suiv >= 0:
                succ[note].append(suiv)
    print("occur =", occur)
    print("succ = ", succ)
    y = 0
    max_occurence = max(occur)
    index = 0
    found = False
    while index < len(occur) and found == False:
        if occur[index] == max_occurence:
            found = True
            i = index
        else:
            index += 1
    print("max_occurence = ", max_occurence)  # trouver indice de la note qui apparait le plus
    m = i
    partition = [m]
    while y < 25:
        m = random.choice(succ[m])
        partition.append(m)
        y += 1
    return partition

def creation_partition_v1(l : list):
    """

    :param l: collection of songs (tuples : title/partition)
    :return: new partition of note
    """
    first = [0, 2, 4, 5, 7, 8, 11]
    succ_do = []
    succ_re = []
    succ_mi = []
    succ_fa = []
    succ_sol = []
    succ_la = []
    succ_si = []
    succ_z = []
    succ = []
    for i in range(12):
        succ.append([])
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(nc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            note = nc[i]
            suiv = nc[i + 1]
            if note >= 0 and suiv >= 0:
                succ[note].append(suiv)
    print("succ = ", succ)
    y = 0
    m = random.choice(first)
    partition = [m]
    while y < 25:
        m = random.choice(succ[m])
        partition.append(m)
        y += 1
    return partition

def creation_duree_v1(l : list):
    """

    :param l: collection of songs (tuples: title/partition)
    :return: new partition of time
    """
    first = [2, 3, 4, 6, 8, 12, 16, 24]
    succ_c = []
    succ_cp = []
    succ_n = []
    succ_np = []
    succ_b = []
    succ_bp = []
    succ_r = []
    succ_rp = []
    succ = []
    for i in range(25):
        succ.append([])
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(nc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            duree = dc[i]
            suiv = dc[i + 1]
            if duree >= 0 and suiv >= 0:
                succ[duree].append(suiv)
    print("succ = ", succ)
    y = 0
    m = random.choice(first)
    partition = [m]
    while y < 25:
        m = random.choice(succ[m])
        partition.append(m)
        y += 1
    return partition



b = 5
l = [0, 9, 2, 11, 7, 9, 5, 4]
# print(transposition(l,b))
# print(inversion(l))
(n, d) = partition_to_noteduree(partition1)
# print(n, d)
# print(frequences(n))
# s = noteduree_to_partition(n, d)
# print(s)
# print(partition_to_noteduree(s))


