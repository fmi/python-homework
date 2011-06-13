import inspect

class interface(type):
    def __init__(self, name, bases, attributes):
        self.methods = {name: attr for name, attr in attributes.items() if not name.startswith('_')}

    def __call__(self, implementor):
        for name, method in self.methods.items():
            implementation = getattr(implementor, name)
            if not implementation.__doc__:
                implementation.__doc__ = method.__doc__
            if self._spec(implementation) != self._spec(method):
                assert False
        return implementor

    def _spec(self, method):
        spec = inspect.getfullargspec(method)
        return spec._replace(annotations=None, kwonlyargs=set(spec.kwonlyargs))
