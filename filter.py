from classes.obstacle import Obstacle

def parse_label(label : str) -> Obstacle:
  name, confidence = label.rsplit(" ", 1)
  return Obstacle(name, float(confidence))

def filter_objects(obstacles : list[Obstacle], obstacles_set : str) -> list[Obstacle]:
  temp_obstacles = []
  for obstacle in obstacles:
    if obstacle.name in obstacles_set and obstacle.confidence >= 0.6:
      temp_obstacles.append(obstacle)
  
  obstacles = temp_obstacles

  print(obstacles)

  return obstacles