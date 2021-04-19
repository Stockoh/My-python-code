# On import les modules
from turtle import *

# On prépare la tortue et les variables
speed(0)
delay(0)
ht()
grille = {}
# La liste de couleur que peut avoir la grille
# (la premiere est toujours le fond de l'écran)
color = ["white", "black", "blue"]
# La liste du mouvement par raport au couleur au-dessus
# (tousjour un multiple de 90)
turn = [90, 0, -90]
cote = 10  # Longueur du coté du carré
title("Fourmi de Langton")
bgcolor(color[0])  # couleur de fond

# On définie les fonctions


def carre(cote, color):
    """Déssine un carré de couleur color et de coté l autour de la tortue  """
    pencolor(color)
    fillcolor(color)
    begin_fill()
    up()
    forward(cote / 2)
    left(90)
    down()
    forward(cote / 2)
    left(90)
    for i in range(3):
        forward(cote)
        left(90)
    forward(cote / 2)
    left(-90)
    end_fill()
    back(cote / 2)
    up()


def cher(x, y):
    """Retourne la couleur de la case a la position x,y .
    Si elle n'existe pas ,elle la crée et
    retourne la premiere couleur de la liste color """
    global grille, color
    pos = (x, y)
    if pos not in grille:
        grille[pos] = color[0]
    return grille[pos]


def choiseturncolor(x, y):
    """Retourne comment tourné et et la couleur à metre
    sur la case où la tortue est et la modifie dans le dictionnaire grille """
    global grille, color, turn
    pos = (x, y)
    for e in enumerate(color):
        if e[1] == cher(x, y):
            i = e[0]
    if i + 1 == len(color):
        grille[pos] = color[0]
    else:
        grille[pos] = color[i + 1]
    return turn[i], grille[pos]


def animate():
    """anime la tortue"""
    global grille
    while True:
        for e in range(20000):
            angle, couleur = choiseturncolor(round(xcor()), round(ycor()))
            carre(cote, couleur)
            left(angle)
            forward(cote)
        y = str(input())
        if y != "":
            break


# programme principale
animate()

# Configuration remarquable
# A mettre a la ligne 10 pour inistialiser la variable turn
# Il faut mettre le même nombre de couleur que la longueur de la liste turn
# [90,90,-90,90,90]
# [90,90,-90]
# [-90,90,0]
# [-90,90]
# [-90,0,0,180]
# [180,0,180]
