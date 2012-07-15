===========
simpleutils
===========

Variety of handy, small utilities to aid in using, testing, debugging, etc in
Python

Overview
========

This contains a number of (small) scripts and utilities I've developed over
time while developing in Python. I've tried to create functions that allow you
to use a particular Python feature with just a single argument, instead of
many required settings arguments, while still letting you get to all the
underlying features. Hence, "simple". Still at a pretty early stage, but all
of the elements in the reference below should work and be useful.

What's In Here
==============

easy import/export of csv and xlsx
----------------------------------

Lets you convert csv and excel files to Python dictionaries/lists using only
the filename as an argument. Similarly, allows export with just file name. (If
you're using a dictionary, it'll also search for all additional keys and save
them too).


debugging via decorators
------------------------

A few really basic decorators to view function execution by tracing.
If you slap on ``@trace`` , it will just print the input arguments and return
value of the function call (indenting each time for recursive calls).

``@special_trace`` works similarly to trace, except you can pass it positions or
keyword arguments that you want ignored (not printed) in the trace output.
Combines with ``special_print``, which makes print output align with the
indentation of ``special_trace``.
