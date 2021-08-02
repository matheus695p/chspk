import numpy as np
import pandas as pd


def actual_nans_df(df, threshold=50):
    """
    Dado un threshold de nans, devuelve las columnas que cumplen con el
    criterio porcentaje de nans < threshold.

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe en el cual ver la cantidad de nans.
    threshold : float, optional
        Threshold de nans. The default is 50.

    Returns
    -------
    cols : list
        Lista de las columnas que cumplen con tener mejor cantidad de nans
        que el threhold establecido.

    """
    nans = pd.DataFrame(df.isna().sum(), columns=["missing"])
    nans.reset_index(drop=False, inplace=True)
    nans.rename(columns={"index": "columna"}, inplace=True)
    nans["porcentaje_nans"] = nans["missing"] / len(df) * 100
    cols = list(nans[nans["porcentaje_nans"] <= threshold]["columna"])
    return cols


def values_treatement(df):
    """
    Hacer el tratamiento de valores sobre el dataset del banco central

    Parameters
    ----------
    df : pandas.dataframe
        Data banco central.

    Returns
    -------
    df : pandas.dataframe
        Data banco central con las columnas tratadas.

    """
    # ordenar datos por fecha
    df.sort_values(by=["Periodo"], inplace=True, ascending=False)
    df.reset_index(drop=True, inplace=True)
    columns = list(df.columns)
    columns.remove("Periodo")
    for col in columns:
        # cada columna tiene un tratamiento distinto, dependiendo de lo que
        # corresponde
        if "Imacec" in col:
            print("Procesando columna IMACEC:", col)
            df = imacec_values_cleaning(df, col, thresh_imacec=20)
        elif "PIB" in col:
            print("Procesando una columna de PIB:", col)
            df = pib_values_cleaning(df, col)
        elif "Precio" in col:
            print("Procesando una columna de Precio:", col)
            # hacer el parsing de la columna como string
            df = string_parser(df, col)
            df[col] = df[col].apply(float) / 10 ** 5
            # aplicar factor de amplificacion
            df[col] = df[col].apply(lambda x: reduction_factor(x))
        else:
            print("Procesando una columna:", col)
            # hacer el parsing de la columna como string
            df = string_parser(df, col)
            df[col] = df[col].apply(float) / 10 ** 5
            # aplicar factor de amplificacion
            df[col] = df[col].apply(lambda x: reduction_factor(x))
    return df


def string_parser(df, col):
    """
    Para una columna en particular hace el parseo del valor entregado en la
    columna

    Parameters
    ----------
    df : pandas.dataframe
        Dataset del banco central.
    col : string
        Columna a tratar.

    Returns
    -------
    df : pandas.dataframe
        Dataset del banco central con la columna parseada.

    """
    # ajusto y parseo los strings para que queden del mismo largo
    df[col] = df[col].apply(str)
    df[col] = df[col].apply(lambda x: x.replace(".", ""))
    length = df[col].apply(lambda x: len(x)).max()
    df[col] = df[col].apply(
        lambda x: string_replacement(x, length))
    return df


def imacec_values_cleaning(df, col, thresh_imacec=20):
    """
    Hace el tratamiento de limpieza de todas las columnas de imacec para dejar
    en un rango de 0-100

    Parameters
    ----------
    df : pandas.datframe
        Dataset de banco.
    col : string
        Nombre de la columna.
    thresh_imacec : float, optional
        Umbral de filtro en la columna. The default is 20.

    Returns
    -------
    df : pandas.dataframe
        Dataset banco central con las columnas del imacec limpias.

    """
    # hacer el parsing de la columna como string
    df = string_parser(df, col)
    # divido en factor 10**7 ---> imacec [90, 120]
    df[col] = df[col].apply(float) / 10**7
    df[col] = df[col].apply(
        lambda x: x * 10 if x <= thresh_imacec else x)
    return df


def pib_values_cleaning(df, col):
    """
    Trata las columans del PIB del dataset del banco central

    Parameters
    ----------
    df : pandas.datframe
        Dataset de banco.
    col : string
        Nombre de la columna.

    Returns
    -------
    df : pandas.dataframe
         Dataset banco central con las columnas del PIB limpias.

    """
    # hacer el parsing de la columna como string
    df = string_parser(df, col)
    # divido en factor 10**5 para con la función estadarizar al [M]
    df[col] = df[col].apply(float) / 10**5
    # aplicar factor de amplificacion
    df[col] = df[col].apply(lambda x: reduction_factor(x))
    # correcciones particulares para cada columna para dejar en el rango
    if col == "PIB_Pesca":
        df[col] = df[col].apply(lambda x: 10 * x if x <= 150 else x)
    if col == "PIB_Refinacion_de_petroleo":
        df[col] = df[col].apply(lambda x: x / 10 if x >= 150 else x)
    if col == "PIB_Minerales_no_metalicos_y_metalica_basica":
        df[col] = df[col].apply(lambda x: 10 * x if x <= 150 else x)
    if col == "PIB_Construccion":
        df[col] = df[col].apply(lambda x: 10 * x if x <= 150 else x)
    if col == "PIB_Servicios_de_vivienda":
        df[col] = df[col].apply(lambda x: 10 * x if x <= 150 else x)
    if col == "PIB_Servicios_personales":
        df[col] = df[col].apply(lambda x: x / 10 if x >= 200 else x)
    return df


def reduction_factor(x):
    """
    Función para amplificar los valores del PIB en función del rango que están
    quedando

    Parameters
    ----------
    x : float
        Valor del KPI.

    Returns
    -------
    valor : float
        Valor del KPI ajustado en el rango.

    """
    if ((x/1000) > 1) & (x < 8000):
        valor = x / 10
    else:
        valor = x / 100
    return valor


def string_replacement(string, length):
    """
    Esta función fue creada para agregar ceros al final de cada string, con
    el fin de dejar a todos los números de una columna con un largo único, de
    tal forma de poder dejarlos en el mismo rango de magnitud de valores, sin
    perdidas de información por generación de outliers.

    Parameters
    ----------
    string : string
        Número que se quiere formatear el flotante.
    length : int
        Máximo largo encontrado en una columna sin los puntos.

    Returns
    -------
    string : string
        Número con el largo equivalente al máximo de su propia columna.

    """
    if str(string) != "nan":
        l_string = len(string)
        diff = length - l_string
        missing = ""
        for i in range(diff):
            missing = missing + "0"
        string += missing
    return string


def renaming_columns(df):
    """
    Convertir columnas de un dataframe en flotantes

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe que se deben renombrar las columnas.

    Returns
    -------
    df : pandas.dataframe
        Dataframe con las columnas renombradas.

    """
    for col in df.columns:
        try:
            new_col = col.lower()
            df.rename(columns={col: new_col}, inplace=True)
        except Exception:
            pass
    df.reset_index(drop=True, inplace=True)
    return df


def convert_df_float(df):
    """
    Convertir columnas de un dataframe en flotantes

    Parameters
    ----------
    df : pandas.dataframe
        Pasar todas las columnas de un dataset tabular a float.

    Returns
    -------
    df : pandas.dataframe
        Dataframe con las columnas transformadas a flotante.

    """
    for col in df.columns:
        try:
            df[col] = df[col].apply(float)
        except Exception:
            pass
    df.reset_index(drop=True, inplace=True)
    return df


def drop_spaces_data(df):
    """
    Sacar los espacios de columnas que podrián venir interferidas

    Parameters
    ----------
    df : pandas.dataframe
        Input data
    column : string
        String sin espacios en sus columnas

    Returns
    -------
        Sacar espacios en los inicios y fines de las columnas categoricas

    """
    for column in df.columns:
        try:
            df[column] = df[column].str.lstrip()
            df[column] = df[column].str.rstrip()
        except Exception as e:
            print(e)
            pass
    return df


def make_empty_identifiable(value):
    """
    Hacer identificables los vacios, dado que pueden venir con el valor "a".

    Parameters
    ----------
    value : int, string, etc
        Valor con el que se trabaja.

    Returns
    -------
        np.nan en los vacios.

    """
    if value == "a":
        value = np.nan
    return value


def replace_empty_nans(df):
    """
    Hace identificable los vacios con nans, para en el momento de tratarlos
    agarrarlos todos.

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe con el que se esta trabajando.

    Returns
    -------
        Colocar nans en los vacios.

    """
    for col in df.columns:
        print("Reemplazando 'a':", col, "...")
        df[col] = df[col].apply(lambda x: make_empty_identifiable(x))
    return df
