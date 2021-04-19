import math_2 as mt

class Stack():
    """class for stack"""
    def __init__(self,*value):
        self.stack=list(value)

    def add(self,*value):
        for a in value:
            self.stack.append(a)

    def out(self,num=1):
        if num<=0 or len(self)==0:raise IndexError
        res=[]
        for e,i in enumerate(reversed(self.stack),1):
            res.append(i)
            self.stack.pop(-1)
            if e==num:break
        res=res[0] if len(res)==1 else tuple(res)
        return res
    
    def __getitem__(self,index):
        try:
            return self.stack[index]
        except:raise IndexError
        
    def __setitem__(self,index,value):
        try:
            self.stack[index] = value
        except:raise IndexError

    def __add__(self,other):
        return Stack(*(self.stack+list(other)))
    
    def __radd__(self,other):
        return Stack(*(list(other)+self.stack))
    
    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.stack)

    def __iter__(self):
        for i in reversed(self.stack):
            yield i
    
    def __next__(self):
        return next(self.__iter__())
    next=__next__
        
"""            
def pre(ex):
    p=Stack()
    for i in reversed(ex):
        if set(str(i)).issubset("1234567890"):
            p.add(i)
        else:
            a,b=p.out(2)
            p.add(eval(str(a)+i+str(b)))
    return p.out()

def pre_str(ex):
    p=Stack()
    for i in reversed(ex):
        if set(str(i)).issubset("1234567890"):
            p.add(str(i))
        else:
            a,b=p.out(2)
            p.add("("+str(a)+i+str(b)+")")
    return p.out()
"""
