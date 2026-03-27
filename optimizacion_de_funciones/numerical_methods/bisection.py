from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

def bisection(f, var, a, b, error):

    if a >= b:
        return Result(message=Message("El límite inferior debe ser menor que el superior.", MessageType.ERROR))

    if error <= 0:
        return Result(message=Message("El error debe ser mayor que cero.", MessageType.ERROR))

    value_type = ValueType.ROOT
    x_str = var[0]
    xl = a
    xu = b

    if f(xl) == 0:

        return Result(
            interest_value=xl,
            function_value=f(xl),
            message=Message(f"Raíz exacta en el límite inferior: {x_str} = {xl}", MessageType.WARNING),
            value_type=value_type
        )

    if f(xu) == 0:

        return Result(
            interest_value=xu,
            function_value=f(xu),
            message=Message(f"Raíz exacta en el límite superior: {x_str} = {xu}", MessageType.WARNING),
            value_type=value_type
        )

    if f(xl) * f(xu) > 0:

        message = (f"No se pudo determinar una raíz en el intervalo [{xl}, {xu}]. Esto pudo ser debido a que :\n"
        "- No existe una raíz en el intervalo.\n"
        "- Hay más de una raíz en el intervalo.\n"
        "- La función toca el eje pero no lo cruza, por lo que no hay cambio de signo aunque exista una raíz. Por ejemplo, f(x)=x**2\n"
        )
        
        return Result(
            interest_value=None,
            message=Message(message, MessageType.ERROR),
            value_type=ValueType.NONE)

    iterations = 0
    errors = []
    approximations = []
    rows = []
    headers = ["i", f"{var}l", f"{var}u", f"f({var}l)", f"f({var}u)", f"{var}r", f"f({var}r)", f"f({var}l)*f({var}r)", "error"]

    xr = (xl + xu) / 2  # se inicializa por si no se cumple la condicion del bucle
    fxr = f(xr)

    while abs(xu - xl) > error:
        
        xr = (xl + xu) / 2

        fxl = f(xl)
        fxu = f(xu)
        fxr = f(xr)

        current_error = abs(xu-xl)
        errors.append(current_error)
        approximations.append(xr)

        rows.append([iterations, xl, xu, fxl, fxu, xr, fxr, fxl * fxr, current_error])

        # Caso raíz exacta
        if abs(fxr) == 0:

            return Result(
                interest_value=xr,
                function_value=fxr,
                iterations=iterations,
                errors=errors,
                approximations=approximations,
                table=Table(headers, rows),
                value_type=value_type,
                message=Message(f"Raíz exacta en {x_str}={xr} con f({x_str})={fxr} a las {iterations+1} iteraciones.", MessageType.INFO),
            )

        elif fxl * fxr < 0:
            xu = xr
        else:
            xl = xr

        iterations += 1

    return Result(
        interest_value=xr,
        function_value=fxr,
        iterations=iterations,
        errors=errors,
        approximations=approximations,
        table=Table(headers, rows),
        value_type=value_type,
        var=var
    )