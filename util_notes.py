#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project: Harmony is digital
Authors: Capucine Foucher and Emma Desté
Promo: EFREI 2025
Role: this is the file containing :
- decode and encode partition,
- associate frequencies to notes,
- transposition,
- inversion,
- creation of new songs using Markov chains
"""

import random

partition1 = "SOLc p Zc SOLn LAn SOLn DOn Zc SIb"

#Emma : fonction calc_duration(figures, d0) qui prend en entrée la liste des 4 figures et la durée de la croche d0. Elle calcule les durées des autres figures et retourne un dictionnaire associant à chaque figure une durée.??

def partition_to_noteduree(partition):  #Emma : Une fonction read_sheet qui à partir d’une ligne du fichier extrait les notes, les figures, les silences et les points de prolongation et construit une séquence de fréquences et de durée qu’elle retourne en sortie.??
    """
    Encode a partition to notes numbers and duration numbers
    :param str partition: partition en toutes lettres à transformer
    :return: les notes et les durées sous forme de chiffres et séparées
    :rtype: tuple (notes numbers, duration numbers)
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
    dc = []
    for i in range(len(n)):
        sn = n[i]
        sd = d[i]
        if sd == 'p' and dc!=[]:
            dc[-1] += dc[-1] // 2
        else:
            if sn in dico_n and sd in dico_d:
                nc.append(dico_n[sn])
                dc.append(dico_d[sd])
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
        partition_l += dico_n[nc] + dico_d[dc]
    return partition_l[:-1]  # -1 pour enlever l'espace final


def transposition(p, k):
    """
    :param p: partition
    :param k: number of semitones from which transpose
    :return: transposed partition
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

    :param p: partition to inverse
    :return: inversed partition
    """
    i = []
    for y in range(len(p)):
        if p[y] < 0:
            a = p[y]
        else:
            a = (12 - p[y]) % 12
        i.append(a)
    return i


def frequences(l):   #Emma : est-ce qu'on remplace par la fonction calc_frequency(notes, frequences) qui prend en entrée une liste de notes et une liste de fréquences et qui retourne une variable de type dictionnaire associant à chaque note une fréquence ??
    """

    :param l: list of notes in number form
    :return: list of frequences to play
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
    first = set()
    succ = []
    for i in range(12):
        succ.append(set())
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(nc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            note = nc[i]
            suiv = nc[i + 1]
            if note >= 0 and suiv >= 0:
                first.add(note)
                succ[note].add(suiv)
    print("succ = ", succ)
    y = 0
    m = random.choice(list(first))
    partition = [m]
    while y < 25:
        m = random.choice(list(succ[m]))
        partition.append(m)
        y += 1
    return partition

def creation_duree_v1(l : list):
    """

    :param l: collection of songs (tuples: title/partition)
    :return: new partition of time
    """
    first = set()
    succ = []
    for i in range(25):
        succ.append(set())
    for t in l:
        (titre, part) = t  # equivalent à part = t[1]
        (nc, dc) = partition_to_noteduree(part)
        for i in range(len(nc) - 1):  # -1 pour ne pas chercher le successeur de la derniere note
            duree = dc[i]
            suiv = dc[i + 1]
            if duree >= 0 and suiv >= 0:
                first.add(duree)
                succ[duree].add(suiv)
    print("succ = ", succ)
    y = 0
    m = random.choice(list(first))
    partition = [m]
    while y < 25:
        m = random.choice(list(succ[m]))
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


