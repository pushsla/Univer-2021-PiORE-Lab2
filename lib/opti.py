import sympy
import numpy as np

from math import *

from .calc import Method


def make_system(method: Method):
    diffs = []

    formula = str(method)
    symbols = ' '.join(method.model.coef_names)
    symbols_dotted = symbols.replace(' ', ',')

    exec(f"{symbols_dotted} = sympy.symbols('{symbols}')")
    tfunc = eval(formula)
    for symbol in method.model.coef_names:
        diffs.append(tuple(sympy.diff(tfunc, symbol).as_coefficients_dict().values()))

    var_coefs = np.array([k[1:] for k in diffs], dtype=np.float)
    free_coefs = np.array([[-k[0]] for k in diffs], dtype=np.float)

    solved = np.linalg.solve(var_coefs, free_coefs)

    return dict(zip(method.model.coef_names, solved.reshape(len(method.model.coef_names),)))




