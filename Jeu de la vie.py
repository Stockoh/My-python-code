# Importation des modules
from tkinter import *
from random import *
from time import *
# Mise en place des variables
colonnes = 4
lignes = colonnes
grille = [[0 for i in range(lignes)]for i in range(colonnes)]
cote = 600
d = False
# Mise en place des fonctions


def grillevierge():  # création d'une grille vierge
    global colonnes, lignes, cote
    c = "white"
    d = cote / lignes
    for i in range(lignes):
        for j in range(colonnes):
            canevas.create_rectangle(
                2 + j * d, 2 + i * d, 2 + (j + 1) * d, 2 + (i + 1) * d, outline='black', fill=c, )


def renit():  # Réinitialise la liste de liste grille et la grille affiché
    global grille, colonnes, lignes
    canevas.delete(ALL)
    grillevierge()
    grille = [[0 for i in range(lignes)]for i in range(colonnes)]


def tirage_aléa():  # Remplace chaque élément de la grille soit par un 0 soit par un 1 puis l'affiche
    global grille, colonnes, lignes
    for i in range(lignes):
        for j in range(colonnes):
            n = random()
            grille[i][j] = 0
            if n < 0.4:
                grille[i][j] = 1
    affiche()
    print(voisinvivant(1, 1))


def affiche():  # Teste chaque case de la grille et afficher soit un carré noir soit un carré blanc
    global colonnes, lignes, cote, grille
    canevas.delete(ALL)
    d = cote / lignes
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] == 1:
                c = "black"
            else:
                c = "white"
            canevas.create_rectangle(
                2 + j * d, 2 + i * d, 2 + (j + 1) * d, 2 + (i + 1) * d, outline='black', fill=c)


def voisinvivant(i, j):  # Compte le nombre de voisin vivant
    global grille, colonnes, lignes
    n = 0
    for a, b in ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1), (0, -1), (0, 1)):
        if i + a < 0 or j + b < 0 or i + a >= colonnes or j + b >= lignes:
            pass
        else:
            n += grille[i + a][j + b]
    return n


def act():
    global grille, colonnes, lignes
    l = [[0 for _ in range(lignes)]for _ in range(colonnes)]
    n = 0
    y = 0
    # print(grille)
    for element in grille:
        for e in element:
            # print(e,end="")
            v = voisinvivant(n, y)
            if v == 3 and e == 0:
                print("La cellule a la ligne {} et la colonne {} a {} voisin vivant et avait l'état {} donc elle nait".format(
                    n, y, v, e))
                l[n][y] = 1
            elif (v == 2 and e == 1) or (v == 3 and e == 1):
                print("La cellule a la ligne {} et la colonne {} a {} voisin vivant et avait l'état {} donc elle survit ".format(
                    n, y, v, e))
                l[n][y] = 1
            else:
                print("La cellule a la ligne {} et la colonne {} meurt car elle a {} voisin vivant et elle était a l'état {}".format(
                    n, y, v, e))
                l[n][y] = 0
            n += 1
        y += 1
        n = 0
        # print()
    grille = l[:]
    affiche()


def auto():
    global d
    if d:
        act()
        Vie.after(50, auto)


def on():
    global d
    if d == False:
        d = True
        auto()


def off():
    global d
    d = False


def clic(event):  # Fonction du clic qui inverse la couleur de la case cliqué
    global colonnes, lignes, cote, grille, d
    x = event.x
    y = event.y
    l = round((y - 2) // (cote / lignes))
    c = round((x - 2) // (cote / colonnes))
    if not(d):
        try:
            grille[l][c] = int(not(grille[l][c]))
            print("clic sur la ligne{} et la colonne{} a maintenant l'état{}".format(
                l, c, grille[l][c]))
            print(voisinvivant(l, c))
            affiche()
        except:
            pass


# Création de la fenetre
Vie = Tk()
Vie.title("Jeu de la vie")

# Création des boutons
Quitter = Button(Vie, text="Quitter",
                 command=Vie.destroy).grid(row=1, column=0)
Rénitialise = Button(Vie, text="Grille vierge",
                     command=renit).grid(row=1, column=1)
Tirage = Button(Vie, text="Tirage aléatoire",
                command=tirage_aléa).grid(row=1, column=2)
Générationsuit = Button(Vie, text="Génération suivante",
                        command=act).grid(row=1, column=3)
AutomateOn = Button(Vie, text="Démarrer l'automate",
                    command=on).grid(row=1, column=4)
AutomateOff = Button(Vie, text="Arrété l'automate",
                     command=off).grid(row=1, column=5)

# Création du canevas et de la grille
canevas = Canvas(Vie, width=cote + 2, height=cote + 2, bg="white")
canevas.grid(row=0, column=0, columnspan=10, padx=5, pady=5)

grillevierge()

# Programe principale
canevas.bind('<Button-1>', clic)
Vie.mainloop()
