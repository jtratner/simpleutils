"""
simple csv - set of simple utilities for handling csv
FOR ALL FUNCTIONS:
    some common keywords are listed for convenience. Only non-None
    keywords are passed.

CONVERT TO CSV: 
    in general, can just use default settings, which are of form
    convert_ABC_to_csv(lstofABC[,path) where 'ABC' is list or dict
    and 'lstofABC' is a list of lists or dicts. 'path' is optional.

    if no path given, defaults to inserting the time into the filename

READ FROM CSV:
    general format:
    read_csv_to_ABC(path) -> ABC
    where path is a path to a csv file and ABC is 'list' or 'dict'.
    All keywords for python csv module are accepted, also possible to
    specify a header row to get titles/keys, etc

All functions work with lists, dicts, or any object that works similarly
"""

    

import csv
from simpletime import pretty_time
from simplesets import get_all_keys
import sys

def convert_dict_to_csv(
        lstofdicts,
        filename = None,
        header_row = None,
        fieldnames = None,
        dialect='excel',
        **kwargs):
    """Takes dict and converts to csv, see csv.DictWriter for more, **kwargs are passed on,
    default filename is pretty_time().csv
    csv.DictReader(csvfile[, fieldnames=None[, restkey=None[, restval=None[, dialect='excel'[, *args, **kwds]]]]])
    Use keyword arguments so you don't have to worry about position"""
    # store defaults in kwargs
    if filename:
        f = open(filename,'wb')
    else:
        filename = pretty_time()+'.csv'
        f = open(filename,'wb')
    try:
        if fieldnames:
            # if fieldnames, store them
            names = fieldnames
        elif header_row:
            # sort keys in header_row for fieldnames
            names = sorted(lstofdicts[header_row].keys())
        else:
            try:
                # try to get fieldnames by getting all keys within lstofdicts
                names = sorted(list(get_all_keys(lstofdicts)))
                print "No fieldnames entered, getting all keys:\nKeys: %r" % names
            except Exception as inst:
                print "Couldn't grab all keys...probably won't work."
                print "MESSAGE: ", inst.message
                print "ARGS: ",inst.args
                names = lstofdicts[0].keys()
        # write fieldnames as first row
        csvwriter = csv.writer(f, **kwargs)
        csvwriter.writerow(names)
        # add fieldnames to kwargs for dictwriter
        kwargs['fieldnames'] = names
        csvDict = csv.DictWriter(f, **kwargs)
        sys.stdout.write("Wrote field names to first row. Continuing")
        i = 0
        for elem in lstofdicts:
            i += 1
            sys.stdout.write('.')
            csvDict.writerow(elem)
        print "\nWrote %d items" % i
    except Exception as inst:
        print inst.message
        print inst.args
    finally:
        f.close()
        return filename

def convert_list_to_csv(
        lst,
        filename = None,
        header_row = 0,
        num_columns = None,
        delimiter = None,
        quotechar = None,
        quoting = None,
        dialect = 'excel',
        **kwargs):
    """Takes a list of data (generally list of list) and writes it to a
    file as a csv. 
    *header_row* specifies index where titles are located
        (becomes first row of csv) 
    All args passed to csv, args with None are written for convenient
    reminder.
    Default filename is pretty_time()"""
    # store defaults in kwargs
    if delimiter is not None: kwargs['delimiter'] = delimiter
    if quotechar is not None: kwargs['quotechar'] = quotechar
    if quoting is not None: kwargs['quoting'] = quoting
    
    # open up a file to write with
    if filename:
        f = open(filename,'wb')
    else:
        filename = pretty_time()+'.csv'
        f = open(filename,'wb')
    # write with csvwriter
    try:
        mycsvwriter =  csv.writer(f,**kwargs)
        mycsvwriter.writerow(lst.pop(header_row))
        sys.stdout.write("Writing rows")
        i = 0
        for elem in lst:
            mycsvwriter.writerow(elem)
            sys.stdout.write('.')
            i += 1
        print "\nWrote %d rows." % i
    finally:
        f.close()
        return filename
        
def read_csv_to_list(
        path,
        dialect='excel',
        delimiter=None,
        quotechar = None,
        encoding = None,
        **kwargs):
    """ reads the csv at 'path' and outputs a list with all lines maintained 
    (so, the column titles) any keywords for csvreader can be passed 
    through if desired)"""
    # store defaults
    kwargs['dialect'] = dialect
    if delimiter is not None: kwargs['delimiter'] = delimiter
    if quotechar is not None: kwargs['quotechar'] = quotechar
    
    f = open(path,'rb')
    
    try:
        mycsvreader = csv.reader(f,**kwargs)
        # if an encoding was specified, decodes the characters and return
        # otherwise just return using list generators
        if encoding:
            return [map(lambda y: y.decode(encoding),x) for x in mycsvreader]
        return [x for x in mycsvreader]
    finally:
        f.close()

def read_csv_to_dict(
        path,
        dialect='excel',
        delimiter=None,
        quotechar=None,
        encoding = None,
        **kwargs):
    """ reads the csv at 'path' and outputs a dict with keywords from the 
    firstline (so, the column titles) any keywords for csvreader can be passed 
    through if desired)
    Keywords are listed for convenience, only non-None are kept"""
    kwargs['dialect'] = dialect
    if not delimiter is None: kwargs['delimiter'] = delimiter
    if not quotechar is None: kwargs['quotechar'] = quotechar
    f = open(path,'rb')
    try:
        mycsvreader = csv.DictReader(f,**kwargs)
        return [x for x in mycsvreader]
    finally:
        f.close()

