import warnings
# import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
warnings.filterwarnings("ignore")
plt.style.use('dark_background')


def historical_time_series_plot(df, region, initial_date, end_date,
                                fontsize=12, window_size=12):
    """
    Graficar e precipitaciones historicas en un rango determinado de fechas
    determinado

    Parameters
    ----------
    df : pandas.dataframe
        Dataset de precipitaciones.
    region : string
        Nombre de la region.
    initial_date : string
        Fecha de inicio del gráfico.
    end_date : string
        Fecha de fin del gráfico.
    fontsize : int, optional
        Tamaño de la letra. The default is 12.
    window_size : int, optional
        Tamaño de la ventana temporal para ver media movil. The default is 5.
    fontsize : int
        Tamaño de la letra.

    Returns
    -------
    Visualización de la serie historica.

    """
    # ordenar valores por por tiempo
    df.sort_values(by=["date"], inplace=True, ascending=True)
    df.reset_index(drop=True, inplace=True)
    # transformar fechas a formato datetime
    initial_date = datetime.strptime(str(initial_date)[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date)[0:10], '%Y-%m-%d')
    # verificar limites de fechas
    initial_date = max(initial_date, df['date'].min())
    end_date = min(end_date, df['date'].max())
    # Media movil para ver tendencias
    df["moving_"+region] = df[region].rolling(window=window_size).mean()
    # filtrar los datos
    df_filter = df[(df['date'] <= end_date) & (df['date'] >= initial_date)]
    try:
        labels = df_filter['date'].apply(lambda x: str(x)[0:10]).to_list()
        rain = df_filter[region].to_list()
        moving = df_filter["moving_"+region].to_list()
        # sacar la columna
        df.drop(columns=["moving_"+region], inplace=True)
        df_filter.drop(columns=["moving_"+region], inplace=True)
        fig, ax = plt.subplots(1, figsize=(20, 12))
        ax.plot(labels, rain, 'blue', linewidth=2)
        ax.plot(labels, moving, 'orangered', linewidth=2)

        ax.set_xlabel('Tiempo', fontname="Arial", fontsize=fontsize)
        ax.set_ylabel(f'Precipitaciones mensuales {region}',
                      fontname="Arial", fontsize=fontsize+2)
        max_date, min_date = str(initial_date)[0:10], str(end_date)[0:10]
        ax.legend([region, f"Media Movil {str(window_size)} meses"],
                  loc='upper left',
                  prop={'size': fontsize+5})
        region = region.replace("_", " ").title()
        title =\
            f"Precipitaciones mm desde {min_date} hasta {max_date} | Región {region}"
        ax.set_title(title,
                     fontname="Arial", fontsize=fontsize+10)
        # Tamaño de los ejes
        for tick in ax.get_xticklabels():
            tick.set_fontsize(fontsize-2)
        for tick in ax.get_yticklabels():
            tick.set_fontsize(fontsize-2)
        plt.xticks(rotation=75)
        plt.show()
    except Exception as e:
        print(e)
        print("La región ingresada no se encuentra disponible en los datos")


def get_historical_data(df, region, initial_date, end_date):
    """
    Obtener información historica, de las precipitaciones para una región 
    en particular

    Parameters
    ----------
    df : pandas.dataframe
        Dataset de las precipitaciones.
    region : string
        Nombre de la región.
    initial_date : string
        Fecha inicial.
    end_date : string
        Fecha Final.

    Returns
    -------
    list
        Lista de los meses.
    list
        Lista de las precipitaciones.

    """
    # transformar fechas a formato datetime
    initial_date = datetime.strptime(str(initial_date)[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date)[0:10], '%Y-%m-%d')
    # verificar limites de fechas
    initial_date = max(initial_date, df['date'].min())
    end_date = min(end_date, df['date'].max())
    df_filter = df[(df['date'] <= end_date) & (df['date'] >= initial_date)]
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio',
              'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    df_filter['mes'] = df_filter['date'].apply(lambda x: months[x.month-1])
    return df_filter['mes'].to_list(), df_filter[region].to_list()


def plot_anual_time_series(df, years_list, region):
    """
    Hacer el gráfico anual como se pide en el desafio

    Parameters
    ----------
    df : pandas.dataframe
        Dataframe de las precipitaciones.
    years_list : list
        Lista con los años a plotear.
    region : string
        Nombre de la región.

    Returns
    -------
    Gráfica a nivel mensual de los años.

    """
    try:
        plt.figure(figsize=(22, 10))
        for year in years_list:
            initial_date = f"{year}-01-01"
            end_date = f"{year}-12-01"
            months, data = get_historical_data(
                df, region, initial_date, end_date)
            plt.plot(months, data)

        plt.legend(years_list)
        plt.xticks(rotation=90)
        plt.xlabel('Fecha')
        plt.ylabel('Precipitaciones mensual')

        title =\
            f"Precipitaciones mm desde {years_list[0]} hasta {years_list[-1]} de {region}"
        plt.title(title)
        plt.show()
    except Exception as e:
        print(e)
        print("La región ingresada no se encuentra en los datos")


def pib_time_series_plot(df, pib_name, initial_date, end_date, fontsize=12):
    """
    Graficar el PIB historico en un rango determinado de fechas
    determinado

    Parameters
    ----------
    df : pandas.dataframe
        Dataset de precipitaciones.
    pib_name : string
        Nombre de la pib_name.
    initial_date : string
        Fecha de inicio del gráfico.
    end_date : string
        Fecha de fin del gráfico.
    fontsize : int, optional
        Tamaño de la letra. The default is 12.
    fontsize : int
        Tamaño de la letra.

    Returns
    -------
    Visualización de la serie historica.

    """
    # ordenar valores por por tiempo
    df.sort_values(by=["Periodo"], inplace=True, ascending=True)
    df.reset_index(drop=True, inplace=True)
    # transformar fechas a formato datetime
    initial_date = datetime.strptime(str(initial_date)[0:10], '%Y-%m-%d')
    end_date = datetime.strptime(str(end_date)[0:10], '%Y-%m-%d')
    # verificar limites de fechas
    initial_date = max(initial_date, df['Periodo'].min())
    end_date = min(end_date, df['Periodo'].max())
    # filtrar los datos
    df_filter = df[(df['Periodo'] <= end_date) &
                   (df['Periodo'] >= initial_date)]
    try:
        labels = df_filter['string_fechas'].apply(
            lambda x: str(x)[0:10]).to_list()
        rain = df_filter[pib_name].to_list()
        fig, ax = plt.subplots(1, figsize=(20, 12))
        ax.plot(labels, rain, 'blue', linewidth=2)
        ax.set_xlabel('Tiempo', fontname="Arial", fontsize=fontsize)
        ax.set_ylabel(f'PIB {pib_name}',
                      fontname="Arial", fontsize=fontsize+2)
        max_date, min_date = str(initial_date)[0:10], str(end_date)[0:10]
        ax.legend([pib_name], loc='upper left', prop={'size': fontsize+5})
        pib_name = pib_name.replace("_", " ").title()
        title = f"PIB desde {min_date} hasta {max_date}"
        ax.set_title(title, fontname="Arial", fontsize=fontsize+10)
        # Tamaño de los ejes
        for tick in ax.get_xticklabels():
            tick.set_fontsize(fontsize-2)
        for tick in ax.get_yticklabels():
            tick.set_fontsize(fontsize-2)
        plt.xticks(rotation=75)
        plt.show()
    except Exception as e:
        print(e)
        print("La región ingresada no se encuentra disponible en los datos")
