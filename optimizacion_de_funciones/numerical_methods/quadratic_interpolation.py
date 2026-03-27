from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

def quadratic_interpolation(f, var, x0, x1, x2, error, objective):

    if not (x0 < x1 < x2):
        return Result(message=Message("Se requiere que x0 < x1 < x2.", MessageType.ERROR))

    if error <= 0:
        return Result(message=Message("El error debe ser mayor que cero.", MessageType.ERROR))

    if objective not in ["Mínimo", "Máximo"]:
        return Result(message=Message("Debe seleccionar 'Mínimo' o 'Máximo'.", MessageType.ERROR))

    value_type = ValueType.MINIMUM if objective == "Mínimo" else ValueType.MAXIMUM
    x_str = var[0]
    iterations = 0
    errors = []
    approximations = []
    rows = []
    headers = ["i", f"{var}0", f"{var}1", f"{var}2", f"f({var}0)", f"f({var}1)", f"f({var}2)", f"{var}3", f"f({var}3)", "error"]

    while True:

        fx0 = f(x0)
        fx1 = f(x1)
        fx2 = f(x2)

        A = fx0 * (x1**2 - x2**2) + fx1 * (x2**2 - x0**2) + fx2 * (x0**2 - x1**2)
        B = 2*fx0 * (x1 - x2) + 2*fx1 * (x2 - x0) + 2*fx2 * (x0 - x1)

        if abs(B) < 1e-12:
            message = (
            "Error de colinealidad: No se puede construir una parábola con los puntos actuales.\n "
            "Esto ocurre cuando los valores f(x0), f(x1) y f(x2) están alineados o son idénticos.\n"
            "Sugerencia: Cambie los puntos iniciales (x0, x1, x2) para que capturen mejor la curvatura de la función."
            )
            return Result(message=Message(message, MessageType.ERROR))

        x3 = A / B
        fx3 = f(x3)

        current_error = abs(x3 - x1)
        errors.append(current_error)
        approximations.append(x3)
        rows.append([iterations, x0, x1, x2, fx0, fx1, fx2, x3, fx3, current_error])

        if current_error < error:
            return Result(
                interest_value=x3,
                function_value=fx3,
                iterations=iterations,
                errors=errors,
                approximations=approximations,
                table=Table(headers, rows),
                value_type=value_type,
                var=var
            )

        if value_type == ValueType.MAXIMUM:
            
            if x3 > x1:
                if fx3 > fx1:
                    x0 = x1
                    x1 = x3
                else:
                    x2 = x3
            else:
                if fx3 > fx1:
                    x2 = x1
                    x1 = x3
                else:
                    x0 = x3
        else:  
            if x3 > x1:
                if fx3 < fx1:
                    x0 = x1
                    x1 = x3
                else:
                    x2 = x3
            else:
                if fx3 < fx1:
                    x2 = x1
                    x1 = x3
                else:
                    x0 = x3

        iterations += 1