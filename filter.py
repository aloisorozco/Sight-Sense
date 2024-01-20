from classes.obstacle import Obstacle

def parse_label(label : str) -> Obstacle:
  name, confidence = label.rsplit(" ", 1)
  return Obstacle(name, float(confidence))

def filter_objects(obstacles : list[Obstacle], filtering_obstacles_set : set) -> list[Obstacle]:
  
  obstacles = [obstacle for obstacle in obstacles if obstacle.name in filtering_obstacles_set and obstacle.confidence >= 0.6]

  print(obstacles)

  return obstacles