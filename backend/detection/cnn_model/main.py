# from siamese_cnn import Siamese_CNN
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras.metrics import BinaryAccuracy
import pandas as pd

CSV_PATH = "backend/detection/cnn_model/dataset.csv"

dataset_df = pd.read_csv(CSV_PATH)

# TODO: figure out a way to vecotrize all the immages in the CSV - maybe look into how it is done with custom dataset of words or somehthing like that
# print(dataset_df)

# scnn = Siamese_CNN(105, 3)
# opt = adam_v2.Adam()
# scnn.compile(loss='binary_crossentropy', optimizer=opt, metrics=[BinaryAccuracy()])
