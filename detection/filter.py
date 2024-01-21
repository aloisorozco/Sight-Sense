from classes.obstacle import Obstacle

def filter_objects(obstacles : list[Obstacle], filtering_obstacles_set : set, min_confidence : float) -> list[Obstacle]:

  obstacles = [obstacle for obstacle in obstacles if obstacle.name in filtering_obstacles_set and obstacle.confidence >= min_confidence]

  return obstacles