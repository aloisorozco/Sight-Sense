import tensorflow as tf
from keras.models import Model
import cv2 as cv
import os

MODEL_REPO = "backend/detection/cnn_model/scnn_custom"
DANIEL_AUTHED_PATH = "backend/detection/cnn_model/daniel_auth"

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
        frame_tensor = tf.convert_to_tensor(frame, dtype=tf.uint8)

        avg_score = 0
        imgs_names = os.listdir(DANIEL_AUTHED_PATH)
        img_count = len(imgs_names)

        for img in imgs_names:
            img = tf.io.decode_jpeg(tf.io.read_file(f'{DANIEL_AUTHED_PATH}/{img}'), channels=3)
        
            input_tensor = tf.concat([frame_tensor, img], axis=-1, name="inputs")
            input_tensor = tf.reshape(input_tensor, (-1, 2, 105, 105, 3))

            print(input_tensor.shape)

            # cv.imwrite("backend/detection/cnn_model/img_test1.png",input_tensor[:,:, :1].numpy())
            # cv.imwrite("backend/detection/cnn_model/img_test2.png",input_tensor[:,:, 1:].numpy())
            avg_score += scnn.predict(input_tensor)[0][0]


        print(avg_score / img_count)
        

camera.release()
cv.destroyAllWindows()