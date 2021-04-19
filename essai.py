from turtle import *
from random import *
from time import *
from math import sqrt,floor
from copy import deepcopy
import math_2 as mt
import itertools
import itertools_2 as it


def tria(n):
    return n*(n+1)/2

def polygone(n,lg):
    angle=360/n
    for i in range(n):
        left(angle)
        forward(lg)


def emboite(n,lg,delta):
    if lg > 0:
        for i in range(n):
            forward(lg)
            left(360/n)
        emboite(n,lg-delta,delta)
   
        

  
def dervicheTourneur(nbTour, n, lg, angle):
    if nbTour != 0:
        polygone(n,lg)
        left(angle)
        dervicheTourneur(nbTour-1, n, lg, angle)
    
        
def  spirale(cote, delta, angle, n=30):
    if n>0:
        forward(cote)
        left(angle)
        spirale(cote+delta, delta, angle, n-1) 

#
def tracer(f):
    decalage = 0
    def g(L,y=0,x=0,):
	    nonlocal decalage
	    print('|        ' * decalage, end='')
	    print('|Appel {}({},{})'.format(f.__name__,x,y))
	    decalage +=1
	    imagefx = f(x)
	    print('|        ' * decalage, end='')
	    print('|-> retourne {}'.format(imagefx) )
	    decalage -= 1
	    return imagefx
    return g
#





def testpui2(n,x=1):
    if n==1: return True
    else:
        if n%2==1: return False
        else:
            if 2**x<n:
                if testpui2(n,x+1):return True
            elif 2**x==n:return True
            else:return False


   
        
def scrolltext(mot):
    """permet d'afficher un text en le 'scrollant' """
    n=str(mot)
    for letre in n:
        print(letre, end="")
        if letre =="." or letre=="?"or letre=="!":sleep(0.6)
        if letre==",":sleep(0.3)
        sleep(0.04)

def fac(n):
    if n<2:return n
    else: return n*fac(n-1)

def crible(m,n=1,l=[],L=[]): 
    if n==1:return crible(m,2,l,L)
    else:
        if not n in L :
            l.append(n)
            x=2
            while n*x<m+1:
                if not n*x in L:L.append(n*x)
                x+=1
        if n+1>m:return l
        else : return crible(m,n+1,l,L)


def dicho(l,x,i=0):
    if len(l)==1 and l[0]!=x:
        return -1
    n=l[len(l)//2]
    if x==n:return len(l)//2 +i
    elif x<n:return dicho(l[:len(l)//2],x,i)
    else:return dicho(l[len(l)//2:],x,i+len(l)//2)

def mini(L) :
    a = min(L)
    L.remove(a)
    return a

def tri(L,T=[]):
    if L==[]:return T
    else:
        T.append(mini(L))
        return tri(L,T)

def ite(n,maxi=1,mini=0):
    for i in range(n):
        yield randint(mini,maxi)

def lookandsay(n):
    m=""
    n=str(n)
    i=0
    while True:
        if i==len(n): break
        try :
            if n[i]==n[i+1]:
                try:
                    if n[i+1]==n[i+2]:
                        m=m+"3"+n[i]
                        i+=3
                    else:
                        m=m+"2"+n[i]
                        i+=2
                except:
                    m=m+"2"+n[i]
                    i+=2
            else:
                m=m+"1"+n[i]
                i+=1
        except:
            m=m+"1"+n[i]
            return m
    return m

def miroir(m):
    mot=str(m)
    if len(mot)<2:return mot
    else:return mot[-1]+miroir(mot[0:-1])

def testpalindrome(m):
    mir=miroir(m)
    return str(m)==mir

def quenine(B):
    M=[]
    while True:
        if B==[]: break
        M.append(B.pop(-1))
        if B==[]: break
        M.append(B.pop(0))
    return M

def testtri(L):
    if len(L)==1: return True
    for i in range(len(L)-1):
        try:
            if L[i]>L[i+1]:return False
        except:
            break
    return True 

def testquenine(n):
    L=[i for i in range(1,n+1)]
    n=0
    while True:
        L=quenine(L)
        n+=1
        if testtri(L):return n
def cherchequenine(n):
    queneau=[]
    premier=crible(n)
    queneau_premier=[]
    queneau_palindrome=[]
    for i in range(1,n+1):
        fois=testquenine(i)
        if fois==i:
            queneau.append(i)
            if i in premier:
                queneau_premier.append(i)
            if testpalindrome(i):
                queneau_palindrome.append(i)
    print("Les nombres de Queneau sont:",str(queneau)[1:-1])
    print()
    print("Les nombres de Queneau premier sont:",str(queneau_premier)[1:-1])
    print()
    print("Les nombres de Queneau palindromes sont:",str(queneau_palindrome)[1:-1])
    print()

def luckynum(n):
    L=[y for y in range(1,n+1)]
    i=2
    f=0
    while i-1<len(L):
        x=i
        #print("x=",x)
        f+=1
        #print("f=",f)
        a=[]
        while x-1<n:
            try:
                a.append(L[x-1])
                #print("on enleve a la place",x-1,"le nombre",a)
            except:
                pass
            x+=i
        for e in a:
            L.remove(e)
        i=L[f]
        #print("i=",i)
    return L

def int_to_list(n):
    n=str(n)
    L=[]
    for i in n:
        L.append(int(i))
    return L
def lookallandsay(n):
    m=""
    c=int_to_list(n)
    while True:
        e=c[0]
        #print("e=",e)
        f=0
        a=[]
        for t in c:
            if t==e:
                f+=1
                a.append(t)
        m+=str(f)+e
        #print(c)
        for x in a:
            c.remove(x)
        if c==[]:
            break
    return m
#    
def iténumfig(k):
    """k est le nombre de cote du polygone"""
    x, y = 1, 1
    k-=2
    yield 0
    while True:
        yield x
        x, y = x + y + k, y + k
#
def testhappy(n):
    y=n
    while True:
        m=0
        for i in str(y):
            m+=int(i)**2
        if m<=1: return True
        elif m==4: return False
        y=m

def copy(L):
    if L==[]:return []
    else: return [x for x in L]
    
def partition(n):
    L=[]
    if n==0:
        return [],0
    if n==1:
        return [1],1
    else:
        for t in range(n-1,-1,-1):
            k=n-t
            par=partition(t)[0]
            for y in par:
                if isinstance(y,list):
                    L.append(y+[k])
                else:
                    L.append(par+[k])
        L.append([n])
        for e in L:
            e.sort()
        A=[]
        for a in L:
            if not a in A: A.append(a)
        return A,len(A)




def huitres(n):
    S=""
    f=0
    v=n
    x=0
    while True:
        if n==0:break
        T=False
        if n%12==0:
            T=True
            n//=12
            if n==1: n=0
            if S=="" or S[13:16]=="que":
                S+=" une"
            S+=" douzaine"
            if n!=0:
                S+=" de"
        elif n%6==0:
            T=True
            n//=6
            if n==1: n=0
            if S=="" or S[13:16]=="que":
                S+=" une"
            S+=" demie-douzaine"
            if n!=0:
                S+=" de"
        elif n%3==0:
            T=True
            n//=3
            if n==1: n=0
            if S=="" or S[13:16]=="que":
                S+=" une"
            S+=" demie-demie-douzaine"
            if n!=0:
                S+=" de"
        elif n%11==0:
            T=True
            n//=11
            if n==1: n=0
            S+=" un peu moins d'une douzaine"
            if n!=0:
                S+=" de"
        elif n%13==0:
            T=True
            n//=13
            if n==1: n=0
            S+=" un peu plus d'une douzaine"
            if n!=0:
                S+=" de"
        elif n%7==0:
            T=True
            n//=7
            if n==1: n=0
            S+=" un peu plus d'une demie-douzaine"
            if n!=0:
                S+=" de"
        elif n%5==0:
            T=True
            n//=5
            if n==1: n=0
            S+=" un peu moins d'une demie-douzaine"
            if n!=0:
                S+=" de"
        elif n%4==0:
            T=True
            n//=4
            if n==1: n=0
            S+=" un peu plus d'une demie-demie-douzaine"
            if n!=0:
                S+=" de"
        elif n%2==0:
            T=True
            n//=2
            if n==1: n=0
            S+=" un peu moins d'une demie-demie-douzaine"
            if n!=0:
                S+=" de"
        if not(T) and x==0 :
            if f!=0:
                n=v
            n+=1
            x=1
            S="*un peu moins que"
        elif not(T) and x==1 :
            n=v
            n-=1
            x=2
            S="*un peu plus que"
        elif not(T) and x==2 :
            return "impossible d'huitres" 
            
        T=False
        f+=1
    return S+" d'huitres"


def roli(n):
    C=["r","l","t","m","k","f","s","p","ch","n"]
    V=["o","i","ou","you","a","ya","é","yé","wi","yo"]
    f=len(str(n))%3
    r=0
    m=""
    for i in enumerate(str(n)):
        if f==0:
            if r==0 or r==2:
                m+=C[int(i[1])]
                if r==2 and not(int(i[0])==len(str(n))-1):
                    m+="-"
                r+=1
                r=r%3
            else:
                m+=V[int(i[1])]
                r+=1
                r=r%3
        elif f==2:
            if r==0:
                m+=C[int(i[1])]
                r+=1
            else:
                m+=V[int(i[1])]
                if not(int(i[0])==len(str(n))-1):
                    m+="-"
                r=0
                f=0
        else:
            m+=V[int(i[1])]
            if not(int(i[0])==len(str(n))-1):
                m+="-"
            r=0
            f=0          
    return m

def créefraction(n,d="",dp=""):
    if d=="":p=0
    else:p=len(str(d))
    if dp=="":
        h=Fraction(int(str(n)+str(d)),10**p)
        h.simplifie()
        return h
    else:
        P=p+len(str(dp))
        p=10**p
        P=10**P
        h=Fraction(int(str(n)+str(d)+str(dp))-int(str(n)+str(d)),P-p)
        h.simplifie()
        return h
    
def trouvlisinbri(L,n,r=0):
    if L==[]: return False
    if not(r+1<=len(L)):return False
    if isinstance(L[r],list): return trouvlisinbri(L[r],n,0) or trouvlisinbri(L,n,r+1)
    elif r+1<=len(L):
        if L[r]==n: return True
        else : return trouvlisinbri(L,n,r+1)
    else: return False
    
def trouvenumtheo(n):
    L=[]
    a=1
    while True:
        t=0
        for i in range(a):
            t+=i
        r=a
        t2=0
        while True:
            t2+=r
            if t==t2:L.append([t,a-1,r])
            elif t2>t:break
            r+=1
        if t>=n: break
        a+=1
    return L


        
def decompo(x,n):
    r=2
    L=[]
    T=Fraction(x)
    a=Fraction(1,2)
    i=0
    n-=1
    while True:
        while True:
            a=Fraction(1,r)
            if a<T:break
            r+=1
        L.append(a)
        T=T-a
        i+=1
        if T.numerateur==1 and i>=n:
            L.append(T)
            break
    return sorted(L)

def numdiv(n):
    L=[]
    for i in range(1,round((n/2))+1):
        if n%i==0:
            L.append(i)
    return L+[n],len(L)+1
def divieuclid(n,d,repet=10):
    a=0
    L=[]
    while a<repet:
        if n==0:return L
        elif n<d:
            n*=10
            L.append(0)
        else:
            L.append(n//d)
            n%=d
            a+=1
            n*=10
    return L

def xor(A,B):
    if A and B:return False
    return A or B

def probleme33(n):
    if n.val()>=1:return False
    a=str(n.numerateur)[0]
    b=str(n.numerateur)[1]
    c=str(n.denominateur)[0]
    d=str(n.denominateur)[1]
    if a==c:
        h=Fraction(int(b),int(d))
    elif a==d:
        h=Fraction(int(b),int(c))
    elif b==d:
        h=Fraction(int(a),int(c))
    elif b==c:
        h=Fraction(int(a),int(d))
    else:return False
    return h==n

def solution(n,ng=False):
    a=1
    m=10000
    if ng:
        ng=-1
    else: ng=0
    while True:
        for b in range(((a+1)*ng)+1,a+1):
            for c in range(((a+1)*ng)+1,b+1):
                T=Fraction(a,b+c)
                V=Fraction(b,a+c)
                A=Fraction(c,a+b)
                r=T+V+A
                if abs(n-r)<m:
                    print(r,(a,b,c))
                    m=abs(n-r)
                if r==n:
                    return a,b,c
        a+=1
def max2(L):
    D=[]
    for i in L:
        if D==[]:
            D.append(i)
            continue
        if isinstance(i,tuple) or isinstance(i,list):
            r=i[0]
        else:r=i
        if isinstance(D[0],tuple) or isinstance(D[0],list):
            z=D[0][0]
        else:z=D[0]
        if z==r:D.append(i)
        elif z<r:
            D=[i]
    return D
        
def exmaths(x):
    def f(n,N,Len=1,L=[]):
        F=numdiv(n)[0]
        for i in itertools.count(2):
            if n*i>N:break
            F.append(n*i)
        A=[]
        for r in F:
            if not r in L and not r in A:A.append(r)
        if len(L)==N:return Len,L
        if A==[]:return Len,L
        return max([f(z,N,Len+1,L+[z]) for z in A])
    return max([f(e,x,L=[e]) for e in range(1,x+1)])

def zeta(p,n):
    a=Fraction(1,1)
    t=0
    r=0
    while True:
        r+=1
        t=a+t
        a=Fraction(1,r**p)
        if r==n:return t

def glouton(N,Lpd,P=[]):
    if N==0:return P
    elif N==1:return P+[1]
    Lpd=sorted(Lpd)
    Lpd.reverse()
    L=[]
    for i in Lpd:
        if i<=N:L.append(i)
    return min([glouton(N-x,Lpd,P+[x]) for x in L],key=len)

def num_prime(n):
    z=1/(10**n)
    a=1
    m=0,0
    while True:
        r=2
        L=[]
        while True:
            s=a**(2**r)
            if not mt.is_prime(floor(s)):break
            L.append(floor(s))
            r+=1
        if m[0]<r-2:m=r-2,a,L
        a+=z
        a=round(a,n)
        if a>=2:return m

def auto_des(n):
    r=list(str(n))
    m=""
    v=0
    j=[]
    if not "0" in r:r.append("0")
    while True:
        a=0
        for i in r:
            if i==str(v):
                a+=1
                j.append(i)
        for z in j:
            r.remove(z)
                
                
        m+=str(a)
        v+=1
        j=[]
        if r==[]:return int(m+"1")if "0" in m else int(m+"0")
        

def isdiffsquares(n):
    for a in range(1,n):
        a2=a*a
        if a2>n:return False
        x=n-a2
        if x%(2*a)==0:yield(x//(2*a)+a,x//(2*a))

class iter2:
    def __init__(self,iterable=None):
        if iterable is None:
            self.iterable=it.emply()
        else:
            self.iterable=iterable
        self.start=it.emply()
        self.end=it.emply()

    def __iter__(self):
        for i in self.start:
            yield i

        for x in self.iterable:
            yield x

        for y in self.end:
            yield y

    def add(self,iterable):
        if it.is_emply(iterable):
            self.end=self.end
        elif it.is_emply(self.end):
            self.end=iterable
        else:
            self.end=iter2(self.end)
            self.end.add(iterable)

    def __add__(self,other):
        if not it.is_iterable(other):
            other=[other]
        t=iter2(self.iterable)
        t.start=self.start
        t.add(self.end)
        t.add(other)
        return t
        
    def __radd__(self,other):
        if not it.is_iterable(other):
            other=[other]
        t=iter2(self.iterable)
        t.start=other
        t.end=self.end
        return t
       
    def __str__(self):
        res=""
        try:
            if not it.is_emply(self.start):
                res+=str(self.start)+"+"
        except:
            res+=self.start.__class__.__name__+"+"

        try:
            if not it.is_emply(self.iterable):
                res+=str(self.iterable)
            else:
                res+="[]"
        except:
            res+=self.iterable.__class__.__name__

        try:
            if not it.is_emply(self.end):
                res+="+"+str(self.end)
        except:
            res+="+"+self.end.__class__.__name__

        return res
    
    def __repr__(self):
        return str(self)
for i in range(2,10):
    m=it.map_deep(lambda x:(mt.mul(x),x),partition(i)[0],0)
    print(i,max(m,key=lambda x:x[0]))
    
