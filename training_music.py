from keras.models import Sequential
from keras.layers import Activation,Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import os

start = 0
maximum_length = 25
part_of_the_song = []
next_part_of_the_song = []
step = 1

learning_rate = 0.01
batch_size_predicting = 128
epochs = 25



file = open("song.txt", "r")
midisong_in_chunks = []

for i in file:
	midisong_in_chunks.append(i.rstrip("\n"))
file.close()

#print midisong_in_chunks

unique_chunks = sorted(list(set(midisong_in_chunks)))

chunk_indices = dict((c, i) for i, c in enumerate(unique_chunks))


for i in range(start, len(midisong_in_chunks) - maximum_length, step):
	part_of_the_song.append(midisong_in_chunks[i: i + maximum_length])
	next_part_of_the_song.append(midisong_in_chunks[i + maximum_length])


training_X = np.zeros((len(part_of_the_song), maximum_length, len(unique_chunks)), dtype = np.bool)
training_Y = np.zeros((len(part_of_the_song), len(unique_chunks)), dtype = np.bool)

for i, part in enumerate(part_of_the_song):
	for j, chunk in enumerate(part):
		training_X[i, j, chunk_indices[chunk]] = 1
		training_Y[i, chunk_indices[next_part_of_the_song[i]]] = 1



# Sequential model is a linear stack of layers
# LSTM Dense and Activation are the layer instances
# The model needs to know what input shape it should expect. For this reason, the first layer in a Sequential model 
#(and only the first, because following layers can do automatic shape inference) needs to receive information about its input shape.
model = Sequential()

# 256 is the batch size
model.add(LSTM(256, input_shape=(maximum_length, len(unique_chunks))))
model.add(Dense(len(unique_chunks)))
# softmax is the activation function used in recurrent neural networks
model.add(Activation('softmax'))

# RMSprop is an optimizer used for recurrent neural networks
# rmsprop: Divide the gradient by a running average of its recent magnitude
optimizer = RMSprop(learning_rate)

# A loss function. This is the objective that the model will try to minimize
# categorical_crossentropy: 
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.fit(training_X, training_Y, batch_size_predicting, epochs)

if not os.path.exists("./model/"):
	os.mkdir("./model/")

model.save('./model/model.h5');
model.save_weights("./model/final_weights.h5")


