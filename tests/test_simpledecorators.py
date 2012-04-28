import nose.tools as nt
from simpleutils import simpledecorators as sd
from simpleutils import simplecsv as sc
from simpleutils import simpletime as st



# basic keys for validating decorator metadata
base_metadata_keys = {'__name__', '__module__', '__doc__'}
def meta_comp(obj, keys=base_metadata_keys):
    if obj is None or keys is None:
        return {'no key':None}
    """generate a dict from list of metadata"""
    return {k : getattr(obj, k) for k in keys if getattr(obj,k) is not None}


@nt.nottest
def simpledec(decorator=None, f=None, *args, **kwargs):
    sd_dec = sd.simple_decorator(decorator)
    decorated_f = sd_dec(f)
    nt.assert_dict_contains_subset(
            meta_comp(f),
            meta_comp(decorated_f),
            msg = "decorated function failed. function: %s - %r decorator: %s - %r" % (
                                            f.__name__, meta_comp(f),decorator.__name__,meta_comp(decorated_f)))
    nt.assert_dict_contains_subset(
            meta_comp(decorator),
            meta_comp(sd_dec), 
            msg = "simple_decorator on decorator fn %s failed" % decorator.__name__)


def unchanged(f):
    return f

def steal_output(f):
    """doesn't use internal function (totally valid)!"""
    def wrapper(*args,**kwargs):
        return args[0] if len(args) > 0 else None
    return wrapper

# functions to test decoration
def apple():
    return 'apple'

def none_returner():
    pass

decorator_set = {
        unchanged,
        steal_output,
        sd.simple_decorator,
        sd.catch_exceptions,
        sd.dump_args,
        }

function_set = {apple,none_returner, st.pretty_time,sc.read_csv_to_dict}


def simpledec_test():
    """ tests all decorators on all functions in function_set"""
    # try f for all decorators
    for decorator in decorator_set:
        for f in function_set:
            yield simpledec, decorator, decorator

# exception producing decorators

@nt.raises(TypeError)
def simpledec_typeerror(*args,**kwargs): simpledec(*args,**kwargs)

@nt.raises(AttributeError)
def simpledec_attribute_error(*args,**kwargs): simpledec(*args,**kwargs)

@nt.raises(ValueError)
def simpledec_value_error(*args,**kwargs): simpledec(*args,**kwargs)

def non_returning_decorator(f):
    """decorators have to return wrapper function. If not, should raise an error"""
    def wrapper(*args,**kwargs):
        pass


def non_returning_test():
    for function in function_set:
        yield simpledec_value_error, non_returning_decorator, function

def too_few_args_decorator():
    """decorators must at least take in the decorated function"""
    def wrapper(*args,**kwargs):
        return 'string'
    return wrapper


def too_few_args_test():
    for function in function_set:
        yield simpledec_typeerror, too_few_args_decorator, function

def miswritten_decorator(f):
    def wrapper(*args,**kwargs):
        lambda x: fun(x)
    return wrapper

def miswritten_test():
    for function in function_set:
        simpledec(miswritten_decorator, function)

# tests for catch_exceptions - handler function not yet tested
@sd.catch_exceptions(TypeError)
def test_type_error_producer():
    raise TypeError

@sd.catch_exceptions(TypeError)
def test_type_error_producer2():
    1 + 'thisstring' + True

@sd.catch_exceptions(TypeError,ValueError,AttributeError,OSError)
def produce_exceptions(exception = None):
    raise exception

def test_multiple_exception_catchign():
    for e in TypeError,ValueError,AttributeError,OSError:
        yield produce_exceptions(e)

@nt.raises(TypeError)
def test_no_call():
    @sd.catch_exceptions
    def myfun(): pass
    myfun()


@nt.raises(TypeError)
def test_no_exceptions():
    @sd.catch_exceptions()
    def myfun(): pass
    myfun()

@sd.catch_exceptions(TypeError,ValueError)
def test_unspecified_exception():
    raise OSError

# testing dump_args (mostly making sure it doesn't produce errors, not
# so much its output. later may implement doctests.
def dumpargs_pass_test():
    @sd.dump_args
    def banana(*args,**kwargs):
        pass
    banana()

def dumpargs_argnames_test():
    @sd.dump_args
    def banana(a,b,c=None,d=True,*args,**kwargs):
        pass
    banana(1,2,3,4)
    banana(1,2,c=4,d=False)
    banana(a=1,b=2,c=3,d=4)

