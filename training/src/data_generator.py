import numpy as np
import PIL
import tensorflow.keras as keras
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input


class DataGenerator(keras.utils.Sequence):
    def __init__(self, image_refs, labels, batch_size, run_parameters, dim=(1,2048), shuffle=True, validation=False):
        self.dim = dim
        self.labels = labels
        self.run_parameters = run_parameters
        self.validation = validation
        # calculate how many images to get per batch based on augmentation
        self.grab_images_per_batch, self.batch_size = self._calc_batch_size(image_refs, batch_size)
        self.image_refs = image_refs
        self.shuffle = shuffle



        if self.run_parameters.get('pre-trained'):
            self.pre_trained_model = self._build_pre_trained_model()
        self.on_epoch_end()

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
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def _calc_batch_size(self, image_refs, batch_size):
        extra_images = 0
        if not self.validation:
            if self.run_parameters.get('flip_left_right'):
                extra_images +=1
            if self.run_parameters.get('flip_up_down'):
                extra_images +=1
            if self.run_parameters.get('rotate_90'):
                extra_images +=1
            if self.run_parameters.get('rotate_180'):
                extra_images += 1
            if self.run_parameters.get('rotate_270'):
                extra_images += 1

        if len(image_refs) < batch_size:
            batch_size = 1

        grab_images_per_batch = round(batch_size / (extra_images + 1))
        if grab_images_per_batch < extra_images + 1:
            batch_size = extra_images + 1
            grab_images_per_batch = 1

        return grab_images_per_batch, batch_size



    def _pre_process_image(self, img: PIL):
        img = img.resize((224,224), Image.ANTIALIAS)
        if self.run_parameters.get('greyscale'):
            img = img.convert('L')
            img = np.array(img)
            img = np.repeat(img[..., np.newaxis], 3, -1)
        else:
            img = img.convert('RGB')
            img = np.array(img)
        img = img / 255
        img = img.reshape((1, 224, 224, 3))
        img = preprocess_input(img) # resnet preprocess
        img = self.pre_trained_model.predict(img)
        return img

    def _build_pre_trained_model(self):
        base_model = ResNet50(weights="imagenet")
        second_2_last_layer = base_model.get_layer("avg_pool")
        model = keras.Model(inputs=base_model.inputs, outputs=second_2_last_layer.output)
        return model

    def _augment_pipeline(self, img: PIL):
        augmented_images = []
        augmented_images.append(img) # append original image by default

        if not self.validation:
            if self.run_parameters.get('flip_left_right'):
                left_right = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                augmented_images.append(left_right)

            if self.run_parameters.get('flip_up_down'):
                up_down = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
                augmented_images.append(up_down)

            if self.run_parameters.get('rotate_90'):
                rotate_90 = img.transpose(PIL.Image.ROTATE_90)
                augmented_images.append(rotate_90)
                rotate_90.save('rotate_90.png')

            if self.run_parameters.get('rotate_180'):
                rotate_180 = img.transpose(PIL.Image.ROTATE_180)
                augmented_images.append(rotate_180)

            if self.run_parameters.get('rotate_270'):
                rotate_270 = img.transpose(PIL.Image.ROTATE_270)
                augmented_images.append(rotate_270)

            if self.run_parameters.get('greyscale'):
                greyscale = img.transpose(PIL.Image.ROTATE_270)
                augmented_images.append(greyscale)


        return augmented_images


    def _data_generation(self, image_refs, image_labels):
        X = []
        y = []
        # Generate data
        for i, img in enumerate(image_refs):
            pil_img = Image.open(img)
            augmented_images = self._augment_pipeline(pil_img) # augments images (flips, zooms ect...)
            for image in augmented_images:
                X.append(self._pre_process_image(image)) # processes the image for the NN
                y.append(image_labels[i])

        X = np.array(X)
        X = X.reshape((self.batch_size, 2048)) # shape is res net output

        print(X.shape)

        return X, np.array(y)