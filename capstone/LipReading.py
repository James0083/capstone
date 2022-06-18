import numpy as np
import cv2
import os
import glob
from keras.utils import load_img
from keras.preprocessing import image
from keras.models import load_model

label_list = ['바지',
              '뱀',
              '버스',
              '사과',
              '옷',
              '자동차',
              '호랑이',
              '귤',
              '모자',
              '포도']


index = []

# image size
img_size = 224

# Load Saved Model
model = load_model('my_model_final.h5')


# Loop Through image folder
file_path = os.path.abspath("../media/output/")
print("file_path : ", file_path)
for img in glob.glob('../media/output/*.jpg'):
    image = load_img(img, target_size=(img_size, img_size))
    print(img)
    img = np.array(image)
    img = img / 255.0
    img = img.reshape(1, img_size, img_size, 3)
    label = model.predict(img)
    classes_x = np.argmax(label, axis=1)[0]
    index.append(classes_x)


class_ = max(index)
print("The Phase is: ", label_list[class_], ' type:', type(label_list [class_]))