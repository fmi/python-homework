import functools

class expr:
    def __init__(self, predicate): self.predicate = predicate
    def __call__(self, value): return self.predicate(value)
    def __and__(self, other): return conjunction(self, other)
    def __or__(self, other): return disjunction(self, other)
    def __invert__(self): return negation(self)
    def __rshift__(self, other): return implication(self, other)

def predicate(function):
    def predicator(*args, **kwargs):
        return expr(lambda value: function(value, *args, **kwargs))
    predicator.__name__ = function.__name__
    return predicator

def predicate(function):
    def predicator(self, value):
        return function(value, *self.args, **self.kwargs)

    def constructor(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    return type(function.__name__, (expr,), {'__call__': predicator, '__init__': constructor})

@predicate
def pred(value, condition):
    return condition(value)

@predicate
def gt(value, minimum):
    return value > minimum

@predicate
def lt(value, minimum):
    return value < minimum

@predicate
def conjunction(value, left, right):
    return left(value) and right(value)

@predicate
def disjunction(value, left, right):
    return left(value) or right(value)

@predicate
def negation(value, function):
    return not function(value)

@predicate
def eq(value, exact):
    return exact == value

@predicate
def implication(value, precondition, condition):
    return condition(value) if precondition(value) else True

@predicate
def oftype(value, kind):
    return isinstance(value, kind)

@predicate
def for_any(value, *predicates):
    return any(predicate(value) for predicate in predicates)

@predicate
def for_all(value, *predicates):
    return all(predicate(value) for predicate in predicates)

@predicate
def present(value):
    return value is not None
