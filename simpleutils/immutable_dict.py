"""
ImmutableDict(iterable)

Hashable, immutable dict. Can call and manipulate like a dict, except cannot be mutated.
Also can generate new dicts using set operators, '&','|', '+', etc

>>> foo = {'a':1,'b':2,'c':3}
>>> foo_set = frozenset(foo)
>>> bar = ImmutableDict(foo)
>>> foo['a'] == bar['a']
True
>>> foo is bar
False
>>> foo.keys() == bar.keys()
True
>>> for k,v in sorted(bar.items(),key=lambda x: x[0]): print "(%r , %r)" % (k, v)
('a' , 1)
('b' , 2)
('c' , 3)
>>> (bar & bar) == bar
True
>>> (foo_set & foo_set) == foo_set
True
>>> (foo_set | foo_set) == foo_set
True
>>> (bar | bar) == bar
True
>>> bar['a']
1
>>> bar['b']
2
>>> bar['c']
3
>>> sorted(bar.keys())
['a', 'b', 'c']
>>> sorted(bar.values())
[1, 2, 3]
"""
import collections
from functools import update_wrapper
def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches return value for each fxn call and looks it up next time"""
    cache = {}
    def _f(*args):
        try:
            cached = cache[args]
            return cached
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(args)
    return _f


@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((trace.level-1)*indent, 
                                      signature, result)
        finally:
            # here we're returning so go down a trace level
            trace.level -= 1
        return result
    trace.level = 0
    return _f

@trace
def _set_method_factory(set_method_str):
    """creates a set operation method by acting directly on the frozensets of each and creating a *new* item"""
    set_method = eval("frozenset.%s" % set_method_str)
    def method(self,other=None):
        other = [other._frozenset] if other is not None else []
        return ImmutableDict(set_method(self._frozenset,*other))
    method.__doc__ = set_method.__doc__
    method.__name__ = set_method.__name__
    return method
@trace
def _dict_method_factory(dict_method_str):
    """creates a set operation method by acting directly on the frozensets of each and creating a *new* item"""
    set_method = eval("dict.%s" % dict_method_str)
    def method(self,other=None):
        other = [other._dict] if other is not None else []
        return ImmutableDict(set_method(self._dict,*other))
    method.__doc__ = set_method.__doc__
    method.__name__ = set_method.__name__
    return method

class ImmutableDict(collections.Mapping,collections.Set):
    def __init__(self, iterable):
        self._dict = dict(iterable)
        self._frozenset = frozenset(self._dict.items())
    def __getitem__(self, n):
        return self._dict[n]
    def __setitem__(self, *args, **kwargs):
        raise TypeError("`ImmutableDict' objects cannot be mutated")
    def __iter__(self):
        return iter(self._dict)
    def __eq__(self, other):
        return self._frozenset == other._frozenset
    def __lt__(self, other):
        return self._frozenset < other._frozenset
    def __le__(self, other):
        return self._frozenset <= other._frozenset
    __or__ = _set_method_factory("__or__")
    __xor__ = _set_method_factory("__xor__")
    __sub__ = _set_method_factory("__sub__")
    __and__ = _set_method_factory("__and__")
    union = _set_method_factory("union")
    intersection = _set_method_factory("intersection")
    isdisjoint = _set_method_factory("isdisjoint")
    __contains__ = _set_method_factory("__contains__")
    __len__ = _set_method_factory("__len__")
    __hash__ = _set_method_factory("__hash__")
    def __repr__(self):
        return "ImmutableDict( %r )" % self._dict


q = ImmutableDict({1:1,2:2,3:3})
r = ImmutableDict({3:2,1:3,4:4})
for i in range(0,100):
    q - q
    q & q
    q | q
    r - r
    r & r
    q | q
