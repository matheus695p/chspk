import numpy as np


def add_lagged_variables(df, columns, nr_of_lags=1):
    """
    Agregar variables pasadas del dataframe con el que se esta trabajando

    Parameters
    ----------
    df_input : pandas.dataframe
        Dataframe a operar.
    nr_of_lags : int
        Número de steps que quirees ir hacia atrás.
    columns : list
        Lista de columas a las cuales agregar variables lagged.

    Returns
    -------
    df : pandas.dataframe
        Dataframe con las variables lag agregadas.

    """
    for i in range(1, nr_of_lags+1):
        for col in columns:
            lagged_column = col + f'_lagged_{i}'
            df[lagged_column] = df[col].shift(i)
    return df


def log_features(df, columns):
    """
    Agregar logaritmo de las variables

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe a operar.
    columns : list
        lista de columas a las cuales agregar variables aplicar log.

    Returns
    -------
    df : df
        Dataframe con las variables agregadas con logaritmo.

    """
    for col in columns:
        log_column = 'log_' + col
        df[log_column] = df[col].apply(lambda x: np.log(x) + 1)
    return df


def cumulative_simple_stats(df, cols, window=3):
    """
    En una ventana temporal de tamaño window, se hace el cálculo de stats
    acumulativas como promedio y stad

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe a tratar.
    cols : list
        Lista de las columnas en las cuales aplicar stats.
    window : int, optional
        Tamaño de la ventana temporal. The default is 3.

    Returns
    -------
    df : pandas.dataframe
        Dataframe con las stats calculadas.

    """
    df.sort_values(by=['date'], inplace=True)
    # como se ven estacionalidades, nos centraremos en stats cercanas, al mes
    # que estamos analizando
    for columna in cols:
        # promedio 3 meses
        name1 = columna + f'_mean_{str(window)}'
        df[name1] = df[columna].rolling(window=window).mean()
        # desviacion standar ultimo año
        name2 = columna + f'_std_{str(window)}'
        df[name2] = df[columna].rolling(window=window).std()
    df.reset_index(drop=True, inplace=True)
    return df


def cumulative_distribution_stats(df, cols, window=12):
    """
    En una ventana temporal de tamaño window, se hace el cálculo de stats
    acumulativas como la como promedio y stad

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe a tratar.
    cols : list
        Lista de las columnas en las cuales aplicar stats.
    window : int, optional
        Tamaño de la ventana temporal. The default is 3.

    Returns
    -------
    df : pandas.dataframe
        Dataframe con las stats calculadas.

    """
    df.sort_values(by=['date'], inplace=True)
    # como se ven estacionalidades, nos centraremos en stats cercanas, al mes
    # que estamos analizando
    for columna in cols:
        # promedio 3 meses
        name1 = columna + f'_kurt_{str(window)}'
        df[name1] = df[columna].rolling(window=window).kurt()
        # desviacion standar ultimo año
        name2 = columna + f'_skew_{str(window)}'
        df[name2] = df[columna].rolling(window=window).skew()
    df.reset_index(drop=True, inplace=True)
    return df
