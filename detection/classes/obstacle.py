URGENT_OBSTACLE_SET = {"car", "bicycle", "bus", "train", "truck", "cellphone"}

class Obstacle:

  #is_not_in_ROI for sorting cuz false comes before true
  def __init__(self, name, confidence, xyxy, zone_polygon):
    self.name = name
    self.confidence = confidence
    self.xyxy = xyxy
    self.size = 0

    self.set_position_and_size()
    self.set_ROI(zone_polygon)

    if name in URGENT_OBSTACLE_SET:
      self.hazard_order = 0
    elif name == 'person':
      self.hazard_order = 1
    elif name == 'bottle':
      self.hazard_order = 2
    else:
      self.hazard_order = 2

  def set_position_and_size(self):
    self.position = [(self.xyxy[0] + self.xyxy[2]) / 2, (self.xyxy[1] + self.xyxy[3]) / 2]

    temp = [self.xyxy[2] - self.xyxy[0], self.xyxy[3] - self.xyxy[1]]

    self.size = ((temp[0] / 1280) + temp[1] / 720) / 2

  def set_ROI(self, zone_polygon):
    if self.position[0] > zone_polygon[0, 0] and self.position[0] < zone_polygon[2, 0] and self.position[1] > zone_polygon[0, 1] and self.position[1] < zone_polygon[2, 1]:
      self.is_not_in_ROI = False
    else:
      self.is_not_in_ROI = True


  def __str__(self):
    return self.name + (" detected" if self.is_not_in_ROI else " in ROI")#+", size: " + str(self.size) + " pos: " + str(self.position) + " in ROI: " + str(not self.is_not_in_ROI)
  
  def __repr__(self):
    return self.__str__()