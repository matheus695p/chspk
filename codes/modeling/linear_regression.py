import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

path = "data/clean/train.csv"
db = pd.read_csv(path)

date_format = "%Y-%m-%d"
db["date"] = db["date"].apply(lambda x: datetime.strptime(x, date_format))
db.sort_values(by=["date"], ascending=True, inplace=True)

features = list(db.columns)
features.remove("date")
features.remove("precio_leche")

x = db[features]
y = db[["precio_leche"]]

for col in features:
    x.rename(columns={col: "col_" + str(col)}, inplace=True)

x = x.to_numpy()
y = y.to_numpy()

# time series kFold
tscv = TimeSeriesSplit(n_splits=10)

errors = []
iteration = 1
for train_index, test_index in tscv.split(x):
    print("TRAIN:", train_index, "TEST:", test_index)
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    lr = LinearRegression().fit(x_train, y_train)
    y_pred = lr.predict(x_test)
    mae = mean_absolute_error(y_pred, y_test)
    mse = mean_squared_error(y_pred, y_test)
    errors.append([iteration, mae, mse])
    iteration += 1
