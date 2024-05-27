import operator

from classes.obstacle import Obstacle
from classes.alert import Alert

def sort_and_trim_objects(obstacles: list[Obstacle], updates_per_message : int, min_obj_size : float) -> list[Obstacle]:

  obstacles.sort(key=operator.attrgetter('hazard_order', 'is_not_in_ROI'))

  temp = None
  vehicle_count = 0
  person_count = 0
  for obstacle in obstacles:
    if obstacle.hazard_order == 0:
      vehicle_count += 1
    if obstacle.hazard_order == 1:
      person_count += 1
    if obstacle.size >= min_obj_size:
      temp = obstacle

  if vehicle_count > 1:
    obstacles[0].name = "vehicles"
    obstacles[0].hazard_order = -1
    obstacles = [obstacle for obstacle in obstacles if obstacle.hazard_order != 0]

  if person_count > 1:
    if vehicle_count == 0:
      obstacles[0].name = "crowd"
      obstacles[0].hazard_order = -1
    else:
      obstacles[1].name = "crowd"
      obstacles[1].hazard_order = -1
    obstacles = [obstacle for obstacle in obstacles if obstacle.hazard_order != 1]
    
  if temp is not None:
    if vehicle_count > 0:
      obstacles.insert(1, temp)
    else:
      obstacles.insert(0, temp)

  if len(obstacles) > updates_per_message:
    return obstacles[:updates_per_message]
  
  return obstacles