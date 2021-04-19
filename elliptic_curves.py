from math_2 import Fraction, xgcd
import math_2 as mt


class EllipticCurve(object):
    def __init__(self, a, b):  # assume we're already in the Weierstrass form
        self.a = a
        self.b = b
        self.discriminant = -16 * (4 * a * a * a + 27 * b * b)

        if not self.isSmooth():
            raise Exception("The curve %s is not smooth!" % self)

    def isSmooth(self):
        return self.discriminant != 0

    def testPoint(self, x, y):
        return y * y == x * x * x + self.a * x + self.b

    def __repr__(self):
        res = "y^2 = x^3"
        if self.a:
            e = "-" if mt.sign(self.a) == -1 else "+"
        if abs(self.a) == 1:
            res += " %s x" % e
        else:
            res += " %s %sx" % (e, abs(self.a))
        if self.b:
            e = "-" if mt.sign(self.b) == -1 else "+"
        if abs(self.b) == 1:
            res += " %s 1" % e
        else:
            res += " %s %s" % (e, abs(self.b))
        return res

    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)


class Point(object):
    def __init__(self, curve, x, y):
        self.curve = curve  # the curve containing this point
        self.x = x
        self.y = y

        if not curve.testPoint(x, y):
            raise Exception(
                "The point %s is not on the given curve %s" % (self, curve))

    def __neg__(self):
        return Point(self.curve, self.x, -self.y)

    def __add__(self, other):
        if isinstance(other, Ideal):
            return self

        x_1, y_1, x_2, y_2 = self.x, self.y, other.x, other.y

        if (x_1, y_1) == (x_2, y_2):
            if y_1 == 0:
                return Ideal(self.curve)
            # use the tangent method
            # slope of the tangent line
            m = (3 * x_1 * x_1 + self.curve.a) / (2 * y_1)
        else:
            if x_1 == x_2:
                return Ideal(self.curve)  # vertical line

        # Using Vieta's formula for the sum of the roots
        m = (y_2 - y_1) / (x_2 - x_1)
        x_3 = m * m - x_2 - x_1
        y_3 = m * (x_3 - x_1) + y_1

        return Point(self.curve, x_3, -y_3)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise Exception(
                "Can't scale a point by something which isn't an int!")
        else:
            if other < 0:
                return -self * -other
        if other == 0:
            return Ideal(self.curve)
        else:
            Q = self
            R = self if other & 1 == 1 else Ideal(self.curve)

            i = 2
            while i <= other:
                Q = Q + Q

                if other & i == i:
                    R = Q + R

            i = i << 1
            return R

    def __rmul__(self, n):
        return self * n

    def __repr__(self):
        return "Point(x=%s ,y=%s)" % (self.x, self.y)

    def __sub__(self, other):
        return self + -other


class Ideal(Point):
  def __init__(self, curve):
    self.curve = curve

  def __repr__(self):
    return "Ideal"

  def __neg__(self):
    return self

  def __add__(self, other):
    return other

  def __mul__(self, n):
    if not isinstance(n, int):
      raise Exception("Can't scale a point by something which isn't an int!")
    else:
      return self


class DomainElement(object):
    def __radd__(self, other): return self + other
    def __rsub__(self, other): return -self + other
    def __rmul__(self, other): return self * other


class FieldElement(DomainElement):
    def __truediv__(self, other): return self * other.inverse()
    def __rtruediv__(self, other): return self.inverse() * other
    def __div__(self, other): return self.__truediv__(other)
    def __rdiv__(self, other): return self.__rtruediv__(other)


def IntegersModP(p):
  class IntegerModP(FieldElement):
    def __init__(self, n):
      self.n = n % p
      self.field = IntegerModP

    def __add__(self, other): return IntegerModP(self.n + other.n)
    def __sub__(self, other): return IntegerModP(self.n - other.n)
    def __mul__(self, other): return IntegerModP(self.n * other.n)
    def __truediv__(self, other): return self * other.inverse()
    def __div__(self, other): return self * other.inverse()
    def __neg__(self): return IntegerModP(-self.n)
    def __eq__(self, other): return isinstance(
        other, IntegerModP) and self.n == other.n

    def __abs__(self): return abs(self.n)
    def __str__(self): return str(self.n)
    def __repr__(self): return '%d (mod %d)' % (self.n, self.p)

    def __divmod__(self, divisor):
      q, r = divmod(self.n, divisor.n)
      return (IntegerModP(q), IntegerModP(r))

    def inverse(self):
      return IntegerModP(xgcd(self.n, self.p)[1])

  IntegerModP.p = p
  IntegerModP.__name__ = 'Z/%d' % (p)
  return IntegerModP
