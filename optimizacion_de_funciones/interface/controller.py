from numerical_methods.bisection import bisection
from numerical_methods.linear_interpolation import linear_interpolation
from numerical_methods.golden_ratio import golden_ratio
from numerical_methods.quadratic_interpolation import quadratic_interpolation
from numerical_methods.newtons_method import newtons_method
from numerical_methods.newton_raphson_method import newton_raphson_method
from numerical_methods.random_search import random_search


class Controller:

    def __init__(self):
        
        self.methods = {
            "Bisección": bisection,
            "Interpolación Lineal": linear_interpolation,
            "Razón Dorada": golden_ratio,
            "Interpolación Cuadrática": quadratic_interpolation,
            "Método de Newton": newtons_method,
            "Método de Newton-Raphson": newton_raphson_method,
            "Búsqueda Aleatoria": random_search,
        }

    def execute(self, method_name, f, **kwargs):

        method = self.methods.get(method_name)

        if not method:
            print("Método no encontrado:", method_name)
            return None

        if method_name in ["Bisección", "Interpolación Lineal"]:
            return method(f, kwargs["var"], kwargs["a"], kwargs["b"], kwargs["error"])

        elif method_name == "Razón Dorada":
            return method(f, kwargs["var"], kwargs["a"], kwargs["b"], kwargs["error"], kwargs.get("objective"))

        elif method_name == "Interpolación Cuadrática":
            return method(f, kwargs["var"], kwargs["x0"], kwargs["x1"], kwargs["x2"], kwargs["error"], kwargs.get("objective"))

        elif method_name == "Método de Newton":
            return method(
                f,
                kwargs["expr"],
                kwargs["var"],
                kwargs["x0"],
                kwargs["error"],
                kwargs.get("objective")
            )

        elif method_name == "Método de Newton-Raphson":
            return method(
                f,
                kwargs["expr"],
                kwargs["var"],
                kwargs["x0"],
                kwargs["error"]
            )

        elif method_name == "Búsqueda Aleatoria":

            def parse_bounds(bounds_str):
                return [float(x) for x in bounds_str.replace(" ", "").split(",")]

            lower_bounds = parse_bounds(kwargs["lim_inf"])
            upper_bounds = parse_bounds(kwargs["lim_sup"])

            return method(
                f,
                kwargs["var"],
                lower_bounds,
                upper_bounds,
                kwargs["iteraciones"],
                kwargs.get("objective")
            )

        else:
            print("Método no implementado:", method_name)
            return None