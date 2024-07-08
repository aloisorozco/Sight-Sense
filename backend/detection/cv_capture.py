from ultralytics import YOLO
from detection.annotators import Annotators
from detection.mesh import FaceMesh

from detection.classes.obstacle import Obstacle
import detection.audio.tts as tts
import threading
import concurrent.futures
import cv2
import supervision as sv
import time
import base64


class Capture():

    _CONFIDENCE_THRESHOLD = 0.5
    _TIME_OUT = 2
    _speech_thread = None

    def __init__(self, args) -> None:

        frame_width, frame_height = args.webcam_resolution

        # change to 1 for webcam - if you have another device connected, otherwise leave at 0 for your default webcam
        # Capture vide + load model
        self.cap = cv2.VideoCapture(0)
        self.model = YOLO("yolov8n.pt")
        self.model.fuse()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        self.annotators = Annotators(args.webcam_resolution)

        self.end_stream = False
        
        # Load TTS and FaceMesh models
        # self.speech = tts.TTS()
        self.face_mesh = FaceMesh(self.cap)

    def _speak_messages(self, obstacles):
        for obstacle in obstacles:
            self.speech.generate_and_play(obstacle.__str__())


    def encode_image(self, image):
        _, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        return jpg_as_text
    

    def set_end_stream(self, val):
        self.end_stream = val


    def start_capture(self):
        thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        face_mesh_futrure = None

        while not self.end_stream:

            succ, frame = self.cap.read()
            if not succ:
                print("frame not returned - exiting")
                break  # Break the loop if no frame is returned

            result = self.model(frame, agnostic_nms=True, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(result)
            labels = []

            hasPerson = False

            for _, _, _, class_id, _, _ in detections:
                entity_type = self.model.names[class_id]
                labels.append(f"{entity_type}")

                if entity_type == "person" and not hasPerson:
                    hasPerson  =True
                    face_mesh_futrure = thread_pool.submit(self.face_mesh.process_frame_face_mesh, frame)
                

            # time_red = time.time()

            # obstacles = [
            #     Obstacle(self.model.names[class_id],
            #              confidence, xyxy, self.annotators.zone_polygon, time_red)
            #     for xyxy, _, confidence, class_id, _, _ in detections
            # ]

            # render only objects that are still on screen
            # time_now = time.time()
            # obstacles_to_speak = [
            #     obstacle for obstacle in obstacles if obstacle is not None and time_now - obstacle.time_registered < TIME_OUT]
            # # submit task to thread pool
            # self.executor.submit(self._speak_messages, obstacles_to_speak)

            # if (Capture._speech_thread == None or not Capture._speech_thread.is_alive()):
            #     obstacles_to_speak = [obstacle for obstacle in obstacles if obstacle != None and time.time(
            #     ) - obstacle.time_registered < Capture._TIME_OUT]
            #     Capture._speech_thread = threading.Thread(
            #         target=self._speak_messages, args=(obstacles_to_speak,))
            #     Capture._speech_thread.start()

            frame = self.annotators.bb_annotator.annotate(
                scene=frame,
                detections=detections
            )

            frame = self.annotators.label_annotator.annotate(
                scene=frame,
                detections=detections,
                labels=labels
            )

            self.annotators.zone.trigger(detections=detections)
            frame = self.annotators.zone_annotator.annotate(scene=frame)

            if(face_mesh_futrure):
                result = face_mesh_futrure.result()
                self.face_mesh.draw(frame, result)

            yield self.encode_image(frame)

            # cv2.imshow("Sight Sence - Frame", frame)

            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        # Release the capture object and close all windows
        self.cap.release()
        cv2.destroyAllWindows()
        thread_pool.shutdown()
        self.face_mesh.ptp()
