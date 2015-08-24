import random
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity
import roadmap

SEED = 13
MAP_SIZE = 100
BLOCK_SIZE_HORIZONTAL = 10
BLOCK_SIZE_VERTICAL = 15
PARKING_DENSITY = 60

def generateRoads():
	roadID = 0
	roads = []
	for x in range(0,MAP_SIZE):
		if (x%BLOCK_SIZE_HORIZONTAL == 0):
			road = Road(roadID,Direction.North,0,MAP_SIZE,x)
			print road
			roads.append(road)
			roadID +=1
	for x in range(0,MAP_SIZE):
		if (x%BLOCK_SIZE_VERTICAL == 0):
			road = Road(roadID,Direction.East,0,MAP_SIZE,x)
			print road
			roads.append(road)
			roadID +=1
	return roads

#parking density is a number between 0-100 which represents percentage of parking spots
def fillWithRoadSection(road,parkingDensity,crossable,cityMap):
	random.seed(SEED)
	for x in range(0,road.max):
		#randomly seed parking spots
		parkingRightAvailable = False
		parkingLeftAvailable = False
		if (random.randint(0,100) <= parkingDensity):
			parkingRightAvailable = True
		if (random.randint(0,100) <= parkingDensity):
			parkingLeftAvailable = True
		if (road.direction == Direction.North):
			coordinates = Coord(road.fixedCoord,x)
			intersection = checkCoordForIntersection(coordinates,cityMap.graph[road.id])
		elif (road.direction == Direction.East):
			coordinates = Coord(x,road.fixedCoord)
			intersection = checkCoordForIntersection(coordinates,cityMap.graph[road.id])

def checkCoordForIntersection(coord,edges):
	intersection = False
	for edge in edges:
		if edge[1] == coord:
			intersection = True
	return intersection

def generateXML(roads,fileName):




if __name__ == '__main__':
	roads = generateRoads()
	city = RoadMap()
	for road in roads:
		city.addStreet(road)
	for road in roads:
		fillWithRoadSection(road,60,True,city)
	