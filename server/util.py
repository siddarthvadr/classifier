import joblib
import json
import numpy as np
import base64
import cv2
from embedding import get_embedding
from PIL import Image
from numpy import asarray
from keras.models import load_model

__class_name_to_number = {}
__class_number_to_name = {}

__model = None


def classify_image(image_base64_data, file_path=None):
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)

    result = []
    facenet_model = load_model('facenet_keras.h5', compile=False)
    for img in imgs:
        final = get_embedding(facenet_model, img)
        final = final.reshape(1, -1)
        result.append({
            'class': class_number_to_name(__model.predict(final)[0]),
            'class_probability': np.around(__model.predict_proba(final) * 100, 2).tolist()[0],
            'class_dictionary': __class_name_to_number
        })

    return result


def class_number_to_name(class_num):
    return __class_number_to_name[class_num]


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __class_name_to_number
    global __class_number_to_name

    with open("./artifacts/class_dictionary.json", "r") as f:
        __class_name_to_number = json.load(f)
        __class_number_to_name = {v: k for k, v in __class_name_to_number.items()}

    global __model
    if __model is None:
        with open('./artifacts/saved_model_knn.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")


def get_cv2_image_from_base64_string(b64str):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    :param uri:
    :return:
    '''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    roi_color = []  # * array for storing multiple faces
    for x, y, w, h in faces:
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) > 0:
            roi_color.append(img[y:y + h, x:x + w])
    roi_required_size = []
    for face in roi_color:
        img = Image.fromarray(face)
        img = img.resize((160, 160))
        face_array = asarray(img)
        roi_required_size.append(face_array)
    return roi_required_size

def get_b64_test_image_for_sid():
    with open("b64.txt") as f:
        return f.read()


if __name__ == '__main__':
    load_saved_artifacts()

    # print(classify_image(get_b64_test_image_for_sid, None))
    # print(classify_image(None, "./test_images/binod_sid.jpg"))
    #print(classify_image(None, "./test_images/sid.jpg"))
    #print(classify_image(None, "./test_images/spects.jpg"))
    #print(classify_image(None, "./test_images/front.jpg"))
    #print(classify_image(None, "./test_images/left.jpg"))
    #print(classify_image(None, "./test_images/right.jpg"))
    #print(classify_image(None, "./test_images/virat1.jpg"))
    #print(classify_image(None, "./test_images/virat2.jpg"))
