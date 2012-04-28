"""
Decorators to handle simple tasks, like making decorators well-behaved,
or catching exceptions.

contains:
    -simple_decorator - decorator to make decorators preserve function metadata
    -catch_exceptions - decorator to catch exceptions and handle them
        TODO: test catch_exceptions' handler
    -dump_args - decorator to print function arguments (taken from the Python
    decorator library)

There are some great, more advanced libraries for decorators out there.
This is not one of them. This aims to be simple, quick and easy to use.
"""

def simple_decorator(decorator):
    """Converts simple functions into well-behaved decorators. (meaning
    that they maintain name, dict, and doc string).
    Heavily based on decorators in Python Decorator Library, but
    modified.
    Example usage::

        @simple_decorator
        def my_decorator(..):
            pass

    INPUT:
        decorator - a decorator function
    OUTPUT:
        the decorator decorated such that it preserves the metadata of the
        functions it decorates
    RAISES:
        ValueError (if decorator function does not return a function)
        """
    # maintain args and kwargs here so that this can work for decorator
    # factories as well
    def new_decorator(f,*args,**kwargs):
        try:
            g = decorator(f,*args,**kwargs)
            g.__name__ = f.__name__
            g.__doc__ = f.__doc__
            g.__module__ = f.__module__
            g.__dict__.update(f.__dict__)
        except AttributeError as e:
            if 'NoneType' in e.message:
                raise ValueError("simple_decorator: decorator must return a function.")
            else:
                raise
        return g
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    # not sure here if better to set equal to old dict or update. I
    # guess this format better saves methods from original function
    new_decorator.__dict__.update(decorator.__dict__)
    new_decorator.__module__ = decorator.__module__
    return new_decorator

def _pass(*args,**kwargs):
    """ lambda function to do nothing with ternary """
    pass

@simple_decorator
def catch_exceptions(*exceptions, **kwargs):
    """catches exceptions. (decorator factory)
    INPUT:
        positional args:
            exceptions to be caught e.g. ValueError, TypeError, etc
        keyword args:
            handler_func - a function called to handle exception, must
            take in keyword arguments. gets passed the following with keywords,
            vals:
                'exception' : the exception instance
                'function' : the function given decorated
                'args' : positional arguments
                'kwargs' : keyword arguments"""
    # function design inspired by a variety of online resources,
    # particularly nose's @raises test decorator. nose is a great test
    # suite, check it out!
    print exceptions, kwargs
    valid_exceptions = ' or '.join([x.__name__ for x in exceptions])
    HANDLER= 'handler_func'
    handler_func = kwargs[HANDLER] if kwargs.has_key(HANDLER) else _pass
    def ce_wrapper(f):
        name = f.__name__
        def catch_function(*args,**kwargs):
            try:
                return f(*args,**kwargs)
            except exceptions as e:
                return handler_func(exception=e,function=f,args=args,kwargs=kwargs)
            except:
                print "Uncaught exception in function %s, not %s" % (
                        name,valid_exceptions)
                raise
        return catch_function
    return ce_wrapper

@simple_decorator
def dump_args(func):
    """This decorator dumps out the arguments passed to a function before
    calling it"""
    # based on the dump_args from the Python Decorator Library, but modified to
    # handle non-named positional arguments.

    # using list here instead of original tuple because allows splicing of list
    # into parts to display positional arg names as well as *args input
    argnames = list(func.func_code.co_varnames[:func.func_code.co_argcount])
    fname = func.func_name

    def echo_func(*args,**kwargs):
        arglist = list(args)
        print fname, ":", ', '.join(
            '%s=%r' % entry
            for entry in (
                zip(argnames,arglist[0:len(argnames)]) #named positional arguments
                + [('*args',arglist[len(argnames):])] # args passed through *args
                + kwargs.items())) #kwargs (form is (kw,val)
        return func(*args, **kwargs)

    return echo_func

