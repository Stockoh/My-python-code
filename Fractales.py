# les importations de module
from math import sqrt
from turtle import *

# les fonctions pour les fractales

# La courde du dragon


def dragon(l, n, i=1):
    if n == 0:
        fd(l)
    else:
        dragon(sqrt(l**2 / 2), n - 1, 1)
        left(90 * i)
        dragon(sqrt(l**2 / 2), n - 1, -1)

# Triangle de Sierpinski


def Sierpinski(cote, n):
    if n > -1:
        for i in range(3):
            if n == 1:
                begin_fill()
            Sierpinski(cote / 2, n - 1)
            forward(cote / 2)
            left(120)
        end_fill()
# courde et flocon de Von Koch


def Koch(cote, n, t=0):
    if n == 0:
        forward(cote)
    else:
        if t == 0:
            Koch(cote / 3, n - 1)
            left(60)
            Koch(cote / 3, n - 1)
            right(120)
            Koch(cote / 3, n - 1)
            left(60)
            Koch(cote / 3, n - 1)
        elif t == 1:
            Koch(cote / 3, n - 1, t)
            left(90)
            Koch(cote / 3, n - 1, t)
            right(90)
            Koch(cote / 3, n - 1, t)
            right(90)
            Koch(cote / 3, n - 1, t)
            left(90)
            Koch(cote / 3, n - 1, t)
        else:
            Koch(cote / 3, n - 1, t)
            left(90)
            Koch(cote / 3, n - 1, t)
            Koch(cote / 3, n - 1, t)
            right(90)
            Koch(cote / 3, n - 1, t)
            right(90)
            Koch(cote / 3, n - 1, t)
            Koch(cote / 3, n - 1, t)
            left(90)
            Koch(cote / 3, n - 1, t)


def flocon(cote, n, t=0):
    up()
    goto(-100, 100)
    down()
    if t == 0:
        for d in range(3):
            Koch(cote, n, t)
            left(-120)
    else:
        fillcolor("blue")
        begin_fill()
        for d in range(4):
            Koch(cote, n, t)
            left(-90)
        end_fill()

# courde de Lévy


def levy(l, n):
    if n == 0:
        forward(l)
    else:
        right(45)
        levy(sqrt(l**2 / 2), n - 1)
        left(90)
        levy(sqrt(l**2 / 2), n - 1)
        right(45)

# courde de peano


def peano(cote, n, i=1):
    if n == 0:
        fd(cote)
    else:
        left(90 * i)
        peano(cote / 2, n - 1, i * -1)
        left(-90 * i)
        peano(cote / 2, n - 1, i)
        peano(cote / 2, n - 1, i)
        left(-90 * i)
        peano(cote / 2, n - 1, i * -1)
        left(90 * i)
# L-systems


def Lsystems(cote, rule, graine, n, angle, const=[]):
    """Un L-systems qui peut dessiner beaucoup de fratale.
    Attention, il faut régler la taille de la fractale(cote) soi meme"""
    Lin = graine
    t = False
    for _ in range(n):
        Lout = []
        for m in Lin:
            for i in m:
                for e in rule:
                    # print(i)
                    # print(e)
                    # print(i==e)
                    if i == e:
                        t = True
                        # print(rule[e])
                        Lout.append(rule[e])
                if not(t):
                    # print("pas trouvé")
                    # print(i)
                    Lout.append(i)
                # print()
                t = False
        Lin = Lout
    draw(cote, Lin, const, angle)


def draw(cote, ordre, const, angle):
    g = (0, 0)
    setheading(90)
    for m in ordre:
        for r in m:
            # print(r,end="=")
            if r == "+":
                # print("on tourne")
                left(angle)
            elif r == "-":
                # print("on tourne")
                right(angle)
            elif r == "[":
                # print("on save")
                g = pos()
                # print(g)
            elif r == "]":
                # print("on va à",g)
                up()
                goto(g)
                down()
            elif not(r in const):
                # print("on avance")
                fd(cote)


# programme principale
speed(0)
delay(0)
Lsystems(10, {"F": "[F-]-FF"}, "F", 5, 60)
# Lsystems(3, {"X": "XF-F+F-XF+F+XF-F+F-X"}, "F+XF+F+XF", 5, 90, "X")
# Lsystems(5, {"X": "XF+G+XF--F--XF+G+X"}, "F--XF--F--XF", 4, 45, "X")
# Lsystems(4, {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}, "A", 4, 60)
# Lsystems(3, {"F": "F+F-F"}, "F", 8, 120, "")
# Lsystems(1, {"X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+"}, "Y", 7, 90)
# Lsystems(2.3, {"X": "-YF+XFX+FY-", "Y": "+XF-YFY-FX+"}, "X", 7, 90, "XY")
# Lsystems(3, {"X": "XFYFX+F+YFXFY-F-XFYFX",
#              "Y": "YFXFY-F-XFYFX+F+YFXFY"}, "X", 4, 90, "XY")
# Lsystems(2, {"A": "BA", "B": "BB+"}, "A", 13, 90)
# ht()
mainloop()
