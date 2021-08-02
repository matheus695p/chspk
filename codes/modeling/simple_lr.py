import warnings
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
warnings.filterwarnings('ignore')


path = "data/modeling/data.pkl"
db = pd.read_pickle(path)

columns = list(db.columns)

model_features = ['date', 'precio_leche', 'year', 'month', 'trimestre',
                  'La_Araucania', 'PIB', 'PIB_Agropecuario_silvicola',
                  'PIB_Alimentos', 'Ocupacion_en_Agricultura_INE',
                  'La_Araucania_lagged_1', 'La_Araucania_lagged_12',
                  'precio_leche_lagged_1', 'precio_leche_lagged_12',
                  'PIB_Alimentos_lagged_12', 'PIB_lagged_12',
                  'Ocupacion_en_Agricultura_INE_lagged_1',
                  'La_Araucania_mean_3', 'La_Araucania_mean_12',
                  'La_Araucania_std_12', 'Los_Rios_mean_3']

# model_features = ['date',
#                   'year', 'month', 'trimestre',
#                   'precio_leche',
#                   'precio_leche_lagged_1', 'precio_leche_lagged_4',
#                   'precio_leche_lagged_12', 'precio_leche_lagged_24',
#                   'La_Araucania',
#                   'La_Araucania_lagged_1', 'La_Araucania_lagged_4',
#                   'La_Araucania_lagged_12', 'La_Araucania_lagged_24',
#                   'PIB_Alimentos',
#                   'PIB',
#                   'PIB_Alimentos',
#                   'PIB_Agropecuario_silvicola',
#                   'Ocupacion_en_Agricultura_INE',
#                   'PIB_Alimentos_lagged_12',
#                   'PIB_lagged_12',
#                   'Ocupacion_en_Agricultura_INE_lagged_1',
#                   'La_Araucania_mean_3', 'La_Araucania_mean_12',
#                   'La_Araucania_std_12', 'Los_Rios_mean_3',
#                   'Precio_del_petroleo_WTI_dolaresbarril',
#                   'Precio_de_la_gasolina_en_EEUU_dolaresm3']


# model_features = actual_nans_df(db, threshold=80)
# model_features.remove("string_fechas")
# seleccionar los features del modelo
db = db[model_features]


db["target"] = db["precio_leche"].shift(-1)

db.sort_values(by=["date"], ascending=True, inplace=True)

# ordenar las columnas para hacerlas visibles
order = list(db.columns)
order.remove("date")
order.remove("target")
order.remove("precio_leche")

db = db[["date", "precio_leche", "target"] + order]


# sacar los features disponibles
features = list(db.columns)
features.remove("date")
features.remove("target")

db.replace([np.inf, -np.inf], np.nan, inplace=True)
db.dropna(inplace=True)
db.reset_index(drop=True, inplace=True)


x = db[features]
x.drop(columns=["precio_leche"], inplace=True)

y = db[["target"]]

x = x.to_numpy()
y = y.to_numpy()

# normalizar los features
# Normalizar datos X
sc = MinMaxScaler()
# training
x = sc.fit_transform(x)

# time series kFold
tscv = TimeSeriesSplit(n_splits=5)

results = []
iteration = 1
for train_index, test_index in tscv.split(x):
    print("TRAIN:", train_index, "TEST:", test_index)
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    lr = LinearRegression().fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    mae = mean_absolute_error(y_pred, y_test)
    mse = mean_squared_error(y_pred, y_test)
    rmse = np.sqrt(mean_squared_error(y_pred, y_test))
    std = np.abs(y_pred-y_test).std()

    results.append([iteration, mae, mse, rmse, std])
    iteration += 1

results = pd.DataFrame(
    results, columns=["iteracion", "MAE", "MSE", "RMSE", "VARIANCE"])
results["algoritmo"] = "regresion_lineal"

print("Mean absolute error:", results["MAE"].mean())
print("Mean squared error:", results["MSE"].mean())
print("Root mean squared error:", results["RMSE"].mean())
print("Root mean squared error:", results["VARIANCE"].mean())
