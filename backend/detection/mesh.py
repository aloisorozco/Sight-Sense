import cv2
import random
import time
import mediapipe.python.solutions.face_mesh as face_mesh
import threading
from detection.cv_capture import Capture
class FaceMesh():

    # These are the IDs of the landmark coords that we need to compute the EAR - its an associative array so DO NOT CHANGE THE ORDER
    _R_EIDS = [33, 160, 158, 155, 153, 144]
    _L_EIDS = [382, 384, 387, 263, 373, 380]
    EAR_THRESHOLD = 0.2
    MAX_BLINKS = 7
    MIN_BLINKS = 3
    TEMPORAL_WINDOW_MIN = 1
    TEMPORAL_WINDOW_MAX = 3

    def __init__(self, capture_referance, cap):
        
        self._timeout = None

        self.capture_referance : Capture = capture_referance

        self.total_blinks = 0
        self.temporal_window  = 3
        self.blink_goal = 3

        self.lEAR = None
        self.rEAR = None

        self.mp_face_mesh = face_mesh
        self.cap = cap

        leye_indeces = self.mp_face_mesh.FACEMESH_LEFT_EYE
        reye_indeces = self.mp_face_mesh.FACEMESH_RIGHT_EYE
        face = self.mp_face_mesh.FACEMESH_FACE_OVAL

        self.leye_indeces = self._get_unique_landmark(leye_indeces)
        self.reye_indeces = self._get_unique_landmark(reye_indeces)
        self.face = self._get_unique_landmark(face)

        self.face_mesh_model = self.mp_face_mesh.FaceMesh(max_num_faces=1,
                                                refine_landmarks=True,
                                                min_detection_confidence=0.7,
                                                min_tracking_confidence=0.5)
        
        self.last_blink_time = None
    
    def _get_unique_landmark(self, landmarks):
        landmark_set = set()

        for l in landmarks:
            landmark_set.add(l[0])

        return list(landmark_set)

    def get_timeout(self):
        return self._timeout

    def start_timeout(self):
        print("Start Blinking!")
        self._timeout = int(time.time()) + 60

    def reset_auth(self):
        self.total_blinks = 0
        self.last_blink_time = None
        self._timeout = None

    # blink detection - source: https://peerj.com/articles/cs-943/
    def _calc_blink(self, coords_dict, ids_to_get):

        filtered_coords = {}
        for index, i in enumerate(ids_to_get):
            filtered_coords[index + 1] = coords_dict[i]

        ear = (abs(filtered_coords[2][1] - filtered_coords[6][1]) + abs(filtered_coords[3][1] -
               filtered_coords[5][1])) / (2 * abs(filtered_coords[1][0] - filtered_coords[4][0]))
        return ear


    def _process_coords(self, landmark_ids, coords, frame, bbox_bottom_left_coord, coords_to_annotate, coords_dict = {}):
        
        img_h, img_w = frame.shape[:2]
        corner_x = int(bbox_bottom_left_coord[0])
        corner_y = int(bbox_bottom_left_coord[1])

        # going from normalised coords to frame coords
        for i in landmark_ids:
            x_coord = int(coords[i].x * img_w)
            y_coord = int(coords[i].y * img_h)
            coord_tuple = (x_coord + corner_x, y_coord + corner_y)

            coords_dict[i] = coord_tuple
            coords_to_annotate.append(coord_tuple)

        return coords_dict
    

    def draw(self, frame, coords):
        if(coords):
            for coord in coords:
                cv2.circle(frame, coord, radius=1, color=(0, 0, 255), thickness=4)

    
    def gen_blink_sequence(self):
        self.blink_goal = random.randint(FaceMesh.MIN_BLINKS, FaceMesh.MAX_BLINKS)
        self.temporal_window = random.randint(FaceMesh.TEMPORAL_WINDOW_MIN, FaceMesh.TEMPORAL_WINDOW_MAX)
        print(f"~~~~~~~~ After coundown, perform {self.blink_goal} blinks, each blink lasting {self.temporal_window} seconds")


    def ptp(self):
        if(self.face_mesh_model):
            self.face_mesh_model.close()
        else:
            print("Model does not exist in memory or has already been closed")


    def process_frame_face_mesh(self, frame, bbox_bottom_corner):

            results = self.face_mesh_model.process(frame)
            frame.flags.writeable = True

            coords_to_annotate = []
            auth_finished = False

            if results.multi_face_landmarks:
                lms = results.multi_face_landmarks[0].landmark #we ever only face-mesh one person at a time for authentication, so can just get first elem in arr

                raw_coords_dict = self._process_coords(self.leye_indeces, lms, frame, bbox_bottom_corner, coords_to_annotate)
                lEAR = self._calc_blink(raw_coords_dict, FaceMesh._L_EIDS) if self._timeout else 0

                raw_coords_dict = self._process_coords(self.reye_indeces, lms, frame, bbox_bottom_corner, coords_to_annotate)
                rEAR = self._calc_blink(raw_coords_dict, FaceMesh._R_EIDS) if self._timeout else 0

                raw_coords_dict = self._process_coords(self.face, lms, frame, bbox_bottom_corner, coords_to_annotate)

                avg_EAR = (rEAR + lEAR) / 2

                if self._timeout:

                    if(int(time.time()) <= self._timeout):
                        if avg_EAR <= FaceMesh.EAR_THRESHOLD:
                            if not self.last_blink_time:
                                self.last_blink_time = int(time.time())

                        else:
                            if self.last_blink_time and int(time.time()) - self.last_blink_time >= self.temporal_window:
                                self.total_blinks += 1

                                if self.total_blinks == self.blink_goal:
                                    # Here we are returning a response indicating that the target is a human
                                    self.capture_referance.update_auth_res('auth_sucess', "Human Authentication Successfull")
                                    print('Yipiee you did it congrats - you are a human!!!')
                                    auth_finished = True
                                    self.capture_referance.auth_timeout_timer = None

                                else:
                                    print(f'---------------------------------- Blinks Remaining {self.blink_goal - self.total_blinks} ----------------------------------')

                            self.last_blink_time = None
                            
                    else:
                        self.capture_referance.update_auth_res('auth_failed', "Nuh uh, not a human")
                        print('~~~~~~~~ TIMEOUT - re-authenticate with admin')
                        auth_finished = True
                        self.capture_referance.auth_timeout_timer = None
            
            if auth_finished:
                self.reset_auth()

                
            return coords_to_annotate, auth_finished