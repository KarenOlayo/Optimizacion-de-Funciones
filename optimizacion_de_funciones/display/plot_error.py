from models.result import Result
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def plot_error(result: Result):

    if result is None or result.errors is None or len(result.errors) == 0:
        print("No hay errores para graficar.")
        return

    errores = result.errors
    x = np.arange(len(errores))

    fig, ax = plt.subplots()

    # Curva de error
    ax.plot(
        x, errores,
        marker="o",
        color="#0b3c5d",  
        linewidth=2,
        label="error",
        zorder=2
    )

    # Ejes de referencia
    ax.axhline(0, linestyle="--", color="gray", linewidth=1, zorder=0)
    ax.axvline(0, linestyle="--", color="gray", linewidth=1, zorder=0)

    """
  # Anotar TODOS los errores
    for i in range(len(errores)):
        ax.annotate(
            f"{errores[i]:.2e}",
            (x[i], errores[i]),
            textcoords="offset points",
            xytext=(4, 4),
            fontsize=7,
            alpha=0.8
        )
    """

    # Punto final destacado
    ax.scatter(
        x[-1], errores[-1],
        color="#e74c3c",
        s=100,
        label="error final",
        zorder=3
    )

    # Etiqueta del último error
    ax.annotate(
        f"{errores[-1]:.6e}",
        (x[-1], errores[-1]),
        textcoords="offset points",
        xytext=(8, 8),
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7)
    )

    # Configuración de ejes
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Error")
    ax.set_title("Convergencia del método")

    # Solo enteros en eje X
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Cuadrícula suave
    ax.grid(True, linestyle="--", alpha=0.3)

    ax.legend()

    plt.tight_layout()

    return fig