from keras.models import Sequential
from keras.layers import Activation,Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from rnn_model import train_simple, train_lstm

import numpy as np
import os

max_len = 25
start = 0
part_of_song = []
next_part = []
step = 1


midisong_in_chunks = []
f = open("./midi/txt/song.txt", "r")
for i in f:
	midisong_in_chunks.append(i.rstrip("\n"))
f.close()

midisong_in_chunks = midisong_in_chunks[1:]

unique_chunks = sorted(list(set(midisong_in_chunks)))
chunk_indices = dict((c, i) for i, c in enumerate(unique_chunks))

for i in range(start, len(midisong_in_chunks) - max_len, step):
	part_of_song.append(midisong_in_chunks[i: i + max_len])
	next_part.append(midisong_in_chunks[i + max_len])

num_chunks = len(unique_chunks)
x_train = np.zeros((len(part_of_song), max_len, num_chunks), dtype=np.bool)
y_train = np.zeros((len(part_of_song), num_chunks), dtype=np.bool)

for i, part in enumerate(part_of_song):
	for j, chunk in enumerate(part):
		x_train[i, j, chunk_indices[chunk]] = 1
	y_train[i, chunk_indices[next_part[i]]] = 1


input_shape = (max_len, num_chunks)
train_lstm(x_train, y_train, input_shape)
train_simple(x_train, y_train, input_shape)
