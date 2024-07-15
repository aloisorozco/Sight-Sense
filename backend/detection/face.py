import numpy as np
from filterpy.kalman import KalmanFilter

# TODO: spend some time understadning the math behind Kalman filter - Udemy is a great place to start
class Face:

    _last_uuid = 0 #change this to use a uuid library or make some hash later so we dont just increment a counter

    def __init__(self, bbox):
        self.bbox = bbox
        self.face_center_params = Face._calc_params_from_bbox(bbox)
        self.face_id = Face._last_uuid
        self.kalman_filter = self._init_kelman_filter()

        Face._last_uuid += 1

    def _calc_params_from_bbox(bbox):
        x1, y1, x2, y2 = bbox

        width = abs(x2 - x1 + 1)
        height = abs(y2 - y1 + 1)

        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        return center_x, center_y, width, height

    def _init_kelman_filter(self):

        # 8 states (x, y, w, h, dx, dy, dw, dh), 4 measurements (x, y, w, h)
        kf = KalmanFilter(dim_x=8, dim_z=4)

        # Initial state
        x, y, w, h = self.face_center_params
        kf.x = np.array([x, y, w, h, 0, 0, 0, 0])

        # State transition matrix
        kf.F = np.array([
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1]
        ])
        
        # Measurement matrix
        kf.H = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]
        ])
        
        # Measurement noise covariance
        kf.R[2:4, 2:4] *= 10.
        
        # Initial error covariance
        kf.P[4:, 4:] *= 1000.
        kf.P *= 10.
        
        # Process noise covariance
        kf.Q[-2, -2] *= 0.01
        kf.Q[4:, 4:] *= 0.01

        return kf

    # calculate the bbox from the kalman estimate of x,y,w,h
    def get_kalman_bbox(self):
        x,y,w,h = self.kalman_filter.x[:4]

        x1 = abs(x - float(w / 2))
        x2 = abs(x + float(w / 2))
        y1 = abs(y - float(h / 2))
        y2 = abs(y + float(h / 2))
        
        return x1, y1, x2, y2
    
    def update(self, new_bbox):
        new_center_params = Face._calc_params_from_bbox(new_bbox)
        self.bbox = new_bbox
        self.face_center_params = new_center_params

        self.kalman_filter.update(new_center_params)

    def predict(self):
        self.kalman_filter.predict()
        return self.kalman_filter.x[:4]
         

# Easy way to test out the Kalman filter - if we fine tune the code to be more inclusive of velocity, this is a good way to test it before deployment
# face_test = Face([1,1,1,1], 1)
# print(face_test.predict())

# face_test.update([2,2,2,2])
# print(face_test.predict())

# face_test.update([3,3,3,3])
# print(face_test.predict())

# face_test.update([4,4,4,4])
# print(face_test.predict())

# face_test.update([5,5,5,5])
# print(face_test.predict())

# face_test.update([6,6,6,6])
# print(face_test.predict())

# face_test.update([7,7,7,7])
# print(face_test.predict())