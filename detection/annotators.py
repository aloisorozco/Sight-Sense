import supervision as sv
import numpy as np

class Annotators:

    MIN_X_BOUND = 0.3
    MAX_X_BOUND = 0.7

    MIN_Y_BOUND = 0
    MAX_Y_BOUND = 1

    ZONE_POLYGON = np.array([
    [MIN_X_BOUND, MIN_Y_BOUND],
    [MAX_X_BOUND, MIN_Y_BOUND],
    [MAX_X_BOUND, MAX_Y_BOUND],
    [MIN_X_BOUND, MAX_Y_BOUND]
    ])

    def __init__(self, webcam_resolution) -> None:
    
        self.bb_annotator = sv.BoundingBoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

        self.zone_polygon = (Annotators.ZONE_POLYGON * np.array(webcam_resolution)).astype(int)
        self.zone = sv.PolygonZone(polygon=self.zone_polygon, frame_resolution_wh=tuple(webcam_resolution))
        self.zone_annotator = sv.PolygonZoneAnnotator(
            zone=self.zone, 
            color=sv.Color.RED,
            thickness=2,
            text_thickness=4,
            text_scale=2
        )