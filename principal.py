import tkinter as tk
from tkinter import Canvas

import simpleaudio as sa
import simpleaudio.functionchecks as fc
import numpy as np
from numpy import pi

glob_racine = tk.Tk()
#Création des variables globales
glob_canvas=0
glob_canvas2=0
glob_po=0

def test_son_gauche_droite():
    '''test son des haut-parleurs droit puis gauche'''

def choix_chanson():
    pass

def mise_en_place_IHM():
def mise_en_place_menus():
    global glob_racine
    glob_racine.title("Capucine and Emma")
    barre_menu=tk.Menu(glob_racine)

    menu_jouer.add_command(label="Choix de la chanson", command=choix_chanson)
    barre_menu.add_cascade(label="Jouer",menu=menu_jouer)

    menu_avancé=tk.Menu(barre_menu)
    menu_avancé.add_command(label="Test son haut-parleurs", command=test_son_gauche_droite)
    menu_avancé.add_command(label="Test son en superposition", command=test_son_superposition)
    menu_avancé.add_separator()
    menu_avancé.add_command(label="Instruments", command=instruments)
    menu_avancé.add_command(label="Vitesse", command=vitesse)
    barre_menu.add_cascade(label="Avancé",menu=menu_avancé)
    menu_avance=tk.Menu(barre_menu)
    menu_avance.add_command(label="Test son haut-parleurs", command=test_son_gauche_droite)
    menu_avance.add_command(label="Test son en superposition", command=test_son_superposition)
    menu_avance.add_separator()
    menu_avance.add_command(label="Instruments", command=instruments)
    menu_avance.add_command(label="Vitesse", command=vitesse)
    barre_menu.add_cascade(label="Avancé",menu=menu_avance)

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
    glob_po=sa.play_buffer(sig_16b,1,2,8000)        #playobject
    '''signal,
    nombre de canal : mono,
    nombre d'octets :2 octets = 16 bits,
    fréquence d'échantillonage")'''

def mise_en_place_canvas():
    global glob_canvas,glob_canvas2
    glob_canvas = Canvas(width=600, height=50)
    glob_canvas2 = Canvas(width=600, height=300)
    glob_canvas.pack(side=tk.TOP)
    glob_canvas2.pack(side=tk.BOTTOM)

def dessin():
    glob_canvas.create_line(600,0, 0,50, width=5)
    glob_canvas2.create_line(600,0, 0,300, width=2)

mise_en_place_IHM()
def joue_des_notes(frequence,duree):
    for i in range(len(frequence)):
        joue_une_note(frequence[i],duree[i])

mise_en_place_menus()
mise_en_place_canvas()
dessin()
joue_des_notes([220,-1,440,220],[1.5,0.5,1.3,0.5])
glob_racine.mainloop()
glob_racine.destroy()
