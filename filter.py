
#cell phone is here just for testing purposes
OBSTACLES = {"person", "car", "bicycle", "bus", "train", "truck", "bench", "chair", "cell phone"}

class Obstacle:
  def __init__(self, name, confidence):
    self.name = name
    self.confidence = confidence

  def __str__(self):
    return "Detected " + self.name + " with " + str(self.confidence) + " confidence"
  
  def __repr__(self):
    return self.__str__()


def parse_label(label : str) -> Obstacle:
  name, confidence = label.rsplit(" ", 1)
  return Obstacle(name, float(confidence))


def filter_objects(labels : list[str]) -> list[Obstacle]:
  temp_objects = []
  for label in labels:
    temp_objects.append(parse_label(label))

  obstacles = []
  for object_ in temp_objects:
    if object_.name in OBSTACLES and object_.confidence >= 0.6:
      obstacles.append(object_)

  return obstacles