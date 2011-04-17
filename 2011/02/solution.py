from itertools import count, starmap
from functools import reduce, partial
from collections import OrderedDict

def groupby(func, seq):
    result = {}
    for item in seq:
        result.setdefault(func(item), []).append(item)
    return result

def iterate(func):
    def apply_n_times(times, arg):
        return reduce(lambda accum, _: func(accum), range(times), arg)

    for times in count(0):
        yield partial(apply_n_times, times)

def zip_with(func, *iterables):
    return starmap(func, zip(*iterables))

def cache(func, cache_size = 0):
    storage = OrderedDict()

    def cached(*args):
        if args in storage:
            return storage[args]

        result = func(*args)

        if cache_size:
            if len(storage) == cache_size:
                storage.popitem(False)
            storage[args] = result

        return result
    return cached