import os

import pandas as pd
from keras.layers import Dense, LSTM
from keras.models import Sequential


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


window = 4
var = ["open", "close", "high", "low"]
future = 1


def get_X_y(data):
    raw = series_to_supervised(data[var], window, future)
    X = raw[raw.columns[:len(var) * window]]
    y = raw[raw.columns[len(var) * window:]]
    # reshape input to be 3D [samples, timesteps, features]
    return X.values.reshape((X.shape[0], 1, X.shape[1])), y.values.reshape((y.shape[0], 1, y.shape[1]))


def predict(uploaded_file_url):
    print(uploaded_file_url)
    print(os.listdir("."))
    data = pd.read_csv("C:/Users/SomaC/PycharmProjects/Stock-prediction/django_server/tempcsv/AAPL.csv")
    # os.remove(uploaded_file_url)
    X_train, y_train = get_X_y(data)

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(4))
    model.compile(loss='mae', optimizer='adam')
    # fit network
    model.summary()

    # print("start train")
    # history = model.fit(X_train, y_train, epochs=50, batch_size=72, verbose=2, shuffle=False)
    # print("finish train")

    # res = pd.DataFrame(model.predict(X_train).reshape(y_train.shape[0], y_train.shape[2]))
    # res.columns = var
    res = data
    return res
