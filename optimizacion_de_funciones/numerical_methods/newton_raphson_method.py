from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

# Para el calculo de una raiz
def newton_raphson_method(f, expr, var, x0, error):

    import sympy as sp
    import numpy as np

    if error <= 0:

        return Result(
            interest_value=None,
            function_value=None,
            iterations=0,
            errors=[],
            approximations=[],
            table=None,
            value_type=ValueType.NONE,
            message=Message("El error debe ser mayor que cero.", MessageType.ERROR)
        )

    # Calcular la primera derivada
    try:
        symbol = sp.symbols(var)
        expr_sym = sp.sympify(expr.replace("^", "**"))

        df_expr = sp.diff(expr_sym, symbol)
        df_lamb = sp.lambdify(symbol, df_expr, modules=["numpy"])

        def df(x_val):
            result = df_lamb(x_val)
            return float(result) if np.isscalar(x_val) else np.array(result, dtype=float)

    except Exception as e:

        message = (
        f"Error al procesar la expresión matemática: {str(e)}.\n"
        "Asegúrese de seguir estas reglas:\n"
        "1. Use '*' para multiplicar (ej. '2*x' en lugar de '2x').\n"
        "2. Use '**' para potencias (ej. 'x**2').\n"
        "3. Use nombres de funciones estándar: 'sin(x)', 'cos(x)', 'exp(x)', 'log(x)', 'sqrt(x)'."
        )

        return Result(message=Message(message, MessageType.ERROR))

    value_type = ValueType.ROOT
    x_str = var[0]
    iterations = 0
    errors = []
    approximations = []
    rows = []
    headers = ["i", f"{var}i", f"f({var}i)", f"f'({var}i)", f"{var}i+1", "error"]

    xi = x0

    while True:

        try:

            fxi = f(xi)
            dfxi = df(xi)

        except Exception as e:

            message = (
            f"Error de cálculo en x = {xi:.6f}: {str(e)}.\n"
            "El método intentó evaluar un punto fuera del dominio de la función.\n"
            "(ej. división por cero, logaritmo de número negativo o raíz de número negativo).\n"
            "Sugerencia: Cambie el punto inicial x0 a una zona donde la función esté definida y sea continua."
            )

            return Result(message=Message(message, MessageType.ERROR))

        # Derivada cero o cercana a cero
        if abs(dfxi) < 1e-12:
            message = (
            f"Derivada nula detectada en x = {xi:.6f}.\n "
            "La recta tangente es horizontal, por lo que no puede calcularse la intersección con el eje X.\n"
            "Sugerencia: Intente con un punto inicial x0 diferente."
            )

            return Result(message=Message(message, MessageType.ERROR))
        
        xi_next = xi - (fxi / dfxi)
        fxi_next = f(xi_next)
        current_error = abs(xi_next - xi)

        errors.append(current_error)
        approximations.append(xi_next)
        rows.append([iterations, xi, fxi, dfxi, xi_next, current_error])

        # Raíz exacta 
        if abs(fxi_next) < 1e-10:
            return Result(
                interest_value=xi_next,
                function_value=fxi_next,
                iterations=iterations,
                errors=errors,
                approximations=approximations,
                table=Table(headers, rows),
                value_type=value_type,
                var=var
            )

        # Convergencia por error
        if current_error < error:
            return Result(
                interest_value=xi_next,
                function_value=fxi_next,
                iterations=iterations,
                errors=errors,
                approximations=approximations,
                table=Table(headers, rows),
                value_type=value_type,
                var=var
            )

        last_error = errors[-1] if errors else None

        # Estancamiento por precisión flotante
        if abs(xi - xi_next) < 1e-15:

            message=message = (
            f"Límite de precisión alcanzado: El valor de {x_str}={xi_next:.15f} ya no cambia significativamente.\n"
            "Esto puede ocurrir si la raíz buscada es de multiplicidad mayor a 1 o si el error solicitado es menor a la capacidad de la máquina.\n"
            f"Última evaluación: f({x_str}) = {fxi_next:.2e} a las {iterations+1} con error = {last_error}."
            )

            return Result(
                interest_value=xi_next,
                function_value=fxi_next,
                iterations=iterations,
                errors=errors,
                approximations=approximations,
                table=Table(headers, rows),
                value_type=ValueType.UNKNOWN,
                message=Message(message, MessageType.WARNING)
            )

        # Divergencia tras incrementos consecutivos
        if len(errors) >= 4:

            last_errors = errors[-4:]
            
            # crecimiento sostenido
            increasing = all(x < y for x, y in zip(last_errors, last_errors[1:]))

            # o crecimiento general
            if increasing or last_errors[-1] > 10 * last_errors[0]:

                return Result(
                    interest_value=xi_next,
                    function_value=fxi_next,
                    iterations=iterations,
                    errors=errors,
                    approximations=approximations,
                    table=Table(headers, rows),
                    value_type=ValueType.NONE,
                    message=Message(f"El método diverge: {x_str} = {xi_next} con f({x_str})={fxi_next} en {iterations+1} iteraciones con error = {last_error}.", MessageType.WARNING)
                )

        xi = xi_next
        iterations += 1