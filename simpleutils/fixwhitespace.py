"""
Clean white space - a quasi-module with some handy functions.

NOTE: for now must be run in interactive mode(python -i
cleanwhitespace.py), may change that in the future.

NOTE2: No tests yet, so be forewarned (though replace_tabs_with_spaces
has been tested These are just a few functions that can easily and
quickly help you to handle annoying excess whitespace in text documents.

replace_tabs_with_spaces is especially written to help resolve the tabs
vs.  spaces problem in python by replacing all tabs with spaces. I hope
to write a function in the future that normalizes spaces (e.g. takes a
3/block spacer and replaces it with 4/block.  For now, that's on you. :P

Copyright (c) Jeffrey Tratner, 2012.
licensed under the GPLv3
(basically, attribute me if you use it, share the source if you can and
help others by making changes and don't use my name to imply endorsement of
your product).

"""

import os


def remove_whitespace(mystr, joinstr=' '):
    """removes all whitespace from mystr, and joins it with joinstr"""
    output = joinstr.join(mystr.split())
    return output


def replace_pattern(mystr, pattern=' ', replacement=None):
    """remove repeating pattern string and replace with just one
    instance of pattern (or a different string if given (pattern must be
        string, not regex"""
    if replacement is None:
        replacement = pattern
    # split on pattern, filter out empty strings (returned by multiple
    # instances of pattern) and join together with 'replacement'
    print "Replacing instances of %r with %r" % (pattern, replacement)
    newstr = replacement.join(
            filter(lambda x: not(x is ''), mystr.split(pattern)))
    return newstr


def replace_tabs_with_spaces(mystr, tabchar='\t', numspaces=4, verbose=False, filename='file'):
    """"replaces tab characters at the beginning of lines with 4 spaces
    (fixing tab/space inconsistencies in documents, replaces tab
            characters even at beginning of triple quote lines """
    # split into lines to work line by line
    spaces = ' ' * numspaces
    linelist = mystr.splitlines()
    num_tabs = 0
    for i in range(0, len(linelist)):
        # keep replacing tabs with spaces until no more tabs at
        # beginning of line (usually only 0-4 tabs max at beginning of
        # line, so faster than any other method while still preserving
        # internal tabs
        j = 0
        line = linelist[i]
        while line.startswith(tabchar):
            line = line.replace(tabchar, '', 1)
            j = j + 1
        if j:
            linelist[i] = spaces * j + line
            num_tabs += j
    if verbose:
        if num_tabs:
            print("Found {tabs} tab characters total in {filename}".format(tabs=num_tabs, filename=filename))
        else:
            print("No tab characters requiring replacement found")
    return os.linesep.join(linelist)
