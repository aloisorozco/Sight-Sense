import cv2
import mediapipe as mp

import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.drawing_utils as drawing_utils
import mediapipe.python.solutions.face_mesh as face_mesh

mp_drawing = drawing_utils
mp_drawing_styles = drawing_styles
mp_face_mesh = face_mesh

cap = cv2.VideoCapture(0)
draw_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

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

            frmae = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame)
            frame.flags.writeable = True

            print(results.multi_face_landmarks)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
