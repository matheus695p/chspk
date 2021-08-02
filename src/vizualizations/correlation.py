import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm as cm
warnings.filterwarnings("ignore")
plt.style.use('dark_background')


def correlation_matrix(df, method="pearson"):
    """
    Hacer matriz de correlaciones según distintos métodos de correlación,
    para analizar a simple vista los datos

    Parameters
    ----------
    df : dataframe
        dataset que estamos analizando.
    method : string, optional
        método de correlación soportados por libreria pandas
        {‘pearson’, ‘kendall’, ‘spearman’} .
        The default is "pearson".

    Returns
    -------
        Plot de matplotlib.pyplot de la matriz de correlación.

    """
    letter_size = 30
    fig = plt.figure(figsize=(70, 70))
    ax = fig.add_subplot(111)
    cmap = cm.get_cmap('hot_r', 30)
    ax = fig.add_subplot(111)
    size = int(len(list(df.columns))/2)
    corr = df.corr(method=method)
    fig, ax = plt.subplots(figsize=(size, size))
    # ax.matshow(corr, cmap=cmap)
    sns.heatmap(corr, annot=True, cmap=cmap)
    plt.xticks(range(len(corr.columns)), corr.columns, fontsize=letter_size)
    plt.yticks(range(len(corr.columns)), corr.columns, fontsize=letter_size)
    ax.set_xticklabels(df.columns, fontsize=letter_size)
    ax.set_yticklabels(df.columns, fontsize=letter_size)
    plt.xticks(rotation=90)
    # plt.yticks(rotation=90)
    ax.set_title(f"Matriz de correlación, método: {method}",
                 fontname="Arial", fontsize=letter_size+10)
