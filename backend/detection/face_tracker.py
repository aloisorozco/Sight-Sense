from detection.face import Face

class FaceTracker():

    IoU_THRESHOLD = 0.5

    def __init__(self):
        self.face_dict = {}
        self.new_faces = {}
        self.processed_list = {}

    def add_face(self, face):
        self.face_dict[face.face_id] = face

    def add_new_faces_to_dict(self):
        for face_id, instance in self.new_faces.items():
            self.face_dict[face_id] = instance
        
        self.new_faces.clear()

    # we are deleting all the faces that are no longer recognised - only call in thread pool for performance
    def swap_dict(self):

        if(len(self.face_dict) > 0):

            self.face_dict.clear()

            for face_id, instance in self.processed_list.items():
                self.face_dict[face_id] = instance
            
            self.processed_list.clear()
        
        else:
            self.face_dict = self.processed_list
            self.processed_list = {} # we DONT clear here - we want the refereance in face_dict to persist
        

    # compute IoU between face.kelman_filter + new_bbox (use _IoU_comparison)
    # if _IoU_comparison passes (match) - then assign face new bbox coords and end loop
    # set face.processed = True (set back to false when computing Kelam Prediction)
    def re_index_faces(self, new_bbox):

        best_match = (0,-1)
        for face_id, instance in self.face_dict.items():
            
            IoU_ratio = self._IoU_comparison(instance, new_bbox)

            if (IoU_ratio < self.IoU_THRESHOLD):
                continue
            
            if(best_match[0] < IoU_ratio):
                best_match = (IoU_ratio, face_id)
        
        if(best_match[1] == -1):
            return False, -1 # Cant re-index because new_bbox is a new face -> return false + id to display
          
        best_face_match = self.face_dict[best_match[1]]
        best_face_match.update(new_bbox)
        self.processed_list[best_face_match.face_id] = best_face_match
        del self.face_dict[best_face_match.face_id]

        return True, best_face_match.face_id

    # For IoU (intersection over union) we are comparing the new bbox to the Kalman filter prediction,
    # calculated during the previous frame, against the new found bbox
    def _IoU_comparison(self, face, bbox_new):

        x1_face, y1_face, x2_face, y2_face = face.get_kalman_bbox()

        x1 = max(x1_face, bbox_new[0])
        y1 = max(y1_face, bbox_new[1])
        x2 = min(x2_face, bbox_new[2])
        y2 = min(y2_face, bbox_new[3])

        kalman_area = (abs(x1_face - x2_face) + 1) * (abs(y1_face - y2_face) + 1)
        new_bbox_area = (abs(bbox_new[0] - bbox_new[2]) + 1) * (abs(bbox_new[1] - bbox_new[3]) + 1)

        intersect_area = max(0, (x2 - x1) + 1) * max(0, (y2 - y1) + 1)

        ratio = intersect_area / float(kalman_area + new_bbox_area - intersect_area)

        return ratio
        

