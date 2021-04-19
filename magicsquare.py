import math_2 as mt
import itertools_2 as it


def tostring(L):
    L2 = it.map_deep(str, L, 1)
    m = len(max([max(x, key=len) for x in L2], key=len))
    string = ""
    for i in L2:
        for e in i:
            z = e + (m - len(e)) * " "
            string += z + " "
        string += "\n"
    return string

# Mean Dirichet square


def mean(L):
    return mt.Fraction(sum(L) / len(L)).reduce()


def mean_case(L, x, y, corners=False):
    """return the mean value off the case around the case at position x,y"""
    Values = []
    Add = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    if corners:
        Add += [(1, 1), (1, -1), (-1, 1), (1, 1)]
    for n, m in Add:
        try:
            a = x + n
            if a < 0:
                continue
            b = y + m
            if b < 0:
                continue
            Values.append(L[a][b])
        except:
            pass
    return mean(Values)


def new_square(L):
    new = it.copy(L)
    for x in range(1, len(L) - 1):
        for y in range(1, len(L[x]) - 1):
            new[x][y] = mean_case(L, x, y)
    return new


def square_close(S, C, rel_tol=1e-09):
    new = it.copy(S)
    for x in range(0, len(S)):
        for y in range(0, len(S[x])):
            new[x][y] = S[x][y] - C[x][y]
    return it.allf(new, lambda x: it.allf(x, lambda y: rel_tol >= abs(y)))


def dirichet_square(c1, c2, c3, c4, rel_tol=0):
    """L=    c1
          0 ------->0
          ^         ^
          |         |
        c4|         |c2
          |         |
          0-------->0
             c3"""
    if it.ndim(c1) == 2:
        L = c1
    else:
        L = [[0] + c1 + [0]] + list(reversed([[a] + ([0] * len(c1)) + [b]
                                              for a, b in zip(c4, c2)])) + [[0] + c3 + [0]]
    new = new_square(L)
    while not square_close(L, new, rel_tol):
        L = new[:]
        new = new_square(L)
    return L


if __name__ == "__main__":
    print(tostring(dirichet_square([1, 1, 100], [
          1, 1, 1], [1, 1, 1], [1, 1, 1], 0.1)))
    # print(mean_case([[0,8,8,0],[0,8,8,0],[0,8,8,0]],1,0))
