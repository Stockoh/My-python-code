import time
from copy import deepcopy
import functools
import logging
import multiprocessing
from multiprocessing import TimeoutError
import itertools
import collections
import operator
logger=logging.getLogger()
logger.setLevel(logging.INFO)

def memoize(f):
    """speed up repeated calls to a function by caching its results in a dict index by params"""
    cache = {}
    def memoizer(*args,**kargs):
        key=str(args)+str(kargs)
        if key not in cache :
            cache[key] = f(*args,**kargs)
        return cache[key]
    return memoizer

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logging.info('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed

def itimeout(iterable,timeout):
    ts=time.time()
    for x in iterable:
        yield x
        te=time.time()
        if te-ts>=timeout:
            raise TimeoutError
        
def find_dict(value,dictionary):
    """return the key off the value of the dictionary
    ex:find_dict([2,3,5,7],{'Prime': [2, 3, 5, 7], 'Composite': [4, 6, 8, 9, 10]})-->'Prime'"""
    for key,value_key in dictionary.items():
        if value_key==value:return key
    raise IndexError

def first(iterable):
    """return the first element off a iterable"""
    for x in iterable:
        return x
    raise IndexError

def last(iterable):
    """return the last element off a iterable"""
    find=False
    for i in iterable:
        x=i
        find=True
    if find:
        return x
    raise IndexError

def anyf(seq, pred=bool):
    """
    :result: bool True if pred(x) is True for at least one element in the iterable
    """
    return (True in map(pred, seq))


def allf(seq, pred=bool):
    """
    :result: bool True if pred(x) is True for all elements in the iterable
    """
    return (False not in map(pred, seq))


def no(seq, pred=bool):
    """
    :result: bool True if pred(x) is False for every element in the iterable
    """
    return (True not in map(pred, seq))

def is_iterable(x):
    if isinstance(x, str):
        return False
    return isinstance(x,collections.Iterable)

def is_emply(iterable):
    for i in iterable:
        return False
    return True

def copy(x):
    """return a copy off x"""
    return deepcopy(x)

def compress(iterable):
    """return compress list or iterable
    ex:compress([6,4,1,1,1,2,5,5])-->[(6, 1), (4, 1), (1, 3), (2, 1), (5, 2)]"""
    prev,count=None,0
    for item in iterable:
        if count and item==prev:
            count+=1
        else:
            if count: 
                yield prev,count
            prev=item
            count=1
    if count:
        yield prev,count

def flatten(iterable,typeskip=(str,)):
    """flatten a iterable
    ex:flatten([5,7,8,[5,7,[4,9]],9,[6]])-->[5, 7, 8, 5, 7, 4, 9, 9, 6]"""
    if isinstance(iterable, dict):
        iterable = iterable.values()
    for i in iterable:
        if not isinstance(i ,collections.Iterable):
            yield i
        elif isinstance(i ,typeskip):
            yield i
        else:
            for x in flatten(i,typeskip):
                yield x

def flatten_first_dim(iterable,numberdim,typeskip=(str,)):
    """flatten a iterable but only the first dim"""
    if isinstance(iterable, dict):
        iterable = iterable.values()
    if numberdim==0:
        yield from iterable
        return
    for i in iterable:
        if not isinstance(i ,collections.Iterable):
            yield i
        elif isinstance(i ,typeskip):
            yield i
        else:
            for x in flatten_first_dim(i,numberdim-1,typeskip):
                yield x

def accumulate(iterable,func=operator.add):
    """return a accumulate version the iterable
    ex:accumulate(range(5))-->0,1,3,6,10"""
    first=True
    for i in iterable:
        if first:
            yield i
            total=i
            first=False
        else:
            total=func(i,total)
            yield total

def refine(iterable,key=min):
    """refine the iterable (it start at the key of the iterable)
    ex:list(refine([7,8,0,9,8],key=min))-->0,9,8,7,8"""
    m=key(iterable)
    v=False
    L=[]
    for i in iterable:
        if i==m:
            v=True
        if v:
            yield i
        else:
            L.append(i)
    for e in L:
        yield e
        
def sorted_iterable(iterable, key=None, buffer=100):
    """sorts an "almost sorted" (infinite) iterable

    :param iterable: iterable
    :param key: function used as sort key
    :param buffer: int size of buffer. elements to swap should not be further than that
    """
    key=key or (lambda x:x)
    L=[]
    for x in iterable:
        if buffer and len(L)>=buffer:
            L.sort()
            res=L.pop(0)
            yield res
        L.append(x)
    for x in L:
        yield x
        
def ilen(iterable):
    try:
        return len(iterable)
    except:
        try:
            return sum(1 for _ in iterable)
        except:raise TypeError
        
def take_index(iterable,key):
    for e,i in enumerate(iterable):
        if key(e):
            yield i
            
def no_take_index(iterable,key):
    for e,i in enumerate(iterable):
        if not key(e):
            yield i
            

def unique(iterable,buffer=100):
    L=[]
    for x in iterable:
        if buffer and len(L)>=buffer:
            res=L.pop(0)
            yield res
        if not x in L:L.append(x)
    for x in L:
        yield x

def emply():
    """return a emply iterable"""
    return iter([])

def diff(iterable1, iterable2):
    """generate items in sorted iterable1 that are not in sorted iterable2"""
    b = next(iterable2)
    for a in iterable1:
        while b < a:
            try:
                b = next(iterable2)
            except:
                break
        if a == b:
            continue
        yield a

def closest(iterable,value,key=lambda x,y:abs(x-y)):
    m=None
    for i in iterable:
        try:
            z=key(i,value)
        except:
            continue
        if (m is None):
            yield i
            m=z
        else:
            if m>z:
                yield i
                m=z

def shape(iterable):
    """ shape of a mutidimensional array, without numpy
    :param iterable: iterable of iterable ... of iterable or numpy arrays...
    :result: list of n ints corresponding to iterable's len of each dimension
    :warning: if iterable is not a (hyper) rect matrix, shape is evaluated from
    the [0,0,...0] element ...
    :see: http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.ndarray.shape.html
    """
    res = []
    try:
        while True:
            res.append(ilen(iterable))
            iterable = first(iterable)
    except TypeError:
        return res


def ndim(iterable):
    """ number of dimensions of a mutidimensional array, without numpy
    :param iterable: iterable of iterable ... of iterable or numpy arrays...
    :result: int number of dimensions
    """
    return len(shape(iterable))

def map_deep(func,L,deep):
    """return a list of a list maped at a deep"""
    if deep==0:
        try:
            return list(map(func,L))
        except:
            return [func(L)]
    if not is_iterable(L):
        return L
    return [map_deep(func,x,deep-1) for x in L]
if __name__=="__main__":
    print(map_deep(str,[[1,2],[3,4]],1))
