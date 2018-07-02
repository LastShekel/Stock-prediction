import os

import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    #     print(data,n_in,n_out)
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


window = 5
var = ["open", "close", "high", "low"]
future = 3
server_root = "C:/Users/SomaC/PycharmProjects/Stock-prediction/"


def get_X_y(data, window, future):
    raw = series_to_supervised(data[var], window, future)

    scaler = MinMaxScaler(feature_range=(0, 1))
    X = scaler.fit_transform(raw[raw.columns[:len(var) * window]].values)
    y = scaler.fit_transform(raw[raw.columns[len(var) * window:]].values)

    return X.reshape((X.shape[0], 1, X.shape[1])), y.reshape((y.shape[0], 1, y.shape[1]))


def predict(uploaded_file_url):
    print(uploaded_file_url)
    print(os.listdir("."))
    data = pd.read_csv(server_root + "django_server" + uploaded_file_url)
    os.remove(server_root + "django_server" + uploaded_file_url)
    test = data[var][(window + future):]
    train = data[var][:(window + future)]
    model = load_model(server_root + "model.h5")
    res=model.predict(test)
    res.reshape(future,len(var))
    return res
