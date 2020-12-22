import tkinter as tk
from tkinter import Canvas

import simpleaudio as sa
import simpleaudio.functionchecks as fc
import numpy as np
from numpy import pi

glob_racine = tk.Tk()
#Création des variables globales
glob_canvas1=0
glob_canvas2=0
glob_po=0

def test_son_gauche_droite():
    '''test son des haut-parleurs droit puis gauche'''
    fc.LeftRightCheck.run()

def test_son_superposition():
    fc.OverlappingCheck.run()


def ajout_partition():
    pass

def ecrire_partition():
    pass

def transposition():
    pass

def inversion():
    pass

def test_son():
    pass

def instruments():
    pass

def vitesse():
    pass

def choix_chanson():
    joue_des_notes([220, -1, 440, 220], [1.5, 0.5, 1.3, 0.5])
    joue_des_notes([220], [0.5])

def mise_en_place_menus():
    global glob_racine
    glob_racine.title("Capucine and Emma")
    barre_menu=tk.Menu(glob_racine)
    glob_racine.config(menu=barre_menu)
    menu_fichier=tk.Menu(barre_menu)
    menu_fichier.add_command(label="Ajouter un fichier de partitions", command=ajout_partition)
    menu_fichier.add_command(label="Écrire un fichier partition", command=ecrire_partition)
    menu_fichier.add_command(label="Quitter", command=glob_racine.quit)
    barre_menu.add_cascade(label="Fichiers",menu=menu_fichier)

    menu_transfo=tk.Menu(barre_menu)
    menu_transfo.add_command(label="Transposition", command=transposition)
    menu_transfo.add_command(label="Inversion", command=inversion)
    barre_menu.add_cascade(label="Transformation",menu=menu_transfo)

    menu_jouer=tk.Menu(barre_menu)
    menu_jouer.add_command(label="Choix de la chanson", command=choix_chanson)
    barre_menu.add_cascade(label="Jouer",menu=menu_jouer)

    menu_avancé=tk.Menu(barre_menu)
    menu_avancé.add_command(label="Test son haut-parleurs", command=test_son_gauche_droite)
    menu_avancé.add_command(label="Test son en superposition", command=test_son_superposition)
    menu_avancé.add_separator()
    menu_avancé.add_command(label="Instruments", command=instruments)
    menu_avancé.add_command(label="Vitesse", command=vitesse)
    barre_menu.add_cascade(label="Avancé",menu=menu_avancé)

def mise_en_place_canvas():
    global glob_canvas1,glob_canvas2
    glob_canvas1 = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas1.pack(side=tk.TOP)
    glob_canvas2.pack(side=tk.BOTTOM)

def joue_une_note(frequence,duree):
    global glob_po
    temps=np.linspace(0,duree,int(8000*duree))
    if frequence>0:
        signal=np.sin(temps*2*pi*frequence)
    else:
        signal=temps*0.0

    sig_16b=(signal*32767).astype(np.int16)          #signal sur 16 bits
    if glob_po!=0:                                  #attente de la fin d'une éventuelle note précédente
        glob_po.wait_done()
    dessine(signal)
    glob_po=sa.play_buffer(sig_16b,1,2,8000)        #playobject
    '''signal,
    nombre de canal : mono,
    nombre d'octets :2 octets = 16 bits,
    fréquence d'échantillonage")'''

def dessin2(signal):                          #on lui passe le signal entre -1 et 1
    glob_canvas2.delete("all")
    glob_canvas2.create_line(0,152, 600,152, width=1, fill="red")
    glob_canvas2.create_line(600,152, 590,142 , width=1, fill="red")
    glob_canvas2.create_line(600,152, 590,162, width=1, fill="red")
    for i in range (0,100):
        t=i/100
        horizontal=int(t*8000)
        glob_canvas2.create_line(horizontal,148, horizontal,156, width=1, fill="red")
        legende="{0}s".format(t)
        glob_canvas2.create_text(horizontal,161, text=legende, fill="black")
    #AXE VERTICAL : trait, flèche, graduation tout les 0.25 sachant que les valeurs vont de -1 à 1 : donc 0=1 et 300=-1
    y=signal[0]
    vertical_pre=149*(1-y) +3
    for i in range (1,600):
        y=signal[i]
        vertical=149*(1-y) +3
        glob_canvas2.create_line(i-1,vertical_pre, i,vertical ,width=1, fill="blue")
        vertical_pre=vertical
    #glob_canvas2.pack(side=tk.BOTTOM)      #sûrement utile sur PC
    #glob_canvas2.update_idletasks()
    glob_canvas2.update()


def joue_des_notes(frequence,duree):
    for i in range(len(frequence)):
        joue_une_note(frequence[i],duree[i])

def dessin1(signal):
    glob_canvas1.delete("all")
    glob_canvas1.create_line(0,27, 600,27, width=1, fill="red")
    glob_canvas1.create_line(600,27, 590,22, width=1, fill="red")
    glob_canvas1.create_line(600,27, 590,32, width=1, fill="red")
    for i in range(0, 100):
        t = i / 100
        horizontal = int(t * 8000)
        glob_canvas1.create_line(horizontal, 23, horizontal, 31, width=1, fill="red")
        legende = "{0}s".format(t)
        glob_canvas1.create_text(horizontal, 36, text=legende, fill="black")
    # AXE VERTICAL : trait, flèche, graduation tout les 0.25 sachant que les valeurs vont de -1 à 1 : donc 0=1 et 300=-1
    y = signal[0]
    vertical_pre = 24*(1-y) +3
    for i in range(1, 600):
        y = signal[i]
        vertical = 24*(1-y) +3
        glob_canvas1.create_line(i - 1, vertical_pre, i, vertical, width=1, fill="blue")
        vertical_pre = vertical
    # glob_canvas1.pack(side=tk.BOTTOM)      #sûrement utile sur PC
    # glob_canvas1.update_idletasks()
    glob_canvas1.update()

def dessine(signal):
    dessin1(signal)
    dessin2(signal)
    dessin2(signal)

mise_en_place_menus()
mise_en_place_canvas()
glob_racine.mainloop()
glob_racine.destroy()