import random
import numpy as np
from PIL import Image, ImageFilter
import PIL


class DataAugmentationPipeline:
    SINGLE_IMAGE_ADD = ['flip_left_right', 'flip_up_down']
    N_IMAGES_ADD = ['rotate_random_25', 'blur']

    def __init__(self, augmentation_params: dict):
        self.augmentation_params = augmentation_params

    """ Calculates total amount of additional images created for each image"""
    @property
    def total_augmented_images(self):
        total_images = 0
        for key in self.augmentation_params:
            if key in DataAugmentationPipeline.SINGLE_IMAGE_ADD:
                total_images += 1
            elif key in DataAugmentationPipeline.N_IMAGES_ADD:
                total_images += self.augmentation_params.get(key)
        return total_images

    def augment(self, img: PIL):
        augmented_images = []
        img = img.convert('RGB')
        augmented_images.append(img)

        if self.augmentation_params.get('flip_left_right'):
            augmented_images.append(self.flip_left_right(img))

        if self.augmentation_params.get('flip_up_down'):
            augmented_images.append(self.flip_up_down(img))

        if self.augmentation_params.get('rotate_random_25'):
            augmented_images = augmented_images + self.rotate_random_25(img)

        if self.augmentation_params.get('blur'):
            augmented_images = augmented_images + self.blur(img)

        assert len(augmented_images) == self.total_augmented_images + 1, "Augment error returning wrong values"
        return augmented_images


    @staticmethod
    def flip_left_right(img):
        return img.transpose(PIL.Image.FLIP_LEFT_RIGHT)

    @staticmethod
    def flip_up_down(img):
        return img.transpose(PIL.Image.FLIP_TOP_BOTTOM)

    def rotate_random_25(self, img):
        rotated = []
        for i in range(self.augmentation_params.get('rotate_random_25')):
            random_degree = random.uniform(-25, 25)
            random_rotate_img = img.rotate(random_degree)
            rotated.append(random_rotate_img)
        return rotated

    def blur(self, img):
        blur_images = []
        blur_start = 3
        for i in range(self.augmentation_params.get('blur')):
            try:
                blur_img = img.filter(ImageFilter.GaussianBlur(blur_start))
                blur_images.append(blur_img)
                blur_start += 1
            except Exception as e:
                print('Failed to blur image:', e)
                print(img.mode)

        return blur_images

