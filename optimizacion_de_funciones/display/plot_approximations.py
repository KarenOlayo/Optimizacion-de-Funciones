from models.result import Result
from models.value_type import ValueType

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_approximations(result: Result):

    if result is None or result.approximations is None or len(result.approximations) == 0:
        print("No hay aproximaciones para graficar.")
        return

    approximations = result.approximations
    x = np.arange(len(approximations))

    fig, ax = plt.subplots()

    # Determinar tipo de valor
    if result.value_type == ValueType.ROOT:
        label_main = "aproximación de la raíz"
        color_main = "#1f77b4"   
    elif result.value_type == ValueType.MINIMUM:
        label_main = "aproximación del mínimo"
        color_main = "#2ecc71"   
    elif result.value_type == ValueType.MAXIMUM:
        label_main = "aproximación del máximo"
        color_main = "#e74c3c"   
    else:
        label_main = "aproximaciones"
        color_main = "#0b3c5d"

    # Curva de aproximaciones
    ax.plot(
        x, approximations,
        marker="o",
        color=color_main,
        linewidth=2,
        label=label_main,
        zorder=2
    )

    # Ejes de referencia
    ax.axhline(0, linestyle="--", color="gray", linewidth=1, zorder=0)
    ax.axvline(0, linestyle="--", color="gray", linewidth=1, zorder=0)

    # Última aproximación destacada
    ax.scatter(
        x[-1], approximations[-1],
        color="#e74c3c",
        s=100,
        label="última aproximación",
        zorder=3
    )

    # Etiqueta del valor final
    ax.annotate(
        f"{approximations[-1]:.6f}",
        (x[-1], approximations[-1]),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7)
    )

    # Configuración de ejes
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Aproximación")
    ax.set_title("Convergencia de las aproximaciones")

    # Solo enteros en eje X
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Cuadrícula suave
    ax.grid(True, linestyle="--", alpha=0.3)

    ax.legend()

    plt.tight_layout()

    return fig
