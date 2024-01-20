from classes.obstacle import Obstacle
from classes.alert import Alert

#pass the obstacles that are already filtered out whether in the region of interest or not
def process_objects_to_alerts(obstacles : list[Obstacle], filtering_obstacles_set : set, filtering_obstacles_category : str) -> Alert:
  
  alerts = [Alert.map_obstacle_to_alert(obstacle) for obstacle in obstacles if obstacle.name in filtering_obstacles_set]

  if len(alerts) > 1:
    return Alert("Multiple " + filtering_obstacles_category + " detected")
  
  elif len(alerts) == 1:
    return alerts[0]
  
  else:
    return None
