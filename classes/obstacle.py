class Obstacle:

  def __init__(self, name, confidence, xyxy):
    self.name = name
    self.confidence = confidence
    self.xyxy = xyxy

  def __str__(self):
    return "Detected " + self.name + " with " + str(self.confidence) + " confidence"
  
  def __repr__(self):
    return self.__str__()