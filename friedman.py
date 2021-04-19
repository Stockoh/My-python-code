from expr import default_context, Expr
from itertools import permutations, product
import logging
import math_2 as mt
import math
import operator as op
import itertools_2 as it


def concat(left, right):
    left = Expr(left)
    right = Expr(right)
    if left.is_number() and right.is_number() and left() > 0 and right() >= 0:
        return int(str(left) + str(right))
    else:
        raise Exception


def sqrt(x):
    return mt.int_or_float(math.sqrt(x))


def periodical(x):
    if x > 0 and x < 10:
        return mt.int_or_float(x / 9)


def limit(*lim, function):
    def lim(*args):
        if not len(args) == len(lim):
            raise Exception
        for a, i in zip(args, lim):
            if a > i:
                return None
        return function(*args)

    return lim


default_context.add_function(
    sqrt, s="sqrt(%s)", numberofentry=1,
    formula=("s", "sqrt"), parenthesis=False)

default_context.add_function(concat, s="%s%s", formula=(
    "_", "concat"), parenthesis=False, basicnumber=True)

default_context.add_function(periodical, s="[.%s]", numberofentry=1, formula=(
    "[]"), parenthesis=False, basicnumber=True)

factorial = limit(20, function=mt.factorial)
default_context.functions["factorial"] = (
    factorial, '%s!', 'factorial(%s)', 1, ('!', 'factorial'), False, False)

power = limit(20, 20, function=op.pow)
default_context.functions["pow"] = (
    power, '%s^%s', '%s**%s', 2, ('^', '**'), True, False)


def gen(digits, monadic=["s"], diadic=["+", "-", "*", "/", "^"], permut=True, monadicrecurse=1):
    if monadicrecurse <= 0:
        monadic = []
    if monadic == []:
        monadicrecurse = 0
    if isinstance(digits, int):
        digits = str(digits)
    if isinstance(digits, str):
        digits = list(digits)
    if permut:
        for d in it.unique(permutations(digits)):
            for x in gen(d, monadic, diadic, False, monadicrecurse):
                yield x
        return
    if len(digits) == 1:
        e = Expr(digits[0])
        for i in monadic_gen([e], monadic, monadicrecurse):
            yield i
        return
    for i in range(1, len(digits)):
        for x in product(
                monadic_gen(gen(
                    digits[:i], monadic, diadic, permut, monadicrecurse),
                monadic, monadicrecurse), diadic,
                monadic_gen(gen(
                    digits[i:], monadic, diadic, permut, monadicrecurse),
                monadic, monadicrecurse),
        ):
            r = x[0].apply(x[1], x[2])
            for z in monadic_gen([r], monadic, min(1, monadicrecurse)):
                yield z


def monadic_gen(iterable, monadic, recurse=0):
    for i in iterable:
        yield i
        if recurse > 0:
            for ope in monadic:
                if not isinstance(i, Expr):
                    i = Expr(i)
                for z in monadic_gen([i.apply(ope)], monadic, recurse - 1):
                    yield z


def seq(digits, maxi=None, monadic=["!","[]"], diadic=["+", "-", "*", "/", "^"], permut=True, monadicrecurse=1, warning=True):
    z = {}
    i = 0
    for e in gen(digits, monadic, diadic, permut, monadicrecurse):
        try:
            key = e()
            if str(e) == str(key):
                continue
            if not(key is None) and (maxi is None or key <= maxi) and key >= 0 and not (key in z) and mt.is_integer(key, rel_tol=1e-9):
                z[mt.rint(key)] = e
                while i in z:
                    yield (i, z[i])
                    i += 1
                    if i > maxi:
                        return
        except:
            pass
    if warning:
        logging.warning('%d has no solution' % i)
    for k in sorted(z):
        if k > i:
            yield (k, z[k])


def pretty_print(e):
    f = str(e[1])
    f = f.replace("+ -", "- ")
    f = f.replace("- -", "+ ")
    f = f.replace("--", "")
    print("%s=%s" % (e[0], f))


def friedman(n, monadic=["!"], diadic=["+", "-", "*", "/", "^"], permut=False, monadicrecurse=2, base=10):
    if "_" in diadic:
        diadic.remove("_")
        diadic.append("_")
    i, expr = it.last(seq(mt.digits(n, base), n, monadic,
                          diadic, permut, monadicrecurse, False))
    if i == n and str(expr) != str(n):
        return i, expr
    return False


if __name__ == "__main__":
    for i in seq(111):
        pretty_print(i)
