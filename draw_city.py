from cs1lib import *
from roadmap import *
from simulation import *
import simpy

CANVAS_WIDTH=2000
CANVAS_HEIGHT=1000
ROAD_SECTION_WIDTH=50
ROAD_SECTION_HEIGHT=50
STEP_LENGTH = .05
FILENAME = "cities/grid100_3.xml"

def runGraphics():
	print("in main")
	set_clear_color(1,1,1)
	clear()

	#Grass
	disable_stroke()
	set_fill_color(0,0.5,0) #Green
	draw_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)

	env = simpy.Environment()

	cityMap = loadCity(FILENAME)
	carList = []
	for i in range(1000):
		car = Car(env,i,cityMap)
		car.randomlyPlaceCarOnRoads()
		carList.append(car)
	for road in cityMap.roads:
			for roadSection in road.roadSections:
				if roadSection.parkingRight.available == False:
					roadSection.parkingRight.isParkingSpot = False
				if roadSection.parkingLeft.available == False:
					roadSection.parkingLeft.isParkingSpot = False

	while not window_closed():
		numDriving = len([car for car in carList if car.parkingSpot == None])
		for i in range(numDriving):
			env.step()
		if numDriving == 0:
			print("Everything parked")
			env.step()
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				#print "drawing road section"
				drawRoadSection(roadSection)
		for car in carList:
			drawCar(car)
		# drawRoads(cityMap)
		request_redraw()
		sleep(STEP_LENGTH)



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
			if(roadSection.crossable == True):
				set_stroke_color(1,1,1) #white
			else:
				set_stroke_color(1,1,0) #white
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingLeft.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
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
			if(roadSection.crossable == True):
				set_stroke_color(1,1,1) #white
			else:
				set_stroke_color(1,1,0) #white
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(1)
			if (roadSection.parkingLeft.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
def drawCar(car):
	myCoordinates=car.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	y_coor = y_coor*ROAD_SECTION_HEIGHT
	x_coor = x_coor*ROAD_SECTION_WIDTH


	enable_stroke()
	set_stroke_width(2)
	set_stroke_color(1,0,0.7) #Yellow
	if (car.wantsToPark):
		set_fill_color(1,0,0.7) #Blue
	else:
		set_fill_color(0,0,1)
	if(car.direction == Direction.North):
		x_coor = x_coor+(ROAD_SECTION_WIDTH/2)+(ROAD_SECTION_WIDTH/5)
		y_coor = y_coor + (ROAD_SECTION_HEIGHT/2)
	elif(car.direction == Direction.South):
		x_coor = x_coor+(ROAD_SECTION_WIDTH/2)-(ROAD_SECTION_WIDTH/5)
		y_coor = y_coor + (ROAD_SECTION_HEIGHT/2)

	elif(car.direction == Direction.West):
		y_coor = y_coor+(ROAD_SECTION_HEIGHT/2)+(ROAD_SECTION_HEIGHT/5)
		x_coor = x_coor + (ROAD_SECTION_WIDTH/2)
	elif(car.direction == Direction.East):
		y_coor = y_coor+(ROAD_SECTION_HEIGHT/2)-(ROAD_SECTION_HEIGHT/5)
		x_coor = x_coor + (ROAD_SECTION_WIDTH/2)
	

	draw_circle(x_coor,y_coor,ROAD_SECTION_WIDTH/4)
	disable_stroke()


if __name__ == '__main__':
	if(len(sys.argv) > 1):
		FILENAME = sys.argv[1]
	start_graphics(runGraphics,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)

	