def get_all_keys(lstofdicts):
    """for a given list of dicts(or dict), returns a set of all the keys within the
    list. Useful for making header rows for csvs, etc"""
    myset = set()
    if isinstance(lstofdicts, list):
        for mydict in lstofdicts:
            myset.update(mydict.keys())
    else:
        myset.update(lstofdicts.keys())
    return myset
