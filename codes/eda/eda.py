import pandas as pd
from src.eda.fast_eda import profiling_report

# paths
path_bc = "data/raw/banco_central.csv"
path_pr = "data/raw/precipitaciones.csv"

# cargar los datos
df_bank = pd.read_csv(path_bc)
df_pr = pd.read_csv(path_pr)

# extraer reportes de análisis exploratorias a través de la libreria
# pandas-profilling resultado en carpeta resutls/eda_{filname}.html
profiling_report(path_bc, minimal_mode=False, dark_mode=True,
                 filename="banco_central")

profiling_report(path_pr, minimal_mode=False, dark_mode=True,
                 filename="precipitaciones")
