from cs1lib import *
from roadmap import *

CANVAS_WIDTH=1000
CANVAS_HEIGHT=1000
ROAD_SECTION_WIDTH=20
ROAD_SECTION_HEIGHT=20

cityMap = loadCity("cities/grid100_2.xml")

def main():
	set_clear_color(1,1,1)
	while not window_closed():
		clear()

		#Grass
		disable_stroke()
		set_fill_color(0,0.5,0) #Green
		draw_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)

		#Roads
		#set_fill_color(0.5,0.5,0.5)
		#draw_rectangle(150,0,100,400)
		#set_fill_color(0.5,0.5,0.5)
		#draw_rectangle(0,150,400,100)

		#Intersection
		#enable_stroke()
		#set_stroke_width(2)
		#set_stroke_color(1,1,0) #Yellow
		#set_fill_color(0.5,0.5,0.5) #Gray
		#draw_rectangle(150,150,100,100)
		
		#Draw Vertical
		myCoordinates=Coord(0,0)
		myParkingRight=ParkingSpot(True)
		myParkingLeft=ParkingSpot(True)
		Direction=1

		myRoadSection=RoadSection(myCoordinates,myParkingRight,myParkingLeft,True,False,Direction)
		#drawRoadSection(myRoadSection)

		myCoordinates=Coord(0,1)
		myParkingRight=ParkingSpot(True)
		myParkingLeft=ParkingSpot(True)
		Direction=1

		myRoadSection2=RoadSection(myCoordinates,myParkingRight,myParkingLeft,True,False,Direction)
		#drawRoadSection(myRoadSection2)
		'''
		myCoordinates3=Coord(200,100-ROAD_SECTION_HEIGHT)
		myParkingRight3=ParkingSpot(True)
		myParkingLeft3=ParkingSpot(True)
		Direction3="Vertical"

		myRoadSection3=RoadSection(myCoordinates3,myParkingRight3,myParkingLeft3,True,False,Direction3)
		drawRoadSection(myRoadSection3)

		#Draw Horizontal
		myCoordinates1=Coord(200-ROAD_SECTION_HEIGHT,200)
		myParkingRight1=ParkingSpot(True)
		myParkingLeft1=ParkingSpot(True)
		Direction1="Horizontal"

		myRoadSection1=RoadSection(myCoordinates1,myParkingRight1,myParkingLeft1,True,False,Direction1)
		drawRoadSection(myRoadSection1)

		#Draw Intersection
		myCoordinates2=Coord(200,200)
		myRoadSection2=RoadSection(myCoordinates2,myParkingRight1,myParkingLeft1,False,True,Direction1)
		drawRoadSection(myRoadSection2)
		'''
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				#print "drawing road section"
				print roadSection
				drawRoadSection(roadSection)
		#drawRoads(cityMap)
		request_redraw()
		sleep(5)



def drawRoadSection(roadSection):
	myCoordinates=roadSection.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	y_coor = y_coor*ROAD_SECTION_HEIGHT
	x_coor = x_coor*ROAD_SECTION_WIDTH
	if (roadSection.intersection==True):
		enable_stroke()
		set_stroke_width(2)
		set_stroke_color(1,1,0) #Yellow
		set_fill_color(0.5,0.5,0.5) #Gray
		draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_WIDTH)
		disable_stroke()
	else:
		if (roadSection.direction==Direction.North):
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_HEIGHT)
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,1) #white
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor+((3*(ROAD_SECTION_WIDTH))/4),y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()


		if (roadSection.direction==Direction.East):
			
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH)
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,1) #white
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(1)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			


	