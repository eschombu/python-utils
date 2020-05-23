import numpy as np


def get_all_arg_sets(*args):
    args = [arg for arg in args]
    for i in range(len(args)):
        if not isinstance(args[i], (list, tuple, np.ndarray)):
            args[i] = [args[i]]
    val_sets = [sorted(set(vals)) for vals in args]
    incrementers = []
    multiplier = 1
    for vals in val_sets:
        incrementers.append(multiplier)
        multiplier = multiplier * len(vals)
    all_sets = []
    for i in range(multiplier):
        this_set = []
        for vals, incrementer in zip(val_sets, incrementers):
            this_set.append(vals[((i % incrementer) + (i // incrementer)) % len(vals)])
        all_sets.append(this_set)
    return all_sets


def get_all_kw_sets(**kwargs):
    keys = sorted(kwargs.keys())
    for key in keys:
        if not isinstance(kwargs[key], (list, tuple, np.ndarray)):
            kwargs[key] = [kwargs[key]]
    val_sets = [sorted(set(kwargs[key])) for key in keys]
    incrementers = []
    multiplier = 1
    for vals in val_sets:
        incrementers.append(multiplier)
        multiplier = multiplier * len(vals)
    all_sets = []
    for i in range(multiplier):
        this_set = {}
        for key, vals, incrementer in zip(keys, val_sets, incrementers):
            this_set[key] = vals[((i % incrementer) + (i // incrementer)) % len(vals)]
        all_sets.append(this_set)
    return all_sets
