import numpy as np
from filterpy.kalman import KalmanFilter

class Face:

    def __init__(self, bbox, id):
        self.bbox = bbox
        self.face_id = id
        self.kelman_filter = self._init_kelman_filter()

    def _init_kelman_filter(self):

        # 8 states (x, y, w, h, dx, dy, dw, dh), 4 measurements (x, y, w, h)
        kf = KalmanFilter(dim_x=8, dim_z=4)
                
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
        kf.R[2:, 2:] *= 10.  # Higher noise for size measurements
        
        # Initial error covariance
        kf.P[4:, 4:] *= 1000.  # High initial uncertainty for velocities
        kf.P *= 10.  # General uncertainty
        
        # Process noise covariance
        kf.Q[-2, -2] *= 0.01  # Lower process noise for dw
        kf.Q[4:, 4:] *= 0.01  # Lower process noise for velocities
        
        # Initial state
        x, y, w, h = self.bbox
        kf.x[:4] = np.array([x, y, w, h]).reshape((4, 1))
        
        return kf