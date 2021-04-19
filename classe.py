from tkinter import *
from random import *
active = False
hau, lar = 800, 1530


class goutte():
    global hau, lar
    ha = hau
    la = lar
    g = 1

    def __init__(self, canevas, x, y, lon, lar=3, dy=0, z=1):
        self.can = canevas
        # print(type(self.can))
        self.z = z
        self.x = x
        self.y = y
        self.dy = dy / self.z
        self.lon = lon / self.z
        self.lar = lar / self.z

    def affiche(self):
        self.soi = self.can.create_line(
            self.x, self.y, self.x, self.y + 1 / self.z,
            width=1 / (self.z * 0.5), fill="purple")

    def ac(self):
        self.can.coords(self.soi, self.x, self.y, self.x,
                        self.y + 1 / (self.z * 0.04))
        self.can.itemconfigure(self.soi, width=1 / (self.z * 0.5))
        self.dy += goutte.g / self.z
        self.y += self.dy
        if self.y > goutte.ha:
            self.reset()

    def reset(self):
        self.x = randint(0, goutte.la)
        self.y = -randint(0, goutte.ha) - self.l
        self.dy = 0
        self.z = randint(1, 3)
        self.lon = self.lon / self.z
        self.lar = self.lar / self.z


fen = Tk()
canevas = Canvas(fen, width=lar, height=hau, bg="black")
canevas.grid(row=0, column=0, columnspan=10, padx=5, pady=5)

Lgoutte = []
for i in range(400):
    Lgoutte.append(goutte(canevas, 0, 10, 20))
    Lgoutte[i].reset()
    Lgoutte[i].affiche()


def on_off(event):
    global active
    active = not(active)
    if active:
        anime()


def anime():
    global active, Lgoutte
    if active:
        for i in Lgoutte:
            i.ac()
        fen.after(30, anime)


canevas.bind('<Button-1>', on_off)
fen.mainloop()
