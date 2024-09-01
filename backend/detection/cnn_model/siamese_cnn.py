#well merge the CNN with the rest of the layers here
from keras.models import Model
from keras.layers import Dense, Conv2D, Input, MaxPool2D, Flatten

class Siamese_CNN(Model):
    
    def __init__(self, shape, chanels) -> None:
        super().__init__()
        self._cnn = self._make_cnn(shape, chanels)
        self.dense_sigmoid = Dense(1, activation='sigmoid')

    
    def _make_cnn(self, shape, chanels):
        input = Input(shape=(shape, shape, chanels))

        c1 = Conv2D(kernel_size=10, filters=64, activation='relu')(input)
        m1 = MaxPool2D()(c1)

        c2 = Conv2D(kernel_size=7, filters=128, activation='relu')(m1)
        m2 = MaxPool2D()(c2)

        c3 = Conv2D(kernel_size=4, filters=128, activation='relu')(m2)
        m3 = MaxPool2D()(c3)

        c4 = Conv2D(kernel_size=4, filters=256, activation='relu')(m3)
        flat1 = Flatten()(c4)
        embedings = Dense(units=4096)(flat1)

        return Model(inputs=input, outputs=embedings)


    def _vector_diff(self, embedings_im1, embedings_im2):
        return embedings_im1 - embedings_im2
    

    def call(self, inputs, **kwargs):
        print(inputs)
        img1 = inputs[:, 0, :, :, :]
        img2 = inputs[:, 1, :, :, :]

        embedings_im1 = self._cnn(img1)
        embedings_im2 = self._cnn(img2)
        
        embedings_diff = self._vector_diff(embedings_im1, embedings_im2)
        return self.dense_sigmoid(embedings_diff)