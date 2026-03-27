import sympy as sp
import numpy as np

def parse_function(expr, var):
    """
    Convierte un string en una función evaluable usando numpy.

    Parámetros:
    - expr: str -> expresión matemática (ej: "x**2 - 4*x + 3")
    - var: str -> variable (ej: "x", "y", "t")

    Retorna:
    - función evaluable f(x) o None si hay error
    """

    try:
        # Permitir uso de ^ como potencia
        expr = expr.replace("^", "**")

        # Definir símbolo dinámico
        symbol = sp.symbols(var)

        # Convertir a expresión simbólica (sin restricciones)
        expr_sym = sp.sympify(expr)

        # Convertir a función numérica con numpy
        f_lamb = sp.lambdify(symbol, expr_sym, modules=["numpy"])

        def f(x_val):
            result = f_lamb(x_val)

            # Caso escalar
            if np.isscalar(x_val):
                return float(result)

            # Caso vector (array)
            return np.array(result, dtype=float)

        return f

    except Exception:
        return None