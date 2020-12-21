import tkinter as tk
import simpleaudio as sa
import simpleaudio.functionchecks as fc

glob_racine = tk.Tk()

def test_son_gauche_droite():
    '''test son des haut-parleurs droit puis gauche'''
    fc.LeftRightCheck.run()

def test_son_superposition():
    fc.OverlappingCheck.run()


def ajout_partition():
    pass

def écrire_partition():
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
    pass

def mise_en_place_IHM():
    global glob_racine
    glob_racine.title("Capucine and Emma")
    barre_menu=tk.Menu(glob_racine)
    glob_racine.config(menu=barre_menu)
    menu_fichier=tk.Menu(barre_menu)
    menu_fichier.add_command(label="Ajouter un fichier de partitions", command=ajout_partition)
    menu_fichier.add_command(label="Écrire un fichier partition", command=écrire_partition)
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



mise_en_place_IHM()
glob_racine.mainloop()
glob_racine.destroy()
