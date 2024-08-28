import tensorflow as tf
from keras.models import Model
import cv2 as cv

MODEL_REPO = "backend/detection/cnn_model/scnn_custom"
ANCHOR_IMG_PATH = "backend/detection/cnn_model/authed_people/92b9f61c-5eab-11ef-bbcf-e63bca865d36.png"

anchor_img = tf.io.decode_jpeg(tf.io.read_file(ANCHOR_IMG_PATH), channels=1)

scnn: Model = tf.keras.models.load_model(MODEL_REPO)

camera = cv.VideoCapture(0)
roi_x, roi_y, roi_w, roi_h = 480,900,400,425

while True:
    ret, frame = camera.read()

    if not ret:
        break

    frame = frame[roi_x:roi_x + roi_w, roi_y:roi_y+roi_h]
    cv.imshow('frame', frame)

    frame = cv.resize(frame, (105,105), interpolation=cv.INTER_AREA)

    if cv.waitKey(1) == ord('q'):
        print("snapshot")
        frame = cv.resize(frame, (105,105), interpolation=cv.INTER_AREA)

        # TODO - convert both frame and anchor tuple into a tensor, the model needs to have a tensor fed to it at inference, not a tuple
        print(scnn.predict((frame, anchor_img)))
        

camera.release()
cv.destroyAllWindows()