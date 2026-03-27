from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

def linear_interpolation(f, var, a, b, error):

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
            message=Message(f"Raíz exacta en el límite inferior: {x_str} = {xl} con f({x_str})={f(xl)} .", MessageType.WARNING),
            value_type=value_type
        )

    if f(xu) == 0:

        return Result(
            interest_value=xu,
            function_value=f(xu),
            message=Message(f"Raíz exacta en el límite superior: {x_str} = {xl} con f({x_str})={f(xl)} .", MessageType.WARNING),
            value_type=value_type
        )

    if f(xl) * f(xu) > 0:

        message = f"No se pudo determinar una raíz en el intervalo [{xl}, {xu}]. Esto pudo ser debido a que:\n"
        "- No existe una raíz en el intervalo.\n"
        "- Hay más de una raíz en el intervalo.\n"
        "- La función toca el eje pero no lo cruza, por lo que no hay cambio de signo aunque exista una raíz. Por ejemplo, f(x)=x**2"

        return Result(message=Message(message, MessageType.ERROR))

    iterations = 0
    errors = []
    approximations = []
    rows = []
    headers = ["i", f"{var}l", f"{var}u", f"f({var}l)", f"f({var}u)", f"{var}r", f"f({var}r)", f"f({var}l)*f({var}r)", "error"]

    while True:

        fxl = f(xl)
        fxu = f(xu)

        # Evitar division por cero 
        if abs(fxl - fxu) < 1e-12:
            message = (
            "Error de división por cero: La pendiente entre los puntos es casi horizontal.\n"
            f"Esto ocurre cuando f({x_str}l) ≈ f({x_str}u), impidiendo calcular la intersección.\n"
            "Sugerencia: Intente ajustar los límites del intervalo [a, b] para que los valores"
            "de la función sean más distantes entre sí."
            )

            return Result(message=Message(message ,MessageType.ERROR))

        xr = xu - (fxu * (xl - xu)) / (fxl - fxu)
        fxr = f(xr)

        current_error = abs(xr-xl)
        errors.append(current_error)
        approximations.append(xr)

        rows.append([iterations, xl, xu, fxl, fxu, xr, fxr, fxl * fxr, current_error])

        iterations += 1
        
        # Caso raiz exacta
        if abs(fxr) == 0:

            message= f"Raíz exacta en {x_str}={xr} con f({x_str})={fxr} a las {iterations+1} iteraciones."

            return Result(
            interest_value=xr,
            function_value=fxr,
            iterations=iterations,
            errors=errors,
            approximations=approximations,
            table=Table(headers, rows),
            value_type=value_type,
            var=var,
            message=Message(message, MessageType.INFO)
        )

        if current_error < error or abs(fxr) < error:
            break

        if fxl * fxr < 0:
            xu = xr
        else:
            xl = xr

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