from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.layers import LSTM, SimpleRNN
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file

import os


output_size = 256
batch_size = 128
epochs = 25
optimizer = RMSprop(lr=0.01)

def train_simple(x_train, y_train, input_shape):
    # Build the simple RNN model
    model = Sequential([
        SimpleRNN(output_size, input_shape=input_shape),
        Dense(input_shape[1]),
        Activation('softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    # Run the model
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)

    # Save the RNN model
    if not os.path.exists("./model/"):
        os.mkdir("./model/")
    model.save('./model/rnn_model.h5')
    model.save_weights("./model/rnn_weights.h5")


def train_lstm(x_train, y_train, input_shape):
    # Build the LSTM model
    model = Sequential([
        LSTM(output_size, input_shape=input_shape),
        Dense(input_shape[1]),
        Activation('softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    # Run the model
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)

    # Save the LSTM model
    if not os.path.exists("./model/"):
        os.mkdir("./model/")
    model.save('./model/lstm_model.h5')
    model.save_weights("./model/lstm_weights.h5")