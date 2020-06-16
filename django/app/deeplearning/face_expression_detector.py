import numpy as np
from PIL import Image
import cv2
from tensorflow import keras

IMAGE_SIZE = 224

FACE_CASCADE_MODEL_PATH = 'deeplearning/output_models/haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(FACE_CASCADE_MODEL_PATH)

TENSORFLOW_MODEL_PATH = 'deeplearning/output_models/face-expression-model.h5'
MODEL = keras.models.load_model(TENSORFLOW_MODEL_PATH)


class FaceExpressionDetector():
    "Given an image with human face, tell me its face expression"

    def __init__(self, img_path):
        self.img_path = img_path

    def isImageValid(self, filename):
        try:
            im = Image.open(filename)
            return True
        except IOError:
            return False

    def getFaceBoundary(self, img_path):
        img = cv2.imread(img_path)
        faces = FACE_CASCADE.detectMultiScale(img, 1.3, 5)

        if len(faces) == 0:
            return None
        faces = list(faces[0])
        return faces

    def cropImage(self, boundaries, img_path):
        im = Image.open(img_path)
        im_width = im.size[0]
        im_height = im.size[1]
        left = boundaries[0]
        top = boundaries[1]
        right = left + boundaries[2]
        bottom = top + boundaries[3]

        diff_width = right - left
        diff_height = bottom - top
        diff = abs(diff_width - diff_height)
        if diff_width > diff_height:
            bottom += diff
            bottom = min(bottom, im_height)
        else:
            right += diff
            right = min(right, im_width)

        if max(diff_width, diff_height) < 200:
            return None

        im1 = im.crop((left, top, right, bottom))

        newsize = (224, 224)
        im2 = im1.resize(newsize)
        return im2

    def getExtractedFace(self, img_path):
        if not self.isImageValid(img_path):
            return

        boundaries = self.getFaceBoundary(img_path)
        if boundaries is None:
            return

        im = self.cropImage(boundaries, img_path)
        if im is None:
            return
        return im

    def predictFaceExpression(self, extracted_face_im):
        im = extracted_face_im.resize((IMAGE_SIZE, IMAGE_SIZE))

        arr = np.array(im)
        # convert it to JPG if it is PNG
        if arr.shape[2] == 4:
            arr = arr[:, :, :3]

        arr = np.expand_dims(arr, axis=0)
        arr = np.array(arr).astype(np.float32)
        return MODEL.predict(arr)

    def run(self):
        img_path = self.img_path
        if not self.isImageValid(img_path):
            return None

        boundaries = self.getFaceBoundary(img_path)
        if boundaries is None:
            return None

        im = self.cropImage(boundaries, img_path)
        if im is None:
            return None

        # example:
        # label = [1, 0], classes = [1, 2]
        # dot<label, classes> = 1 (the class of the label)
        label = self.predictFaceExpression(im)[0]
        classes = np.array([1, 2])
        label = np.dot(label, classes)
        return int(label)
