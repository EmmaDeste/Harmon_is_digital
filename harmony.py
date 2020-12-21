import tkinter as tk

glob_racine = tk.Tk()

def donothing():
    print ("Rien a faire")

def mise_en_place_IHM():
    global glob_racine
    glob_racine.title("Capucine and Emma")
    barre_menu=tk.Menu(glob_racine)
    glob_racine.config(menu=barre_menu)
    menu_fichier=tk.Menu(barre_menu)
    menu_fichier.add_command(label="Quitter", command=glob_racine.quit)
    barre_menu.add_cascade(label="coucou",menu=menu_fichier)


mise_en_place_IHM()
glob_racine.mainloop()
glob_racine.destroy()
