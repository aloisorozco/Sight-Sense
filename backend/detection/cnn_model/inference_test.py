import tensorflow as tf
from keras.models import Model
import cv2 as cv

MODEL_REPO = "backend/detection/cnn_model/scnn_custom"
ANCHOR_IMG_PATH = "backend/detection/cnn_model/authed_people/92b9f61c-5eab-11ef-bbcf-e63bca865d36.png"

anchor_img = tf.io.decode_jpeg(tf.io.read_file(ANCHOR_IMG_PATH), channels=3)

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
        
        input_tensor = tf.concat([frame_tensor, anchor_img], axis=-1, name="inputs")
        input_tensor = tf.reshape(input_tensor, (-1, 2, 105, 105, 3))

        print(input_tensor.shape)

        # cv.imwrite("backend/detection/cnn_model/img_test1.png",input_tensor[:,:, :1].numpy())
        # cv.imwrite("backend/detection/cnn_model/img_test2.png",input_tensor[:,:, 1:].numpy())
        
        print(scnn.predict(input_tensor))
        

camera.release()
cv.destroyAllWindows()