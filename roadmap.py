class RoadMap():
  def __init__(self):
    self.graph = {} #graph of streets and intersections
    self.roads = [] #set of streets

  def addStreet(road):
    #keep track of streets
    roads.add(road)

    intersectingRoads = calculateIntersections(road)

    #street name should be unique
    self.graph[road.name] = intersections

  def calculateIntersections(road):
    #roads are vertical or horizontal, i.e. have direction North/South or East/West
    direction = 0
    if road.direction == Direction.North:
      direction = Direction.North
    if road.direction == Direction.East:
      direction = Direction.East

    intersectingRoads = [road for road in self.roads if road.direction == direction]

    edges = []
        
    if road.direction == Direction.North:
      edges = [Coord(road.fixedCoord, intersectingRoad.fixedCoord) for intersectingRoad in intersectingRoads]
    if road.direction == Direction.East:
      edges = [Coord(intersectingRoad.fixedCoord, road.fixedCoord) for intersectingRoad in intersectingRoads]

    return edges 

if __name__  == "__main__"
  unitTests
