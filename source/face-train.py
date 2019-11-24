import cv2
import os
import numpy as np
from PIL import Image
import pickle
import os.path as path

BASE_DIR = os.path.dirname(os.path.abspath(path.join(__file__, "..")))
image_dir = os.path.join(BASE_DIR, "ima_user")
face_cascade = cv2.CascadeClassifier('lib/haarcascade_frontalface_alt.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            label,current_id = label.rsplit('_',1)
            label_ids[label] = int(current_id)
            id_ = label_ids[label]
            # y_labels.append(label) # some number
            # x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
            pil_image = Image.open(path) # grayscale
            #size = (550, 550)
            #final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(pil_image, "uint8")
            # print(image_array)
            faces = face_cascade.detectMultiScale(image_array,1.1,4)
            #print(faces)
            for (x, y, w, h) in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
with open("face-labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.write("face-trainner.yml")
