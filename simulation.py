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
	def __init__(self,env,carID,cityMap,moveFunction = "random", wantsToPark = True,coordinates = None,direction = None):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.cityMap = cityMap
		self.coordinates = coordinates
		self.direction = direction

		self.setMoveFunction(moveFunction)

		#default settings
		self.parkingSpot = None
		self.currentStreetId = None
		self.destinationStack = []
		self.currentDestination= None 
		self.totalDestinations = 0
		self.timeSpent=0
		self.circlingBool = False
		self.intersectionCount = 1

	#random
	#circling
	#
	def setMovementPattern(moveFunction):
		if (moveFunction == "random"):
			self.moveFunction = randomMove()
		if (moveFunction == "circling"):
			self.moveFunction = circling
		if (moveFunction == "smart"):
			self.moveFunction == smartMove()
		else:
			print("setMoveFunction error: invalid move function choice; setting to random")
			self.moveFunction == randomMove()

	#execute a move in a random direction
	def randomMove(self,prevDirection):
		validDirections = self.getValidDirections()
		print validDirections
		if len(validDirections) > 1: #don't u-turn unless we have to
			oppositeDirection = (self.direction + 2) % 4
			if oppositeDirection == 0:
				oppositeDirection = 4
		oppositeDirection = (self.direction + 2) % 4
		if oppositeDirection == 0: #since directions are not 0-indexed
			oppositeDirection = 4
		if len(validDirections) > 1: #remove u-turn direction if we have other options
			try:
				validDirections.remove(oppositeDirection) #remove backwards direction
			except ValueError:
				pass #this is okay
		print validDirections
		self.direction = random.choice(validDirections)
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id

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

	#executes a move towards a destination
	def smartMove(self):
		return True

	#randomly place self on a road
	def randomlyPlaceCarOnRoads(self):
		self.coordinates = generateValidCoordinate
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
			if self.parkingSpot != None: #unpark if parked
				self.parkingSpot.release()
				self.parkingSpot = None
			if len(self.destinationStack) == 0:
				setMovementPattern("random")
			elif goal == None:
				#if self.
				goal=destinationStack.pop(0)
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
			self.circling()
			trip_duration = 1
			yield self.env.timeout(trip_duration)

	#search for parking in a "dumb" circling pattern
	def circling (self):
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
		
		
		if(self.direction == Direction.North):
			self.coordinates.increaseY(1)
		elif(self.direction == Direction.East):
			self.coordinates.increaseX(1)
		elif(self.direction == Direction.South):
			self.coordinates.decreaseY(1)
		elif(self.direction == Direction.West):
			self.coordinates.decreaseX(1)
		else:
			print("circling error: invalid direction")
		
		self.currentStreetId = self.cityMap.getRoadFromCoord(self.coordinates).id

	def getRight(self,currentDirection):
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

	#Returns RoadSection's List of Parking Spots
	def getParkingSpotsDistance(self,parking_destination):
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

		myDistance = (float("inf")) #infinity
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
		return destinations

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

