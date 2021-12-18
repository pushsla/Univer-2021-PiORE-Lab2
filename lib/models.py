import math
from functools import reduce


class Model:
    def __init__(self):
        self.coefficients = list()
        self.coef_names = tuple()

    def y(self, x: float) -> float:
        raise NotImplementedError()

    def y_with_custom_coefs(self, x: float, coefs: tuple) -> float:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def name():
        raise NotImplementedError()

    @property
    def params(self) -> tuple[dict, dict]:
        properties = {name: value
                  for name, value in self.__dict__.items()
                  if not (name.startswith("_") or name in ("coefficients", "coef_names"))}
        coefs = dict(zip(self.coef_names, self.coefficients))

        for key in properties.keys():
            if (v := f"_{key}_variants") in self.__dict__:
                properties[key] = self.__dict__[v]

        return properties, coefs

    def set_prop(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        else:
            raise KeyError(f"{name} not in {self.__dict__}")

    def set_coef(self, name, value):
        if name in self.coef_names:
            self.coefficients[self.coef_names.index(name)] = value
        else:
            raise KeyError(f"{name} not in {self.coef_names}")


class PolyModel(Model):

    def __init__(self):
        self.max_pow = 2
        self.coefficients = list(1 for i in range(self.max_pow))
        self.coef_names = tuple(f'a{i}' for i in range(self.max_pow))

    def y(self, x: float) -> float:
        return reduce(lambda a, b: a+b, (self.coefficients[i]*(x**i) for i in range(self.max_pow)))

    def y_with_custom_coefs(self, x: float, coefs: tuple) -> float:
        return reduce(lambda a, b: a+b, (coefs[i]*(x**i) for i in range(self.max_pow)))

    def set_prop(self, name, value):
        super().set_prop(name, value)
        if name == "max_pow":
            self.coefficients = list(1 for i in range(self.max_pow))
            self.coef_names = tuple(f'a{i}' for i in range(self.max_pow))

    @staticmethod
    def name():
        return "Polynominal"

    def __str__(self) -> str:
        return f"{self.coef_names[0]}" + \
               reduce(lambda a, b: a+b, (f" + {self.coef_names[i]}*x**{i}" for i in range(1, self.max_pow)))


class PowModel(Model):
    def __init__(self):
        self.coefficients = [1, 1]
        self.coef_names = ('a', 'b')

    def y(self, x: float) -> float:
        return self.coefficients[0]*(x**self.coefficients[1])

    def y_with_custom_coefs(self, x: float, coefs: tuple) -> float:
        return coefs[0]*(x**coefs[1])

    @staticmethod
    def name():
        return "Powered"

    def __str__(self) -> str:
        return f"{self.coef_names[0]}x**{self.coef_names[1]}"


class SinusModel(Model):

    def __init__(self):
        self.x_pow = 1
        self.coefficients = [1]
        self.coef_names = ('a0',)

    @property
    def _func(self):
        return math.sin

    @staticmethod
    def name():
        return "Sin"

    def y(self, x: float) -> float:
        return self.coefficients[0]*self._func(x**self.x_pow)

    def y_with_custom_coefs(self, x: float, coefs: tuple) -> float:
        return coefs[0]*self._func(x**self.x_pow)

    def __str__(self) -> str:
        return f"{self.coef_names[0]}*sin(x**{self.x_pow})"


class CosModel(Model):

    def __init__(self):
        self.x_pow = 1
        self.coefficients = [1]
        self.coef_names = ('a0',)

    @property
    def _func(self):
        return math.cos

    @staticmethod
    def name():
        return "Cos"

    def y(self, x: float) -> float:
        return self.coefficients[0]*self._func(x**self.x_pow)

    def y_with_custom_coefs(self, x: float, coefs: tuple) -> float:
        return coefs[0]*self._func(x**self.x_pow)

    def __str__(self) -> str:
        return f"{self.coef_names[0]}*cos(x**{self.x_pow})"


Models = [PolyModel, SinusModel, CosModel]
