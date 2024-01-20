class Alert:
  def __init__(self, message):
    self.message = message

  def __str__(self):
    return self.message
  
  def __repr__(self):
    return self.__str__()
  
  @staticmethod
  def map_obstacle_to_alert(obstacle):
    return Alert(obstacle.name + " detected")