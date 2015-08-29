import random
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity
import roadmap
from lxml import etree as ET
import sys
import xml.dom.minidom
import argparse

SEED = 13
MAP_SIZE = 11
BLOCK_SIZE_HORIZONTAL = 10
BLOCK_SIZE_VERTICAL = 10
PERCENT_OPEN = 3
PERCENT_CROSSABLE = 100

FILENAME = "cities/foo.xml"
random.seed(SEED)
def generateRoads():
	roadID = 0
	roads = []
	for x in range(0,MAP_SIZE):
		if (x%BLOCK_SIZE_HORIZONTAL == 0):
			road = Road(roadID,Direction.North,0,MAP_SIZE,x)
			roads.append(road)
			roadID +=1
	for x in range(0,MAP_SIZE):
		if (x%BLOCK_SIZE_VERTICAL == 0):
			road = Road(roadID,Direction.East,0,MAP_SIZE,x)
			roads.append(road)
			roadID +=1
	return roads

#parking density is a number between 0-100 which represents percentage of parking spots
def fillWithRoadSection(road,parkingDensity,crossable,cityMap):
	for x in range(0,road.max+1):
		if (road.direction == Direction.North):
			coordinates = Coord(road.fixedCoord,x)
		elif (road.direction == Direction.East):
			coordinates = Coord(x,road.fixedCoord)
		intersection = checkCoordForIntersection(coordinates,cityMap.graph[road.id])
		#randomly seed parking spots
		parkingRightAvailable = False
		parkingLeftAvailable = False
		if intersection == False:
			if (random.randint(0,100) <= parkingDensity):
				parkingRightAvailable = True
			if (random.randint(0,100) <= parkingDensity):
				parkingLeftAvailable = True
		roadSection = RoadSection(coordinates,ParkingSpot(parkingRightAvailable),ParkingSpot(parkingLeftAvailable),crossable,intersection,road.direction)
		road.addRoadSection(roadSection)
def checkCoordForIntersection(coord,edges):
	intersection = False
	for edge in edges:
		if edge[1] == coord:
			intersection = True
	return intersection

def generateXML(roads,filename):
	root = ET.Element("data")
	for road in roads:
		roadXML = ET.SubElement(root, "road", name=str(road.id))
		data = ET.SubElement(roadXML, "direction").text = str(road.direction)
		data = ET.SubElement(roadXML, "min").text = str(road.min)
		data = ET.SubElement(roadXML, "max").text = str(road.max)
		data = ET.SubElement(roadXML, "fixedCoord").text = str(road.fixedCoord)
		for roadSection in road.roadSections:
			roadSectionXML = ET.SubElement(roadXML, "roadSection")
			data = ET.SubElement(roadSectionXML, "coordX").text = str(roadSection.coordinates.x)
			data = ET.SubElement(roadSectionXML, "coordY").text = str(roadSection.coordinates.y)
			data = ET.SubElement(roadSectionXML, "parkingRight").text = boolToXML(roadSection.parkingRight.available)
			data = ET.SubElement(roadSectionXML, "parkingLeft").text = boolToXML(roadSection.parkingLeft.available)
			data = ET.SubElement(roadSectionXML, "crossable").text = boolToXML(roadSection.crossable)
			data = ET.SubElement(roadSectionXML, "intersection").text = boolToXML(roadSection.intersection)
			data = ET.SubElement(roadSectionXML, "direction").text = str(roadSection.direction)
			

	tree = ET.ElementTree(root)

	#write to file with header
	header = "<!-- GENERATION INFO:\nSEED = " + str(SEED) + "\nMAP_SIZE = " + str(MAP_SIZE) + "\nBLOCK_SIZE_HORIZONTAL = " + str(BLOCK_SIZE_HORIZONTAL) + "\nBLOCK_SIZE_VERTICAL = " + str(BLOCK_SIZE_VERTICAL) + "\nPERCENT_OPEN = " + str(PERCENT_OPEN) + "\nPERCENT_CROSSABLE = " + str(PERCENT_CROSSABLE) +" -->\n"
	open(filename, 'w').write(header + ET.tostring(tree, pretty_print=True))

def boolToXML(bool):
	if bool:
		return 'Y'
	else:
		return 'N'

if __name__ == '__main__':

	#Get Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('-s','--map_size',help="City Size")
	parser.add_argument('-l','--block_length',help="Block Length")
	parser.add_argument('-w','--block_width',help="Block Width")
	parser.add_argument('-o','--percent_open',help="Number between 0-100 representing percent of spaces open")
	parser.add_argument('-f','--file',help="File to write too")
	args = vars(parser.parse_args())

	if (args["map_size"] != None):
		MAP_SIZE = args["map_size"]
	if (args["block_length"] != None):
		BLOCK_SIZE_VERTICAL = args["block_length"]
	if (args["block_width"] != None):
		BLOCK_SIZE_HORIZONTAL = args["block_width"]
	if (args["percent_open"] != None):
		PERCENT_OPEN = args["percent_open"]
	if (args["file"] != None):
		FILENAME = args["file"]
	
	roads = generateRoads()
	city = RoadMap()
	for road in roads:
		city.addStreet(road)
	for road in roads:
		if (random.randint(0,100) <= PERCENT_CROSSABLE):
			fillWithRoadSection(road,PERCENT_OPEN,True,city)
		else:
			fillWithRoadSection(road,PERCENT_OPEN,False,city)
	generateXML(city.roads,FILENAME)
	