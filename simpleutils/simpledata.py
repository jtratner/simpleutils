# concept inventory:
#   import of files
#   formatting data/keys
#   storage format for data and recall based on tags
#     - dict
#     - list w/ keylist s.t. can access w/ getitem (depends on overhead...but
#     could have single list reference)
#   writing data
#     - ordering of entries (key function?)
#     - auto handling of extra keys, etc
#   handling duplicates/joining
#     - define custom object IDs via keys
#     - ability to use set notation to merge entries would be cool:
#       OR just allow merge via keys or something
#  grouping/searching by keys
#  easy function mapping and manipulation
#     - e.g. define global variables once and use them repeatedly to call
#     objects but instead of needing to redefine each time, just import,
#     define keys via script and call each entry via key (so even if you've
#     stored data as a list, you can access via dict keys using getitem
#     notation, and references index in central list)
#  simple quantitative function support (+ easy numpy integration??)
#     - average
#     - standard deviation
#     - count (count by key, or by value-key)
#     - sorting via object values (handled by getitem already)
#     - 
#  mutating data
#     - updates to key list occur on the fly (added to key list)
#     - Q: what's the difference in overhead between dicts and lists?
#     - use a default dict? or named tuple? ordered dict?

DEBUG = True
import re
import simplecsv as sc

def average(iterable):
    lst = list(iterable)
    return sum(lst)/len(lst)

def sum_keys(data, keys):
    return sum(data[k] for k in keys)


def strip_to_number(thestr, convert_fn = float, error_val = None):
    """strips all nonint/non'.' characters from string, returns float
    returns error value in case of TypeError or ValueError"""
    try:
        return convert_fn(re.sub('[^0-9^.]','',thestr))
    except (TypeError, ValueError):
        return error_val


def store_value_in_key(obj,newkey,fun, error_val='', store_error_val=True,reraise=DEBUG, verbose=DEBUG):
    """ For a given object, store the result of fun(key) in obj[key]
    INPUT:
    OUTPUT:
        None (stores the value in object)
        """
    try:
        obj[newkey] = fun(obj)
    except (TypeError, ValueError):
        if verbose: print "Could not handle newkey %r" % newkey
        if reraise:
            raise
        else:
            obj[newkey] = error_val
    except KeyError:
        if verbose: print "KeyError, nothing stored."
        if reraise:
            raise
class Reader(object):
    def __init__(self, intkeys=None, floatkeys=None, fix_fns=None, **kwargs):
        self.intkeys = intkeys
        self.floatkeys = floatkeys
        self.fix_fns = fix_fns
    def load(filename,*args, **kwargs):
    @property
    def intkeys(self): return self.intkeys
    @property
    def floatkeys(self): return self.floatkeys
    @property
    def fix_fns(self): return self.fix_fns
