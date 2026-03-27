from models.result import Result
import pandas as pd


def show_table(result: Result, styled=False):

    if result is None or result.table is None:
        print("No hay tabla para mostrar.")
        return

    table = result.table

    if table.rows is None or len(table.rows) == 0:
        print("La tabla está vacía.")
        return

    df = pd.DataFrame(table.rows, columns=table.headers)

    if not styled:
        print(df)
        return df

    return (
        df.style
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#0b3c5d"),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("border", "1px solid black"),
                    ("text-align", "center")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("border", "1px solid black"),
                    ("text-align", "center")
                ]
            }
        ])
    )