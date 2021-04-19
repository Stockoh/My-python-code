from time import *
from random import *


def chmin(l):
    n = l[0]
    for i in l:
        if i < n:
            n = i
    return n


def triselec(l):
    for i in range(len(l) - 1):
        h = chmin(l[i:])
        l.remove(chmin(l[i:]))
        l.insert(i, h)
    return l


def fusion(L1, L2):
    L = []
    while True:
        if L1 == [] or L2 == []:
            return L + L1 + L2
        if L1[0] <= L2[0]:
            L.append(L1.pop(0))
        elif L2[0] <= L1[0]:
            L.append(L2.pop(0))


def trifusion(l):
    if len(l) == 1:
        return l
    else:
        return fusion(trifusion(l[:len(l) // 2]), trifusion(l[len(l) // 2:]))


def insertion(l, x):
    for e in enumerate(l):
        if e[1] >= x:
            return e[0]
    else:
        return len(l) - 1


def triinsertion(l):
    r = 0
    while r < len(l):
        t = l.pop(r)
        l.insert(insertion(l[:r], t), t)
        r += 1
    return l


def Bubble_sort(l):
    n = len(l) - 1
    for i in range(0, n):
        e = False
        for j in range(n, i, -1):
            if l[j] < l[j - 1]:
                l[j], l[j - 1] = l[j - 1], l[j]
                e = True
        if not e:
            break
    return l


def melange(l, n=-1):
    for i in range(len(l)):
        for j in range(i, -1, n):
            l[i], l[j] = l[j], l[i]
    return l
