import os
from PIL import Image
from sklearn.model_selection import train_test_split


class ImageProcessing:

    def __init__(self, directory, accepted_files=['jpg', 'jpeg', 'png'], test_size=0.20):
        self.directory = directory
        self.accepted_files = accepted_files
        self.test_size = test_size
        self.X_train, self.X_test, self.y_train, self.y_test = self.pre_process_data()

    def pre_process_data(self):
        data_refs = []
        data_labels = []
        classes = os.listdir(self.directory)
        current_label_idx = 0
        for class_ in classes:
            images = os.listdir(os.path.join(self.directory, class_))
            for image in images:
                # create list of 0s representing classes
                encoded_label = [0 for i in range(len(classes))]
                # if image is not in the accepted extensions, delete it.
                if image.split('.')[1] not in self.accepted_files:
                    os.remove(os.path.join(self.directory, class_, image))
                    continue
                try:
                    # try to open image as PIL image if it fails delete it
                    im = Image.open(os.path.join(self.directory, class_, image))
                except OSError as e:
                    print("failed opening image", e)
                    os.remove(os.path.join(self.directory, class_, image))
                    continue
                # indicate class by setting index to 1 (1 hot encoded labels)
                encoded_label[current_label_idx] = 1

                data_refs.append(os.path.join(self.directory, class_, image))
                data_labels.append(encoded_label)

            current_label_idx += 1

        X_train, X_test, y_train, y_test = train_test_split(data_refs, data_labels, test_size=self.test_size)

        setattr(self, 'n_classes', current_label_idx)

        return X_train, X_test, y_train, y_test














