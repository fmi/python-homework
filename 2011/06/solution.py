import inspect
from functools import partial
from itertools import starmap

class multimethod:
    def __init__(self, method):
        self.methods = [method]

    def __get__(self, obj, objtype):
        return partial(self.invoke, obj)

    def invoke(self, target, *args):
        runtime_types = tuple(map(type, args))
        for method in self.methods:
            spec = inspect.getfullargspec(method)
            signature = tuple(spec.annotations.get(arg, object) for arg in spec.args[1:])

            if all(starmap(isinstance, zip(args, signature))):
                return method(target, *args)

        raise LookupError("Can't dispatch")

    def multimethod(self, target):
        self.methods.append(target)
        return self
