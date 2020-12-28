#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Project: Harmony is digital
Authors: Capucine Foucher and Emma Desté
Promo: EFREI 2025
Role: this is the main file in charge of :
- setting the graphic interface,
- read songs collection from a file,
- write songs collection in a file,
- create digital sound using numpy,
- play sound using simpleaudio.
"""

from util_notes import *

import tkinter as tk
from tkinter import Canvas

import simpleaudio as sa
import simpleaudio.functionchecks as fc

import numpy as np
from numpy import pi

from math import sqrt

import re  # regular expression to clean special characters (here carriage return)

# Creation of global variables
# Simpleaudio variables
glob_po = 0  # simpleaudio playable object
sample_rate = 8000  # audio signal is sliced 8000 times per second

# General usage global variable
glob_collection = [] # all songs in a list of [(tile1, partition1),(title2, partition2),...]
glob_croche_duration = 0.125  # a croche has a musical duration of 125ms, linked to glob_croche_dur_sv

# Graphic interface variables
glob_root = tk.Tk()
glob_lbsong = 0  # listbox with all songs title
glob_canvas1 = 0  # graphical display of the note beginning
glob_canvas2 = 0  # graphical display of the entire note
glob_instrum = tk.StringVar()  # instrument name, e.g. "Organ"
glob_inv = tk.StringVar()  # inversion ticked box
glob_transpo = tk.StringVar()  # input area for the transposition value, e.g. "0" means no transposition
glob_croche_dur_sv = tk.StringVar()  # input area for the croche duration in ms, e.g. "125" means 0.125s


# Simpleaudio functions

def sound_test_loudspeakers():
    """sound test on left and right loudspeakers"""
    fc.LeftRightCheck.run()


def sound_test_superposition():
    """sound test on superposition of notes"""
    fc.OverlappingCheck.run()


def play_note(frequence, musical_duration):
    """
    role:
    :param frequence:
    :param musical_duration:
    no return:
    effect on the program:
    """
    global glob_po
    print(frequence)
    duration = (musical_duration * glob_croche_duration) / 2  # croche has a musical duration of 2
    time = np.linspace(0, duration, int(duration * sample_rate), False)  # time is a list of time
    if frequence > 0:
        if glob_instrum.get() == "Sinus":
            signal = np.sin(frequence * time * 2 * pi)  # Emma: 2*pi ==> (6) * np.pi
        elif glob_instrum.get() == "Rectangles":
            signal = np.sign(np.sin(time * 2 * pi * frequence))
        elif glob_instrum.get() == "Organ":
            signal = 0.4 * (np.sin(time * 2 * pi * frequence)) + 0.5 * (
                np.sin(time * 2 * pi * (frequence / 4))) + 0.1 * (np.sin(time * 2 * pi * (frequence * 4)))
        elif glob_instrum.get() == "UFO":
            signal = 0.2 * (np.sin(time * 2 * pi * frequence)) + 0.4 * (
                np.sin(time * 2 * pi * (frequence / sqrt(2)))) + 0.4 * (np.sin(time * 2 * pi * (frequence * sqrt(2))))
        else:
            print("Erreur : instrument inconnu")
            return
    else:
        signal = time * 0.0

    # envelope : important to differentiate two following same notes (with ears)
    # TODO : https: // fr.wikipedia.org / wiki / Enveloppe_sonore
    envelope = np.exp(-time * 3)
    signal = signal * envelope
    draw(signal)  # when we are between -1 and 1

    maxi = np.max(np.abs(signal))
    if maxi <= 0:  # case of null signal : silence
        maxi = 1
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
    # Emma: Une fonction play_sheet qui à partir d’une séquence de fréquences et de durées, appelle les fonctions sound et sleep pour lire la partition musicale ??
    if glob_po != 0:  # wait for the end of a potential previous note
        glob_po.wait_done()

    '''signal,
    nombre de canal : mono,
    nombre d'octets :2 octets = 16 bits,
    fréquence d'échantillonage")'''


def play_notes(frequence, duration):
    """
    role:
    :param frequence:
    :param duration:
    no return:
    """
    for i in range(len(frequence)):
        play_note(frequence[i], duration[i])

# General usage functions

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


def title_creation(title_current_song, inv, tr):
    """
    role:
    :param title_current_song:
    :param inv:
    :param tr:
    :return res:
    """
    res = title_current_song
    if inv == 1:
        res += " reverse"
    if tr != 0:
        res += " transposed of " + str(tr)
    return res


def set_croche_duration(duration):
    # duration in string
    # pas de return parce que seulement effet de bord sur glob_croche_duration
    global glob_croche_duration
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    if duration.isdigit():
        dur = float(duration)
        if 0 < dur < 4000:
            glob_croche_duration = dur / 1000


def file_reading(file_name):  #Emma: Une fonction read_line_file(f, num) qui prend en paramètres un nom de fichier et un numéro de ligne et qui retourne le contenu de la ligne en question.
    """
    role:
    :param file_name:
    :return collection:
    """
    collection = []
    file = open(file_name, "r", encoding="utf-8")  # indicate "r"ead only
    line1 = file.readline()
    # https://qastack.fr/programming/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)   # + means it replace special characters present at least once
    line2 = file.readline()
    line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    while line2 != "":                     # to avoid end of lines and end of files, specific for Mac
        collection.append((line1, line2))  # the last character of the line is a carriage return. /!\ carriage return has a different coding on Windows and on Mac
        line1 = file.readline()
        line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)
        line2 = file.readline()
        line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    file.close()
    return collection


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


# Functions to be called by graphical interface

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


def play_song():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    song_num = glob_lbsong.curselection()[0]
    partition = glob_collection[song_num][1]
    (n, d) = partition_to_noteduree(partition)
    tr = int(glob_transpo.get())
    n = transposition(n, tr)

    inv = int(glob_inv.get())
    if inv == 1:
        n = inversion(n)

    title_current_song = glob_collection[song_num][0]
    addition_if_needed((title_creation(title_current_song, inv, tr), noteduree_to_partition(n,d)))

    set_croche_duration(glob_croche_dur_sv.get())
    print("glob_croche_duration : ", glob_croche_duration, "glob_croche_dur_sv : ", glob_croche_dur_sv.get())

    f = frequences(n)
    play_notes(f, d)


def setting_songs_list():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    global glob_lbsong, glob_collection
    lb = tk.Listbox(glob_root, width=40, height=6,
                    selectmode=tk.SINGLE)
    for element in glob_collection:
        (title, part) = element
        lb.insert(tk.END, title)  # tk.END is a defined constant that is added at the end of a list
    lb.select_set(0)              # set the default value
    lb.grid(row=0, column=0, rowspan=3)
    glob_lbsong = lb


# Graphical interface functions using Tkinter

def controls_settings():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    global glob_root, glob_transpo
    # transposition
    le = tk.Label(text="transposition")
    le.grid(row=1, column=2, sticky=tk.W)
    e = tk.Entry(width=3, textvariable=glob_transpo)
    e.grid(row=1, column=1, sticky=tk.E)
    glob_transpo.set('0')

    # inversion
    cb = tk.Checkbutton(text="inversion", variable=glob_inv)
    cb.grid(row=2, column=1, columnspan=2)
    glob_inv.set('0')

    # croche duration
    cd = tk.Label(text="croche duration in ms")
    cd.grid(row=0, column=2, sticky=tk.W)
    d = tk.Entry(width=5, textvariable=glob_croche_dur_sv)
    d.grid(row=0, column=1, sticky=tk.E)
    glob_croche_dur_sv.set('125')

    # play
    bplay = tk.Button(text="Play", command=play_song)
    bplay.grid(row=1, column=3)


def menus_settings():
    """
    role:
    no param:
    no return:
    effect on the program:
    """
    global glob_root
    glob_root.title("Capucine and Emma")
    menu_bar = tk.Menu(glob_root)
    glob_root.config(menu=menu_bar)

    menu_markov = tk.Menu(menu_bar)
    menu_markov.add_command(label="Version 1", command=markov_chain_v1)
    menu_markov.add_command(label="Version 2", command=markov_chain_v2)
    menu_bar.add_cascade(label="Markov chains", menu=menu_markov)

    menu_avance = tk.Menu(menu_bar)
    menu_avance.add_command(label="Sound test loudspeakers", command=sound_test_loudspeakers)
    menu_avance.add_command(label="Sound test superposition", command=sound_test_superposition)
    menu_avance.add_separator()
    menu_avance.add_radiobutton(label="Instrument: sinus", var=glob_instrum, value="Sinus")
    menu_avance.add_radiobutton(label="Instrument: rectangles", var=glob_instrum, value="Rectangles")
    menu_avance.add_radiobutton(label="Instrument: organ", var=glob_instrum, value="Organ")
    menu_avance.add_radiobutton(label="Instrument: UFO", var=glob_instrum, value="UFO")
    glob_instrum.set("Sinus")  # set the default value
    menu_bar.add_cascade(label="Advanced", menu=menu_avance)


def canvas_settings():
    global glob_canvas1, glob_canvas2
    glob_canvas1 = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas1.grid(row=3, column=0, columnspan=4)
    glob_canvas2.grid(row=4, column=0, columnspan=4)


def drawing1(signal):
    """
    role:
    :param signal:
    no return:
    """
    glob_canvas1.delete("all")
    # horizontal axis
    glob_canvas1.create_line(0, 27, 600, 27, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 22, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 32, width=1, fill="red")
    for i in range(1, 10):
        t = i / 10
        horizontal = int(t * 1000)
        glob_canvas1.create_line(horizontal, 23, horizontal, 31, width=1, fill="red")
        legend = "{0}s".format(t)
        glob_canvas1.create_text(horizontal, 36, text=legend, fill="black")

    # vertical axis
    glob_canvas1.create_line(0, 27, 600, 27, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 22, width=1, fill="red")
    glob_canvas1.create_line(600, 27, 590, 32, width=1, fill="red")
    for i in range(1, 10):
        t = i / 10
        horizontal = int(t * 1000)
        glob_canvas1.create_line(horizontal, 23, horizontal, 31, width=1, fill="red")
        legend = "{0}s".format(t)
        glob_canvas1.create_text(horizontal, 36, text=legend, fill="black")

    y = signal[0]
    vertical_pre = 24 * (1 - y) + 3
    for h in range(1, 600):
        t = h / 1000
        ind = int(t * 8000)
        if ind >= len(signal):
            break  # stop drawing if the signal finish before 0.6s
        y = signal[ind]
        vertical = 24 * (1 - y) + 3
        glob_canvas1.create_line(h - 1, vertical_pre, h, vertical, width=1, fill="blue")
        vertical_pre = vertical
    glob_canvas1.update()   # useful for PC ??


def drawing2(signal):
    """
    role:
    :param signal: signal between -1 and 1
    no return:
    """
    glob_canvas2.delete("all")
    # horizontal axis
    glob_canvas2.create_line(0, 152, 600, 152, width=1, fill="red")
    glob_canvas2.create_line(600, 152, 590, 142, width=1, fill="red")
    glob_canvas2.create_line(600, 152, 590, 162, width=1, fill="red")
    for i in range(1, 100):
        t = i / 100
        horizontal = int(t * sample_rate)
        glob_canvas2.create_line(horizontal+9, 148, horizontal+9, 156, width=1, fill="red")
        legend = "{0}s".format(t)
        glob_canvas2.create_text(horizontal+9, 161, text=legend, fill="black")

    # vertical axis
    glob_canvas2.create_line(9, 5, 9, 300, width=1, fill="red")
    glob_canvas2.create_line(9, 5, 14, 10, width=1, fill="red")
    glob_canvas2.create_line(9, 5, 4, 10, width=1, fill="red")
    for i in range(-4, 4):
        y = i / 4
        vertical = 149 * (1 - y) + 3
        glob_canvas2.create_line(4, vertical, 14, vertical, width=1, fill="red")
        legend = "{0}".format(y)
        glob_canvas2.create_text(24, vertical, text=legend, fill="black")

    y = signal[0]
    vertical_pre = 149 * (1 - y) + 3
    last_i = min(len(signal),600)
    for i in range(1, last_i):
        y = signal[i]
        vertical = 149 * (1 - y) + 3
        glob_canvas2.create_line(i-1+9, vertical_pre, i+9, vertical, width=1, fill="blue")
        vertical_pre = vertical
    glob_canvas2.update()  # useful on PC ??


def draw(signal):
    """
    role:
    :param signal:
    no return:
    """
    drawing1(signal)
    drawing2(signal)


controls_settings()
menus_settings()
glob_collection = file_reading("partitions.txt")
setting_songs_list()
canvas_settings()
glob_root.mainloop()
glob_root.quit()


