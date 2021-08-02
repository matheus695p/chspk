![Build Status](https://www.repostatus.org/badges/latest/concept.svg)

# Spike Challenge

Repositorio para hacer el desafío de la empresa Spike.

Link al desafío:
[Desafio](https://github.com/matheus695p/chspk/blob/master/documents/Spike_Challenge_precios.pdf)


## Jupyter Notebook que tiene las respuestas al desafío:

[Notebook](https://github.com/matheus695p/chspk/blob/master/main.ipynb)

## Setup ambiente

```sh
$ git clone https://github.com/matheus695p/chspk.git
$ cd chspk
$ pip install -r requirements.txt
```

## Arbol del desafío

```sh

│   .gitignore
│   main.ipynb --- > JUPYTER NOTEBOOK A REVISAR
│   README.md
│   requirements.txt
│
├───.ipynb_checkpoints
│       main-checkpoint.ipynb
│
├───codes
│   ├───cleaning
│   │       clean.py
│   │
│   ├───eda
│   │       eda.py
│   │
│   ├───feature-engineering
│   │       feature_engineering.py
│   │
│   ├───modeling
│   │       linear_regression.py
│   │       simple_lr.py
│   │
│   └───preprocessing
│           preprocessing.py
│           visualization_ts.py
│
├───data
│   ├───clean
│   │       to_be_featured.csv
│   │       train.csv
│   │
│   ├───modeling
│   │       data.pkl
│   │
│   └───raw
│           banco_central.csv
│           precio_leche.csv
│           precipitaciones.csv
│
├───images
│   │   impulso_artistico.jpeg
│   │   ts_cross_validation.png
│   │
│   ├───banco-central
│   └───precipitaciones
│           fecha.png
│           histogram.png
│           overview.png
│
├───results
│       eda_banco_central.html
│       eda_precipitaciones.html
│
└───src
    │   __init__.py
    │
    ├───eda
    │       fast_eda.py
    │       __init__.py
    │
    ├───preprocessing
    │       cleaner.py
    │       feature_engineering.py
    │       stationarity.py
    │
    └───vizualizations
            correlation.py
            historical_series.py
```
