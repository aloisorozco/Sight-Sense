import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers import Input, Flatten, Dense, Conv2D, MaxPooling2D
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras.models import Model

#this is the paper by which I will make the siamese model - popular paper = very documented so I use this one: https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf

input_layer = Input(shape=(105,105,3))

conv_1 = Conv2D(filters=64,kernel_size=10, activation='relu', padding='same') (input_layer)
max_pool_1 = MaxPooling2D()(conv_1)

conv_2 = Conv2D(filters=128, kernel_size=7, activation='relu', padding='same') (max_pool_1)
max_pool_2 = MaxPooling2D()(conv_2)

conv_3 = Conv2D(filters=128, kernel_size=4, activation='relu', padding='same') (max_pool_2)
max_pool_3 = MaxPooling2D()(conv_3)

conv_4 = Conv2D(filters=256, kernel_size=4, activation='relu', padding='same') (max_pool_3)

flatten_layer = Flatten()(conv_4)
output = Dense(4096, activation='sigmoid')(flatten_layer)

opt = adam_v2(lr=0.0005)
model = Model(input_layer, output)
model.compile(optimizer=opt, loss="categorical_crossentropy", metrics=['accuracy, precision'])


