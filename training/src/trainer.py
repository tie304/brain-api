import os
import json
from tensorflow.keras.callbacks import EarlyStopping
from src.data_generator import DataGenerator
from src.image_processing import ImageProcessing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow.keras.backend as K


class Trainer:
    def __init__(self, data_path, model_path, log_path, batch_size, epochs, test_size, run_number, run_parameters):
        self.data_path = data_path
        self.model_path = model_path
        self.log_path = log_path
        self.epochs = epochs
        self.batch_size = batch_size
        self.test_size = test_size
        self.run_number = run_number
        self.run_parameters = run_parameters

    def train(self):
        ip = ImageProcessing(self.data_path, test_size=self.test_size)
        train_generator = DataGenerator(ip.X_train, ip.y_train, batch_size=self.batch_size, run_parameters=self.run_parameters)
        valid_generator = DataGenerator(ip.X_test, ip.y_test, batch_size=self.batch_size, run_parameters=self.run_parameters, validation=True)

        es = EarlyStopping(monitor='val_loss', mode='min', verbose=1)

        feature_model = Sequential()
        feature_model.add(Dense(ip.n_classes, activation="softmax"))
        feature_model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        K.clear_session()
        history = feature_model.fit_generator(generator=train_generator, validation_data=valid_generator,
                                              epochs=self.epochs,  callbacks=[es])

        self.save_logs(history)

        if not os.path.exists(self.model_path):
            os.makedirs(os.path.join(self.model_path))

        feature_model.save(os.path.join(self.model_path, f"model-{self.run_number}.h5"))


    def save_logs(self, history):
        if not os.path.exists(self.data_path):
            os.makedirs(os.path.join(self.data_path))
            with open(os.path.join(self.log_path, "logs.json"), 'w') as f:
                json.dump(history.history, f)