import math
import math_2 as mt
import itertools
import itertools_2 as it

def str_base(num,base):
    if isinstance(num,str):return num
    return mt.str_base(num,base,
                       numerals='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

class Digits:
    def __init__(self,digits,base):
        digits=int(digits)
        if digits>=base:raise ValueError("digits must be smaller than base")
        self.digits=digits
        if isinstance(self.digits,str):
            self.digts=int(self.digits,base)
        self.base=base
    
    def __repr__(self):
        return str_base(self.digits,self.base)+"*"
    
    def __mul__(self,other):
        if self.digits==0:return "0"*other
        return ((self.base**other)-1)//(self.base-1)*self.digits

    def __pow__(self,other):
        return str_base(self*other,self.base)

class DigitsList:
    def __init__(self,*args,base):
        if len(args)==1:
            if isinstance(args[0],DigitsList):
                self.list=args[0].list[:]
                self.base=args[0].base
                return
            if isinstance(args[0],str):
                try:
                    int(args[0],base)
                except:
                    raise TypeError("'%s' isn't a base %s number"%(args[0],base))
                self.list=[args[0]]
                self.base=base
                return
            if it.is_iterable(args[0]):
                self.list=list(args[0])
            else:
                self.list=[args[0]]
        else:
            self.list=list(args)
        self.base=base
        self.list=list(map(lambda x:str_base(x,self.base),self.list))
        self.list.sort(key=lambda x:int(x,self.base))
        self.list=list(it.unique(self.list))
        
    def __repr__(self):
        res="{"
        for i in self:
            if isinstance(i,str):res+=i+","
            else:res+=str_base(i,self.base)+","
        res=res[:-1]
        res+="}"
        return res

    def __iter__(self):
        return iter(self.list)

    def __add__(self,other):
        if isinstance(other,(str,int)):
            return DigitsList(self.list+[other],base=self.base)
        if not isinstance(other,DigitsList):
            raise TypeError
        if self.base!=other.base:raise Exception("base must be equal")
        return DigitsList(self.list+other.list,base=self.base)

    def __mul__(self,other):
        if isinstance(other,int):
            other=str_base(other,base=self.base)
        if isinstance(other,str):
            other=DigitsList([other],base=self.base)
        if it.is_iterable(other):
            if it.is_emply(other):
                return self
            other=DigitsList(other,base=self.base)
        if self.base!=other.base:raise Exception("base must be equal")
        return DigitsList(list(map(lambda x:x[0]+x[1]
                                   ,itertools.product(self.list,other.list))),base=self.base)

    def __rmul__(self,other):
        if it.is_iterable(other):
            if it.is_emply(other):
                return self
        return DigitsList(other,base=self.base)*self

    def __pow__(self,other):
        res=[]
        for _ in range(other):
            res=self*res
        return res

    def remove(self,value):
        self.list.remove(value)

    def __getitem__(self,index):
        try:
            return self.list[index]
        except:raise IndexError

    def __setitem__(self,index,value):
        try:
            self.list[index]=value
        except:raise IndexError
        
class Family:
    def __init__(self,*args,base):
        if len(args)==1:
            if isinstance(args[0],Family):
                self.list=args[0].list[:]
                self.base=args[0].base
                return 
            if isinstance(args[0],DigitsList):
                self.list=[args[0]]
                self.base=args[0].base
                return 
            if it.is_iterable(args[0]):
                args=list(args[0])
            else:
                args=[args[0]]
        self.base=base
        self.list=[]
        for i in args:
            if isinstance(i,int):
                i=str_base(i,self.base)
            if isinstance(i,str):
                try:
                    int(i,base)
                except:
                    raise TypeError("'%s' isn't a base %s number"%(i,base))
                self.list.append(i)
            elif it.is_iterable(i):
                if it.is_emply(i):pass
                if len(i)==1:self.list.append(Digits(i[0],base=self.base))
                else:self.list.append(DigitsList(i,base=self.base))

    def __repr__(self):
        res=""
        for i in self:
            if isinstance(i,str):
                res+=i
            elif isinstance(i,Digits):
                res+=str(i)
            else:
                res+=str(i)+"*"
        return res

    def __iter__(self):
        return iter(self.list)

    def iternum(self):
        return filter(lambda x:isinstance(x,str),self)

    def iternotnum(self):
        return filter(lambda x:not isinstance(x,str),self)
    
    def __getitem__(self,index):
        try:
            return self.list[index]
        except:raise IndexError

    def __setitem__(self,index,value):
        try:
            self.list[index]=value
        except:raise IndexError
        
    def notnumindex(self):
        res=[]
        for e,i in enumerate(self):
            if not isinstance(i,str):
                res+=[e]
        return res

    def numindex(self):
        res=[]
        for e,i in enumerate(self):
            if isinstance(i,str):
                res+=[e]
        return res
    
    def pop(self,index=-1):
        return self.list.pop(index)
    
    def __call__(self,n,integer=False):
        if n==0:
            if integer:
                return int(str(Family(list(self.iternum())
                                      ,base=self.base)),base=self.base)
            else:
                return str(Family(list(self.iternum()),base=self.base))
        res=[]
        L=self.notnumindex()
        if not L:
            return self(0,integer)
        for i in itertools.product(*map(lambda x:[x**n] 
                                        if isinstance(x,Digits) else x**n,self.iternotnum())):
            z=list(self)
            for index,string in zip(L,i):
                z[index]=string
            res.append(int("".join(z),base=self.base) if integer else "".join(z))
        return res

    def contain_prime(self):
        if self.is_num():return mt.is_prime(self(0,True))
        return not(1<mt.gcd(*self(1,True),self(0,True))<self(0,True))

    def lemma19(self):
        try: 
            res=[]
            L=it.first(self.notnumindex())
            a=Family(self,base=self.base)
            a.pop(L)
            res.append(a)
            if isinstance(self[L],Digits):
                t=[str_base(self[L].digits,self.base)]
            else:
                t=self[L]
            for i in t:
                a=Family(self,base=self.base)
                a.list=a.list[:L]+[i]+a.list[L:]
                res.append(a)
            return res
        except:
            return [Family(self,base=self.base)]
    
    def is_num(self):
        return self(0,True)==self(1,True)

    def lemma21(self,minimal,k):
        try:
            L=it.first(self.notnumindex())
            x=DigitsList(self[L],base=self.base)
            for i in self[L]:
                i=Digits(i,base=self.base)
                a=Family(list(self.iternum()),base=self.base)
                a.list=a.list[:L]+[i]+a.list[L:]
                if subword_in_minimal(a(k,True)[0],minimal,self.base):
                    x.remove(str_base(i.digits,self.base))
                    res=[]
                    for j in range(k):
                        a=Family(self,base=self.base)
                        a.list=a.list[:L]+[x]+([str_base(i.digits,self.base)]+[x])*j+a.list[L+1:]
                        res.append(a)
                    return res
            return [Family(self,base=self.base)]
        except:
            return [Family(self,base=self.base)]

    def lemma23(self,minimal):
        try:
            L=it.first(self.notnumindex())
            R=it.first(self.numindex())
            for a,b in itertools.product(self[L],self[L]):
                if a==b:continue
                x=Family(list(self.iternum()),base=self.base)
                y=Family(x,base=self.base)
                x.list=x.list[:L]+[a]+[b]+x.list[L:]
                y.list=y.list[:L]+[b]+[a]+y.list[L:]
                if subword_in_minimal(x(0,True),minimal,self.base) and subword_in_minimal(y(0,True),minimal,self.base):
                    family1=Family(self,base=self.base)
                    family2=Family(self,base=self.base)
                    n=DigitsList(self[L],base=self.base)
                    n.remove(a)
                    family1.list=family1.list[:L]+[n]+family1.list[L+1:]
                    n=DigitsList(self[L],base=self.base)
                    n.remove(b)
                    family2.list=family2.list[:L]+[n]+family2.list[L+1:]
                    return family1,family2
            return [Family(self,base=self.base)]
        except:
            return [Family(self,base=self.base)]
        
                
def is_subsequence(x,y,base=10):
    """return True if x is a subsequence of y in base """
    if isinstance(x,str):
        x=int(x,base)
    if isinstance(y,str):
        y=int(y,base)
    x=iter(mt.digits(x,base))
    y=mt.digits(y,base)
    q=next(x)
    for a in y:
        if a==q:
            try:
                q=next(x)
            except:
                return True
    return False

def prime_digits(base=10):
    """return all the prime with a length of 1 in base"""
    return list(mt.primegen(end=base))

def minimal_digits(base=10):
    """return digits which are used by minimal prime"""
    if base==2:return [0,1]
    return list(it.diff(range(base),iter(prime_digits(base))))

def minimal_last_digits(base=10):
    """return last digits of num which are used by minimal prime of length >1"""
    digits=minimal_digits(base)
    digits=filter(lambda x:mt.coprimes(x,base),digits)
    return list(digits)

def minimal(base):
    minimal=[]
    for i in mt.minimal(mt.primegenfast(),base,limit=base**3):
        minimal.append(i)
    familytest=[]
    last_digits=minimal_last_digits(base)
    digits=minimal_digits(base)
    for x in digits[1:]:
        for z in last_digits:
            Y=[dig for dig in digits if not
               any(is_subsequence(num,str_base(x,base)+str_base(dig,base)+str_base(z,base),base)
                   for num in minimal)]
            if Y:
                familytest.append(Family(x,Y,z,base=base))
    familytest=list(filter(lambda x:x.contain_prime(),familytest))
    i=0
    while familytest:
        new=[]
        for family in familytest:
            new+=family.lemma19()
        familytest=new[:]
        new=[]
        for family in familytest:
            w=family(0,True)
            if subword_in_minimal(w,minimal,base):pass
            elif mt.is_prime(w):
                minimal.append(w)
            else:
                new+=family.lemma21(minimal,1)
                
        familytest=new[:]
        new=[]
        #print(familytest)
        for family in familytest:
            new+=family.lemma23(minimal)
        familytest=new[:]
        familytest=list(filter(lambda x:x.contain_prime(),familytest))
        if i%10==0:print(familytest)
        i+=1
    return minimal

def subword_in_minimal(num,minimal,base):
    """return True if num has a subword in minimal"""
    return any(is_subsequence(x,num,base) for x in minimal)

def form_transform(form,minimal,base):
    for a,b in itertools.product(form[2],form[2]):
        if a==b:continue
        num1=int(form[0]+str_base(a,base)+str_base(b,base)+form[1],base)
        num2=int(form[0]+str_base(b,base)+str_base(a,base)+form[1],base)
        if any(is_subsequence(y,num1,base)and is_subsequence(y,num2,base) for y in minimal):
            form1=form[:]
            form2=form[:]
            form1[2].remove(a)
            form2[2].remove(b)
            return form1,form2
    return [form]

def pretty_print(L,base):
    try:
        for i in L:
            if base==10:print(i,end=",")
            else:
                print("%s=%s"%(str_base(i,base),i),end=",")
    except:
        if base==10:print(L)
        else:
            print("%s=%s"%(str_base(L,base),L))

if __name__=="__main__":
    base=14
    pretty_print(minimal(base),base)
