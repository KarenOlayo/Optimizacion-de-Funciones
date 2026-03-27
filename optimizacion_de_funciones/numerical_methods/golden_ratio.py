from models.result import Result
from models.value_type import ValueType
from models.message_type import MessageType
from models.table import Table
from models.message import Message

import numpy as np


def golden_ratio(f, var, a, b, error, objective):

    if a >= b:
        return Result(message=Message("El límite inferior debe ser menor que el superior.", MessageType.ERROR))

    if error <= 0:
        return Result(message=Message("El error debe ser mayor que cero.", MessageType.ERROR))

    if objective not in ["Mínimo", "Máximo"]:
        return Result(message=Message("Debe seleccionar 'Mínimo' o 'Máximo'.", MessageType.ERROR))

    phi = (1 + np.sqrt(5)) / 2
    resphi = 2 - phi

    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)

    fx1 = f(x1)
    fx2 = f(x2)

    iterations = 0
    errors = []
    approximations = []
    rows = []
    headers = ["i", "a", "b", f"{var}m", "error"]

    while abs(b - a) > error:

        prev_a, prev_b = a, b

        xm = (a + b) / 2
        current_error = abs(b - a)

        approximations.append(xm)
        errors.append(current_error)
        rows.append([iterations, a, b, xm, current_error])

        if objective == "Mínimo":
            if fx1 > fx2:
                a = x1
                x1 = x2
                fx1 = fx2
                x2 = b - resphi * (b - a)
                fx2 = f(x2)
            else:
                b = x2
                x2 = x1
                fx2 = fx1
                x1 = a + resphi * (b - a)
                fx1 = f(x1)

        elif objective == "Máximo":
            if fx1 < fx2:
                a = x1
                x1 = x2
                fx1 = fx2
                x2 = b - resphi * (b - a)
                fx2 = f(x2)
            else:
                b = x2
                x2 = x1
                fx2 = fx1
                x1 = a + resphi * (b - a)
                fx1 = f(x1)

        iterations += 1

        # Evitar bucle infinito por precision
        if a == prev_a and b == prev_b:
            break

    x_opt = (a + b) / 2
    f_opt = f(x_opt)

    if objective == "Mínimo":
        value_type = ValueType.MINIMUM
    else:
        value_type = ValueType.MAXIMUM

    table = Table(headers, rows)

    return Result(
        interest_value=x_opt,
        function_value=f_opt,
        iterations=iterations,
        errors=errors,
        approximations=approximations,
        table=table,
        value_type=value_type,
        var=var
    )