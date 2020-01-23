import os
import json
import traceback
import numpy as np
from src.network_factory import NetworkFactory
from tensorflow.keras.callbacks import EarlyStopping
from src.data_generator import DataGenerator
from src.image_processing import ImageProcessing

import tensorflow.keras.backend as K


class Trainer:
    def __init__(self, data_path, model_path, log_path, run_number, run_parameters):
        self.data_path = data_path
        self.model_path = model_path
        self.log_path = log_path
        self.run_number = run_number
        self.run_parameters = run_parameters

    def train(self):
        ip = ImageProcessing(self.data_path, test_size=self.run_parameters.get('test_size'))
        network_factory = NetworkFactory(network_parameters=self.run_parameters.get('network'), n_classes=ip.n_classes)

        model = network_factory.build()

        train_generator = DataGenerator(ip.X_train, ip.y_train, batch_size=self.run_parameters.get('batch_size'),
                                        run_parameters=self.run_parameters)

        valid_generator = DataGenerator(ip.X_test, ip.y_test, batch_size=self.run_parameters.get('batch_size'),
                                        run_parameters=self.run_parameters, validation=True)

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, restore_best_weights=True)



        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        K.clear_session()
        history = model.fit_generator(generator=train_generator, validation_data=valid_generator,
                                              epochs=self.run_parameters.get('epochs'),  callbacks=[es])

        if not os.path.exists(self.model_path):
            os.makedirs(os.path.join(self.model_path))

        model.save(os.path.join(self.model_path, f"model-{self.run_number}.h5"))

        data = {'history': history.history, 'epochs': len(history.history.get('loss'))}

        return data


