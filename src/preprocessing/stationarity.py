import pandas as pd
from statsmodels.tsa.stattools import adfuller


def stationary_adf_test(df, cols):
    """
    Test de estacionaridad
    Augmented Dickey-Fuller puede ser una de las más utilizadas.
    Utiliza un modelo autorregresivo y optimiza un criterio de información
    a través de múltiples valores de retardo (lags) diferentes.

    La hipótesis nula de la prueba es que la serie de tiempo se puede
    representar mediante una raíz unitaria, que no es estacionaria
    (tiene alguna estructura dependiente del tiempo).

    La hipótesis alternativa (que rechaza la hipótesis nula) es que la serie
    de tiempo es estacionaria.

    * Hipótesis nula (H0): si no se rechaza, sugiere que la serie de tiempo
    tiene una raíz unitaria, lo que significa que no es estacionaria.
    Tiene alguna estructura dependiente del tiempo.

    * Hipótesis alternativa (H1): Se rechaza la hipótesis nula; sugiere que
    la serie de tiempo no tiene una raíz unitaria, lo que significa que es
    estacionaria. No tiene una estructura dependiente del tiempo.

    Voy a interpretar este resultado utilizando el valor p de la prueba.
    Un valor p por debajo de un umbral (como 5% o 1%) sugiere que rechazamos

    la hipótesis nula (estacionaria); de lo contrario, un valor p por encima
    del umbral sugiere que no rechazamos la hipótesis nula (no estacionaria),
    este es el lo clásico en tests estadísticos.

    * Valor p> 0.05: No se rechaza la hipótesis nula (H0),
    los datos no son estacionarios
    * Valor de p <= 0.05: Rechaza la hipótesis nula (H0),
    los datos son estacionarios

    Parameters
    ----------
    df : pandas.dataframe
        dataframe al cual se le harán pruebas de estacionaridad a todas sus
        columnas.
    cols : list
        Lista de columnas.

    Returns
    -------
    output : pandas.dataframe
        Resultados del test.

    """
    output = []
    for col in cols:
        try:
            datai = df[[col]]
            # datai = datai[datai[col] > 0]
            result = adfuller(datai.values)
            # descomprimir valores
            p = result[1]
            print("Para la columna: ", col)
            print(comentary_stationarity(p))
            print('ADF estadisticas: %f' % result[0])
            print('Valor de p: %f' % result[1])
            print('Valores criticos:')
            for key, value in result[4].items():
                print('\t%s: %.3f' % (key, value))
            output.append([col, comentary_stationarity(p),
                          p, list(result[4].items())])
        except Exception:
            print("No hubo convergencia")
    output = pd.DataFrame(output, columns=["columna", "resultado",
                                           "valor_p", "intervalos"])
    return output


def comentary_stationarity(p):
    """
    Comentario de la estacionaridad de las
    Parameters
    ----------
    p : TYPE
        DESCRIPTION.
    Returns
    -------
    comments : TYPE
        DESCRIPTION.
    """
    if p <= 0.05:
        comments =\
            "Rechaza la hipótesis nula (H0), los datos son estacionarios"
    else:
        comments =\
            "No se rechaza la hipótesis nula (H0), los datos no son estacionarios"
    return comments
