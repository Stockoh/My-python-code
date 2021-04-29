import random


class Systeme:
    def __init__(self, utilisateurs=[]):
        self.utilisateurs = utilisateurs
        for i in self.utilisateurs:
            i.blockchain = Blockchain()
            for e in self.utilisateurs:
                i.blockchain.add(e, e.compte)

    def __str__(self):
        string = "Systeme:\n"
        for i in self.utilisateurs:
            string += "       |" + str(i) + "\n"
        return string[:-1]

    def __repr__(self):
        return str(self)

    def transaction(self, envoyeur, valeur, destinataire):
        if isinstance(envoyeur, str):
            for i in self.utilisateurs:
                if i.__name__ == envoyeur:
                    envoyeur = i

        if isinstance(destinataire, str):
            for i in self.utilisateurs:
                if i.__name__ == destinataire:
                    destinataire = i

        vérifieur = random.choice(self.utilisateurs)
        while vérifieur == envoyeur or vérifieur == destinataire:
            vérifieur = random.choice(self.utilisateurs)
        if vérifieur.blockchain.vérifié(envoyeur.__name__, valeur, envoyeur.compte):
            envoyeur.add(-valeur)
            destinataire.add(valeur)
            for uti in self.utilisateurs:
                uti.blockchain.add(envoyeur, valeur, destinataire)


class Utilisateur:
    def __init__(self, name, argent):
        self.__name__ = str(name)
        self.compte = argent

    def __str__(self):
        return self.__name__ + ":" + str(self.compte) + " $"

    def add(self, valeur):
        self.compte += valeur

    def __eq__(self, other):
        return str(self) == str(other)


class Blockchain:
    def __init__(self):
        self.list = []

    def add(self, envoyeur, valeur, destinataire=None):
        if destinataire == None:
            self.list.append([envoyeur.__name__, valeur, None])
        else:
            self.list.append(
                [envoyeur.__name__, valeur, destinataire.__name__])

    def vérifié(self, name, valeur, argent_envoyeur):
        utilisateurs = []
        for i in self.list:
            if i[2] == None:
                utilisateurs.append((i[0], i[1]))
            else:
                for x in utilisateurs:
                    x = list(x)
                    if x[0] == i[0]:
                        x[1] -= i[1]
                    if x[0] == i[2]:
                        x[1] += i[1]
                    if x[1] < 0:
                        return False
        for z in utilisateurs:
            if z[0] == name:
                return z[1] >= valeur and z[1] == argent_envoyeur


if __name__ == "__main__":
    a = Utilisateur("Alfred", 200)
    b = Utilisateur("Michel", 300)
    c = Utilisateur("Jean", 100)
    A = Systeme([a, b, c])
    print(A)
