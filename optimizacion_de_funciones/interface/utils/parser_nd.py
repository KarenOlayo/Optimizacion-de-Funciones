import sympy as sp
import numpy as np


def parse_function_nd(expr, variables):
    try:
      
        if not isinstance(variables, str):
            raise ValueError("Las variables deben ser un texto.")

        # Limpiar espacios
        variables = variables.replace(" ", "")

        # Separar por coma
        var_list = variables.split(",")

        # Eliminar vacíos
        var_list = [v for v in var_list if v != ""]

        if len(var_list) == 0:
            raise ValueError("Debe ingresar al menos una variable.")

        # Crear símbolos respetando el orden
        vars_symbols = sp.symbols(" ".join(var_list))

        # Asegurar tupla (importante para 1D)
        if not isinstance(vars_symbols, tuple):
            vars_symbols = (vars_symbols,)

        # Procesar expresion
        expr_sym = sp.sympify(expr)

        # Validar que la expresión solo use variables definidas
        expr_vars = expr_sym.free_symbols
        defined_vars = set(vars_symbols)

        if not expr_vars.issubset(defined_vars):
            raise ValueError(
                "La expresión contiene variables no definidas en el campo de variables."
            )

        # Crear funcion numerica
        f_lamb = sp.lambdify(vars_symbols, expr_sym, modules=["numpy"])

        def f(*args):
            # Permitir entrada como lista/vector
            if len(args) == 1 and isinstance(args[0], (list, tuple, np.ndarray)):
                args = tuple(args[0])

            # Validar número de argumentos
            if len(args) != len(vars_symbols):
                raise ValueError(
                    f"Se esperaban {len(vars_symbols)} variables, pero se recibieron {len(args)}."
                )

            result = f_lamb(*args)

            # Retornar escalar si corresponde
            if np.isscalar(result):
                return float(result)

            return np.array(result, dtype=float)

        return f

    except Exception as e:
        print(f"[parse_function_nd] Error: {e}")
        return None