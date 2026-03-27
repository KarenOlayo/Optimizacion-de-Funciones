from models.value_type import ValueType
from models.message_type import MessageType
from models.message import Message


class Result:

    def __init__(self,
                 interest_value=None,
                 function_value=None,
                 iterations=0,
                 errors=None,
                 approximations=None,
                 table=None, 
                 value_type=ValueType.NONE,
                 var = 'x',
                 message: Message = None):
        
        self.interest_value = interest_value
        self.function_value = function_value
        self.iterations = iterations
        self.errors = errors or []
        self.approximations = approximations or []
        self.table = table
        self.value_type = value_type
        self.var = [v.strip() for v in var.split(",")]
        self.message = message or self._build_message()
        

    # Generador de mensaje
    def _build_message(self):

        if self.interest_value is None:
            return Message("No se obtuvo resultado.", MessageType.ERROR)

        x = self.interest_value
        fx = self.function_value
        error = self.errors[-1] if self.errors else None

        if isinstance(x, list):
            x_str = ", ".join(f"{name}={val:.4f}" for name, val in zip(self.var, x))
        else:
            x_str = self.var[0]

        if self.value_type == ValueType.MINIMUM:
            text = f"Mínimo aproximado en {x_str} ≈ {x} con f({x_str}) ≈ {fx} a las {self.iterations} iteraciones y error = {error}"
            return Message(text, MessageType.INFO)

        elif self.value_type == ValueType.MAXIMUM:
            text = f"Máximo aproximado en {x_str} ≈ {x} con f({x_str}) ≈ {fx}  a las {self.iterations} iteraciones y error = {error}"
            return Message(text, MessageType.INFO)

        elif self.value_type == ValueType.ROOT:
            text = f"Raíz aproximada en {x_str} ≈ {x} con f({x_str}) ≈ {fx} a las {self.iterations} iteraciones y error = {error}"
            return Message(text, MessageType.INFO)

        elif self.value_type == ValueType.UNKNOWN:
            text = (
                f"Se encontró un punto en {x_str} ≈ {x} con f({x_str}) ≈ {fx} a las {self.iterations} iteraciones y error = {error}"
            "pero no fue posible clasificarlo como mínimo o máximo.\n"
            "Esto puede indicar que la función no es unimodal o que el extremo está en el borde del intervalo.\n " 
            "Se recomienda analizar la gráfica o usar un intervalo más adecuado.\n"
            )
            return Message(text, MessageType.WARNING)

        return Message("Resultado obtenido.", MessageType.INFO)

    # Metodos para la interfaz
    def get_message_text(self):
        return self.message.text

    def get_message_type(self):
        return self.message.type

    def has_converged(self):
        return self.value_type != ValueType.NONE