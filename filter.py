from classes.obstacle import Obstacle

def parse_label(label : str) -> Obstacle:
  name, confidence = label.rsplit(" ", 1)
  return Obstacle(name, float(confidence))

def filter_objects(labels : list[str], obstacles_set : str) -> list[Obstacle]:
  temp_objects = []
  for label in labels:
    temp_objects.append(parse_label(label))

  obstacles = []
  for object_ in temp_objects:
    if object_.name in obstacles_set and object_.confidence >= 0.6:
      obstacles.append(object_)

  print(obstacles)

  return obstacles