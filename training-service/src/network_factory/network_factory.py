import tensorflow.keras as keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D



""" Generates neural networks """


class NetworkFactory:
    def __init__(self, network_parameters, n_classes, input_shape):
        self.input_shape = input_shape
        self.network_parameters = network_parameters
        self.n_classes = n_classes

    def build_cnn(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',input_shape=self.input_shape))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.n_classes, activation=self.network_parameters.get('activation')))
        return model



