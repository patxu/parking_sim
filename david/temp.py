
import xml.etree.ElementTree as ET

def enum(**enums):
	return type('Enum',(),enums)
Direction = enum(North=1,East=2,South=3,West=4)

class ParkingSpot(object):
	def __init__(self,env,coord,available):
		self.env = env
		self.coord = coord
		self.available = available
	
	def request(self):
		self.available = True

	def release(self):
		self.available = False

	def available(self):
		return self.available

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



tree = ET.parse('city1.xml')
root = tree.getroot()
for road in root:
	for x in range(0,3)