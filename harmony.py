import tkinter as tk

glob_racine = tk.Tk()

def mise_en_place_IHM():
    global glob_racine
    glob_racine.title("Capucine and Emma")

mise_en_place_IHM()
glob_racine.mainloop()
glob_racine.destroy()
