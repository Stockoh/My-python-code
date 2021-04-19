import operator as op
import math_2 as mt
import classtools
import itertools_2 as it
import re

class Context():
    """Context for operations"""
    def __init__(self):
        self.functions={}
        self.add_function(op.add,"%s + %s",formula="+")
        self.add_function(op.sub,"%s - %s",formula="-")
        self.add_function(op.mul,"%s * %s",formula="*")
        self.add_function(op.truediv,"%s / %s",formula="/")
        self.add_function(op.floordiv,"%s // %s",formula="//")
        self.add_function(op.mod,"%s mod %s",formula=("%","mod"))
        self.add_function(op.pos,"+%s",numberofentry=1,formula="pos",parenthesis=False)
        self.add_function(op.neg,"-%s",numberofentry=1,formula="neg",parenthesis=False)
        self.add_function(op.pow,"%s^%s","%s**%s",formula=("^","**"))
        self.add_function(mt.factorial,"%s!","factorial(%s)",numberofentry=1,formula=("!","factorial"),parenthesis=False)
        self.add_function(mt.factorial2,"%s!2","factorial2(%s)",numberofentry=1,formula=("!!","factorial2","!2"),parenthesis=False)
        self.add_function(mt.factorialk,"%s!k(%s)","factorialk(%s,%s)",formula=("!k","factorialk"))
        
    def add_function(self,f,s=None,r=None,numberofentry=2,formula=None,parenthesis=True,basicnumber=False):
        """add a function to use after

        :param f: function
        :param s: string representation, should be formula-like , with %s for place number
        :param r: repr representation, should be cut&pastable in a calculator, or in python, with also %s for place number
        :param numberofentry: number of entry of function f
        :param formula: string or tuple of string for identify the function
        """
        self.functions[f.__name__]=(f,s,r or s,numberofentry,formula,parenthesis,basicnumber)
        return self.functions[f.__name__]
    
    def __contains__(self,op):
        for z in self.functions.values():
            if op in z:return True
            if not isinstance(z[4],tuple):continue
            if op in z[4]:return True
        try:
            if op.__name__ in self.functions:return True
        finally:
            return False

    def function_from_formula(self,formula):
        for function,z in self.functions.items():
            if formula in z:return function
            if not isinstance(z[4],tuple):continue
            if formula in z[4]:return function
        return False

default_context = Context()

def test_number(i):
    return set(str(i)).issubset("1234567890") or \
        (str(i)[0]=="-" and len(str(i))>1 and set(str(i)[1:]).issubset("1234567890"))

class Expr():
    def __init__(self,f,context=default_context):
        """f:list"""
        if isinstance(f,Expr):
            self.body=f.body
            self.context=f.context
        else:
            self.body=list(f) if it.is_iterable(f) and not(isinstance(f,str)) else [f]
            self.context=context
        
    def __call__(self):
        try:
            p=classtools.Stack()
            for e,i in reversed(list(enumerate(self.body))):
                if test_number(i):
                    p.add(int(i))
                elif i in self.context:
                    function=self.context.function_from_formula(i)
                    t=p.out(self.context.functions[function][3])
                    if not isinstance(t,tuple):t=(t,)
                    try:
                        #print(e,i,len(t))
                        #print(list((self.body[e+z]) for z in range(1,len(t)+1)))
                        a=any(not test_number(self.body[e+z]) for z in range(1,len(t)+1))
                        #print("a=",a)#test basic number
                    except:
                        a=False
                        #print("a=",a)
                    #print("a=",a)
                    #print(self.context.functions[function][-1],function)
                    #print("a=",a)
                    if self.context.functions[function][6] and a:
                        #print("None")
                        raise Exception
                    p.add(self.context.functions[function][0](*t))
                else:raise Exception
            return p.out()
        except:return None
    
    def __repr__(self):
        p=classtools.Stack()
        for i in reversed(self.body):
            if set(str(i)).issubset("1234567890") or (str(i)[0]=="-" and len(str(i))>1 and set(str(i)[1:]).issubset("1234567890")):
                p.add(str(i))
            elif i in self.context:
                function=self.context.function_from_formula(i)
                t=p.out(self.context.functions[function][3]) 
                p.add(("("+self.context.functions[function][2]%t+")" if self.context.functions[function][5] else self.context.functions[function][2]%t))
            else:raise Exception
        return p.out()[1:-1] if p[-1][0]=="(" and p[-1][-1]==")" else p.out()
    
    def __str__(self):
        p=classtools.Stack()
        for i in reversed(self.body):
            if set(str(i)).issubset("1234567890") or (str(i)[0]=="-" and len(str(i))>1 and set(str(i)[1:]).issubset("1234567890")):
                p.add(str(i))
            elif i in self.context:
                function=self.context.function_from_formula(i)
                t=p.out(self.context.functions[function][3])
                p.add(("("+self.context.functions[function][1]%t+")" if self.context.functions[function][5] else self.context.functions[function][1]%t))
            else:raise Exception
        return p.out()[1:-1] if p[-1][0]=="(" and p[-1][-1]==")" else p.out()

    def apply(self,op,*args):
        if not op in self.context:raise Exception(str(op))
        function=self.context.function_from_formula(op)
        if not self.context.functions[function][3]==len(args)+1:raise Exception
        t=[L.body for L in args if isinstance(L,Expr)]
        z=[x for x in args if not isinstance(x,Expr)]
        return Expr([self.context.functions[function][0]]+self.body+z+list(it.flatten(t)),self.context)
    
    def is_number(self):
        try:
            return (len(self)==1 and mt.int_or_float(int(self.body[0]))==self.body[0])
        except:
            return False
        
    def __add__(self,other):
        return self.apply(op.add,other)
    
    def __radd__(self,other):
        return Expr(other).apply(op.add,self)
    
    def __mul__(self,other):
        return self.apply(op.mul,other)
    
    def __rmul__(self,other):
        return Expr(other).apply(op.mul,self)
    
    def __sub__(self,other):
        return self.apply(op.sub,other)
    
    def __rsub__(self,other):
        return Expr(other).apply(op.sub,self)
    
    def __pow__(self,other):
        return self.apply("^",other)

    def __rpow__(self,other):
        return Expr(other).apply("^",self)
    
    def __floordiv__(self,other):
        return self.apply(op.floordiv,other)

    def __rfloordiv__(self,other):
        return Expr(other).apply(op.floordiv,self)
    
    def __truediv__(self,other):
        return self.apply(op.truediv,other)
    
    def __rtruediv__(self,other):
        return Expr(other).apply(op.truediv,self)
    
    def __mod__(self,other):
        return self.apply(op.mod,other)
    
    def __rmod__(self,other):
        return Expr(other).apply(op.mod,self)
    
    def __neg__(self):
        return self.apply(op.neg)
    
    def __len__(self):
        return len(self.body)

ja=0
def stringtoexpr(str):
    global ja
    print("str",str,ja)
    ja+=1
    pat=re.compile(r"[^0-9]")
    str=str.replace("$","").replace(" ","").replace("**","^")
    if not str:
        return Expr(0)
    if not pat.findall(str):
        return Expr(int(str))
    n=0
    for i in str:
        if i=="(":
            n+=1
        if i==")":
            n-=1
        if n<0:raise Exception("'%s' isn't a Expr string"%str)
    for s in (r"\^","\*|\/","\+|\-"):
        pat=re.compile(r"(\d+|\d*\)+)(%s)(\d+|\(+\d*)"%s)
        indexlen=0
        for a,b,c in pat.findall(str):
            abc=a+b+c
            print("abc",abc)
            index=str[indexlen:].find(abc)
            indexlen=index+len(abc)
            print("index",index,indexlen,str[indexlen:])
            if abc==str:
                return Expr(int(a)).apply(b,int(c))
            if c[0]=="(":
                return Expr(int(a)).apply(b,stringtoexpr(c+str[indexlen:]))
            if index==0:
                print("la")
                return Expr(int(a)).apply(b,int(c)).apply(str[indexlen],stringtoexpr(str[indexlen+1:]))
            if a[-1]!=")" or c[0]!="(":
                if len(str)==indexlen:
                    return stringtoexpr(str[:index-1]).apply(str[index-1],
                                                         Expr(int(a)).apply(b,int(c)))
                return stringtoexpr(str[:index-1]).apply(str[index-1],
                                                         Expr(int(a)).apply(b,int(c)).apply(str[indexlen],stringtoexpr(str[indexlen+1:])))
            
            
if __name__=="__main__":
    pass
