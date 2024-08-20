# from siamese_cnn import Siamese_CNN
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras.metrics import BinaryAccuracy
import tensorflow as tf
import pandas as pd

CSV_PATH = "backend/detection/cnn_model/dataset.csv"
CSV_SMOL_PATH = "backend/detection/cnn_model/smol.csv"

dataset_df = pd.read_csv(CSV_SMOL_PATH)
val_size = int(len(dataset_df) * 0.2)
train_size = len(dataset_df) - val_size

x_train = []
y_train = []

x_val = []
y_val = []

def decode_img(row):
    img1 = tf.io.read_file(row.iloc[0])
    img2 = tf.io.read_file(row.iloc[1])

    row.iloc[0] = tf.io.decode_jpeg(img1, channels=1)
    row.iloc[1] = tf.io.decode_jpeg(img2, channels=1)
    return row

dataset_df = dataset_df.apply(decode_img, axis=1)
print('done')
print(dataset_df)
# train_df = dataset_df.iloc[0: train_size]
# val_df = dataset_df.iloc[train_size:]

# print(train_df)

# TODO: figure out a way to vecotrize all the immages in the CSV - maybe look into how it is done with custom dataset of words or somehthing like that
# print(dataset_df)

# scnn = Siamese_CNN(105, 3)
# opt = adam_v2.Adam()
# scnn.compile(loss='binary_crossentropy', optimizer=opt, metrics=[BinaryAccuracy()])
