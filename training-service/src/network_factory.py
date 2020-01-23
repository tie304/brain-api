import tensorflow.keras as keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D



""" Generates neural networks """


class NetworkFactory:

    def __init__(self, network_parameters, n_classes):
        self.network_parameters = network_parameters
        self.n_classes = n_classes

    def build(self):
        if self.network_parameters.get('model') == "perceptron":
            return self._build_perceptron()
        elif self.network_parameters.get('model') == "resnet50":
            return self._build_resnet()
        elif self.network_parameters.get('model') == "base_cnn":
            return self._build_baseline_cnn()
        else:
            raise NotImplementedError('Sorry that network is not supported')

    def _build_perceptron(self):
        model = Sequential()
        model.add(Dense(self.n_classes, activation=self.network_parameters.get('activation')))
        return model

    def _build_resnet(self):
        base_model = ResNet50(weights=self.network_parameters.get('pretrained', None))
        second_2_last_layer = base_model.get_layer("avg_pool")
        resnet_layers = keras.Model(inputs=base_model.inputs, outputs=second_2_last_layer.output)

        model = Sequential()
        model.add(resnet_layers)
        model.add(Dense(self.n_classes, activation=self.network_parameters.get('activation')))

        if self.network_parameters.get('fine_tune', False):
            model.layers[0].trainable = True
            # We let the last 3 blocks train
            for layer in model.layers[0].layers[:-11]:
                layer.trainable = False
            for layer in model.layers[0].layers[-11:]:
                layer.trainable = True
        return model

    def _build_baseline_cnn(self):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu',input_shape=(224,224,3)))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.n_classes, activation=self.network_parameters.get('activation')))
        return model
