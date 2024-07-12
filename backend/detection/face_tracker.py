from detection.face import Face

class FaceTracker():

    def __init__(self):
        self.face_list = []
        self.last_uuid = 0 #change this to use a uuid library or make some hash later so we dont just increment a counter

    def add_face(self, face):
        self.face_list.append(face)

    def re_index_faces(new_bbox):
        # check all new bbox, and compare them agaisnt each other o find the ones that match best using Kalamn filter
        # compare IoU of bbox to the kalman filter estimate of each existing face
        # any face that does not have a copunterpart "new bbox" should be removed
        pass

    def _IoU_comparison(self, bbox_old, bbox_new):
        pass
