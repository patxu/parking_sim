import simpy
import random
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity
import roadmap
from threading import Thread
from cs1lib import *
from draw_city import *

#DEBUGGING (must have ipdb and iPython set up)
# import ipdb; ipdb.set_trace()
# import pdb, traceback, sys, code

SEED = 10

#random.seed(SEED)

class Car(object):
	def __init__(self,env,carID,cityMap,wantsToPark = True,coordinates = None,currentStreetId = None,direction = None,parkingSpot=None):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.cityMap = cityMap
		self.coordinates = coordinates
		self.currentStreetId = currentStreetId
		self.direction = direction
		self.parkingSpot = parkingSpot
		self.destinations = []
		self.goal = None 
		self.timeSpent=0
		self.circling = False
		self.intersectionCount = 0

	#execute a move
	def move(self,direction):
		validDirections = self.getValidDirections()
		print validDirections
		if len(validDirections) > 1: #don't u-turn unless we have to
			oppositeDirection = (self.direction + 2) % 4
			if oppositeDirection == 0:
				oppositeDirection = 4
			try:
				validDirections.remove(oppositeDirection) #remove backwards direction
			except ValueError:
				pass #this is okay
		print validDirections
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
		return self.coordinates

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
			if self.parkingSpot != None: #unpark if parked
				self.parkingSpot.release()
				self.parkingSpot = None

			section = self.cityMap.getRoadFromCoord(self.coordinates).getRoadSectionFromCoord(self.coordinates)
			parkingSpots = section.getParkingSpots(self.direction)

			if len(parkingSpots) > 0 and self.wantsToPark: #park
				print ("\t\t\t\t\t\tCar %d parking at time %d at coord %s.  Total Time Elapsed: %d" % (self.carID,self.env.now,str(self.coordinates),self.timeSpent))
				parkingSpot = random.choice(parkingSpots)
				parkingSpot.request()
				self.wantsToPark = False
				self.parkingSpot = parkingSpot
				park_duration = 15
				yield self.env.timeout(park_duration)

			else: #default behavior- drive
				print ("Car %d driving at time %d at coord %s. Total Time Elapsed: %d" % (self.carID,self.env.now,str(self.coordinates),self.timeSpent))
				trip_duration = 1
				self.move(self.direction)
				if(self.wantsToPark):
					self.clockCounter()
				yield self.env.timeout(trip_duration)


	def circling ():
		roads = [self.cityMap.getRoadFromCoord(self.coordinates)]
		intersectingStreets = ([edge[0] for edge in self.cityMap.graph[self.currentStreetId] if edge[1] == self.coordinates])

		if(len(intersectingStreets)>0):
			if(self.intersectionCount%7 != 0):
				self.direction = getRight(self.direction)
			self.intersectionCount +=1
		
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

	def getRight(currentDirection):
		if(currentDirection == Direction.North):
			return Direction.East
		elif(currentDirection == Direction.East):
			return Direction.South
		elif(currentDirection == Direction.South):
			return Direction.West
		elif(currentDirection == Direction.West):
			return Direction.North

	def clockCounter(self):
		self.timeSpent=self.timeSpent+1

	def getTime(self):
		return self.timeSpent
	def getCarID(self):
		return self.carID

	def generateRandomDestinations(self,numOfDestination):
		for i in range(0,numOfDestination):
			destination = self.randomlyPlaceCarOnRoads()
			self.destinations.append(destination)

	def __str__(self):
		return "Car " + str(self.carID) + " (Coordinates: " + str(self.coordinates) + ", Direction: " + roadmap.directionToCardinalDirection(self.direction) + ")" + "Time: "+ str(self.timeSpent)
	

if __name__ == "__main__":
	env = simpy.Environment()
	
	# roadMap = loadCity("cities/city1.xml")
	# roadMap = loadCity("cities/city3.xml")
	cityMap = loadCity("cities/grid100_1.xml")
	carList = []
	for i in range(100):
		car = Car(env,i,cityMap)
		car.randomlyPlaceCarOnRoads()
		carList.append(car)


	
	for i in range(1,100):
		#env.run(until=i)
		env.step()
		sleep(1)
	#
	#env.run(until=10)

	# Thread(target = env.step()).start()
	# Thread(target = func2).start()
