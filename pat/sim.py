import simpy

class Car:
  def __init__ (self, env):
    self.env = env
    self.action=env.process(self.run())

  def run():
    yield env.timeout(trip_duration) 
    print("%s attempting park at %d" % (name, env.now))
    print("%s parking at %d" % (name, env.now))
    yield env.timeout(parking_duration)
    print("%s leaving at %d" % (name, env.now))

class Spot:
  def __init__ (self, coord, available):
    self.x = coord.x
    self.y = coord.y
    self.available = available

  def isAvailable():
    print("Spot at %s is %r" % (coord, available,))
    return self.available

  def take():
    self.available = False
    print("Spot at %s taken" % (coord,))

  def free():
    self.available = True 
    print("Spot at %s freed" % (coord,))

  def location():
    return (self.x, self.y)

class Coord:
  def __init__ (self, x, y):
    self.x = x
    self.y = y

if __name__ == "__main__":
  env = simpy.Environment()
  env.run()

  coord.x = 1
  spot = Spot(coord, True)
  print spot
  spot.take()
  spot.free()
