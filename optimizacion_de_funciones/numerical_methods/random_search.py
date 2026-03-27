from models.result import Result
from models.message_type import MessageType
from models.value_type import ValueType
from models.table import Table
from models.message import Message

import random

def random_search(f, var, lower_bounds, upper_bounds, iterations, objective):

    if not isinstance(lower_bounds, list) or not isinstance(upper_bounds, list):
        return Result(
            value_type=ValueType.NONE,
            message=Message("Los límites deben ser listas (valores separados por coma).", MessageType.ERROR)
        )

    if len(lower_bounds) != len(upper_bounds):
        return Result(
            value_type=ValueType.NONE,
            message=Message("Los límites deben tener la misma dimensión.", MessageType.ERROR)
        )

    if len(lower_bounds) != 2:
        return Result(
            value_type=ValueType.NONE,
            message=Message("Este método solo está implementado para 2 variables.", MessageType.ERROR)
        )

    x1_min, x2_min = lower_bounds
    x1_max, x2_max = upper_bounds

    if x1_min >= x1_max or x2_min >= x2_max:
        return Result(
            value_type=ValueType.NONE,
            message=Message("Cada límite inferior debe ser menor que el superior.", MessageType.ERROR)
        )

    if iterations <= 0:
        return Result(
            value_type=ValueType.NONE,
            message=Message("Las iteraciones deben ser mayores que cero.", MessageType.ERROR)
        )

    if objective not in ["Mínimo", "Máximo"]:
        return Result(
            value_type=ValueType.NONE,
            message=Message("Debe seleccionar 'Mínimo' o 'Máximo'.", MessageType.ERROR)
        )

    approximations = []
    rows = []

    headers = ["i", "X", "f(X)", "mejor_X", "mejor_f"]

    # Valor centinela 
    if objective == "Máximo":
        best_f = -1e9
    else:
        best_f = 1e9

    best_x = None

    
    #   x = xl + (xu - xl) * r     donde r = random.uniform(0, 1)
    #   y = yl + (yu - yl) * r
  
    for j in range(1, iterations + 1):

        # Generar punto aleatorio dentro del dominio
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)

        xi1 = x1_min + (x1_max - x1_min) * r1
        xi2 = x2_min + (x2_max - x2_min) * r2

        xi = [xi1, xi2]
        fxi = f(xi1, xi2)

        if objective == "Máximo":
            if fxi > best_f:
                best_x = xi.copy()
                best_f = fxi
        else:  
            if fxi < best_f:
                best_x = xi.copy()
                best_f = fxi

        approximations.append(best_x.copy() if best_x is not None else xi.copy())

        rows.append([
            j,
            str(xi),
            fxi,
            str(best_x) if best_x is not None else "-",
            best_f
        ])

    # Si ningún punto supero el centinela, best_x puede seguir siendo None — se usa el ultimo xi.

    if best_x is None:
        best_x = [xi1, xi2]

    value_type = ValueType.MAXIMUM if objective == "Máximo" else ValueType.MINIMUM

    table = Table(headers, rows)

    message = Message(f"Mejor solución encontrada: X = {best_x} con f(X) = {best_f} en {iterations} iteraciones.", MessageType.INFO)

    return Result(
        interest_value=best_x,
        function_value=best_f,
        iterations=iterations,
        approximations=approximations,
        table=table,
        message=message,
        var=var,
        value_type=value_type
    )