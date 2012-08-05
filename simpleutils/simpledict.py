"""
utilities for handling Python dicts.

:class:`defaultfunctiondict`:

* like a default dict, but creates output based upon key instead
* Implementation (and suggestion to use override the :meth:`__missing__` method
of :class:`defaultdict` instead of subclassing dict, are credit `Jochen Ritzel`_
of Stack Overflow

_JochenRitzel : http://stackoverflow.com/users/95612/jochen-ritzel

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


