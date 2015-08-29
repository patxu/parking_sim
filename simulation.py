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
PARK_DURATION = 15
PARK_RADIUS = 20

#random.seed(SEED)

class Car(object):
	def __init__(self,env,carID,cityMap,moveFunction = "random",wantsToPark = False,coordinates = None,direction = None):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.cityMap = cityMap
		self.coordinates = coordinates
		self.direction = direction

		self.moveFunction = moveFunction

		#default settings
		self.parkingSpot = None
		self.currentStreetId = None
		self.totalDestinations = 0
		self.destinations = []
		self.smartParkingDestination= None 
		self.timeSpent=0
		self.intersectionCount = 1

	def executeMovementBehavior(self):
		if (self.moveFunction == "random"):
			self.randomMove()
		elif (self.moveFunction == "dumb"):
			self.dumbMove()
		elif (self.moveFunction == "circling"):
			self.circling()
		elif (self.moveFunction == "smart"):
			self.smartMove()
		else:
			print("executeMovementBehvaior error: invalid move function choice %s; setting to random" %self.moveFunction)
			self.randomMove()

	# ---- Random ---- #

	#execute a move in a random direction
	def randomMove(self):
		if self.coordinates == None:
			return
		
		validDirections = self.getValidDirections()
		oppositeDirection = (self.direction + 2) % 4
		if oppositeDirection == 0: #since directions are not 0-indexed
			oppositeDirection = 4
		if len(validDirections) > 1: #remove u-turn direction if we have other options
			try:
				validDirections.remove(oppositeDirection) #remove backwards direction
			except ValueError:
				pass #this is okay
		self.direction = random.choice(validDirections)
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id
		self.moveTowardsCurrentDirection()

	# ---- Circling ---- #

	#search for parking in a "dumb" circling pattern
	def circling (self):
		if self.coordinates == None:
			return
		intersectingStreets = ([edge[0] for edge in self.cityMap.graph[self.currentStreetId] if edge[1] == self.coordinates])
		
		#if there is a road to turn onto
		if(len(intersectingStreets)>0):
			#and we have not made 7 rights
			if(self.intersectionCount%8 != 0):
				self.direction = self.getRight(self.direction) #turn right
				self.intersectionCount +=1
			else:
				self.intersectionCount = 1 #go straight

		currentRoad = self.cityMap.getRoadFromCoord(self.coordinates)
		if (self.cityMap.willBeOutOfBounds(self.coordinates,self.direction,currentRoad)):
			oppositeDirection = (self.direction + 2) % 4
			if oppositeDirection == 0:
				oppositeDirection = 4
			self.direction = oppositeDirection
		
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id
		self.moveTowardsCurrentDirection()

	def getRight(self,currentDirection):
		if(currentDirection == Direction.North):
			return Direction.East
		elif(currentDirection == Direction.East):
			return Direction.South
		elif(currentDirection == Direction.South):
			return Direction.West
		elif(currentDirection == Direction.West):
			return Direction.North

	# ---- Smart Movement ---- #

	#executes a move towards a destination
	def smartMove(self):
		if self.coordinates == None:
			return
		if self.coordinates.distanceFrom(self.destinations[0]) < PARK_RADIUS:
			self.wantsToPark = True
		self.smartParkingDestination = self.getClosestRoadSectionToDestination(self.destinations[0])
		self.goToCoordinate(self.smartParkingDestination.coordinates)

	# ---- Normal "Dumb" Movement ---- #
	def dumbMove(self):
		if self.coordinates == None:
			return
		if self.coordinates.distanceFrom(self.destinations[0]) < PARK_RADIUS:
			self.wantsToPark = True
		else:
			self.wantsToPark = False
		if self.coordinates == self.destinations[0]:
			self.moveFunction = "circling"
		self.goToCoordinate(self.destinations[0])


	# ---- Go To Destination ---- #
	def goToCoordinate(self, destination):
		currentSection = self.cityMap.getRoadFromCoord(self.coordinates).getRoadSectionFromCoord(self.coordinates)
		if currentSection.intersection == False:
			self.moveTowardsCurrentDirection()
			return

		# validDirections = self.getValidDirections()

		xDiff = abs(destination.x - self.coordinates.x)
		yDiff = abs(destination.y - self.coordinates.y)

		if xDiff > yDiff:
			if destination.x < self.coordinates.x:
				self.direction = Direction.West
			elif destination.x > self.coordinates.x:
				self.direction = Direction.East
		else:
			if destination.y < self.coordinates.y:
				self.direction = Direction.South
			elif destination.y > self.coordinates.y:
				self.direction = Direction.North
		self.moveTowardsCurrentDirection()

	def moveTowardsCurrentDirection(self):
		currentRoad = self.cityMap.getRoadFromCoord(self.coordinates)
		if (self.cityMap.willBeOutOfBounds(self.coordinates,self.direction,currentRoad)):
			oppositeDirection = (self.direction + 2) % 4
			if oppositeDirection == 0:
				oppositeDirection = 4
			self.direction = oppositeDirection
		if(self.direction == Direction.North):
			self.coordinates.increaseY(1)
		elif(self.direction == Direction.East):
			self.coordinates.increaseX(1)
		elif(self.direction == Direction.South):
			self.coordinates.decreaseY(1)
		elif(self.direction == Direction.West):
			self.coordinates.decreaseX(1)
		else:
			print("randomMove error: invalid direction")

	#randomly place self on a road
	def randomlyPlaceCarOnRoads(self):
		self.coordinates = self.generateValidCoordinate()
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id
		self.direction = random.choice(self.getValidDirections())
		return self.coordinates

	#a valid coordinate is one that is on a street
	def generateValidCoordinate(self):
		startRoad = random.choice(self.cityMap.roads)
		freeCoord = random.randrange(startRoad.min, startRoad.max + 1)
		if startRoad.direction == Direction.North:
			coordinate = Coord(startRoad.fixedCoord,freeCoord)
		elif startRoad.direction == Direction.East:
			coordinate = Coord(freeCoord,startRoad.fixedCoord)
		else:
			print("generateRandomValidCoordinate error: unable to generate valid coordinate; None returned")
			coordinate = None
		return coordinate


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
			elif road.direction == Direction.East:
				if self.coordinates.x != road.max:
					validDirections.append(Direction.East)
				if self.coordinates.x != road.min:
					validDirections.append(Direction.West)
			else:
				print("getValidDirections error: invalid direction")

		return validDirections #it's theoretically possible to get multiples of the same direction, but the setup of the roads will not allow it


	def getNextMove(self):
		return True

	#define car behavior
	def run(self):
		while self.getNextMove() is not None:
			if self.parkingSpot != None: #release parking spot
				self.parkingSpot.release()
				self.parkingSpot = None

			if len(self.destinations) == 0:
				self.moveFunction = "random"
				self.wantsToPark = False

			currentSection = self.cityMap.getRoadFromCoord(self.coordinates).getRoadSectionFromCoord(self.coordinates)
			parkingSpots = currentSection.getParkingSpots(self.direction)

			if len(parkingSpots) > 0 and self.wantsToPark: #park
				if self.smartParkingDestination != None and self.smartParkingDestination.coordinates != self.coordinates:
					print ("if")
					self.executeMovementBehavior()
					if(self.wantsToPark):
						self.clockCounter()
					yield self.env.timeout(1)
				else:					
					print ("else")
					# print ("\t\t\t\t\t\tCar %d parking at time %d at coord %s.  Total Time Elapsed: %d" % (self.carID,self.env.now,str(self.coordinates),self.timeSpent))
					parkingSpot = random.choice(parkingSpots)
					parkingSpot.request()
					print(str(parkingSpot))
					self.wantsToPark = False
					self.parkingSpot = parkingSpot
					self.destinations.pop(0)
					print(self.destinations)
					yield self.env.timeout(PARK_DURATION)

			else: #default behavior- drive
				# print ("Car %d driving at time %d at coord %s. Total Time Elapsed: %d" % (self.carID,self.env.now,str(self.coordinates),self.timeSpent))
				self.executeMovementBehavior()
				if(self.wantsToPark):
					self.clockCounter()
				yield self.env.timeout(1)

	def clockCounter(self):
		self.timeSpent=self.timeSpent+1

	def getTime(self):
		return self.timeSpent
	def getCarID(self):
		return self.carID

	#Returns RoadSection's List of Parking Spots
	def getClosestRoadSectionToDestination(self,parking_destination):
		#For each car Get RoadMap
		RoadSectionList=[]
		roadList=self.cityMap.roads
		#Get Roads
		for road in roadList:
			#Get RoadSection
			RoadSectionsForRoad=road.roadSections
			for roadSection in RoadSectionsForRoad:
				#If road section has available spots, then add to list
				myList= []
				myList=roadSection.getParkingSpots(road.direction)
				#print(str(roadSection.coordinates.x))
				if len(myList)>0:
					RoadSectionList.append(roadSection)

		myDistance = 100000000000#(float("inf")) #infinity
		#For each road section compute distance, find the closest distance
		for RoadSectionWithParkingSpot in RoadSectionList:
			parking_spot_coordinates=RoadSectionWithParkingSpot.coordinates
			thisDistance=parking_spot_coordinates.distanceFrom(parking_destination)
			if thisDistance<myDistance:
				myDistance=thisDistance
				myRoadSection=RoadSectionWithParkingSpot

		return myRoadSection

	def generateDestinations(self,numOfDestination):
		for i in range(numOfDestination):
			self.destinations.append(self.generateValidCoordinate())
		self.totalDestinations = numOfDestination
		return self.destinations

	def __str__(self):
		return "Car " + str(self.carID) + " (Coordinates: " + str(self.coordinates) + ", Direction: " + roadmap.directionToCardinalDirection(self.direction) + ")" + "Time: "+ str(self.timeSpent)
	

if __name__ == "__main__":
	env = simpy.Environment()
	
	cityMap = loadCity("cities/grid100_1.xml")
	carList = []
	for i in range(1):
		car = Car(env,i,cityMap)
		car.randomlyPlaceCarOnRoads()
		carList.append(car)

	env.run(until=10)

