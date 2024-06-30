import cv2
import mediapipe.python.solutions.face_mesh as face_mesh

def calc_movement(landmark, prev_coords):
    # lets do blink detection - great ressource: https://peerj.com/articles/cs-943/
    pass

def draw(landmark_ids, coords, frame, cap):

    coords_dict = {}
    frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # goind from normalised coords to frame coords
    for i in landmark_ids:
        x_coord = int(coords[i].x * frame_w)
        y_coord = int(coords[i].y * frame_h)
        coords_dict[i] = (x_coord, y_coord)

    for _, coord in coords_dict.items():
        cv2.circle(frame, coord, radius=1, color=(0, 0, 255), thickness=4)

def getUniqueLandmark(landmarks):
    landmark_set = set()

    for l in landmarks:
        landmark_set.add(l[0])

    return list(landmark_set)

mp_face_mesh = face_mesh
cap = cv2.VideoCapture(0)

leye_indeces = mp_face_mesh.FACEMESH_LEFT_EYE
reye_indeces = mp_face_mesh.FACEMESH_RIGHT_EYE
face = mp_face_mesh.FACEMESH_FACE_OVAL

leye_indeces = getUniqueLandmark(leye_indeces)
reye_indeces = getUniqueLandmark(reye_indeces)
face = getUniqueLandmark(face)

with mp_face_mesh.FaceMesh(
        max_num_faces=1, 
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:

    if not cap.isOpened():
        print("Error: Could not open video device")
    else:

        has_verified = False

        while True:
            succ, frame = cap.read()

            if not succ:
                break

            results = face_mesh.process(frame)
            frame.flags.writeable = True

            if results.multi_face_landmarks:    
                
                for face_landmarks in results.multi_face_landmarks:
                    lms = face_landmarks.landmark
                    draw(leye_indeces, lms, frame, cap)
                    draw(reye_indeces, lms, frame, cap)
                    draw(face, lms, frame, cap)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
