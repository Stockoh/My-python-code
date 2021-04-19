from tkinter import *


class grid():
    """grid for curve"""

    def __init__(self, xmin, xmax, ymin, ymax, hauteur, longueur):
        self.fen = Tk()
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xlong = xmax - xmin
        self.ylong = ymax - ymin
        self.longueur = longueur
        self.hauteur = hauteur
        self.soi = Canvas(self.fen, width=self.hauteur,
                          height=self.longueur, bg="white")
        self.soi.grid(row=0, column=0)
        self.isrepere = False

    def coords_point(self, x, y):
        """return x and y for the canevas"""
        if x > self.xmax or x < self.xmin or y > self.ymax or y < self.ymin:
            return False
        else:
            y = -y
            x2 = x - self.xmin
            y2 = y - self.ymin
            x2 = x2 * (self.longueur / self.xlong)
            y2 = y2 * (self.hauteur / self.ylong)
            return x2, y2

    def create_point(self, x, y, color="black", taille=3):
        """create point at grid x,y"""
        if x > self.xmax or x < self.xmin or y > self.ymax or y < self.ymin:
            return False
        else:
            x2, y2 = self.coords_point(x, y)
            self.soi.create_rectangle(
                x2, y2, x2 + taille, y2 + taille, fill=color, width=0)

    def repere(self):
        for x in range(self.xmin, self.xmax + 1):
            self.create_point(x, 0, taille=3.5)
        for y in range(self.ymin, self.ymax + 1):
            self.create_point(0, y, taille=3.5)
        self.isrepere = True

    def plot_function(self, function, precision=0.1, color="black"):
        x = self.xmin
        while x <= self.xmax:
            y = function(x)
            self.create_point(x, y, color)
            x += precision

    def clean(self):
        self.soi.delete(ALL)
        if self.isrepere:
            self.repere()


if __name__ == "__main__":
    e = grid(-2, 2, -2, 2, 500, 500)
    e.repere()
    e.plot_function(lambda x: 1 / x, 0.01, color="black")
    e.plot_function(lambda x: 2 * x - 5 / x, 0.001, color="red")
    e.plot_function(lambda x: x * x * x + x * x - x, 0.01, color="blue")
    e.plot_function(lambda x: x * x * x - 2 + x, 0.001, color="green")
    e.fen.mainloop()
