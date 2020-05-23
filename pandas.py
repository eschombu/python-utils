import numpy as np


def get(df_, **conditions):
    """Utility function for getting portions of dataframe."""
    include = np.ones(len(df_)).astype(bool)
    for col, condition in conditions.items():
        if callable(condition):
            include = include & np.array([condition(x) for x in df_[col]])
        else:
            include = include & (df_[col] == condition)
    return df_[include]


def less_than(y, include_equal=False):
    if include_equal:
        return lambda x: x <= y
    else:
        return lambda x: x < y
    

def greater_than(y, include_equal=False):
    if include_equal:
        return lambda x: x >= y
    else:
        return lambda x: x > y


def has(*items, has_all=True, and_not=None):
    """Returns a selection function for use with the `get` function. Selects rows where a column's
    element contains the specified items."""

    def flatten(items):
        flattened = []
        if isinstance(items, str):
            return [items]
        else:
            for item in items:
                flattened.extend(flatten(item))
            return flattened

    items = flatten(items)
    def has_item(x):
        and_nots = and_not
        if has_all:
            does_have = all([item in x for item in items])
        else:
            does_have = any([item in x for item in items])
        if and_nots:
            if isinstance(and_nots, str):
                and_nots = [and_nots]
            return does_have and all([item not in x for item in and_nots])
        else:
            return does_have

    return has_item


def isin(group):
    """Returns a selection function for use with the `get` function. Selects rows where a column's 
    element is in the specified collection."""
    def check(x):
        try:
            return x in group
        except TypeError:
            return x in [group]
    return check
