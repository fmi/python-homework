from numbers import Number

class Lazy:
    def __init__(self, arg):
        if isinstance(arg, Lazy):
            self._expression = arg._expression
        elif isinstance(arg, Number):
            self._expression = lambda: arg

    def delay_operator(operator):
        def delayed(*args):
            expression = lambda: operator(*[Lazy(arg).force() for arg in args])
            number = LazyExpression(expression)
            return number
        return delayed

    def force(self):
        return self._expression()

    __add__ =       delay_operator(lambda self, other: self + other)
    __radd__ =      delay_operator(lambda self, other: other + self)
    __sub__ =       delay_operator(lambda self, other: self - other)
    __rsub__ =      delay_operator(lambda self, other: other - self)
    __mul__ =       delay_operator(lambda self, other: self * other)
    __rmul__ =      delay_operator(lambda self, other: other * self)
    __truediv__ =   delay_operator(lambda self, other: self / other)
    __rtruediv__ =  delay_operator(lambda self, other: other / self)
    __floordiv__ =  delay_operator(lambda self, other: self // other)
    __rfloordiv__ = delay_operator(lambda self, other: other // self)
    __mod__ =       delay_operator(lambda self, other: self % other)
    __rmod__ =      delay_operator(lambda self, other: other % self)

    def __pos__(self):
        return self

    @delay_operator
    def __neg__(self):
        return -self

    def __bool__(self):
        return bool(self.force())

    def __int__(self):
        return int(self.force())

    def __float__(self):
        return float(self.force())

    def __str__(self):
        return str(self.force())

class LazyExpression(Lazy):
    def __init__(self, expression):
        self._expression = expression
