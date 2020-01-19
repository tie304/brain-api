import random
import numpy as np
import PIL
import tensorflow.keras as keras
from PIL import Image, ImageFilter
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from src.data_augmentation_pipeline import DataAugmentationPipeline



class DataGenerator(keras.utils.Sequence):
    def __init__(self, image_refs, labels, batch_size, run_parameters, validation=False):
        print("Initializing data generator...")
        self.labels = labels
        self.run_parameters = run_parameters
        self.validation = validation
        if self.run_parameters.get("augmentation", False):
            self.augment_pipeline = DataAugmentationPipeline(run_parameters.get('augmentation'))
        # calculate how many images to get per batch based on augmentation
        self.grab_images_per_batch, self.batch_size = self._calc_batch_size(image_refs, batch_size)
        self.image_refs = image_refs
        if self.run_parameters.get('model'):
            self.pre_trained_model = self._build_pre_trained_model(run_parameters.get('model'))
        self.on_epoch_end()


        print(f"Processing: {self.grab_images_per_batch} images per batch and feeding {self.batch_size}  images per batch")
        print(f"Training with {self.run_parameters.get('model')} ")

    def __len__(self):
        return int(np.floor(len(self.image_refs) / self.grab_images_per_batch))

    def __getitem__(self, index):
        indexes = self.indexes[index*self.grab_images_per_batch:(index+1)*self.grab_images_per_batch]
        # Find list of IDs
        image_refs = [self.image_refs[k] for k in indexes]
        image_labels = [self.labels[k] for k in indexes]
        # Generate data
        X, y = self._data_generation(image_refs, image_labels)
        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.image_refs))
        if self.run_parameters.get('shuffle', False):
            np.random.shuffle(self.indexes)

    def _calc_batch_size(self, image_refs, batch_size):
        """Calculate the batch size with consideration to the amount of images your augmenting

            we need to calculate the number of images being augmented to add to the batch size. This function keeps the
            amount of data retrieved from the fs consistent with the batch output to NN.
            If amount of images to grab from fs is less than 1: increment the batch size until images_to_grab >=1


            EX:
            batch_size = 32
            extra_images = 6

            amount of images to grab from data = 32 // 6 = 5
            batch size = 5 * 6 = 30


            :param image_refs: list of strings containing url refs to images
            :param batch_size user defined batch size
            :return: number of images to grab, batch size
            """

        extra_images = 0
        if not self.validation and self.run_parameters.get("augmentation", False):
            extra_images = self.augment_pipeline.total_augmented_images

            if len(image_refs) < batch_size:
                batch_size = 1

            grab_images_per_batch = batch_size // (extra_images + 1)

            if grab_images_per_batch < 1:
                # increase batch size because we cant grab less than 1 image at a time EX: 64 // 65 = 0
                # recalculate by doubling batch size #EX: 64 + 64 = 128
                # 128 // 64 = 1
                #  batch_size:1 * 65 = 65
                # grab one image and it will generate a batch of 65

                self._calc_batch_size(image_refs, batch_size=batch_size + 1)

            batch_size = (grab_images_per_batch * (extra_images + 1))
        else:
            grab_images_per_batch = batch_size
            if len(image_refs) < batch_size:
                batch_size = 1
                grab_images_per_batch = 1

        return grab_images_per_batch, batch_size


    def _pre_process_image(self, img: PIL):
        img = img.resize((224,224), Image.ANTIALIAS)
        img = img.convert('RGB')
        img = np.array(img)
        img = img / 255
        img = img.reshape((1, 224, 224, 3))
        img = preprocess_input(img) # resnet preprocess
        img = self.pre_trained_model.predict(img)
        return img

    @staticmethod
    def _build_pre_trained_model(model):
        if model == "resnet50":
            base_model = ResNet50(weights="imagenet")
            second_2_last_layer = base_model.get_layer("avg_pool")
            model = keras.Model(inputs=base_model.inputs, outputs=second_2_last_layer.output)
        else:
            raise NotImplementedError('only resnet 50 supported at this time')
        return model



    def _data_generation(self, image_refs, image_labels):
        X = []
        y = []
        # Generate data
        for i, img in enumerate(image_refs):
            pil_img = Image.open(img)
            if not self.validation and self.run_parameters.get("augmentation", False):
                augmented_images = self.augment_pipeline.augment(pil_img) # augments images (flips, zooms ect...)
                for image in augmented_images:
                    X.append(self._pre_process_image(image)) # processes the image for the NN
                    y.append(image_labels[i])
            else: # not validation do no form of augmentation
                X.append(self._pre_process_image(pil_img))
                y.append(image_labels[i])

        X = np.array(X)
        X = X.reshape((self.batch_size, 2048)) # shape is res net output

        return X, np.array(y)