import math
import itertools
import itertools_2 as it
import random

inf = float("inf")


def sign(n):
    if n > 0:
        return 1
    return -1 if n < 0 else 0


def is_number(n):
    return isinstance(n, (int, float, complex))


def is_integer(x, rel_tol=0, abs_tol=0):
    """
    :return: True if  float x is an integer within tolerances
    """
    if isinstance(x, int):
        return True
    try:
        if rel_tol + abs_tol == 0:
            return x == rint(x)
        return isclose(x, round(x), rel_tol=rel_tol, abs_tol=abs_tol)
    except TypeError:  # for complex
        return False


def rint(n):
    return int(round(n))


def int_or_float(n, rel_tol=0, abs_tol=0):
    if is_integer(n, rel_tol, abs_tol):
        return rint(n)
    return n


def float_part(n):
    return round(n - math.floor(n), len_float_part(n))


def len_float_part(n):
    try:
        return len(str(n).split(".")[1])
    except IndexError:
        return 0


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''approximately equal. Use this instead of a==b in floating point ops
        implements https://www.python.org/dev/peps/pep-0485/
        :param a,b: the two values to be tested to relative closeness
        :param rel_tol: relative tolerance
        it is the amount of error allowed, relative to 
        the larger absolute value of a or b.
        For example, to set a tolerance of 5%, pass tol=0.05.
        The default tolerance is 1e-9, which assures that 
        the two values are the same within
        about 9 decimal digits. rel_tol must be greater than 0.0
        :param abs_tol: minimum absolute tolerance 
        level -- useful for comparisons near zero.
        '''
    # https://github.com/PythonCHB/close_pep/blob/master/isclose.py
    if a == b:  # short-circuit exact equality
        return True

    if rel_tol < 0.0 or abs_tol < 0.0:
        raise ValueError('error tolerances must be non-negative')

        # use cmath so it will work with complex ot float
    if math.isinf(abs(a)) or math.isinf(abs(b)):
            # This includes the case of two infinities of opposite sign, or
            # one infinity and one finite number. Two infinities of opposite sign
            # would otherwise have an infinite relative tolerance.
        return False
    diff = abs(b - a)

    return (((diff <= abs(rel_tol * b)) or (diff <= abs(rel_tol * a))) or (diff <= abs_tol))

# optimization


def ipow(x, n, z=0):
    """integer pow
    param x: number(int or float or fraction)
    param n:integer
    param z: int optional modulus
    return: (x**n)%z
    """
    if n < 0:
        if z:
            raise NotImplementedError('no modulus allowed for negative power')
        elif x == 0:
            raise ZeroDivisionError("0 cannot be raised to a negative power")
        else:
            return 1 / ipow(x, -n)
    elif n == 0:
        return 1
    elif x == 0 or x == 1:
        return x
    elif n == 1:
        return x
    a, b = 1, x
    while n > 0:
        if n % 2 == 1:
            a = (b * a) % z if z else b * a
        b = (b * b) % z if z else b * b
        n = n // 2
    return a


def mod_matmul(A, B, mod=0):
    """return (A*B)%mod"""
    if mod:
        return [[sum(a * b for a, b in zip(A_row, B_col)) % mod for B_col in zip(*B)] for A_row in A]
    else:
        return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]


def mod_matpow(M, power, mod=0):
    """return (M^power)%mod"""
    result = [[1, 0], [0, 1]]
    for power in digits(power, 2, True):
        if power:
            result = mod_matmul(result, M, mod)
        M = mod_matmul(M, M, mod)
    return result


def fibonacci(n, mod=0):
    """gives the n-th fibonacci number modulo mod
    """
    return int(mod_matpow([[1, 1], [1, 0]], n, mod)[0][1])


def factorialk(n, k):
    """multifactorial of n of order k,n(!!...!) """
    if n < 0:
        return None
    elif n <= 0:
        return 1
    elif k == 0:
        return float("inf")
    t = mul(range(n, 0 -k))
    return t


def factorial(n):
    return factorialk(n, 1)


def factorial2(n):
    return factorialk(n, 2)


def binomial(n, r):
    if r > n:
        return 0
    elif n == r or r == 0:
        return 1
    return factorial(n) / (factorial(r) * factorial(n - r))

def collatz(n):
    if n%2==0:return int(n/2)
    else:return 3*n+1
    
def period_collatz(n):
    if n==1 or n==0 or n==-17 or n==-5 or n==-1:return 1
    return 1+period_collatz(collatz(n))

def collatz_gen(n):
    yield n
    while True:
        n=collatz(n)
        yield n

def sum_tronq_right(n):
    """
    n=abc
    return abc+bc+c
    if n=a0c
    return a0c+c
    """
    T=0
    while True:
        T+=int(n)
        if len(str(n))==1:return T
        n=str(n)[1:]

def list_sum_trong_right(n):
    """return a list [m0,m1...] such that m0=abc and m1=def and abc+bc+c=def+ef+f=n"""
    L=[]
    r=ilog(n,10)*"8"
    if r=="":r=0
    else:r=int(r)
    for i in range(r,n+1):
        if sum_tronq_right(i)==n:L.append(i)
    return L



def is_polygon_constructible(n):
    """return True if n-gons is construtible  """
    L=[3, 5, 17, 257, 65537]
    if n in [0,1]:return True
    for i in prime_factors(n):
        if i==2:continue
        elif not i in L:return False
        else:L.remove(i)
    return True

def iterfibo(n=inf):
    a,b=1,0
    p=0
    while True:
        yield a
        a,b=a+b,a
        p+=1
        if p==n:break


def ilog(x,n):
    """return a number j such that n^j<=x<n^(j+1)"""
    if n==0 or x==0:return 0
    elif n==1 : return 0
    j=1
    r=n
    while True:
        if r==x:return j
        elif r>x:return j-1
        r*=n
        j+=1

def ilog10(x):
    return ilog(x,10)

def ilog2(x):
    return ilog(x,2)

def iroot(x,r):
    """return a number j such that j^n<=x<(j+1)^n"""
    if x<0:return None
    if x<=1:return x
    up=x//2
    low=1
    while up-low!=1:
        res=(up+low)//2
        m=res**r
        if m==x:return res
        elif m>x:up=res
        elif m<x:low=res
    return low

def isqrt(x):
    if x<0:return inf
    if x<=1:return x
    y=0
    z=x//2
    while z!=y:
        y=z
        z=y-rint((y*y-x)/(2*y))
    return z

def is_pow_kth(x,k):
    """retrun True if x is a k-th power """
    r=iroot(x,k)
    return r**k==x

def is_square(x):
    r=isqrt(x)
    return r*r==x

def is_pow_of_k(x,k):
    """retrun True if x is a power of k """
    z=x
    while True:
        if z==1:return True
        if z%k!=0:return False
        z//=k

def find_power(x):
    """retrun the tuple (r,p) such that r**p=x if it does not exist return False
    """
    if x==0 or is_prime(x):return False
    for i in primegen(end=x):
        r=iroot(x,i)
        if r**i==x :return (r,i)
        if r==1:return False
    return False

def is_power(x):
    """retrun True if x is a perfect power
    """
    if find_power(x):return True
    return False

def is_repfigit(n,base=10,revers=False):
	if n<base:return False
	l=digits(n,base,revers)
	while l[-1]<n:
		l=l[1:]+[sum(l)]
	if l[-1]==n:return True
	return False

def champernowne_constant_gen(base=10):
    for i in itertools.count():
        for z in digits(i,base):
            yield z
            
#prime function

smallprime=([],0)

def sieve(n):
    """return all the prime <=n
    >>> sieve(30)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]"""
    global smallprime
    n=int(n)
    n_sqrt=isqrt(n)+1
    if n<=smallprime[1]:
        L=[]
        for i in smallprime[0]:
            if i<=n:L.append(i)
            else:return L
    L=[False,False,True,True]+[False,True]*((n-2)//2)
    for r,i in enumerate(L):
        if r<=2:continue
        if i and r<=n_sqrt:
            v=False
            for e in range(3,(n//r)+1,2):
                if r*e<=n:
                    L[r*e]=False
                    v=True
                else:break
            if not v:break
        elif not r<=n_sqrt:break
    smallprime=([x for x in range(n+1) if L[x]],n)
    return smallprime[0]

smallprime=(sieve(100),100)

def prime(n):
    """return the n-th prime"""
    global smallprime
    if n==0:return None
    if n<=len(smallprime[0]):return smallprime[0][n-1]
    z=it.last(smallprime[0])
    v=len(smallprime[0])+1
    for e,i in enumerate(primegen(z),start=v):
        smallprime=(smallprime[0]+[i],i)
        if e==n:return i

def is_prime_euler(n,base=(2,3)):
    """Return true if n is a Euler-peusdo-prime in base"""
    for a in base:
        r=ipow(a,(n-1)//2,n)
        if not (r==1 or r==n-1):return False
    return True

def is_prime(n):
    """A prime test whit the Miller-Rabbin test"""
    global smallprime
    kp=smallprime[0][1:101]
    if n==1: return False
    
    elif n<=0:return False
    
    elif n==2:return True
    
    elif n%2==0:return False
    elif n in kp:return True
    if any((n%pr == 0 and n not in kp) for pr in kp):return False
    
    if not is_prime_euler(n):return False
    s,d=pfactor(n)
    if not sprp(n,2,s,d):return False
    elif n<2047:return True
    return all(sprp(n,pr,s,d) for pr in kp)

def primegen(start=2,end=None):
    """Generate prime from start to end """
    if (start,end)==(2,None):yield from primegenfast()
    if not((end is None) or start<end):
        n=start+1
        if end is None:end=1
        while True:
            n=prevprime(n)
            if n is None:break
            if (end is None) or n>end:
                yield n
            else:
                break
    else:
        if start==1:
            yield 1
            start=2
        n=start-1
        while True:
            n=nextprime(n)
            if (end is None) or n<end:
                yield n
            else:
                break
            
def primegenfast():
    """faster than primegen but he must start at 0"""
    yield 2;yield 3;yield 5;yield 7;yield 11;yield 13;yield 17;yield 19
    ps=primegenfast()
    allprime=next(ps)
    prime=next(ps)
    allprime*=prime
    nextprime=next(ps)
    limit=nextprime*nextprime
    n=21
    while True:
        if n<limit:
            if coprimes(n,allprime):
                yield n
        else:
            prime=nextprime
            allprime*=prime
            nextprime=next(ps)
            limit=nextprime*nextprime
        n+=2

def nextprime(n):
    """return the prime following n
    >>>nextprime(17)
    19
    """
    n=rint(n) # for use 1E6
    if n<2:return 2
    if n==2:return 3
    if n%6==5:
        if is_prime(n+2):return n+2
        n+=2
    n=n-n%6+5
    for i in itertools.count(n,6):
        if is_prime(i):return i
        if is_prime(i+2):return i+2

def prevprime(n):
    """return the prime before n
    >>>prevprime(17)
    13
    """
    n=rint(n)
    if n<=2:return None
    elif n<5:return n-1
    elif n==5:return 3
    m=n%6
    if m==0:a=-1
    elif m==1 or m==3:a=-2
    elif m==2:a=-1
    elif m==5:a=-4
    elif m==4:a=-3
    if m==1 or m==0:v=4
    else :v=2
    while True:
        if is_prime(n+a):return n+a
        a-=v
        if v==2:v=4
        else:v=2

def random_prime(digit):
    """return a random prime with digit len of digits"""
    if digit==1:
        r=(2*(random.randint(0,4))+1)
    else:r=int(str((random.randint(10**(digit-2),10**(digit-1)-1)))+str((2*(random.randint(0,4))+1)))
    while True:
        a=nextprime(r)
        if len(str(a))>digit:return prevprime(r)
        else:return a

def lucas_lehmer(p):
    """Lucas-Lehmer primality test for Mersenne prime (2**p-1)"""
    if p==2:return True
    elif not is_prime(p):return False
    s=4
    mp=(1<<p)-1 #2**p-1
    for i in range(p-2):
        s=s*s
        s-=2
        s=s%mp
    return s==0

def prime_factors(n,start=2):
    """generates prime factors of n"""
    if n<4:yield n;return 
    elif is_prime(n):yield n;return
    n_root=isqrt(n)
    for i in primegen(start):
        if n%i==0:
            while n%i==0:
                yield i
                n//=i
            if is_prime(n):
                yield n
                break
            n_root=isqrt(n)
        if n==1:break
        if i>n_root:
            yield n
            break

def pfactor(n):
    """Helper function for sprp
    return a tuple (s,d)such that n-1=(2^s)*d"""
    s=n-1
    a=0
    while s%2==0:
        s,a=s//2,a+1
    return n//s,s

def sprp(n,a,s=None,d=None):
    """Test primality for n with the Strong Probable Primelity Test to base a
    If present s and d should be the first and second items,
    of the tuple return by  the function pfactor
    """
    if n%2==0:
        return False
    elif (s is None) or (d is None):
        s,d=pfactor(n)
    x=pow(a,d,n)
    if x==1:
        return True
    for r in range(s):
        if x==n-1:return True
        x=pow(x,2,n)
    return False

def factorise(n,start=2):
    return list(it.compress(prime_factors(n,start)))

def number_of_divisors(n):
    z=1
    if n>1:
        for (e,p) in factorise(n):
            z*=p+1
    return z

def divisors(n):
    """return all divisors off n
    ex:divisors(20)->1,2,4,5,10,20"""
    if n == 1:
        yield 1
    else:
        div=[]
        all_factors = [[f ** p for p in range(0, fp+1)] for (f, fp) in factorise(n)]
        for ns in itertools.product(*all_factors):
            div.append(mul(ns))
        for i in sorted(div):
            yield i

def proper_divisors(n):
    """return all divisors of n except n itself."""
    return (divisor for divisor in divisors(n) if divisor != n)

def is_perfect(n):
    """return 0 if n is perfect elif -1 is deficient else 1 is abundant"""
    for s in it.accumulate(divisors(n)):
        if s>2*n:
            return 1
    return 0 if s == 2 * n else -1

def sigma(n):#1st definition of sigma
    """return the sigma function on n (sum off divisors)"""
    if n<4:return n+1
    return sum(divisors(n))

def sigma2(n):#2st definition of sigma
    """return the sigma function on n (sum off proper divisors)"""
    if n==1 or n==0:return 0
    if n<4:return 1
    return sum(proper_divisors(n))

def mul(iterable):
    t=1
    for i in iterable:
        t*=i
    return t

def phi(n):
    return mul((p-1)*p**(k-1) for p,k in factorise(n))
        
###Digit function

def reverse(m,base=10):
    return num_from_digit(digits(m,base=base,rev=True),base=base)

def is_palindromic(m,base=10):
    q=digits(m,base)
    mir=list(reversed(q))
    return q==mir

def digits_gen(n,base=10):
    """generates int digits of n in base BACKWARD"""
    if n==0:
        yield 0
    while n:
        n,r=divmod(n,base)
        yield r

def digits(n,base=10,rev=False):
    """return list of digits of n in base"""
    digit=list(digits_gen(n,base))
    if not rev:digit.reverse()
    return digit

def num_from_digit(digit,base=10):
    if isinstance(digit,str):
        return int(digit,base)
    re=0
    f=1
    for x in reversed(list(digit)):
        re=re+int(x*f)
        f=f*base
    return re

def str_base(num, base=10, numerals='0123456789abcdefghijklmnopqrstuvwxyz'):
    '''
    :return: string representation of num in base
    :param num: int number (decimal)
    :param base: int base, 10 by default
    :param numerals: string with all chars representing numbers in base base. chars after the base-th are ignored
    '''
    if base == 10 and numerals[:10] == '0123456789':
        return str(num)
    if base == 2 and numerals[:2] == '01':
        return "{0:b}".format(int(num))
    if base < 2 or base > len(numerals):
        raise ValueError(
            "str_base: base must be between 2 and %d" % len(numerals))
    if num < 0:
        sign = '-'
        num = -num
    else:
        sign = ''

    result = ''
    for d in digits_gen(num, base):
        result = numerals[d] + result

    return sign + result

def digop(n,f=None,op=sum,base=10):
    """return operation on digits in base

    param n: int number
    param f: None or int number of a power or a function apply on all digits of n
    param op: function on the number obtained after the fonction f
    param base: base off the digits of n

    example:
        digits_op(254,f=None,op=sum,base=10) return 2+5+4 = 11
        digits_op(254,f=2,op=sum,base=10) return 2*2+5*5+4*4 = 46
        digits_op(143,f=factorial,op=mul,base=10) return factorial(1)*factorial(4)*factorial(3)=144
    
    """
    d=digits(n,base)
    if f is None:
        return op(d)
    elif is_number(f):
        p=f
        f=lambda x: x**p
    try:
        d=op(map(f,d))
        return d
    except TypeError:
        pass
    d=[f(x,i) for i,x in enumerate(d)]
    return op(d)



def recurse(f,x):
    while True:
        yield x
        x=f(x)

def recurse_orbit(f,x):
    """like recurse but it stop when he loop """
    L=[]
    for i in recurse(f,x):
        yield i
        if not i in L:L.append(i)
        else:break

def find_cycle(f,end,start=0):
    """find cycle off function f appearing between start and end
    example:
        find_cycle(lambda x: digits_op(x,f=2,op=sum,base=10),100)-->[[0], [1], [4, 16, 37, 58, 89, 145, 42, 20]]#is happy and not happy cycle"""
    cycle=[]
    flattencycle=[]
    for i in range(start,end,sign(end-start)):
        L=[]
        for z,e in enumerate(recurse_orbit(f,i)):
            if e==i and z!=0 :
                L2=list(it.refine(L))
                if not L2 in cycle:
                    cycle.append(L2)
                    flattencycle=it.flatten(cycle)
                break
            L.append(e)
        if not e in flattencycle:
            W=list(recurse_orbit(f,e))[:-1]
            W=list(it.refine(W))
            if not W in cycle:
                    cycle.append(W)
                    flattencycle=it.flatten(cycle)
    return sorted(cycle)
            
def period(f,n):
    return it.ilen(recurse_orbit(f,n))-1

def gcd(*args):
    """greatest common divisor of an arbitrary number of args"""
    L=list(args)
    a=L[0]
    while len(L)>1:
        b=L[-1]
        a=L[-2]
        L=L[:-2]
        while b:
            a,b=b,a%b
        L.append(a)
    return abs(a)

def xgcd(a, b):
    '''Extended GCD
    :return: (gcd, x, y) where gcd is the greatest common divisor of a and b
    with the sign of b if b is nonzero, and with the sign of a if b is 0.
    The numbers x,y are such that gcd = ax+by.'''
    # taken from http://anh.cs.luc.edu/331/code/xgcd.py
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q, r = divmod(a, b)
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, r
    return a, prevx, prevy

def lcm(*args):
    """least common multiple of any number of integers"""
    L=list(args)
    if set(L)==set([0]):return 0
    elif len(L)<=2:
        return mul(L)//gcd(*L)
    cm=lcm(L[0],L[1])
    for n in L[2:]:
        cm=lcm(n,cm)
    return cm

def coprimes(*args):
    """return: True if args are coprime to each other"""
    return gcd(*args)==1

def is_pandigital(n,start=1):
    z=sorted(list(set(str(n))))
    e=sorted(list(str(n)))
    if e!=z:return False
    for i in range(start,len(str(n))+start):
        if not str(i) in str(n):return False
    return True

class Fraction:
    """A classe for fraction
    Fraction(5,9)-->5/9
    """
    def __init__(self, numerator, denominator=1):
        if isinstance(numerator,Fraction):
            numerator=numerator/denominator
            self._numerator=numerator.numerator
            self._denominator=numerator.denominator
            return 
        if isinstance(denominator,Fraction):
            denominator=numerator/denominator
            self._numerator=denominator.numerator
            self._denominator=denominator.denominator
            return
        
        if denominator<0:
            self._numerator=-int_or_float(numerator)
            self._denominator=-int_or_float(denominator)
        else:
            self._numerator=int_or_float(numerator)
            self._denominator=int_or_float(denominator)
            
        if isinstance(self.numerator,float):
            r=(10**(len_float_part(self.numerator)))
            self.numerator=int_or_float(self.numerator*r)
            self.denominator=int_or_float(self.denominator*r)
            
        if isinstance(self.denominator,float):
            r=(10**(len_float_part(self.denominator)))
            self.numerator=int_or_float(self.numerator*r)
            self.denominator=int_or_float(self.denominator*r)
        
    @property
    def numerator(self):
        return self._numerator

    @property
    def denominator(self):
        return self._denominator

    @numerator.setter
    def numerator(self, value):
	    self._numerator = value

    @denominator.setter
    def denominator(self, value):
        if value<0:
            self._numerator=-self._numerator
            self._denominator=-value
        else:
            self._denominator=value

    def inverse(self):
        """inverse the fraction
        3/4-->4/3"""
        self.numerator,self.denominator=self.denominator,self.numerator

    def value(self):
        """return value off the fraction
        5/2-->2.5"""
        if self.denominator==0:return 0
        return self.numerator/self.denominator
    
    def reducing(self):
        """reduce the fraction
        5703/9801-->1901/3267"""
        d = gcd(abs(self.numerator), abs(self.denominator))
        self.numerator = self.numerator//d
        self.denominator = self.denominator//d

    def reduce(self):
        """return a this reducing fraction"""
        res=Fraction(self)
        res.reducing()
        return res
    
    def __str__(self):
        if self.numerator == 0 or abs(self.denominator) == 1:
            return str(self.numerator*self.denominator)
        return str(self.numerator) + '/' + str(self.denominator)
        
    def __repr__(self):
        return str(self)
    
    def __add__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.denominator+self.denominator*other.numerator,self.denominator*other.denominator).reduce()
    
    def __radd__(self,other):
        return self+other
    
    def __sub__(self,other):
        return self+ -other
    
    def __rsub__(self,other):
        return other+ -self
    
    def __neg__(self):
        return Fraction(-self.numerator,self.denominator)
    
    def __rmul__(self,other):
        return self*other
    
    def __mul__(self,other):
        other=Fraction(other)
        return Fraction(self.numerator*other.numerator,self.denominator*other.denominator).reduce()
        
    
    def __truediv__(self,other):
        if other==1:return self
        return self*(1/other)
    
    def __rtruediv__(self,other):
        if other==1:
            return Fraction(self.denominator,self.numerator)
        return self*(1/other)
    
    def __pow__(self,other):
        if is_integer(other):
            return ipow(self,rint(other))
        other=Fraction(other)
        return Fraction(self.numerator**other,self.denominator**other)
        

    def __rpow__(self,other):
        if is_integer(self):
            return ipow(other,rint(self))
        other=Fraction(other)
        return Fraction(other.value()**(self.value()))
    
    def __lt__(self,other):
        if other==0:return self.numerator<0
        return self-other<0
    
    def __le__(self,other):
        if other==0:return self.numerator<=0
        return self-other<=0
    
    def __eq__(self,other):
        if other==0:return self.numerator==0
        return self-other==0
    
    def __ne__(self,other):
        return not self==other
    
    def __gt__(self,other):
        if other==0:return self.numerator>0
        return self-other>0
    
    def __ge__(self,other):
        if other==0:return self.numerator>=0
        return self-other>=0
    
    def __abs__(self):
        return Fraction(abs(self.numerator),abs(self.denominator))
    
    def __round__(self,ndigits=None):
        return round(self.value(),ndigits)
    
    def floor(self):
        """return the floor value of the fraction"""
        return self.numerator//self.denominator
    def ceil(self):
        """return the ceil value of the fraction"""
        return self.floor+1
    
def create_fraction (num,decimal="",repeat=""):
    """Create Fraction such that a/b=num.decimalrepeatrepeatrepeat...
    param num:integer
    param decimal:integer or string
    param repeat:integer or string
    example:
        create_fraction(num=3,decimal="5",repeat="6")=107/30=3.5666...
        create_fraction(num=1,decimal="0901",repeat="96")=71953/66000=1.0901969696..."""
    if decimal=="":p=0
    else:p=len(str(decimal))
    if repeat=="":
        h=Fraction(int(str(num)+str(decimal)),10**p)
        h.reducing()
        return h
    else:
        P=p+len(str(repeat))
        p=10**p
        P=10**P
        h=Fraction(int(str(num)+str(decimal)+str(repeat))-int(str(num)+str(decimal)),P-p)
        h.reducing()
        return h


def is_happy(n):
    """retrun True if n is happy"""
    return it.last(recurse_orbit(lambda x:digop(x,2),n))==1

def is_triples(a,b,c):
    """Return True if a,b,c is a Pythagoras triples """
    return a*a+b*b==c*c

def triples_prime():
    """generates triple primitives of Pythagoras sorted with the longest side x<y<z"""
    triples=[[5,4,3]]#For sorting with the longest side
    R1=[[1,-2,2],[2,-1,2],[2,-2,3]]
    R2=[[1,2,2],[2,1,2],[2,2,3]]
    R3=[[-1,2,2],[-2,1,2],[-2,2,3]]
    while True:
        c,b,a=triples.pop(0)
        yield a,b,c
        for X in [R1,R2,R3]:
            triple = [sum(x * y for (x, y) in zip([a, b, c], X[i]))for i in range(3)]
            if triple[0]>triple[1]:
                triple[0],triple[1]=triple[1],triple[0]
            triples.append(list(reversed(triple)))#For sorting with the longest side
        triples.sort()
        
        
def triples(): #code form https://stackoverflow.com/a/575728
    """generates all Pythagorean triplets triplets x<y<z"""
    for z in itertools.count(5):
        z2= z*z # time saver
        x= x2= 1
        y= z - 1; y2= y*y
        while x < y:
            x2_y2= x2 + y2
            if x2_y2 == z2:
                yield x, y, z
                x+= 1; x2= x*x
                y-= 1; y2= y*y
            elif x2_y2 < z2:
                x+= 1; x2= x*x
            else:
                y-= 1; y2= y*y	

def de_bruijn(k, n):
    '''De Bruijn sequence for alphabet k and subsequences of length n.
    :param k: int for alphabet in base k else string or list for alphabet k

    https://en.wikipedia.org/wiki/De_Bruijn_sequence
    '''
    try:
        # let's see if k can be cast to an integer;
        # if so, make our alphabet a list
        _ = int(k)
        alphabet = list(map(str, range(k)))

    except (ValueError, TypeError):
        alphabet = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return "".join(alphabet[i] for i in sequence)

def pollard_rho(n):
    """Pollard rho"""
    if is_prime(n):return n
    x=2
    for cycle in itertools.count(1):
        y=x
        a=random.randint(1,10)
        for _ in range(2**cycle):
            x=(x*x+a)%n
            factor=gcd(x-y,n)
            if factor>1:return factor


def pollardp1(n):
    """Pollard p-1"""
    if is_prime(n):return n
    g=n
    B=19
    while g==1 or g==n:
        a=random.randint(3,n)
        logB=math.log(B)
        for q in primegen(end=B):
            e=math.floor(logB/math.log(q))
            a=ipow(a,q**e,n)
        g=gcd(a-1,n)
        if g==1:B=nextprime(B)
    return g

def minimal(iterable,base=10,minimal=None,limit=None):
    """Return a minimal iterable
    see http://www.wiskundemeisjes.nl/wp-content/uploads/2007/02/minimal.pdf"""
    def _in(x,z):
        x=iter(digits(x,base))
        z=digits(z,base)
        q=next(x)
        for a in z:
            if a==q:
                try:
                    q=next(x)
                except:
                    return True
        return False
    minimal=minimal or []
    for i in minimal:
        yield i
    
    for i in iterable:
        if minimal==[]:
            yield i
            minimal.append(i)
        else:
            if limit and  i>limit:break
            if not any(_in(w,i) for w in minimal):
                yield i
                minimal.append(i)
        
    
def repunit_function(digit,start=0,end=0,base=10):
    """Return a function who gives the n-th number 
    in base of shape:startdigit...digitend with n times digits
    :param digit:the digit repeated (lower than base)
    :param start:the beginning of the number gives by the function 
    (if start=0 then there is nothing at the beginning)
    (start must be smaller than base)
    :param end:the end of the number gives by the function 
    (if end=0 then there is nothing at the end)
    (end must be smaller than base)"""
    end="0" if end==0 else "0"+str(end)
    try:
        start=int(start,base)
    except:
        pass
    return lambda n:((base**n-1)//(base-1)*digit+start*base**n)*base**(len(end)-1)+int(end)

def continued_fraction_gen(numerator, denominator=1):
    frac=Fraction(numerator,denominator)
    z = math.floor(frac.value())
    L = []
    if z:
        L = [z]
    frac -= z
    yield z
    while True:
        z = (1 / frac).floor()
        yield z
        frac=1/frac
        frac-=z
        if frac==0:break


def convergent(numerator, denominator=1):
    hn = [0, 1]
    kn = [1, 0]
    for an in continued_fraction_gen(numerator, denominator):
        hn, kn = [hn[1], an * hn[1] + hn[0]], [kn[1], an * kn[1] + kn[0]]
        yield Fraction(hn[1], kn[1])


if __name__ == "__main__":
    print(list(divisors(108)))
