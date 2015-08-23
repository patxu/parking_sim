import xml.etree.ElementTree as ET

#-----------------Direction Enum-------------------#

def enum(**enums):
  return type('Enum',(),enums)

Direction = enum(North=1,East=2,South=3,West=4)

#-----------------Coordinate Class-------------------#

class Coord:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def equal(self,other):
    if(self.x == other.x and self.y == other.y):
      return True
    else:
      return False
  def increaseX(self,value):
    self.x += value
  def increaseY(self,value):
    self.y += value
  def __str__(self):
    return str(self.x)+','+str(self.y)

#-----------------Parking Spot Class-------------------#

class ParkingSpot(object):
  def __init__(self,available):
    self.available = available
  
  def request(self):
    self.available = True

  def release(self):
    self.available = False

  def available(self):
    return self.available
  def __str__(self):
    return "available: " + str(self.available)

#-----------------Road Section Class-------------------#

class RoadSection(object):
  def __init__(self,coordinates,parkingSpotRight,parkingSpotLeft,crossable,interstection,direction):
    self.coordinates = coordinates
    self.parkingSpotRight = parkingSpotRight
    self.parkingSpotLeft = parkingSpotLeft
    self.crossable = crossable
    self.interstection = interstection
    self.direction = direction

  #This assumes south->north or east->west
  def parkingAvailable(carDirection):
    if (self.interstection == True):
      return false
    if(self.crossable == True):
      return parkingSpotRight.available or parkingSpotLeft.available
    else:
      if(carDirection == Direction.North):
        return parkingSpotRight.available()
      elif(carDirection == Direction.South):
        return parkingSpotLeft.available()
      elif(carDirection == West):
        return parkingSpotRight.available()
      else:
        return parkingSpotLeft.available()
  def isIntersection():
    return self.interstection

  def __str__(self):
    return "Coordinates: " +str(self.coordinates)+", Parking spot right " + str(self.parkingSpotRight)+", Parking spot left " + str(self.parkingSpotLeft)

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
    self.roadSections.append(roadSection)


#-----------------Road Map Class-------------------#

class RoadMap():
  def __init__(self):
    self.graph = {} #graph of streets and intersections
    self.roads = [] #set of streets


  def calculateIntersections(self,road):
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

  def addStreet(self,road):
    #keep track of streets
    self.roads.append(road)

    intersectingRoads = self.calculateIntersections(road)

    #street name should be unique
    self.graph[road.id] = intersectingRoads


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
    for roadSection in root.findall('./road/roadSection'):
      coordX = roadSection.find('coordX').text
      coordY = roadSection.find('coordY').text
      parkingSpotLeft = ParkingSpot(xmlToBool(roadSection.find('parkingLeft').text))
      parkingSpotRight = ParkingSpot(xmlToBool(roadSection.find('parkingRight').text))
      crossable = xmlToBool(roadSection.find('crossable')) 
      intersection = xmlToBool(roadSection.find('intersection').text) 
      direction = xmlToDirection(roadSection.find('direction').text)   
      #create new road section
      newRoadSection = RoadSection(Coord(coordX,coordY),parkingSpotRight,parkingSpotLeft,crossable,intersection,direction)
      #add it to road
      road.addRoadSection(newRoadSection)
    roadMap.addStreet(road)

def xmlToDirection(value):
  if (value == 1):
    return Direction.North
  elif(value == 2):
    return Direction.East
  elif(value == 3):
    return Direction.South
  else:
    return Direction.West

def xmlToBool(value):
  if (value == 'Y'):
    return True
  else:
    return False

if __name__ == '__main__':
  loadCity("cities/city3.xml")


