#!/usr/bin/python
# -*- coding: utf-8 -*-

from util_notes import *

import tkinter as tk
from tkinter import Canvas

import simpleaudio as sa
import simpleaudio.functionchecks as fc
import numpy as np
from numpy import pi

from math import sqrt
import re      #expression régulière pour nettoyer les caractères spéciaux (ici le retour à la ligne)

glob_racine = tk.Tk()
glob_instrum = tk.StringVar()
glob_inv=tk.StringVar()         #case inversion cochée ou non
glob_transpo = tk.StringVar()
# Creation des variables globales
glob_canvas1 = 0
glob_canvas2 = 0
glob_po = 0
glob_recueil=[]
glob_lbchanson = 0

def test_son_gauche_droite():
    '''test son des haut-parleurs droit puis gauche'''
    fc.LeftRightCheck.run()


def test_son_superposition():
    fc.OverlappingCheck.run()

def ajout_partition():
    pass

def existe_titre(titre):
    global glob_recueil
    for chanson in glob_recueil:
        if titre==chanson[0]:
            return True
    return False


def ajout_if_needed(chanson):
    global glob_recueil, glob_lbchanson
    (titre, part) = chanson
    if existe_titre(titre) == False :
        glob_recueil.append(chanson)
        glob_lbchanson.insert(tk.END, titre)  # tk.END est une constante définie qu'on ajoute à la fin d'une liste
        glob_lbchanson.select_clear(0, tk.END)   #pour déselectionner
        glob_lbchanson.select_set(tk.END)   #pour sélectionner le titre de la chanson en cours
    # TODO : vérifier si la chanson existe déjà, donc son titre
    # TODO : cohérence sur titre, chanson, partition
    #mise à jour de la liste des chansons


def ecrire_partition(partition):
    file=open("newpartitions.txt",'w') #'w' pour ouvert en écriture
    file.write(partition)
    file.close()


def chaine_de_makov_v1():
    print("Chaine de mrrkov v1")
    print(creation_partition_v1(glob_recueil))
    print(creation_duree_v1(glob_recueil))
    print(noteduree_to_partition(creation_partition_v1(glob_recueil), creation_duree_v1(glob_recueil)))

def chaine_de_makov_v2():
   print("chaine de markov v2")
   print(creation_duree_v2(glob_recueil))
   print(noteduree_to_partition(creation_partition_v2(glob_recueil), creation_duree_v2(glob_recueil)))

def vitesse():
    pass


def jouer_chanson():
    global glob_lbchanson, glob_recueil
    num_chanson = glob_lbchanson.curselection()[0]
    print('num : ',num_chanson)
    partition = glob_recueil[num_chanson][1]
    (n,d) = partition_to_noteduree(partition)
    print("n,d : ",n,d)
    tr=int(glob_transpo.get())
    n=transposition(n, tr)

    inv=int(glob_inv.get())
    if inv==1:
        n=inversion(n)

    titre_chansonactuelle = glob_recueil[num_chanson][0]
    ajout_if_needed((creation_de_titre(titre_chansonactuelle, inv, tr),noteduree_to_partition(n,d)))
    f=frequences(n)
    joue_des_notes(f,d)

    #joue_des_notes([220, -1, 440, 220], [1.5, 0.5, 1.3, 0.5])
    #joue_des_notes([220], [0.5])

def creation_de_titre(titre_chansonactuelle, inv, tr):
    res = titre_chansonactuelle
    if inv==1:
        res += " inversé"
    if tr!=0:
        res += " transposé de " + str(tr)
    return res


def mise_en_place_controles():
    global glob_racine,glob_transpo
    # transposition
    le = tk.Label(text="transposition")
    le.grid(row=0, column=2, sticky=tk.W)
    e = tk.Entry(width=3, textvariable=glob_transpo)
    e.grid(row=0, column=1, sticky=tk.E)
    glob_transpo.set('0')
    # inversion
    cb=tk.Checkbutton(text="inversion", variable=glob_inv)
    cb.grid(row=1, column=1, columnspan=2)
    glob_inv.set('0')

    #jouer
    bj=tk.Button(text="Jouer", command=jouer_chanson)
    bj.grid(row=0, column=3)


def mise_en_place_menus():
    global glob_racine
    glob_racine.title("Capucine and Emma")
    barre_menu = tk.Menu(glob_racine)
    glob_racine.config(menu=barre_menu)
    menu_fichier = tk.Menu(barre_menu)
    menu_fichier.add_command(label="Ajouter un fichier de partitions", command=ajout_partition)
    menu_fichier.add_command(label="Écrire un fichier partition", command=ecrire_partition)
    menu_fichier.add_command(label="Quitter", command=glob_racine.quit)
    barre_menu.add_cascade(label="Fichiers", menu=menu_fichier)

    menu_markov = tk.Menu(barre_menu)
    menu_markov.add_command(label="Version 1", command=chaine_de_makov_v1)
    menu_markov.add_command(label="Version 2", command=chaine_de_makov_v2)
    barre_menu.add_cascade(label="Chaines de Markov", menu=menu_markov)

    menu_avance = tk.Menu(barre_menu)
    menu_avance.add_command(label="Test son haut-parleurs", command=test_son_gauche_droite)
    menu_avance.add_command(label="Test son en superposition", command=test_son_superposition)
    menu_avance.add_separator()
    menu_avance.add_radiobutton(label="Instrument: sinus", var=glob_instrum, value="Sinus")
    menu_avance.add_radiobutton(label="Instrument: rectangles", var=glob_instrum, value="Rectangles")
    menu_avance.add_radiobutton(label="Instrument: orgue", var=glob_instrum, value="Orgue")
    menu_avance.add_radiobutton(label="Instrument: ovni", var=glob_instrum, value="Ovni")
    glob_instrum.set("Sinus")
    menu_avance.add_separator()
    menu_avance.add_command(label="Vitesse", command=vitesse)
    barre_menu.add_cascade(label="Avancé", menu=menu_avance)


def mise_en_place_canvas():
    global glob_canvas1, glob_canvas2
    glob_canvas1 = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas1.grid(row=2, column=0, columnspan=4)
    glob_canvas2.grid(row=3, column=0, columnspan=4)


def joue_une_note(frequence, duree_musicale):
    global glob_po
    print(frequence)
    duree = (duree_musicale * 0.125) / 2        #une croche a une durée musicale de 2 et une durée réelle de 125ms
    sample_rate=8000
    temps = np.linspace(0, duree, int(duree*sample_rate),False)  # temps est une liste de temps
    if frequence > 0:
        if glob_instrum.get() == "Sinus":
            signal = np.sin(frequence * temps * 2 * pi)     # 2*pi ==> (6) * np.pi
        elif glob_instrum.get() == "Rectangles":
            signal = np.sign(np.sin(temps * 2 * pi * frequence))
        elif glob_instrum.get() == "Orgue":
            signal = 0.4 * (np.sin(temps * 2 * pi * frequence)) + 0.5 * (
                np.sin(temps * 2 * pi * (frequence / 4))) + 0.1 * (np.sin(temps * 2 * pi * (frequence * 4)))
        elif glob_instrum.get() == "Ovni":
            signal = 0.2 * (np.sin(temps * 2 * pi * frequence)) + 0.4 * (
                np.sin(temps * 2 * pi * (frequence / sqrt(2)))) + 0.4 * (np.sin(temps * 2 * pi * (frequence * sqrt(2))))
        else:
            print("Erreur : instrument inconnu")
            return
    else:
        signal = temps * 0.0

    # enveloppe : important pour différencier à l'oreille 2 même notes qui se suivent
    # TODO : https: // fr.wikipedia.org / wiki / Enveloppe_sonore
    enveloppe = np.exp(-temps * 3)
    signal = signal * enveloppe
    dessine(signal)     #lorsqu'on est encore entre -1 et 1

    maxi = np.max(np.abs(signal))
    if maxi <= 0:    #cas d'un signal nul = silence
        maxi=1
    signal *= 8388607 / maxi
    signal = signal.astype(np.int32)  # signal sur 16 bits


    i = 0
    byte_array = []
    for b in signal.tobytes():
        if i % 4 != 3:
            byte_array.append(b)
        i += 1
    audio = bytearray(byte_array)

    glob_po = sa.play_buffer(audio, 1, 3, sample_rate)  # playobject
    if glob_po != 0:  # attente de la fin d'une éventuelle note précédente
        glob_po.wait_done()

    '''signal,
    nombre de canal : mono,
    nombre d'octets :2 octets = 16 bits,
    fréquence d'échantillonage")'''


def dessin2(signal):  # on lui passe le signal entre -1 et 1
    glob_canvas2.delete("all")
    # axe horizontal
    glob_canvas2.create_line(0,152, 600,152, width=1, fill="red")
    glob_canvas2.create_line(600,152, 590,142, width=1, fill="red")
    glob_canvas2.create_line(600,152, 590,162, width=1, fill="red")
    for i in range(1, 100):
        t = i / 100
        horizontal = int(t * 8000)
        glob_canvas2.create_line(horizontal+9, 148, horizontal+9, 156, width=1, fill="red")
        legende = "{0}s".format(t)
        glob_canvas2.create_text(horizontal+9, 161, text=legende, fill="black")

    # axe vertical
    glob_canvas2.create_line(9,5, 9,300, width=1, fill="red")
    glob_canvas2.create_line(9,5, 14,10, width=1, fill="red")
    glob_canvas2.create_line(9,5, 4,10, width=1, fill="red")
    for i in range(-4, 4):
        y = i / 4
        vertical = 149 * (1 - y) + 3
        glob_canvas2.create_line(4,vertical, 14,vertical, width=1, fill="red")
        legende = "{0}".format(y)
        glob_canvas2.create_text(24,vertical, text=legende, fill="black")

    y = signal[0]
    vertic_pre = 149 * (1 - y) + 3
    for i in range(1, 600):
        y = signal[i]
        vertic = 149 * (1 - y) + 3
        glob_canvas2.create_line(i-1+9,vertic_pre, i+9, vertic, width=1, fill="blue")
        vertic_pre = vertic
        #surement utile sur PC
    # glob_canvas2.update_idletasks()
    glob_canvas2.update()


def joue_des_notes(frequence, duree):
    for i in range(len(frequence)):
        joue_une_note(frequence[i], duree[i])


def dessin1(signal):
    glob_canvas1.delete("all")
    #axe horizontal
    glob_canvas1.create_line(0, 27, 600, 27, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 22, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 32, width=1, fill="red")
    for i in range(1, 10):
        t = i / 10
        horizontal = int(t * 1000)
        glob_canvas1.create_line(horizontal, 23, horizontal, 31, width=1, fill="red")
        legende = "{0}s".format(t)
        glob_canvas1.create_text(horizontal, 36, text=legende, fill="black")

    # AXE VERTICAL : trait, flèche, graduation tout les 0.25 sachant que les valeurs vont de -1 à 1 : donc 0=1 et 50=-1
    glob_canvas1.create_line(0, 27, 600, 27, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 22, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 32, width=1, fill="red")
    for i in range(1, 10):
        t = i / 10
        horizontal = int(t * 1000)
        glob_canvas1.create_line(horizontal, 23, horizontal, 31, width=1, fill="red")
        legende = "{0}s".format(t)
        glob_canvas1.create_text(horizontal, 36, text=legende, fill="black")

    y = signal[0]
    vertical_pre = 24 * (1 - y) + 3
    for h in range(1, 600):
        t = h / 1000
        ind = int(t * 8000)
        if ind >= len(signal):
            break  # arrêter le dessin si on est arriver au bout du signal avant 0.6s
        y = signal[ind]
        vertical = 24 * (1 - y) + 3
        glob_canvas1.create_line(h - 1, vertical_pre, h, vertical, width=1, fill="blue")
        vertical_pre = vertical
         #sûrement utile sur PC
    # glob_canvas1.update_idletasks()
    glob_canvas1.update()


def dessine(signal):
    dessin1(signal)
    dessin2(signal)

def lecture_fichier():
    recueil = []
    file = open("partitions.txt","r", encoding="utf-8")       #indicate "r"ead only
    line1 = file.readline()
    # https://qastack.fr/programming/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)   #+ veut dire qu'on remplace les caractères spéciaux présents au moins une fois
    line2 = file.readline()
    line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    while line1 != "":             #pour éviter les fins de lignes et fin de fichier, spécial sur Mac
        recueil.append((line1, line2))  # le dernier caractère de line est un passage à la ligne
        line1 = file.readline()     # /!/ fin de ligne n'est pas codé pareil sur Mac et Windows
        line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)
        line2 = file.readline()
        line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
        print(line1)
    file.close()
    print(recueil)
    return recueil

def mise_en_place_liste_chansons():
    global glob_lbchanson, glob_recueil
    lb = tk.Listbox(glob_racine, width=40, height=6,
                    selectmode=tk.SINGLE)
    for element in glob_recueil:
        (titre,part)=element
        lb.insert(tk.END,titre)     #tk.END est une constante définie qu'on ajoute à la fin d'une liste
    lb.select_set(0)                #défini la valeur par défaut
    lb.grid(row=0, column=0)
    glob_lbchanson=lb
    #print("global chanson: ", glob_lbchanson)
    #print("global recueil: ", glob_recueil)


mise_en_place_controles()
mise_en_place_menus()
glob_recueil=lecture_fichier()
mise_en_place_liste_chansons()
mise_en_place_canvas()
glob_racine.mainloop()
glob_racine.quit()


#recueil.append[("Happy birthday", "DOc Dob")]
#recueil.append[("J'ai du bon tabac", "DOn REn Min Don REn p Zc REn MIn FAn FAn Min Min")]
