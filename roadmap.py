import xml.etree.ElementTree as ET

#DEBUGGING (must have ipdb and iPython set up)
# import ipdb; ipdb.set_trace()

#-----------------Direction Enum-------------------#

def enum(**enums):
  return type('Enum',(),enums)

Direction = enum(North=1,East=2,South=3,West=4)

#-----------------Coordinate Class-------------------#

class Coord:
  def __init__(self,x,y):
    self.x = x
    self.y = y

  def __eq__(self,other):
    if(self.x == other.x and self.y == other.y):
      return True
    else:
      return False

  def increaseX(self,value):
    self.x += value

  def decreaseX(self,value):
    self.x -= value

  def increaseY(self,value):
    self.y += value

  def decreaseY(self,value):
    self.y -= value

  def __str__(self):
    return "(" + str(self.x) + ',' + str(self.y) + ")"

#-----------------Parking Spot Class-------------------#

class ParkingSpot(object):
  def __init__(self,available):
    self.available = available
  
  def request(self):
    self.available = False

  def release(self):
    self.available = True

  def __str__(self):
    return "available: " + str(self.available)

#-----------------Road Section Class-------------------#

class RoadSection(object):
  def __init__(self,coordinates,parkingRight,parkingLeft,crossable,intersection,direction):
    self.coordinates = coordinates
    self.parkingRight = parkingRight
    self.parkingLeft = parkingLeft
    self.crossable = crossable
    self.intersection = intersection
    self.direction = direction

  #orientation of north and east as "postitive" - south->north and west->east
  def getParkingSpots(self, carDirection):
    availableSpots = []
    if (self.intersection == True): #cannot park at intersections
      pass
    elif(self.crossable == True): #can park on either side
      if (self.parkingRight.available()):
        availableSpots.extend([self.parkingRight])
      if (self.parkingLeft.available()):
        availableSpots.extend([self.parkingLeft])
    else:
      if(carDirection == Direction.North):
        if(self.parkingRight.available):
          availableSpots.extend([self.parkingRight])
      elif carDirection == Direction.South:
        if self.parkingLeft.available:
          availableSpots.extend([self.parkingLeft])
      elif carDirection == Direction.East:
        if self.parkingRight.available:
          availableSpots.extend([self.parkingRight])
      else:
        if self.parkingLeft.available:
          availableSpots.extend([self.parkingLeft])
    return availableSpots

  def isIntersection(self):
    return self.intersection

  def __str__(self):
    return "Road Section " +str(self.coordinates) + " (Parking right " + str(self.parkingRight)+", Parking left " + str(self.parkingLeft) + ")"

#-----------------Road Class-------------------#

class Road(object):
  def __init__(self,id,direction,min,max,fixedCoord):
    self.direction = direction
    self.min = min
    self.max = max
    self.fixedCoord = fixedCoord
    self.roadSections = []
    self.id = id

  def addRoadSection(self,roadSection):
    self.roadSections.extend([roadSection])

  #find the road section based on a coordinate
  def getRoadSectionFromCoord(self, coord):
    return [section for section in self.roadSections if section.coordinates == coord][0]

  def __str__(self):
    return "Road " + str(self.id) + " (Direction: " + str(directionToCardinalDirection(self.direction)) + ", FixedCoord: " + str(self.fixedCoord) + ")"


#-----------------Road Map Class-------------------#

class RoadMap():
  def __init__(self):
    self.graph = {} #graph where nodes are roads and edges are intersections; Road: (Road, Coord)
    self.roads = [] #list of roads

  def calculateIntersections(self,road):
    #roads are vertical or horizontal, i.e. have direction North/South or East/West- we want the perpendicular direction
    intersectingRoadDirection = 0
    if road.direction == Direction.North:
     intersectingRoadDirection  = Direction.East
    if road.direction == Direction.East:
      intersectingRoadDirection = Direction.North

    intersectingRoads = [road for road in self.roads if road.direction == intersectingRoadDirection]

    edges = []
        
    if road.direction == Direction.North:
      edges = [(intersectingRoad, Coord(road.fixedCoord, intersectingRoad.fixedCoord)) for intersectingRoad in intersectingRoads]
    if road.direction == Direction.East:
      edges = [(intersectingRoad, Coord(intersectingRoad.fixedCoord, road.fixedCoord)) for intersectingRoad in intersectingRoads]

    return edges 

  def addStreet(self,road):
    #keep track of street   s
    self.roads.append(road)

    edges = self.calculateIntersections(road)

    #street name should be unique
    self.graph[road.id] = edges 

    for edge in edges:
      ID = edge[0].id
      # if ID not in self.graph:
      #   self.graph[ID] = []
      self.graph[ID].append((road, edge[1]))

  def __str__(self):
    string = "Roads and Road Intersections:\n"
    for road, intersectingRoads in self.graph.iteritems():
      r = [x for x in self.roads if x.id == road]
      string += str(r[0]) + "\n"
      for edge in intersectingRoads:
        string += "\t" + str(edge[0]) + " intersects at " + str(edge[1]) + "\n"
    return string

  def getRoadFromCoord(self, coord):
    vertRoads = [road for road in self.roads if road.direction == Direction.North]
    r1 = [road for road in vertRoads if road.fixedCoord == coord.x]
    horRoads = [road for road in self.roads if road.direction == Direction.East]
    r2 = ([road for road in horRoads if road.fixedCoord == coord.y])
    roads = []
    if r1 != []:
      roads.extend(r1)
    if r2 != []:
      roads.extend(r2)
    if roads == []:
      return None
    else:
      return roads[0] #return first row (always vertical road if > 1 road?)

#-----------------Helper Classes-------------------#

def loadCity(file):
  roadMap = RoadMap()
  tree = ET.parse(file)
  root = tree.getroot()
  for road in root.findall('road'):
    min = int(road.find('min').text)
    max = int(road.find('max').text)
    fixedCoord = int(road.find('fixedCoord').text)
    direction = xmlToDirection(int(road.find('direction').text))
    roadID = int(road.attrib["name"])
    road = Road(roadID,direction,min,max,fixedCoord)

    
    #Get the road sections
    for roadSection in root.findall(".//*[@name='" + str(road.id) + "']/roadSection"):
      coordX = int(roadSection.find('coordX').text)
      coordY = int(roadSection.find('coordY').text)
      parkingSpotLeft = ParkingSpot(xmlToBool(roadSection.find('parkingLeft').text))
      parkingSpotRight = ParkingSpot(xmlToBool(roadSection.find('parkingRight').text))
      crossable = xmlToBool(roadSection.find('crossable')) 
      intersection = xmlToBool(roadSection.find('intersection').text) 
      direction = int(xmlToDirection(roadSection.find('direction').text))
      #create new road section
      newRoadSection = RoadSection(Coord(coordX,coordY),parkingSpotRight,parkingSpotLeft,crossable,intersection,direction)
      #add it to road
      road.addRoadSection(newRoadSection)
    roadMap.addStreet(road)

  return roadMap

def xmlToDirection(value):
  if (value == "1"):
    return Direction.North
  elif(value == "2"):
    return Direction.East
  elif(value == "3"):
    return Direction.South
  else:
    return Direction.West

def directionToCardinalDirection(value):
  if (value == 1):
    return "North"
  elif(value == 2):
    return "East"
  elif(value == 3):
    return "South"
  else:
    return "West"

def xmlToBool(value):
  if (value == 'Y'):
    return True
  else:
    return False

if __name__ == '__main__':
  loadCity("cities/test.xml")

