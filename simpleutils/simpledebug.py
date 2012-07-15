from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

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


def special_trace(ignore_args=None, ignore_kwargs=None, pretty=True):
    """ Decorator factory. Similar to standard trace, except that this trace allows function
    to ignore certain arguments. And set special tracing

    parameters:

        ignore_args - list of ints...positions in input args to ignore
        ignore_kwargs - list of keys; keyword arguments to ignore
        pretty - whether to pretty print signature

    NOTE: if you just want pretty print can just use @special_trace and it will work
    exactly the same as trace
        """

    @decorator
    def _trace(f):
        def _f(*args, **kwargs):
            signature = "%s(%s)" % (f.__name__,
                    _format_signature(args, kwargs))
            print '%s--> %s' % (special_trace.level*indent, signature)
            special_trace.level += 1
            try:
                result = f(*args, **kwargs)
                print '%s<-- %s == %s' % ((special_trace.level-1)*indent,
                                        signature.replace("\n" + indent, "\n"), result)
            finally:
                # here we're returning so go down a trace level
                special_trace.level -= 1
            return result
        special_trace.level = 0
        return _f

    special_trace.indent = indent = '   '
    def _format_signature(args, kwargs):
        """ returns a string, the format of args and kwargs to be displayed"""
        sig = ""
        if pretty:
            from pprint import pformat
            format = lambda *args : pformat(*args)
        else:
            format = repr
        sig += ", ".join(format(arg) for i, arg in enumerate(args) if i not in ignore_args)
        sig += ", ".join(format(kw) + " = " + format(val) for kw, val in kwargs.items() if kw not in ignore_kwargs)
        if sig: sig = "\n" + sig
        return sig.replace("\n", "\n" + special_trace.level * indent)

    if type(ignore_args) == type(_format_signature):
        # if the first arg was actually a function (meaning was called without any arguments)
        # we want this to behave just like a normal decorator
        f = ignore_args
        ignore_args = set()
        ignore_kwargs = set()
        return _trace(f)
    else:
        ignore_args = set(ignore_args or [])
        ignore_kwargs = set(ignore_kwargs or [])
        return _trace
# initialize special_trace level s.t. special_print can use it to
special_trace.level = 0

def special_print(*args):
    """ print from a function as normal, but if using special_trace,
    let's you print text with the same indent as trace (making it easier
    to see what belongs to what)"""
    args = "".join(str(a) for a in args)
    indent = special_trace.level * special_trace.indent
    print indent + args.replace("\n", "\n" + indent)

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


