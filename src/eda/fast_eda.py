import pandas as pd
from pandas_profiling import ProfileReport


def profiling_report(path_csv, minimal_mode=False, dark_mode=True,
                     filename="data"):
    """
    Utiliza la libreria pandas_profiling para hacer una exploración visual
    rápida de los datos

    Parameters
    ----------
    path_csv : string
        path al .csv que contiene la data.
    minimal_mode : string, optional
        En el caso de que sea True, hace cálculo de correlaciones no lineales.
        The default is False.
    dark_mode : string, optional
        si es en el modo oscuro o no. The default is True.
    filename : string, optional
        Nombre del archivo a analizar. The default is "data".

    Returns
    -------
    Archivo .html con un análisis exploratorio rápido de los datos.

    """
    # lectura del .csv
    df = pd.read_csv(path_csv)
    name = filename.replace("_", " ").title()

    title = f"Análisis Eploratorio de Data: Spike {name}"
    prof = ProfileReport(df,
                         title=title,
                         explorative=False,
                         minimal=minimal_mode,
                         dark_mode=dark_mode)
    # guardar el html
    path_output = f'results/eda_{filename}.html'
    prof.to_file(output_file=path_output)
