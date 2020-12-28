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

import re      # regular expression to clean special characters (here carriage return)

"""Creation of global variables"""
glob_root = tk.Tk()
glob_instrum = tk.StringVar()
glob_inv = tk.StringVar()     # inversion ticked box or not
glob_transpo = tk.StringVar()
glob_collection = []
glob_canvas1 = 0
glob_canvas2 = 0
glob_po = 0
glob_lbsong = 0

def sound_test_loudspeakers():
    """sound test on left and right loudspeakers"""
    fc.LeftRightCheck.run()


def sound_test_superposition():
    """sound test on superposition of notes"""
    fc.OverlappingCheck.run()


def exists_title(title):
    """
    role: detect if a title already exists
    :param title: title of the song
    :return: boolean to know if the title given in parameter already exists
    effect on the program: the global variable glob_collection will maybe have a song with a new title
    """
    global glob_collection
    for song in glob_collection:
        if title == song[0]:
            return True
    return False


def addition_if_needed(song):
    """
    role:
    :param song:
    :return:
    effect on the program:
    """
    global glob_collection, glob_lbsong
    (title, part) = song
    if exists_title(title) == False :
        glob_collection.append(song)
        glob_lbsong.insert(tk.END, title)    # tk.END is a defined constant that we add at the end of a list
        glob_lbsong.select_clear(0, tk.END)  # to deselect all
        glob_lbsong.select_set(tk.END)       # to select the title of the song going on
        glob_lbsong.see(tk.END)              # to bring the scroll bar on the selected title
    write_collection()   # to add the song to the collection


def write_collection():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    global glob_collection
    file = open("partitions.txt", 'w', encoding="utf-8") # 'w' open for writing
    for song in glob_collection:
        (title, part) = song
        file.write(title + "\n")
        file.write(part + "\n")
    file.close()


def markov_chain_v1():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    print("Markov chain v1")
    print(creation_partition_v1(glob_collection))
    print(creation_duree_v1(glob_collection))
    print(noteduree_to_partition(creation_partition_v1(glob_collection), creation_duree_v1(glob_collection)))

def markov_chain_v2():
    """
    role: 
    no param: 
    no return: 
    effect on the program:
    """
    global glob_collection
    print("Markov chain v2")
    (nc, dc) = ([1,1,1,3,5,3,1],[2,2,2,2,2,2,4])  # simulation de l'appel à la fonction de Capucine
    title = "#" + str(len(glob_collection)) + " New musical rhythm of Markov2"
    markov_song_v2 = (title, noteduree_to_partition(nc, dc))
    addition_if_needed(markov_song_v2)

def vitesse():
    # not sure we keep that
    pass


def play_song():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    global glob_lbsong, glob_collection
    song_num = glob_lbsong.curselection()[0]
    partition = glob_collection[song_num][1]
    (n, d) = partition_to_noteduree(partition)
    tr = int(glob_transpo.get())
    n = transposition(n, tr)

    inv = int(glob_inv.get())
    if inv == 1:
        n = inversion(n)

    title_current_song = glob_collection[song_num][0]
    addition_if_needed((creation_de_title(title_current_song, inv, tr),noteduree_to_partition(n,d)))

    f = frequences(n)
    play_notes(f, d)


def title_creation(title_current_song, inv, tr):
    res = title_current_song
    if inv == 1:
        res += " reverse"
    if tr != 0:
        res += " transposed of " + str(tr)
    return res


def controls_settings():
    global glob_root, glob_transpo
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
    bj=tk.Button(text="Play", command=play_song())
    bj.grid(row=0, column=3)


def menus_settings():
    global glob_root
    glob_root.title("Capucine and Emma")
    menu_bar = tk.Menu(glob_root)
    glob_root.config(menu=menu_bar)

    menu_markov = tk.Menu(menu_bar)
    menu_markov.add_command(label="Version 1", command=chaine_de_markov_v1)
    menu_markov.add_command(label="Version 2", command=chaine_de_markov_v2)
    menu_bar.add_cascade(label="Markov chains", menu=menu_markov)

    menu_avance = tk.Menu(menu_bar)
    menu_avance.add_command(label="Sound test loudspeakers", command=sound_test_loudspeakers())
    menu_avance.add_command(label="Sound test superposition", command=sound_test_superposition())
    menu_avance.add_separator()
    menu_avance.add_radiobutton(label="Instrument: sinus", var=glob_instrum, value="Sinus")
    menu_avance.add_radiobutton(label="Instrument: rectangles", var=glob_instrum, value="Rectangles")
    menu_avance.add_radiobutton(label="Instrument: organ", var=glob_instrum, value="Organ")
    menu_avance.add_radiobutton(label="Instrument: UFO", var=glob_instrum, value="UFO")
    glob_instrum.set("Sinus")  #set the default value
    menu_avance.add_separator()
    menu_avance.add_command(label="Speed", command=vitesse)
    menu_bar.add_cascade(label="Advanced", menu=menu_avance)


def canvas_settings():
    global glob_canvas1, glob_canvas2
    glob_canvas1 = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas1.grid(row=2, column=0, columnspan=4)
    glob_canvas2.grid(row=3, column=0, columnspan=4)


def play_note(frequence, duree_musicale):
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
        elif glob_instrum.get() == "Organ":
            signal = 0.4 * (np.sin(temps * 2 * pi * frequence)) + 0.5 * (
                np.sin(temps * 2 * pi * (frequence / 4))) + 0.1 * (np.sin(temps * 2 * pi * (frequence * 4)))
        elif glob_instrum.get() == "UFO":
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
    #Une fonction play_sheet qui à partir d’une séquence de fréquences et de durées, appelle les fonctions sound et sleep pour lire la partition musicale ??
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


def play_notes(frequence, duree):
    for i in range(len(frequence)):
        play_note(frequence[i], duree[i])


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

def lecture_fichier():  #Une fonction read_line_file(f, num) qui prend en paramètres un nom de fichier et un numéro de ligne et qui retourne le contenu de la ligne en question.
    collection = []
    file = open("partitions.txt","r", encoding="utf-8")       #indicate "r"ead only
    line1 = file.readline()
    # https://qastack.fr/programming/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)   #+ veut dire qu'on remplace les caractères spéciaux présents au moins une fois
    line2 = file.readline()
    line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    while line1 != "":             #pour éviter les fins de lignes et fin de fichier, spécial sur Mac
        collection.append((line1, line2))  # le dernier caractère de line est un passage à la ligne
        line1 = file.readline()     # /!/ fin de ligne n'est pas codé pareil sur Mac et Windows
        line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)
        line2 = file.readline()
        line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    file.close()
    return collection

def setting_songs_list():
    global glob_lbsong, glob_collection
    lb = tk.Listbox(glob_root, width=40, height=6,
                    selectmode=tk.SINGLE)
    for element in glob_collection:
        (title,part)=element
        lb.insert(tk.END,title)     #tk.END est une constante définie qu'on ajoute à la fin d'une liste
    lb.select_set(0)                #défini la valeur par défaut
    lb.grid(row=0, column=0)
    glob_lbsong = lb


controls_settings()
menus_settings()
glob_collection=lecture_fichier()
setting_songs_list()
canvas_settings()
glob_root.mainloop()
glob_root.quit()


