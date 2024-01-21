from classes.obstacle import Obstacle

def filter_objects(obstacles : list[Obstacle], filtering_obstacles_set : set) -> list[Obstacle]:
  
  obstacles = [obstacle for obstacle in obstacles if obstacle.name in filtering_obstacles_set and obstacle.confidence >= 0.6]

  return obstacles