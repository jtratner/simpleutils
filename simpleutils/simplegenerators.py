"""
Some generators to facilitate common processes.

nested_generator - traverses iterables and yields values
"""

from collections import Iterable

def nested_generator(obj, depth=None, sort_fn=lambda x: x):
    """ traverses iterables until reaches non-nested value
    specifically: [x for x in nested_generator(obj)] returns
    a list of all non-iterable objects in obj. If obj is ordered
    then output list will be ordered as well

    INPUTS:
        obj - the iterable to be un-nested
        depth - max depth of iteration, when depth is 0, yields object, 
            if depth is None, does not check
            ->default: None
        sort_fn - sorting function to be applied to iterable at each
            level.
            -> default: lambda x: x"""
    def recursive_generator(myobj, depth=None):
        """ recursively generates flat list of items"""
        if depth == 0:
            # base case: depth is zero
            yield myobj
        elif not isinstance(myobj,Iterable):
            # base case: object is not iterable
            yield myobj
        else:
            # recursive case: generate over all items in list, in order
            # if keeping track of depth, decrement by 1
            depth = depth if depth is None else depth - 1
            for elem in sort_fn(myobj):
                recursive_generator(elem, depth)
    # checks that input is iterable (and also excludes None)
    if not isinstance(obj, Iterable):
        raise TypeError("obj %r is not iterable" % type(obj))
    else:
        try:
            recursive_generator(obj, depth)
        except RuntimeError as e:
            # produce more informative error message so clear where
            # recursion error is coming from
            if 'recursion' in e:
                raise RuntimeError(
                """Exceeded recursion limit in generator. Do you have an
                object that always produces an iterable or generator
                when generated ? If so, handle by passing a sort
                function. Here's the error message: %r""" % e)
            else:
                raise
