import random
import copy

# Menace Code


class Box:
    def __init__(self, name, result):
        self.name = str(name)
        self.result = list(result)
        self.last = None
        self._out = False

    def out(self):
        self.last = random.choice(self.result)
        self._out = True
        return copy.deepcopy(self.last)

    def remove(self, value):
        try:
            self.result.remove(value)
        except:
            raise Exception

    def append(self, *value):
        self.result += [*value]

    def __repr__(self):
        return "Box(name=%s ,result=%s)" % (self.name, self.result)

    def good(self, n):
        if not self._out:
            raise Exception("Can't say good because nothing is out")
        self.append(*(self.last,) * n)

    def bad(self):
        if not self._out:
            raise Exception("Can't say bad because nothing is out")
        try:
            self.remove(self.last)
        except:
            pass

    def reset(self, newresult=None):
        self.result = newresult or self.result
        self.last = None
        self._out = False


class Menace():
    def __init__(self, boxs):
        self.dict = dict()
        for box in boxs:
            self[box.name] = box
        self._open = []

    def add(self, name, result):
        self[name] = Box(name, result)

    def open(self, name):
        if not self.exist(name):
            return False
        self._open.append(str(name))
        return self[name].out()

    def exist(self, name):
        try:
            self[str(name)]
            return True
        except:
            return False

    def good(self, n):
        for i in self._open:
            self[i].good(n)

    def bad(self):
        for i in self._open:
            self[i].bad()

    def close(self):
        for i in self._open:
            self[i].reset()
        self._open = []

    def __getitem__(self, index):
        try:
            return self.dict[str(index)]
        except:
            raise Exception

    def __setitem__(self, index, value):
        try:
            self.dict[str(index)] = value
        except:
            raise Exception

    def append_at(self, name, *value):
        try:
            self.dict[str(name)].append(*value)
        except:
            raise Exception
