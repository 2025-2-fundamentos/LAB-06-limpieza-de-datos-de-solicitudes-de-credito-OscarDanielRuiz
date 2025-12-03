"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import pandas as pd
    import os


    def cargar_datos(ruta):
        return pd.read_csv(ruta, sep=";", index_col=0)

    def limpiar_sexo(df):
        df["sexo"] = df["sexo"].str.lower().astype("category")
        return df

    def parsear_fecha(df, columna="fecha_de_beneficio"):
        fecha_formato_1 = pd.to_datetime(df[columna], format="%d/%m/%Y", errors="coerce")
        fecha_formato_2 = pd.to_datetime(df[columna], format="%Y/%m/%d", errors="coerce")

        df[columna] = fecha_formato_1.combine_first(fecha_formato_2)
        return df

    def limpiar_monto(df):
        df["monto_del_credito"] = (
            df["monto_del_credito"]
            .str.strip()
            .str.replace(r"[$,]", "", regex=True)
            .str.replace(".00", "", regex=False)
            .astype(int)
        )
        return df

    def limpiar_barrio(df):
        df["barrio"] = (
            df["barrio"]
            .str.lower()
            .str.replace(r"[_-]", " ", regex=True)
        )
        return df

    def normalizar_textos(df, columnas):
        for columna in columnas:
            df[columna] = (
                df[columna]
                .str.lower()
                .str.replace(r"[_-]", " ", regex=True)
                .str.strip()
            )
        return df

    def eliminar_duplicados_y_nulos(df):
        df = df.drop_duplicates()
        df = df.dropna()
        return df


    ruta_entrada = "files/input/solicitudes_de_credito.csv"
    carpeta_salida = "files/output/"
    columnas_norm = ["idea_negocio", "línea_credito", "tipo_de_emprendimiento"]
    os.makedirs(carpeta_salida, exist_ok=True)
    df = cargar_datos(ruta_entrada)
    df = limpiar_sexo(df.copy())
    df = parsear_fecha(df)
    df = limpiar_monto(df)
    df = limpiar_barrio(df)
    df = normalizar_textos(df, columnas_norm)
    df = eliminar_duplicados_y_nulos(df)
    ruta_salida = os.path.join(carpeta_salida, "solicitudes_de_credito.csv")
    df.to_csv(ruta_salida, sep=";", index=True)