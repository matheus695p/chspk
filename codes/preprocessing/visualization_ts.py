import pandas as pd
from datetime import datetime
from src.vizualizations.historical_series import (historical_time_series_plot,
                                                  pib_time_series_plot)

path_pr = "data/raw/precipitaciones.csv"
df_pr = pd.read_csv(path_pr)

date_format = "%Y-%m-%d"
df_pr["date"] = df_pr["date"].apply(
    lambda x: datetime.strptime(x, date_format))


region = 'Metropolitana_de_Santiago'
initial_date = '2000-01-01'
end_date = '2020-01-01'
historical_time_series_plot(df_pr, region, initial_date, end_date,
                            window_size=12)

path_pr = "data/raw/banco_central.csv"
df_bank = pd.read_csv(path_pr)

# pasar fechas a timestamps
date_format = "%Y-%m-%d"
df_bank = df_bank[df_bank["Periodo"] != "2020-13-01 00:00:00 UTC"]
df_bank["Periodo"] = df_bank["Periodo"].apply(
    lambda x: datetime.strptime(str(x[0:10]), date_format))
df_bank['string-fechas'] = df_bank['Periodo'].apply(
    lambda x: str(x.month)+'-'+str(x.year))
pib_columns = ['PIB_Servicios_financieros', 'PIB_Agropecuario_silvicola']
initial_date = '2013-01-01'
end_date = str(df_bank['Periodo'].max())[0:10]
for col in pib_columns:
    print(col)
    pib_time_series_plot(df_bank, col, initial_date, end_date)
