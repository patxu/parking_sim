
import xml.etree.ElementTree as ET

def enum(**enums):
  return type('Enum',(),enums)

Direction = enum(North=1,East=2,South=3,West=4)

def loadCity(file):
	tree = ET.parse(file)
	root = tree.getroot()
	for road in root.findall('road'):
		min = road.find('min').text
		max = road.find('max').text
		fixedCoord = road.find('fixedCoord').text
		
		

		
		#Get the road sections
		for roadSection in range(4,len(road)):
			for x in roadSection:
				print(x)

if __name__ == '__main__':
	loadCity("city1.xml")