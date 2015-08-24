from cs1lib import *
from roadmapcopy import *

CANVAS_WIDTH=600
CANVAS_HEIGHT=600
ROAD_SECTION_WIDTH=180
ROAD_SECTION_HEIGHT=100

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
		myCoordinates=Coord(200,200-ROAD_SECTION_HEIGHT)
		myParkingRight=ParkingSpot(True)
		myParkingLeft=ParkingSpot(True)
		Direction="Vertical"

		myRoadSection=RoadSection(myCoordinates,myParkingRight,myParkingLeft,True,False,Direction)
		drawRoadSection(myRoadSection)

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

		request_redraw()
		sleep(5)

def drawRoadSection(roadSection):
	myCoordinates=roadSection.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	if (roadSection.intersection==True):
		enable_stroke()
		set_stroke_width(2)
		set_stroke_color(1,1,0) #Yellow
		set_fill_color(0.5,0.5,0.5) #Gray
		draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_WIDTH)
		disable_stroke()
	else:
		if (roadSection.direction=="Vertical"):
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_HEIGHT)
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,1) #white
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			if (roadSection.parkingLeft.available==True):
				enable_stroke()
				set_stroke_width(2)
				set_stroke_color(1,1,0) #Yellow
				set_fill_color(0,0.9,0)
				draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
				disable_stroke()

			if (roadSection.parkingRight.available==True):
				enable_stroke()
				set_stroke_width(2)
				set_stroke_color(1,1,0) #Yellow
				set_fill_color(0,0.9,0)
				draw_rectangle(x_coor+((3*(ROAD_SECTION_WIDTH))/4),y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
				disable_stroke()


		if (roadSection.direction=="Horizontal"):
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH)
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,1) #white
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			if (roadSection.parkingLeft.available==True):
				enable_stroke()
				set_stroke_width(2)
				set_stroke_color(1,1,0) #Yellow
				set_fill_color(0,0.9,0)
				draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
				disable_stroke()

			if (roadSection.parkingRight.available==True):
				enable_stroke()
				set_stroke_width(2)
				set_stroke_color(1,1,0) #Yellow
				set_fill_color(0,0.9,0)
				draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
				disable_stroke()


start_graphics(main,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)
	