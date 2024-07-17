import cv2
import random
import mediapipe.python.solutions.face_mesh as face_mesh

class FaceMesh():

    # These are the IDs of the landmark coords that we need to compute the EAR - its an associative array so DO NOT CHANGE THE ORDER
    _R_EIDS = [33, 160, 158, 155, 153, 144]
    _L_EIDS = [382, 384, 387, 263, 373, 380]
    EAR_THRESHOLD = 0.2
    MAX_BLINKS = 10
    MIN_BLINKS = 3
    TEMPORAL_WINDOW_MIN = 3
    TEMPORAL_WINDOW_MAX = 5

    temporal_window  = 3
    blink_goal = 3

    def __init__(self, cap):

        self.blink_counter = 0
        self.total_blinks = 0

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
    
    def gen_blink_sequence(self):
        self.blink_goal = random.randint(FaceMesh.MIN_BLINKS, FaceMesh.MAX_BLINKS)
        self.temporal_window = random.randint(FaceMesh.TEMPORAL_WINDOW_MIN, FaceMesh.TEMPORAL_WINDOW_MAX)


    def ptp(self):
        if(self.face_mesh_model):
            self.face_mesh_model.close()
        else:
            print("Model does not exist in memory or has already been closed")


    # blink detection - source: https://peerj.com/articles/cs-943/
    def _calc_blink(self, coords_dict, ids_to_get):

        filtered_coords = {}
        for index, i in enumerate(ids_to_get):
            filtered_coords[index + 1] = coords_dict[i]

        ear = (abs(filtered_coords[2][1] - filtered_coords[6][1]) + abs(filtered_coords[3][1] -
               filtered_coords[5][1])) / (2 * abs(filtered_coords[1][0] - filtered_coords[4][0]))
        return ear

    def _process_coords(self, landmark_ids, coords, frame, cap, coords_to_annotate, coords_dict = {}):

        frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # going from normalised coords to frame coords
        for i in landmark_ids:
            x_coord = int(coords[i].x * frame_w)
            y_coord = int(coords[i].y * frame_h)
            coord_tuple = (x_coord, y_coord)

            coords_dict[i] = coord_tuple
            coords_to_annotate.append(coord_tuple)

        return coords_dict
    
    def draw(self, frame, coords):
        if(coords):
            for coord in coords:
                cv2.circle(frame, coord, radius=1, color=(0, 0, 255), thickness=4)

    def _get_unique_landmark(self, landmarks):
        landmark_set = set()

        for l in landmarks:
            landmark_set.add(l[0])

        return list(landmark_set)

    def process_frame_face_mesh(self, frame):

            results = self.face_mesh_model.process(frame)
            frame.flags.writeable = True

            coords_to_annotate = []

            if results.multi_face_landmarks:

                for face_landmarks in results.multi_face_landmarks:
                    lms = face_landmarks.landmark

                    raw_coords_dict = self._process_coords(self.leye_indeces, lms, frame, self.cap, coords_to_annotate)
                    rEAR = self._calc_blink(raw_coords_dict, FaceMesh._L_EIDS)

                    raw_coords_dict = self._process_coords(self.reye_indeces, lms, frame, self.cap, coords_to_annotate)
                    lEAR = self._calc_blink(raw_coords_dict, FaceMesh._R_EIDS)

                    raw_coords_dict = self._process_coords(self.face, lms, frame, self.cap, coords_to_annotate)

                    avg_EAR = (rEAR + lEAR) / 2

                    if avg_EAR < FaceMesh.EAR_THRESHOLD:
                        self.blink_counter += 1

                    else:
                        if self.blink_counter >= FaceMesh.temporal_window:
                            self.total_blinks += 1

                        self.blink_counter = 0
                        # print(f'---------------------------------- Total Blinks {self.total_blinks} ----------------------------------')
                
                return coords_to_annotate