import pandas as pd
from hampel import hampel
from datetime import datetime
from src.preprocessing.cleaner import (drop_spaces_data, replace_empty_nans,
                                       values_treatement)

# paths
path_bc = "data/raw/banco_central.csv"
path_pr = "data/raw/precipitaciones.csv"

# cargar los datos
df_bank = pd.read_csv(path_bc)
df_pr = pd.read_csv(path_pr)

df_bank = drop_spaces_data(df_bank)
df_bank = replace_empty_nans(df_bank)

date_format = "%Y-%m-%d"
df_bank = df_bank[df_bank["Periodo"] != "2020-13-01 00:00:00 UTC"]
df_bank["Periodo"] = df_bank["Periodo"].apply(
    lambda x: datetime.strptime(str(x[0:10]), date_format))

df = df_bank.copy()
# limpieza de los datos
df_bank = values_treatement(df_bank)
