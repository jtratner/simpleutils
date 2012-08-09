"""
utilities for handling Python dicts.

:class:`defaultfunctiondict`:

* like a default dict, but creates output based upon key instead
* Implementation (and suggestion to use override the :meth:`~collections.defaultdict.__missing__` method
  of :class:`collections.defaultdict` instead of subclassing dict, are credit `Jochen Ritzel`_
  of Stack Overflow

.. _Jochen Ritzel : http://stackoverflow.com/users/95612/jochen-ritzel

"""

from collections import defaultdict
class defaultfunctiondict(defaultdict):
    """ like a defaultdict, but instead takes in a function factory that
    takes a single argument -- a key, and returns a value
    that dynamically returns a value based upon the given key.

    Advantage over :meth:`dict.setdefault` : the default is *only* evaluated
    as necessary.
    """
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        ret = self[key] = self.default_factory(key)
        return ret

from collections import defaultdict

def dicts_to_list(lstofdicts, fieldnames = None, key_sorter = None,
        ignore_keys = None):
    """ given an ordered list of fieldnames and an optional key_sorter,
    returns (fieldnames, lstoflsts) a list of fieldnames (in order) and the list of dicts as a list of
    lists (optional: ignore_keys...list of keys to leave out from dict
    conversion)"""
    if ignore_keys is None:
        ignore_keys = tuple()
    if fieldnames is None:
        fieldnames = tuple()
    else:
        # remove any keys in ignore_keys from fieldnames and convert to tuple
        fieldnames = tuple(elem for elem in fieldnames if elem not in ignore_keys)
    try:
        all_names = set(get_all_keys(lstofdicts))
    except Exception as inst:
        print("Couldn't grab all keys...probably won't work.")
        print("MESSAGE: {!r}".format(inst.MESSAGE))
        print("ARGS: {!r}".format(inst.args))
        all_names = lstofdicts[0].keys()
    # just get the names that *aren't* in fieldnames (or ignore keys) already, then sort by
    # given keyfunction
    extra_names = sorted(all_names.difference(set(fieldnames),
        set(ignore_keys)), key = key_sorter)
    if extra_names:
        print("Found additional fieldnames: {!r}".format(extra_names))
    fieldnames += tuple(extra_names)
    output = defaultdict(lambda : [None] * len(fieldnames))
    for row, dct in enumerate(lstofdicts):
        # assign each dict, in order, to a row
        curr = output[row]
        for i, k in enumerate(fieldnames):
            # for each key in fieldnames, store the key from current dict in
            # the current row. If the dict doesn't have the particular key,
            # just keep going
            try:
                curr[i] = dct[k]
            except KeyError:
                pass
    output = [output[k] for k in range(max(output.keys()) + 1)]
    return fieldnames, output

def list_to_dict(lst):
    return dict((i, elem) for i, elem in enumerate(lst))

def dicts_to_namedtuples(lstofdicts, classname = 'Fields', fieldnames = None, key_sorter = None):
    """ works exactly the same as convert_dict_to_list, but creates a
    namedtuple with the elements used as fieldnames. Numbers converted to
    'f'+# (e.g. '1' --> 'f1').
    Note that additional namedtuples can be made by using the obj._make
    function of any element returned from this function, or by grabbing the class
    from :meth:`~object.__class__`
    """
    from collections import namedtuple
    fieldnames, data = dicts_to_list(lstofdicts, fieldnames=fieldnames,
            key_sorter=key_sorter)
    NewClass = namedtuple(classname, fieldnames)
    return map(NewClass._make, data)
