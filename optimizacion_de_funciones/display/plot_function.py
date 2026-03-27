from models.result import Result
from models.value_type import ValueType

import numpy as np
import matplotlib.pyplot as plt

import warnings
from matplotlib.widgets import Button


def plot_function(f, a, b, result: Result, user_points: dict = None):

    # Validación básica
    if result is None or result.interest_value is None:
        print("No hay valor de interés para graficar.")
        return

    xi = result.interest_value

    # Detectar dimension

    if isinstance(xi, (list, tuple, np.ndarray)):
        n = len(xi)
    else:
        n = 1

    # Determinar tipo de valor
    if result.value_type == ValueType.ROOT:
        label = "raíz aproximada"
        color_point = "#1f77b4"   
    elif result.value_type == ValueType.MINIMUM:
        label = "mínimo"
        color_point = "#2ecc71"   
    elif result.value_type == ValueType.MAXIMUM:
        label = "máximo"
        color_point = "#e74c3c"   
    else:
        label = "valor encontrado"
        color_point = "#1f77b4"
    

    # Caso 1D

    if n == 1:

        xi = float(xi)
        f_vec = np.vectorize(f)

        # Detectar si hay intervalo válido
        has_interval = False
        try:
            if a is not None and b is not None:
                a_f = float(a)
                b_f = float(b)
                has_interval = True
        except Exception:
            pass

        # Rango de graficación
        if has_interval:
            margin = abs(b_f - a_f) * 0.15 if a_f != b_f else max(abs(xi), 1.0) * 0.5
            x_min_full = min(a_f, b_f, xi) - margin
            x_max_full = max(a_f, b_f, xi) + margin
        else:
            # Sin intervalo: centrar en xi con radio fijo
            radius = max(abs(xi) * 2, 10.0)
            x_min_full = xi - radius
            x_max_full = xi + radius

        x_full = np.linspace(x_min_full, x_max_full, 800)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y_full = f_vec(x_full)

        y_masked = np.where(np.isfinite(y_full), y_full, np.nan)

        def safe_eval(val):
            try:
                v = f_vec(np.array([float(val)]))[0]
                return v if np.isfinite(v) else None
            except Exception:
                return None

        fxi = safe_eval(xi)
        fa  = safe_eval(a_f) if has_interval else None
        fb  = safe_eval(b_f) if has_interval else None

        fig, ax = plt.subplots(figsize=(9, 5))
        plt.subplots_adjust(bottom=0.18)

        ax.plot(x_full, y_masked,
                color="#0b3c5d", linewidth=2, label="f(x)", zorder=2)

        ax.axhline(0, linestyle="--", color="gray", linewidth=0.8, alpha=0.6, zorder=1)
        ax.axvline(0, linestyle="--", color="gray", linewidth=0.8, alpha=0.6, zorder=1)

        # ── Intervalo [a, b] — solo si existe ──
        if has_interval:
            ax.axvspan(a_f, b_f, facecolor="#5dade2", alpha=0.10, edgecolor="none", zorder=0)
            ax.axvline(a_f, color="#5dade2", linewidth=1.2, linestyle="-", alpha=0.8, zorder=1)
            ax.axvline(b_f, color="#5dade2", linewidth=1.2, linestyle="-", alpha=0.8, zorder=1)

            if fa is not None:
                ax.scatter(a_f, fa, color="#2980b9", s=90, zorder=5, label=f"a = {a_f}")
                ax.annotate(
                    f"a = {a_f}\nf = {fa:.4f}", (a_f, fa),
                    textcoords="offset points", xytext=(-58, 8),
                    fontsize=8, color="#2980b9",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              alpha=0.80, ec="#2980b9", lw=0.8)
                )

            if fb is not None:
                ax.scatter(b_f, fb, color="#2980b9", s=90, zorder=5, label=f"b = {b_f}")
                ax.annotate(
                    f"b = {b_f}\nf = {fb:.4f}", (b_f, fb),
                    textcoords="offset points", xytext=(6, 8),
                    fontsize=8, color="#2980b9",
                    bbox=dict(boxstyle="round,pad=0.25", fc="white",
                              alpha=0.80, ec="#2980b9", lw=0.8)
                )

        # Punto de interés
        if fxi is not None:
            ax.scatter(xi, fxi, color=color_point, s=120, zorder=6, label=label)
            mid = (x_min_full + x_max_full) / 2
            offset_x = -100 if xi > mid else 8
            ax.annotate(
                f"{label}\nx = {xi:.6f}\nf(x) = {fxi:.6f}", (xi, fxi),
                textcoords="offset points", xytext=(offset_x, 10),
                fontsize=8.5, color=color_point,
                bbox=dict(boxstyle="round,pad=0.3", fc="white",
                          alpha=0.85, ec=color_point, lw=1)
            )

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Gráfica de la función y resultado del método")
        ax.legend(loc="upper left", fontsize=8)

        y_finite = y_masked[np.isfinite(y_masked)]
        pad_y = (y_finite.max() - y_finite.min()) * 0.10 if len(y_finite) > 1 else 1.0
        x_lim0 = (x_min_full, x_max_full)
        y_lim0 = (y_finite.min() - pad_y, y_finite.max() + pad_y)

        ax.set_xlim(*x_lim0)
        ax.set_ylim(*y_lim0)

        # Puntos del usuario
        if user_points:
            colors = {"a": "#2980b9", "b": "#2980b9", "x0": "#8e44ad", "x1": "#e67e22", "x2": "#16a085"}
            offsets = {"a": (-58, 8), "b": (6, 8), "x0": (-58, 8), "x1": (6, 8), "x2": (6, -30)}

            for name, val in user_points.items():
                if val is None:
                    continue
                try:
                    px = float(val)
                    py = safe_eval(px)
                    if py is None:
                        continue

                    color = colors.get(name, "#555")
                    offset = offsets.get(name, (6, 8))

                    ax.scatter(px, py, color=color, s=80, zorder=5, label=f"{name} = {px}")
                    ax.annotate(
                        f"{name} = {px}\nf = {py:.4f}",
                        (px, py),
                        textcoords="offset points",
                        xytext=offset,
                        fontsize=8,
                        color=color,
                        bbox=dict(boxstyle="round,pad=0.25", fc="white",
                                alpha=0.80, ec=color, lw=0.8)
                    )
                except Exception:
                    continue

        return fig
        
    # Caso 2D con superficie 3D
    elif n == 2:

        if a is None or b is None:
            print("Límites no definidos para graficar.")
            return None

        try:
            if isinstance(a, str):
                a = [float(x) for x in a.replace(" ", "").split(",")]
            if isinstance(b, str):
                b = [float(x) for x in b.replace(" ", "").split(",")]
        except:
            print("Error al convertir límites.")
            return None

        x_opt, y_opt = xi

        x_vals = np.linspace(a[0], b[0], 100)
        y_vals = np.linspace(a[1], b[1], 100)

        X, Y = np.meshgrid(x_vals, y_vals)

        Z = np.zeros_like(X)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = f(X[i, j], Y[i, j])

        z_opt = f(x_opt, y_opt)

        

        fig = plt.figure(figsize=(9, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Angulo de vista inicial 
        elev_init, azim_init = 25, -60
        ax.view_init(elev=elev_init, azim=azim_init)

        # Superficie
        surf = ax.plot_surface(
            X, Y, Z,
            cmap='viridis',
            alpha=0.85,
            linewidth=0,
            antialiased=True
        )

        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)

        # Punto optimo
        ax.scatter(
            x_opt, y_opt, z_opt,
            color=color_point,
            s=120,
            zorder=5,
            label=f"{label}\nx={x_opt:.4f}, y={y_opt:.4f}\nf={z_opt:.4f}"
        )

        # Linea vertical punteada desde la base hasta el punto optimo
        ax.plot(
            [x_opt, x_opt],
            [y_opt, y_opt],
            [Z.min(), z_opt],
            color=color_point,
            linewidth=1.2,
            linestyle='--',
            alpha=0.7
        )

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("f(x, y)")
        ax.set_title("Superficie de la función y resultado del método")
        ax.legend(loc='upper left', fontsize=8)

        # Boton para resetear la vista al ángulo inicial
        ax_button = fig.add_axes([0.82, 0.02, 0.12, 0.04])
        btn = Button(ax_button, 'Centrar vista', color='#f0f0f0', hovercolor='#d0d0d0')

        def reset_view(event):
            ax.view_init(elev=elev_init, azim=azim_init)
            fig.canvas.draw_idle()

        btn.on_clicked(reset_view)

        # Guardar referencia para evitar que el garbage collector elimine el boton
        fig._reset_btn = btn

        return fig
    
    # Caso de 3 o mas variables (no implementado en el programa)
    else:
        return None