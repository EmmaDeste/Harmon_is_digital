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
sample_rate = 44100  # audio signal is sliced 44100 times per second

# General usage global variable
glob_collection = []  # all songs in a list of [(tile1, partition1),(title2, partition2),...]
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
    """
    Sound test on left and right loudspeakers
    :return None, drive the audio output
    effect on the program: audible sound played
    """
    fc.LeftRightCheck.run()


def sound_test_superposition():
    """
    Sound test on superposition of notes
    :return None, drive the audio output
    effect on the program: multiple audible sounds played
    """
    fc.OverlappingCheck.run()


def play_note(frequence, musical_duration):
    """
    Create the sound of a note based on its frequency, its duration and the instrument used
    :param int frequence: frequency in Hertz
    :param int musical_duration: duration of a note, e.g. 2 for croche, 16 for ronde
    :return None, drive the audio output
    effect on the program: audible sound played
    """
    global glob_po
    duration = (musical_duration * glob_croche_duration) / 2  # code duration of croche is 2
    time = np.linspace(0, duration, int(duration * sample_rate), False)  # time is a list of time
                                                               # False because we want 1/sample_rate between each value
    if frequence > 0:
        if glob_instrum.get() == "Sinus":
            signal = np.sin(frequence * time * 2 * pi)
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
    else:  # to play nothing (silence)
        signal = time * 0.0  # to generate a flat signal

    # envelope : important to differentiate two following same notes (with ears)
    # TODO improved envelope using https: // fr.wikipedia.org / wiki / Enveloppe_sonore
    envelope = np.exp(-time * 3)
    signal = signal * envelope
    draw(signal)  # when we are between -1 and 1

    tone = signal * 8388607  # 8388607 = 2^23 : to stretch -1,1 to 24 bits
    tone = tone.astype(np.int32)  # transform list of floats to list of integers on 32 bits

    i = 0
    byte_array = []
    for b in tone.tobytes():
        if i % 4 != 3:  # to keep only 3  bytes on 4
            byte_array.append(b)
        i += 1
    audio = bytearray(byte_array)

    glob_po = sa.play_buffer(audio, 1, 3, sample_rate)  # playobject
    # 1 = number of audio channel : mono,
    # 3 = number of bytes : 3 bytes = 24 bits

    if glob_po != 0:  # wait for the end of a potential previous note
        glob_po.wait_done()


def play_notes(frequence, duration):
    """
    Create the sound of each notes based on its frequency and its duration using the function play_note
    :param int frequence: frequency in Hertz
    :param int duration: list of duration of notes, e.g. [2,16] for 1 croche and 1 ronde
    :return None, drive the audio output
    effect on the program: sound of notes played
    """
    for i in range(len(frequence)):
        play_note(frequence[i], duration[i])


# General usage functions

def exists_title(title):
    """
    Detects if a title already exists in the collection
    :param str title: title of the searched song
    :return if the title given in parameter already exists
    :rtype boolean
    effect on the program: the function will tell to addition_if_needed if a new title need to appear
    """
    for song in glob_collection:
        if title == song[0]:
            return True
    return False


def addition_if_needed(song):
    """
    Detect a new song and add it in the collection, add its title in the listbox and place the cursor on it
    :param tuple song: song containing (title, partition)
    :return None, directly add the song to glob_collection
    effect on the program: update the list of songs and override text file with the updated collection
    """
    global glob_collection, glob_lbsong
    (title, part) = song
    if exists_title(title) == False:
        glob_collection.append(song)
        glob_lbsong.insert(tk.END, title)  # tk.END is a defined constant that we add at the end of a list
        glob_lbsong.select_clear(0, tk.END)  # to deselect all
        glob_lbsong.select_set(tk.END)  # to select the title of the song going on
        glob_lbsong.see(tk.END)  # to bring the scroll bar on the selected title
    write_collection("partitions.txt")  # to add the song to the collection


def file_reading(file_name):
    """
    Create a collection of songs by reading by pairs of lines the file
    :param str file_name: name of the file that has to be read
    :return collection: collection of the songs contained in the file
    :rtype list
    effect on the program: create a collection of songs [(title1, partition1),(title2, partition2),...]
    """
    collection = []
    file = open(file_name, "r", encoding="utf-8")  # indicate "r"ead only
    line1 = file.readline()
    # https://qastack.fr/programming/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '',
                   line1)  # + means it replace special characters present at least once
    line2 = file.readline()
    line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    while line2 != "":  # to avoid end of lines and end of files, specific for Mac
        collection.append((line1,
                           line2))  # the last character of the line is a carriage return. /!\ carriage return has a different coding on Windows and on Mac
        line1 = file.readline()
        line1 = re.sub('[^A-Za-z0-9 èéêâ?!#\'\-]+', '', line1)
        line2 = file.readline()
        line2 = re.sub('[^A-Za-z0-9 ]+', '', line2)
    file.close()
    return collection


def write_collection(file_name):
    """
    Create a text file with the collection of songs by writing pairs of lines
    :param str file_name: name of the file that has to be written
    :return None, create and write in a text file
    effect on the program:  override the file containing collection of songs
    """
    global glob_collection
    file = open(file_name, 'w', encoding="utf-8")  # 'w' open for writing
    for song in glob_collection:
        (title, part) = song
        file.write(title + "\n")
        file.write(part + "\n")
    file.close()


def title_creation(title_current_song, inv, tr):
    """
    Create a title for a new song based on the title of the current song and transformation applied
    :param str title_current_song: title of the current song
    :param int inv: ticked box or not, e.g. 1 if ticked
    :param int tr: value of the transposition, e.g. -2 to down transposed of two half tones
    :return res: the new title
    :rtype str
    effect on the program: new songs have a fitting title
    """
    res = title_current_song
    if inv == 1:
        res += " reverse"
    if tr != 0:
        res += " transposed of " + str(tr)
    return res


def set_croche_duration(duration):
    """
    Set the croche duration in seconds based on a string giving the number of ms
    :param str duration: duration of a note in ms
    :return None, directly set the global variable glob_croche_duration
    effect on the program: give the speed of the song, e.g. 250 is two times slower than 125
    """
    global glob_croche_duration
    # https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    if duration.isdigit():
        dur = float(duration)
        if 0 < dur < 4000:
            glob_croche_duration = dur / 1000  # to convert seconds in ms


# Functions to be called by graphical interface

def markov_chain_v1():
    """
    Creation of a new musical rhythm using Markov chain version 1 based on the full collection
    glob_collection will be used as input (all songs) and output (one song added)
    :return None, to be used by Tkinter menu
    effect on the program: create a new song, add to the text file, add to the listbox
    """
    nc = creation_partition_v1(glob_collection)
    dc = creation_duree_v1(glob_collection)
    title = "#" + str(len(glob_collection)) + " New musical rhythm of Markov1"
    markov_song_v1 = (title, noteduree_to_partition(nc, dc))
    addition_if_needed(markov_song_v1)


def markov_chain_v2():
    """
    Creation of a new musical rhythm using Markov chain version 2 based on the full collection
    glob_collection will be used as input (all songs) and output (one song added)
    :return None, to be used by Tkinter menu
    effect on the program: create a new song, add to the text file, add to the listbox
    """
    nc = creation_partition_v2(glob_collection)
    dc = creation_duree_v2(glob_collection)
    title = "#" + str(len(glob_collection)) + " New musical rhythm of Markov2"
    markov_song_v2 = (title, noteduree_to_partition(nc, dc))
    addition_if_needed(markov_song_v2)


def play_song():
    """
    Create and play the sound of the song currently selected in the list box
    :return None, drive the audio output
    effect on the program: sound of the song played
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
    addition_if_needed((title_creation(title_current_song, inv, tr), noteduree_to_partition(n, d)))

    set_croche_duration(glob_croche_dur_sv.get())

    f = frequences(n)
    play_notes(f, d)


# Graphical interface functions using Tkinter

def setting_songs_list():
    """
    Display the list of songs on the screen using the collection
    :return None, drive on the graphic interface
    effect on the program: full fill the listbox with all the titles
    """
    global glob_lbsong
    lb = tk.Listbox(glob_root, width=40, height=6,
                    selectmode=tk.SINGLE)
    for element in glob_collection:
        (title, part) = element
        lb.insert(tk.END, title)  # tk.END is a defined constant that is added at the end of a list
    lb.select_set(0)  # set the default value
    lb.grid(row=0, column=0, rowspan=3)
    glob_lbsong = lb


def transformation_settings():
    """
    Setting up a cell to enter the value of the transposition, a box to ticked for an inversion,
    a cell to enter the value of the duration of a croche and a button to trigger play
    :return None, set up the graphic interface
    effect on the program: set the graphic interface to transform the play of a partition
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
    Setting up the menus to choose to use the Markov chains, to test the loudspeakers and to use different instruments
    :return None, set up the graphic interface
    effect on the program: set the graphic interface regarding top bar menus
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
    """
    Define two Canvas to have an area dedicated to the drawings
    :return None, set up the graphic interface
    impact of the program: signals could be draw in these two areas
    """
    global glob_canvas1, glob_canvas2
    glob_canvas1 = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas1.grid(row=3, column=0, columnspan=4)
    glob_canvas2.grid(row=4, column=0, columnspan=4)


def drawing1(signal):
    """
    Draw the general signal of a note on a coordinate system
    :param np.array signal: signal of a note between -1 and 1
    :return None, drive on the graphic interface
    effect on the program: display a drawing of the signal attitude during the first 600ms
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
        ind = int(t * sample_rate)
        if ind >= len(signal):
            break  # stop drawing if the signal finish before 0.6s
        y = signal[ind]
        vertical = 24 * (1 - y) + 3
        glob_canvas1.create_line(h - 1, vertical_pre, h, vertical, width=1, fill="blue")
        vertical_pre = vertical
    glob_canvas1.update()  # useful for PC ??

def drawing2(signal):
    """
    Draw the signal of the beginning of a note on a coordinate system
    :param np.array signal: signal of a note between -1 and 1
    :return None, drive on the graphic interface
    effect on the program: display a drawing of the beginning of signal
    on the horizontal axis, 1 pixel corresponds to 1/glob_sample_rate seconds
    """
    glob_canvas2.delete("all")
    # horizontal axis
    glob_canvas2.create_line(0, 152, 600, 152, width=1, fill="red")
    glob_canvas2.create_line(600, 152, 590, 142, width=1, fill="red")
    glob_canvas2.create_line(600, 152, 590, 162, width=1, fill="red")
    for i in range(1, 100):
        t = i / 100
        horizontal = int(t * sample_rate)
        glob_canvas2.create_line(horizontal + 9, 148, horizontal + 9, 156, width=1, fill="red")
        legend = "{0}s".format(t)
        glob_canvas2.create_text(horizontal + 9, 161, text=legend, fill="black")

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
    last_i = min(len(signal), 600)
    for i in range(1, last_i):
        y = signal[i]
        vertical = 149 * (1 - y) + 3
        glob_canvas2.create_line(i - 1 + 9, vertical_pre, i + 9, vertical, width=1, fill="blue")
        vertical_pre = vertical
    glob_canvas2.update()  # useful on PC ??


def draw(signal):
    """
    Draw the signal on two Canvas
    :param np.array signal: signal of a note between -1 and 1
    :return None, drive on the graphic interface
    effect on the program: display the signal on two drawings with different horizontal axis scale
    """
    drawing1(signal)
    drawing2(signal)


transformation_settings()
menus_settings()
glob_collection = file_reading("partitions.txt")
setting_songs_list()
canvas_settings()
glob_root.mainloop()
glob_root.quit()
