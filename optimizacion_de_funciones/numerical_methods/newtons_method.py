from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

import sympy as sp
import numpy as np


def newtons_method(f, expr, var, x0, error, objective):

    if error <= 0:
        return Result(message=Message("El error debe ser mayor que cero.", MessageType.ERROR))

    if objective not in ["Mínimo", "Máximo"]:
        return Result(message=Message("Debe seleccionar 'Mínimo' o 'Máximo'.", MessageType.ERROR))

    # Calcular derivadas
    try:
        x = sp.symbols(var)
        expr_sym = sp.sympify(expr)

        df_expr = sp.diff(expr_sym, x)
        d2f_expr = sp.diff(expr_sym, x, 2)

        df_lamb = sp.lambdify(x, df_expr, modules=["numpy"])
        d2f_lamb = sp.lambdify(x, d2f_expr, modules=["numpy"])

        def df(x_val):
            return float(df_lamb(x_val))

        def d2f(x_val):
            return float(d2f_lamb(x_val))

    except Exception as e:

        message = (
        f"Error al procesar la expresión matemática: {str(e)}.\n"
        "Asegúrese de seguir estas reglas:\n"
        "1. Use '*' para multiplicar (ej. '2*x' en lugar de '2x').\n"
        "2. Use '**' para potencias (ej. 'x**2').\n"
        "3. Use nombres de funciones estándar: 'sin(x)', 'cos(x)', 'exp(x)', 'log(x)', 'sqrt(x)'."
        )

        return Result(message=Message(message, MessageType.ERROR))

    x_str = var[0]

    xi = x0
    iterations = 0
    errors = []
    approximations = []

    headers = ["i",f"{var}i", f"f({var}i)", f"f'({var}i)", f"f''({var}i)", f"{var}i+1", "error"]
    rows = []

    while True:

        try:
            
            fxi = f(xi)
            dfxi = df(xi)
            d2fxi = d2f(xi)

        except Exception as e:

            message = (
            f"Error de cálculo en x = {xi:.6f}: {str(e)}.\n"
            "El método intentó evaluar un punto fuera del dominio de la función."
            "(ej. división por cero, logaritmo de número negativo o raíz de número negativo).\n"
            "Sugerencia: Cambie el punto inicial x0 a una zona donde la función esté definida y sea continua."
            )

            return Result(message=Message(message, MessageType.ERROR))

        if abs(d2fxi) < 1e-12:

            message = (
            f"Error: La segunda derivada en {xi} es prácticamente cero.\n "
            "Esto indica un punto de inflexión o una zona plana donde el método no puede"
            "determinar la curvatura para encontrar un óptimo.\n"
            "Sugerencia: Intente con un punto inicial (x0) diferente, alejado de puntos de inflexión."
            )

            return Result(message=Message(message, MessageType.ERROR))

        xi_next = xi - (dfxi / d2fxi)
        error_actual = abs(xi_next - xi)

        errors.append(error_actual)
        approximations.append(xi_next)
        rows.append([iterations, xi, fxi, dfxi, d2fxi, xi_next, error_actual])

        # Convergencia por error
        if error_actual < error or abs(dfxi) < error:

            second = d2f(xi_next)

            if second > 0:
                detected = ValueType.MINIMUM
            elif second < 0:
                detected = ValueType.MAXIMUM
            else:
                detected = ValueType.UNKNOWN

            expected = ValueType.MINIMUM if objective == "Mínimo" else ValueType.MAXIMUM

            if detected != expected:

                message = (
                f"Se encontró un punto crítico en {x_str} ≈ {xi_next} con f({x_str}) = {f(xi_next)} a las {iterations+1} y error = {error_actual}, "
                f"pero es un {detected.value.lower()} y usted buscaba un {objective.lower()}.\n"
                "Causa: El método de Newton converge al punto crítico más cercano, sea cual sea su tipo.\n"
                "Sugerencia: Cambie el punto inicial x0 hacia una zona donde la función tenga la "
                "concavidad deseada (hacia arriba para mínimos, hacia abajo para máximos)."
                )
                
                return Result(
                    interest_value=xi_next,
                    function_value=f(xi_next),
                    iterations=iterations,
                    errors=errors,
                    approximations=approximations,
                    table=Table(headers, rows),
                    value_type=ValueType.UNKNOWN,
                    var=var,
                    message=Message(message, MessageType.WARNING)
                    )
            
            return Result(
                    interest_value=xi_next,
                    function_value=f(xi_next),
                    iterations=iterations,
                    errors=errors,
                    approximations=approximations,
                    table=Table(headers, rows),
                    value_type=expected,
                    var=var,
                    )

        # Divergencia
        if len(errors) >= 4:
            
            last_errors = errors[-4:]
            
            # crecimiento sostenido
            increasing = all(x < y for x, y in zip(last_errors, last_errors[1:]))

            # o crecimiento general
            if increasing or last_errors[-1] > 10 * last_errors[0]:

                message = (
                "El método parece diverger (los errores están aumentando drásticamente).\n"
                "Esto suele ocurrir cuando el punto inicial x0 está muy lejos del óptimo "
                "o en una zona donde la función cambia de concavidad bruscamente.\n"
                "Sugerencia: Elija un punto inicial más cercano al máximo/mínimo esperado o verifique "
                "si la función tiene un óptimo en esa región."
                )

                return Result(
                    interest_value=xi_next,
                    function_value=f(xi_next),
                    iterations=iterations,
                    errors=errors,
                    approximations=approximations,
                    table=Table(headers, rows),
                    value_type=ValueType.UNKNOWN,
                    var=var,
                    message=Message(message, MessageType.WARNING),
                )

        xi = xi_next
        iterations += 1