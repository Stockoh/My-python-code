# ----- Importation des Modules -----#
from tkinter import *


# ----- Variables globales et conditions initiales -----#
l, h = 1350, 660  # Dimensions du canevas
# "pas" initial du déplacement
dx, dy = 5, 0
# Coordonnées initiales du cercle
x0, y0 = l // 2, h // 2
r = 10   # Rayon du cercle
dr = False
gravity = 0.4
# ----- Fonction générale pilotant les déplacements -----#


def move():
    """ Entrées : Fonction déclenchée par le bouton [Démarrer]- pas d'entrée
        Sorties : Fonction récursive qui redéfinit les coordonnées du centre
            du cercle toutes les 30 ms, à condition que le drapeau soit levé"""
    global x0, y0, dx, dy, r, l, h, dr
    x0 = x0 + dx
    y0 = y0 + dy
    dessin.coords(cercle, x0 - r, y0 - r, x0 + r, y0 + r)
    if x0 >= l - r or x0 <= r:
        dx = dx * -0.9
    if y0 <= r:
        dy = dy * -0.9
    elif y0 >= h - r:
        dy = dy * -0.9
    else:
        dy += gravity
    if dr:
        fen.after(30, move)


def clic(event):
    global dx, dy, x0, y0
    dx = (event.x - x0) / 15
    dy = (event.y - y0) / 15

# ----- Fonctions réceptionnant les événements -----#


def onOff():
    """Cette fonction lève le drapeau et lance l'animation."""
    global dr
    if not dr:
        dr = True
        move()
    else:
        dr = False


def grav():
    global gravity
    if gravity != 0:
        gravity = 0
    else:
        gravity = 0.4


# ----- Création de la fenêtre -----#
fen = Tk()
fen.title('Balle qui rebondit')


# ----- Création des boutons -----#
bouton_quitter = Button(fen, text="Quitter", width=9, command=fen.destroy)
bouton_quitter.grid(row=1, column=2, padx=3, pady=3)

bouton_stop = Button(fen, text="On/Off gravité", width=9, command=grav)
bouton_stop.grid(row=1, column=1, padx=3, pady=3)

bouton_start = Button(fen, text="On/Off", width=9, command=onOff)
bouton_start.grid(row=1, column=0, padx=3, pady=3)

# ----- Création du canevas -----#
dessin = Canvas(fen, bg="white", width=l, height=h)
dessin.grid(row=0, column=0, columnspan=3, padx=3, pady=3)


# ----- Objets graphiques -----#
cercle = dessin.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, width=2, outline="red")

# ----- Programme principal -----#
dessin.bind("<Button-1>", clic)

fen.mainloop()                    # Boucle d'attente des événements
