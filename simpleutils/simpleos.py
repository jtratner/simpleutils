"""
Relatively self-explanatory - utilities to quickly handle files
(generally meant to be used in interactive mode).
"""

import re
import os
import sys


def check_root(warnmsg=None, endscript=False):
    """ Checks to see that user id is root (=0) and gives user option to quit
    if not.  If endscript set to True, then will attempt to exit script if user
    is not root and user does not choose to continue.

    We're all adults. This function treats your user like one too.
    Returns True if everything's okay, False if user elects to continue
    and raises OSError or quits otherwise.

    INPUT:
        warnmsg - string, warning message to be displayed to user if not root
        endscript - bool, whether to call sys.exit if user doesn't continue
            -> TRUE: calls sys.exit
            -> FALSE: raises OSError
    RETURNS:
        True - if user is root
        False - otherwise

    RAISES:
        OSError
    """
    # make sure user is root
    if not os.geteuid() == 0:
        if warnmsg is None:
            warnmsg = """
            Not running as root, may not be able to have script to function.
            Are you sure you want to continue?
            'y' to continue, otherwise will quit"""
        # prompt user about warn message
        cont = raw_input(warnmsg)
        if cont != 'y':
            if endscript or __name__ == '__main__':
                sys.exit('\nQuitting...\n')
            else:
                raise OSError(
                    "User did not have root permission and elected to stop")
        else:
            print "OK. Continuing."
            return False
    else:
        return True


def check_platform(platform='posix', warnmsg=None, endscript=False):
    """ Checks to see that os is on given platform and gives user option
    to quit if not.  If endscript set to True, then will attempt to exit
    script if user is not root and user does not choose to continue.

    We're all adults. This function treats your user like one too.
    Returns True if everything's okay, False if user elects to continue
    and raises OSError or quits otherwise.

    INPUT:
        platform - string, platform to be checked. default is 'posix'.
            NOTE: It is recommended that you explicitly set platform.
        warnmsg - string, warning message to be displayed to user if not
            root default: warning that script is meant to be run on given
            platform
        endscript - bool, whether to call sys.exit if user doesn't continue
            -> True: calls sys.exit
            -> False: raises OSError
            default: False
    RETURNS:
        True - if user is root
        False - otherwise

    RAISES:
        OSError
    """
    if not os.name == platform:
        if warnmsg is None:
            warnmsg = """
            This script is meant to run on posix platforms.
            Are you sure you want to run this script?
            'y' or enter to continue, otherwise script will quit.
            [ENTER to continue]>
            """
        cont = raw_input(warnmsg)
        if cont is not None or cont != 'y':
            if endscript or __name__ == '__main__':
                sys.exit('\nQuitting...\n')
            else:
                raise OSError("Non-posix OS, user elected to stop.")
        else:
            print "OK. Continuing."
            return False
    else:
        return True


def rm_symlink(path):
    """removes file so long as it is a symlink.
    path must be an absolute path.
    Returns True if removed, False if not."""
    if os.path.islink(path):
        print "Removing path %r" % path
        os.remove(path)
        return T
    else:
        return False

def identity(*args,**kwargs):
    """ returns all positional arguments, discards keyword arguments """
    # return a list of arguments if multiple otherwise return single argument
    return list(args) if len(args) > 1 else args


def make_filter_fn(thefilter=None, use_regex=False):
    """for a given `thefilter`, returns a one-argument function:
            None - pattern - True
            str -  pattern - thefilter
            str and use_regex or re obj - pattern -re.pattern or thefilter
            function - pattern - function.__name__
            (output function gets __name__ = "filter_by_%s" %pattern
            and pattern attr `pattern`)
            NOTE: if you get ValueError or Type Error, check fn passed in here."""
    re_type = type(re.compile(''))
    if thefilter is None:
        # use default function
        newfn = lambda x: True
        pattern = 'True'
    elif use_regex or isinstance(thefilter,re_type):
        # if user forced regex or it is a match object, use re.search
        newfn = lambda x: re.search(thefilter,x)
        pattern = (thefilter.pattern 
                     if isinstance(thefilter,re_type)
                     else thefilter)
    elif isinstance(thefilter,str):
        # if str and not use_regex, use default str search
        newfn = lambda x: thefilter in x
        pattern = thefilter
    else:
        # otherwise assume it's a method
        newfn = thefilter
        pattern = thefilter.__name__
    # set name and pattern for display
    newfn.__name__ = "filter_by_%s" % pattern
    newfn.pattern = pattern
    return newfn


def get_paths_by_filter(thefilter=None, dirpath=None, use_regex=False):
    """generate list of file paths by filtering in given directiory.
    Defaults to filtering files just by str 'thefilter' in current working
    directory
    INPUT:
        thefilter - text, regex, or one-input function to filter
            -> uses make_filter_fn to create filter function 
               (uses its defaults too)
        dirpath - path to desired directory, default: os.getcwd()
        use_regex - bool, if true then searches using re.search, default:False
        NOTE: for regularexpression, either set use_regex to true or send a
            compiled regex object, otherwise program will just check
            if str in filename
    RETURNS:
        list of absolute paths matching thefilter
    COMMON EXCEPTIONS:
        ValueError, TypeError - if this happens, check your thefilter, is it a
        str, match object, or fn that accepts one argument?"""

    # use absolute path to dirpath if given, otherwise use default
    dirpath = os.getcwd() if dirpath is None else os.path.abspath(dirpath)
    filter_fn = make_filter_fn(thefilter, use_regex)
    print "using path %r. Exists? %r" % (dirpath, os.path.exists(dirpath))
    if not os.path.exists(dirpath):
        print "returning empty"
        return []
    else:
        print "filtering by %r" % filter_fn.pattern
        outputlist = filter(filter_fn,os.listdir(os.getcwd()))
        # reconstruct absolute paths by adding back dirpath and separator to the
        # filtered files from outputlist
        outputpaths = map(lambda x: os.path.join(dirpath, x), outputlist)
        print 'Found files: \n' + '\n'.join(outputpaths)
        return outputpaths


def read_file(path):
    """reads the file at given path and returns a string"""
    f = open(path, 'r')
    fread = f.read()
    f.close()
    return fread


def read_file_by_line(path):
    """given a path, opens with 'rb' and interactively reads line by line."""
    try:
        response = None
        i = 0
        f = open(path, 'rb')
        print "Reading line by line, type q to exit"
        while not (response == 'q'
                   or response == 'quit'
                   or response == 'exit'):
            i = i + 1
            print "[Line %s]" % i
            print f.readline()
            response = raw_input(
                    '\n[L%sPress RETURN to continue, q to exit]>' % i)
    finally:
        f.close()
