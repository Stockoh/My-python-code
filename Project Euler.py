from math import sqrt,floor
from time import time
import math_2 as mt
import itertools_2 as it
def produitchiffre(n):
    t=1
    if isinstance(n,int):
        for i in str(n):
            t*=int(i)
    else:
        for i in n:
            t*=int(i)
    return t


def probleme8(s,d):
    s=str(s)
    m=0,0
    a=0
    while True:
        i=s[a:a+d]
        r=produitchiffre(i)
        if r>m[0]:
            m=r,i
        a+=1
        if a+d==len(s)+1: break
    return m

def probleme16(n):
    t=0
    for i in str(n):
        t+=int(i)
    return t
def probleme20(n):
    t=1
    for i in range(1,n+1):
        t*=i
    return probleme16(t),t



def memorise(f):
    memoire = {}
    def seSouvenir(L,x=0,y=0):
        if (x,y) not in memoire : memoire[(x,y)] = f(L,x,y)
        return memoire[(x,y)]
    return seSouvenir


def probleme15(x,y):
    if x<0 or y<0: return 0
    elif x==0 and y==0: return 1
    elif x==0: return y
    elif y==0: return x
    else:
        t=g(x-1,y)
        y=g(x,y-1)
        return t+y


def ishexa(n):
    for i in range(1,n//2+1):
        if n/i==2*i-1:return True,i
    return False,0

def tronqueg(n):
    n=str(n)
    n=n[1:]
    while n!="":
        if not(testprimes(int(n))):return False
        n=n[1:]
    return True

def tronqued(n):
    n=str(n)
    n=n[:-1]
    while n!="":
        if not(testprimes(int(n))):return False
        n=n[:-1]
    return True


def probleme11(L,n=4):
    m=0,[]
    x,y=0,0
    while True:
        #print(x,y)
        if len(L[y])>=x+1:
            A=[L[y][x+a] for a in range(min(len(L[y])-x,n))]
            #print(min(len(L[y])-x,n))
        else:A=[]
        if len(L)>=y+1:
            B=[L[y+a][x] for a in range(min(len(L)-y,n))]
        else:B=[]
        if  len(L[y])>=x+1 and len(L)>=y+1:
            C=[L[y+a][x+a] for a in range(min(len(L)-y,n,len(L[y])-x))]
        else:C=[]
        if  len(L[y])>=x+1 and len(L)>=y+1:
            D=[L[y+a][x-a] for a in range(min(len(L)-y,n,len(L[y])+x))]
        else:D=[]
        r=produitchiffre(A)
        if m[0]<r :m=r,A
        r=produitchiffre(B)
        if m[0]<r:m=r,B
        r=produitchiffre(C)
        if m[0]<r:m=r,C
        r=produitchiffre(D)
        if m[0]<r:m=r,D
        if x+1>=len(L[y]):
            if y+1>=len(L):
                return m
            else:
                x=0
                y+=1
        else:
            x+=1

def probleme206(n):
    a=0
    x=1
    for i in str(n):
        #print(i,a,x)
        if a==0:
            if int(i)!=x: return False
            x+=1
        a+=1
        a%=2
        x%=10
    return True

def testLychrel(n):
    a=0
    while True:
        n+=int(miroir(n))
        a+=1
        if testpalindrome(n):return False,a
        elif a==50:return True,0
def probleme55(n):
    L=[]
    for i in range(1,n):
        r=testLychrel(i)
        if r[0]:L.append([i])
    return len(L)
def int_to_list(n):
    n=str(n)
    L=[]
    for i in n:
        L.append(int(i))
    return L

def isrebon(n):
    m=int_to_list(n)
    b=miroir(m)
    c=sorted(m)
    if m==c or c==b:return False
    return True

def probleme112(n):
    a=100
    rebon=0
    n/=100
    while True:
        if isrebon(a):rebon+=1
        if rebon/a==n:return a
        a+=1

def sommepower(n):
    q=probleme16(n)
    a=1
    if q==1:return False
    while True:
        if q**a==n:return True
        elif q**a<n:a+=1
        else:return False
def is_reversible(n):
    if miroir(n)[0]=="0":return False,0
    v=int(miroir(n))+n
    for i in str(v):
        if int(i)%2==0:return False,0
    return True,miroir(n),v
def probleme145(n):
    m=0
    for i in range(n):
        if is_reversible(i):m+=1
    return m
        

def probleme46(n):
    for x in range(2,n):
        if testprimes(x):
            for y in range(1,n//2):
                if x+(2*(y*y))==n:return True,x,y
    return False,0,0
def numdiv(n):
    L=[]
    for i in range(1,round((n/2))+1):
        if n%i==0:
            L.append(i)
    return L
def sommeliste(L):
    t=0
    for i in L:
        t+=i
    return t
def probleme21(n):
    m=0
    L=[]
    for a in range(n):
        b=sommeliste(numdiv(a))
        r=sommeliste(numdiv(b))
        if r==a and b!=a:
            m+=a
            L.append(a)
            L.append(b)
    A=[]
    for z in L:
        if not z in A:A.append(z)
    return m,A

def testquadratic(a,b,affi=False):
    n=0
    while True:
        r=(n**2)+(a*n)+b
        #print(r)
        if r<0:return n,r
        elif not mt.is_prime(r):
            return n,r
        if affi:print(r)
        n+=1

def probleme30(n):
    y=n
    m=0
    for i in str(y):
        m+=int(i)**5
    return m
def probleme43(n):
    n=str(n)
    if not int(n[1]+n[2]+n[3])%2==0:return False
    elif not int(n[2]+n[3]+n[4])%3==0:return False
    elif not int(n[3]+n[4]+n[5])%5==0:return False
    elif not int(n[4]+n[5]+n[6])%7==0:return False
    elif not int(n[5]+n[6]+n[7])%11==0:return False
    elif not int(n[6]+n[7]+n[8])%13==0:return False
    elif not int(n[7]+n[8]+n[9])%17==0:return False
    return True
               

@it.memoize
def partitionspiece(n):
    L=[]
    if n==0:
        return [],0
    if n==1:
        return [1],1
    else:
        par=partitionspiece(n-1)[0]
        for y in par:
                if isinstance(y,list):
                    L.append(y+[1])
                else:
                    L.append(par+[1])
        if n>=2:
            par=partitionspiece(n-2)[0]
            for y in par:
                if isinstance(y,list):
                    L.append(y+[2])
                else:
                    L.append(par+[2])
            if n>=5:
                par=partitionspiece(n-5)[0]
                for y in par:
                    if isinstance(y,list):
                        L.append(y+[5])
                    else:
                        L.append(par+[5])
                if n>=10:
                    par=partitionspiece(n-10)[0]
                    for y in par:
                        if isinstance(y,list):
                            L.append(y+[10])
                        else:
                            L.append(par+[10])
                    if n>=20:
                        par=partitionspiece(n-20)[0]
                        for y in par:
                            if isinstance(y,list):
                                L.append(y+[20])
                            else:
                                L.append(par+[20])
                        if n>=50:
                            par=partitionspiece(n-50)[0]
                            for y in par:
                                if isinstance(y,list):
                                    L.append(y+[50])
                                else:
                                    L.append(par+[50])
                            if n>=100:
                                par=partitionspiece(n-2)[0]
                                for y in par:
                                    if isinstance(y,list):
                                        L.append(y+[2])
                                    else:
                                        L.append(par+[2])
                                if n>=200:
                                    par=partitionspiece(n-2)[0]
                                    for y in par:
                                        if isinstance(y,list):
                                            L.append(y+[2])
                                        else:
                                            L.append(par+[2])
    A=[]
    for i in L:
        i.sort()
        if not i in A: A.append(i)
    return A,len(A)

def probleme50(n):
    t=2
    mp=2
    ml=0
    l=1
    A=[2]
    R=[]
    for i in range(3,10**n,2):
        if testprimes(i):
            t+=i
            A.append(i)
            l+=1
            if t>10**n:break
            if testprimes(t) and ml<l :
                ml=l
                R=A
                mp=t
            
    t=0
    l=0
    A=[]
    for i in range(3,10**n,2):
        if testprimes(i):
            t+=i
            A.append(i)
            l+=1
            if t>10**n:break
            if testprimes(t) and ml<l :
                ml=l
                R=A
                mp=t
    a=2
    while True:
        t=0
        l=0
        A=[]
        for i in range(3+a,10**n,2):
            if testprimes(i):
                t+=i
                A.append(i)
                l+=1
                if t>10**n:break
                if testprimes(t) and ml<l:
                    ml=l
                    R=A
                    mp=t
                    #print(R)
        a+=2
        if a==10**n:break
    return mp,ml
def squarefree(n):
    z=list(mt.factorise(n))
    for e,i in z :
        if i>1:return False
    return True,z
inf=float("inf")

def iterfibosquarefree(n=inf):
    p=0
    for i in iterfibo():
        z=squarefree(i)
        if z:
            yield i,z[1]
            p+=1
            if p==n:break

def digitpower(n):
    a=len(str(n))
    q=1
    if a==1:return False
    while True:
        if q**a==n:return True
        elif q**a<n:q+=1
        else:return False

@it.memoize
def probleme18(L,y=0,x=0):
    if y+1==len(L):return L[y][x]
    else: return L[y][x]+max(probleme18(L,y+1,x),probleme18(L,y+1,x+1))



def testleapyears(year):
    return year%4==0 and not (year%100==0 and not year%400==0)
@it.timeit
def problem19(start=1901,end=2001):
    len_months=[31,28,31,30,31,30,31,31,30,31,30,31]
    m=0
    year=start
    numday=2
    day=0
    months=0
    while True:
        day+=1
        numday+=1
        numday%=7
        if (day==len_months[months] and not ( months==1 and  testleapyears(year))) or (testleapyears(year) and months==1 and day==29):
            months+=1
            months%=12
            day=0
            if months==0:
                year+=1
        if year==end:return m
        if day==0 and numday==0:
            m+=1
            #print(day+1,"/",months+1,"/",year)
def probleme66(D):
    if mt.is_square(D):return 0,0
    a=1
    while True:
        for b in range(1,a):
            r=a**2-(D*(b**2))
            print(r)
            if r==1:return a,b
            if r<1:break
        a+=1

def copy(s):
    return [x for x in s]
def int2(m):
    if m=="":return 0
    return int(m)
def probleme719(n):
    r=mt.isqrt(n)
    if sum(int_to_list(n))==r:
        return True
    n=str(n)
    for i in range(len(n)-1):
        #print(int_to_list(n[:i]))
        #print("%d+%d+%d=%d"%(int2(n[i]+n[i+1]),sum(int_to_list(n[i+2:])),sum(int_to_list(n[:i])),int2(n[i]+n[i+1])+sum(int_to_list(n[i+2:]))+sum(int_to_list(n[:i]))))
        if int2(n[i]+n[i+1])+sum(int_to_list(n[i+2:]))+sum(int_to_list(n[:i]))==r:return True
    for e in range(len(n)-2):
        if int2(n[e]+n[e+1]+n[e+2])+sum(int_to_list(n[e+3:]))+sum(int_to_list(n[:e]))==r:return True
    for z in range(len(n)-3):
        if int2(n[z]+n[z+1]+n[z+2]+n[z+3])+sum(int_to_list(n[z+4:]))+sum(int_to_list(n[:z]))==r:return True
    if int2(n[:2])+int2(n[2:4])+sum(int_to_list(n[4:]))==r:return True
    if int2(n[-2:])+int2(n[-4:-2])+sum(int_to_list(n[:-4]))==r:return True
    if int2(n[:2])+int2(n[-2:])+sum(int_to_list(n[2:-2]))==r:return True
    
    return False
def permutations(s):
    s.sort()
    def f(s):
        if len(s)<=1:yield s[0]if isinstance(s,list)  and s!=[] else ""
        for i in s:
            r=copy(s)
            r.remove(i)
            e=f(r)
            for d in e:
                r=str(i)+str(d)
                if len(r)==len(s):
                    yield r
    for i,e in enumerate(f(s)):
        if i%2==0:yield e
def probleme49(L):
    r=set(str(L[0]))
    for i in L:
        if not r==set(str(i)):return False
        if not mt.is_prime(i):return False
        r=set(str(i))
    return True

def ondiag(x,y):
    return abs(x)==abs(y)

def countrepate(start=1,reapt=2):
    e=start
    while True:
        yield e,True
        for i in range(reapt-1):
            yield e,False
        e+=1

def probleme28(c):
    m=0
    x=0
    y=0
    v=1
    r=0
    direc=(0,1)
    for i,change in countrepate():
        if change:
            r+=1
        if direc==(0,1):direc=(1,0)
        elif direc==(1,0):direc=(0,-1)
        elif direc==(0,-1):direc=(-1,0)
        elif direc==(-1,0):direc=(0,1)
        for i in range(r):
            if ondiag(x,y):
                m+=v
            v+=1
            x+=direc[0]
            y+=direc[1]
            if v-1==c*c:return m

def list_to_int(L):
    t=""
    for i in L:
        t+=str(i)
    return int(t)

def probleme56(n):
    m=0,0,0
    for a in range(2,n):
        for b in range(2,n):
            r=mt.mul(int_to_list(a**b))
            if r>m[0]:
                m=r,a,b,a**b
                print(m)
    return m

def is_pentagonal(n):
    '''
    :return: True if x is a pentagonal number
    '''
    if n<1:
        return False
    n=1+24*n
    s=mt.isqrt(n)
    if s*s != n:
        return False
    return mt.is_integer((1+s)/6.0)

def iterfibo():
    a=1
    b=0
    yield 0
    while True:
        yield a
        a,b=a+b,a
def penta(n):
    return int(n*(3*n-1)/2)

def sum_abundant(n):
    if n%2==0:
        if n>46:return True
        if mt.is_perfect(n//2)==1:return True
    elif n<957:return False
    for i in range(12,n-11):
        if mt.is_perfect(i)==1:
            if mt.is_perfect(n-i)==1:return True
            if i<945:
                if n%2==1 and n-i<945:return False
    return False

def primeConway():
    n=2
    L=[mt.Fraction(17,91),mt.Fraction(78,85),mt.Fraction(19,51),mt.Fraction(23,38),mt.Fraction(29,33),mt.Fraction(77,29),mt.Fraction(95,23),mt.Fraction(77,19),mt.Fraction(1,17),mt.Fraction(11,13),mt.Fraction(13,11),mt.Fraction(15,2),mt.Fraction(1,7),mt.Fraction(55,1)]
    while True:
        for i in L:
            a=n*i
            if mt.is_integer(a):break
        n=int(a.value())
        yield n

def sumoffsquares(n):
    r=mt.isqrt(n)
    squares=[x*x for x in range(0,r+1)]
    a=1
    for e,i in enumerate(squares):
        if i>=n/2:
            a=e
            break
    while a<=r:
        a2=squares[a]
        b2=n-a2
        if b2 in squares:
            yield a,mt.isqrt(b2)
        a+=1
        
def suminverse(n):
    a=mt.Fraction(1,n)
    frac=mt.Fraction(1,n)
    maxi=frac/2
    b=0
    L=[]
    while b<=maxi:
        b=frac-a
        #print(a,b,maxi)
        if b.numerator==1:
            yield a,b
            L.append(b)
        a.denominator+=1

def suite_farey(n):
    a,b,c,d=0,1,1,n
    yield mt.Fraction(a,b)
    while c<n:
        k=int((n+b)//d)
        e=k*c-a
        f=k*d-b
        a,b,c,d=c,d,e,f
        yield mt.Fraction(a,b)

print(1+sum(mt.phi(n) for n in range(1,1000001)))
