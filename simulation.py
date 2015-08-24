import simpy
import random
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity
import roadmap

#DEBUGGING (must have ipdb and iPython set up)
# import ipdb; ipdb.set_trace()

class Car(object):
	def __init__(self,env,wantsToPark,carID,cityMap,coordinates = None,currentStreetId = None,direction = None):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.cityMap = cityMap
		self.coordinates = coordinates
		self.currentStreetId = currentStreetId
		self.direction = direction

	#execute a move
	def move(self,direction):
		validDirections = self.getValidDirections()
		if len(validDirections) > 1: #don't u-turn unless we have to
			oppositeDirection = (self.direction + 2) % 4
			if oppositeDirection == 0:
				oppositeDirection = 4
			try:
				validDirections.remove(oppositeDirection) #remove backwards direction
			except ValueError:
				pass #this is okay
		self.direction = random.choice(validDirections)

		if(self.direction == Direction.North):
			self.coordinates.increaseY(1)
		elif(self.direction == Direction.East):
			self.coordinates.increaseX(1)
		elif(self.direction == Direction.South):
			self.coordinates.decreaseY(1)
		elif(self.direction == Direction.West):
			self.coordinates.decreaseX(1)
		else:
			print("invalid direction")

	#randomly place self on a road
	def randomlyPlaceCarOnRoads(self):
		#set coordinate
		startRoad = random.choice(self.cityMap.roads)
		freeCoord = random.randrange(startRoad.min, startRoad.max + 1)
		if startRoad.direction == Direction.North:
			coordinates = Coord(startRoad.fixedCoord,freeCoord)
		if startRoad.direction == Direction.East:
			coordinates = Coord(freeCoord,startRoad.fixedCoord)
		self.coordinates = coordinates

		#set direction
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id
		self.direction = random.choice(self.getValidDirections())

	#return all valid directions the car may move in; must account for size of street and any intersections
	def getValidDirections(self):
		#get valid roads
		roads = [self.cityMap.getRoadFromCoord(self.coordinates)]
		intersectingStreets = ([edge[0] for edge in self.cityMap.graph[self.currentStreetId] if edge[1] == self.coordinates])
		if intersectingStreets:
			roads.extend(intersectingStreets)

		#search roads for valid directions
		validDirections = []
		for road in roads:
			if road.direction == Direction.North:
				if self.coordinates.y != road.max:
					validDirections.append(Direction.North)
				if self.coordinates.y != road.min:
					validDirections.append(Direction.South)
			if road.direction == Direction.East:
				if self.coordinates.x != road.max:
					validDirections.append(Direction.East)
				if self.coordinates.x != road.min:
					validDirections.append(Direction.West)

		return validDirections #it's theoretically possible to get multiples of the same direction, but the setup of the roads will not allow it


	def getNextMove(self):
		return True

	#define car behavior
	def run(self):
		while self.getNextMove() is not None:
			section = self.cityMap.getRoadFromCoord(self.coordinates).getRoadSectionFromCoord(self.coordinates)
			parkingSpots = section.getParkingSpots(self.direction)
			if len(parkingSpots) == 0: #no parking available
				print ("Car %d driving at time %d at coord %s" % (self.carID,self.env.now,str(self.coordinates)))
				trip_duration = 1
				self.move(self.direction)
				yield self.env.timeout(trip_duration)
			else:
				parkingSpot = random.choice(parkingSpots)
				parkingSpot.request()
				print ("Car %d parking at time %d at coord %s" % (self.carID,self.env.now,str(self.coordinates)))
				park_duration = 1
				yield self.env.timeout(park_duration)

	def __str__(self):
		return "Car " + str(self.carID) + " (Coordinates: " + str(self.coordinates) + ", Direction: " + roadmap.directionToCardinalDirection(self.direction) + ")"
			
if __name__ == "__main__":
	env = simpy.Environment()

	# roadMap = loadCity("cities/city1.xml")
	roadMap = loadCity("cities/city3.xml")

	for i in range(1):
		car = Car(env,True,i,roadMap)
		car.randomlyPlaceCarOnRoads()
		car.coordinates=Coord(0,1)
		print car

	env.run(until=10)
