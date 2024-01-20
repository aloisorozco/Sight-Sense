URGENT_OBSTACLE_SET = {"car", "bicycle", "bus", "train", "truck", "cell phone"}

class Obstacle:

  #is_not_in_ROI for sorting cuz false comes before true
  def __init__(self, name, confidence, xyxy, is_not_in_ROI=True):
    self.name = name
    self.confidence = confidence
    self.xyxy = xyxy
    self.is_not_in_ROI = is_not_in_ROI
    self.size = 0

    if name in URGENT_OBSTACLE_SET:
      self.hazard_order = 0
    elif name == 'person':
      self.hazard_order = 1
    #bottle is here for testing purposes
    elif name == 'bottle':
      self.size = 0.9
      self.hazard_order = 2
    else:
      self.hazard_order = 2

  def __str__(self):
    return self.name + " detected"
  
  def __repr__(self):
    return self.__str__()