from src.preprocessing.stationarity import stationary_adf_test
import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from src.preprocessing.cleaner import actual_nans_df
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
warnings.filterwarnings("ignore")

date_format = "%Y-%m-%d"
path = "data/clean/to_be_featured.csv"
db = pd.read_csv(path, index_col=0)
db["date"] = db["date"].apply(lambda x: datetime.strptime(x, date_format))

# columnas que corresponde a features
features = list(db.columns)
features.remove("precio_leche")
features.remove("date")
db = db[["date", "precio_leche"] + features]
db.sort_values(by=["date"], inplace=True, ascending=False)
db.reset_index(drop=True, inplace=True)

# filtro en la temporalidad que tenemos la columna target
initial_date_milk = "1979-01-01"
initial_date_milk = datetime.strptime(initial_date_milk, date_format)
final_date_milk = "2020-05-01"
final_date_milk = datetime.strptime(final_date_milk, date_format)

# filtro
db = db[(db["date"] > initial_date_milk) & (db["date"] < final_date_milk)]
db.reset_index(drop=True, inplace=True)
# nans
cols_nans = actual_nans_df(db, threshold=50)
# columans que tinene menor al 50 % de nans
db = db[cols_nans]
features = list(db.columns)
features.remove("precio_leche")
features.remove("date")

# solo procesar los features [debo normalizar antes de hacer la imputación]
x = db[features]
# Normalizar datos X
sc = MinMaxScaler(feature_range=(0, 1))
# training
x = sc.fit_transform(x)

# hacer imputacion de nans
# podria imputar con interpolaciones lineales en la serie de tiempo, pero
# hay periodos que tienen muchos vacios, por tanto voy a hacer alguna técnica
# fancy de imputación de nans
imputer = KNNImputer(n_neighbors=5, weights='uniform', metric='nan_euclidean')
imputer.fit(x)
x_features = imputer.transform(x)
x_features = sc.inverse_transform(x_features)
x_features = pd.DataFrame(x_features, columns=features)
others = db[["date", "precio_leche"]]

# datos imputados
db_imputed = pd.concat([others, x_features], axis=1)

db = db_imputed.copy()


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

    for col in columns:
        lagged_column = col + f'_lagged_{str(nr_of_lags)}'
        df[lagged_column] = df[col].shift(nr_of_lags)
    return df


def cumulative_simple_stats(df, cols, window=3):
    """
    En una ventana temporal de tamaño window, se hace el cálculo de las medias
    mobiles en el tiempo y desviaciones estandar mobiles, solo para tener en
    cuenta el tamaño de la ventana debe ser mayor a 2

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


db.sort_values(by=["date"], inplace=True, ascending=True)
db.reset_index(drop=True, inplace=True)


cols = list(db.columns)
cols.remove("date")
# lag de 1 mes hacía atrás
db = add_lagged_variables(db, cols, nr_of_lags=1)
# lag de un trimestre hacía atrás
db = add_lagged_variables(db, cols, nr_of_lags=4)
# lag de 1 año
db = add_lagged_variables(db, cols, nr_of_lags=12)
# lag de dos años
db = add_lagged_variables(db, cols, nr_of_lags=24)

cols_nans = actual_nans_df(db, threshold=50)
print(len(cols_nans))
print(db.shape)

# estadisticas acumuladas de 3 meses
db = cumulative_simple_stats(db, cols, window=3)
# estadisticas acumuladas de 4 meses
db = cumulative_simple_stats(db, cols, window=4)
# estadisticas acumuladas de 12 meses
db = cumulative_simple_stats(db, cols, window=12)
# estadisticas acumuladas de 24 meses
db = cumulative_simple_stats(db, cols, window=24)


cols_nans = actual_nans_df(db, threshold=50)
print(len(cols_nans))
print(db.shape)

# # estadisticas acumuladas de 12 mes
db = cumulative_distribution_stats(db, cols, window=12)
# estadisticas acumuladas de 24 mes
db = cumulative_distribution_stats(db, cols, window=24)

db = log_features(db, cols)

cols_nans = actual_nans_df(db, threshold=50)
print(len(cols_nans))
print(db.shape)

alpha = db.isna().sum()
db.dropna(inplace=True)
print(db.shape)

stationary_test = stationary_adf_test(db, list(db.columns))
cols_stationaries = list(
    stationary_test[stationary_test["valor_p"] <= 0.05]["columna"])
cols_stationaries = ["date", "precio_leche"] + cols_stationaries
