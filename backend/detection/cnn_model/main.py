# from siamese_cnn import Siamese_CNN
import tensorflow as tf
from keras.optimizers import Adam
from keras.metrics import BinaryAccuracy
from siamese_cnn import Siamese_CNN
import csv


CSV_PATH = "backend/detection/cnn_model/dataset.csv"
CSV_SMOL_PATH = "backend/detection/cnn_model/smol.csv"
MODEL_REPO = "backend/detection/cnn_model/scnn_custom"

dataset_pre_x = []
dataset_pre_y = []

def decode_img(row):
    img1 = tf.io.read_file(row[0])
    img2 = tf.io.read_file(row[1])

    decoded_img1 = tf.io.decode_jpeg(img1, channels=1)
    decoded_img2 = tf.io.decode_jpeg(img2, channels=1)
    return decoded_img1, decoded_img2

def configure_for_performance(dataset):
    dataset = dataset.cache()
    dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(32)
    return dataset

with open(CSV_SMOL_PATH, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0] == "img1":
            continue
        dataset_pre_x.append(decode_img(row))
        dataset_pre_y.append(int(row[2]))

dataset = tf.data.Dataset.from_tensor_slices((dataset_pre_x, dataset_pre_y))
split_index = int(len(dataset_pre_x) * 0.8)

train_dataset = dataset.take(split_index)
val_dataset = dataset.skip(split_index)

train_dataset = configure_for_performance(train_dataset)
val_dataset = configure_for_performance(val_dataset)

print("trining model")

scnn = Siamese_CNN(105, 1)
opt = Adam()
scnn.compile(loss='binary_crossentropy', optimizer=opt, metrics=[BinaryAccuracy()])
hist = scnn.fit(train_dataset, validation_data=val_dataset)
print(hist)
scnn.save(MODEL_REPO, save_format='tf')