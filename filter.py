from classes.obstacle import Obstacle

#cell phone is here just for testing purposes
OBSTACLES = {"person", "car", "bicycle", "bus", "train", "truck", "bench", "chair", "cell phone"}

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

  print(obstacles)

  return obstacles